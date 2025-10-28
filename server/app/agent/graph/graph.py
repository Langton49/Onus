from langgraph.graph import StateGraph, START, END
from .graph_state import State
from ....config import server_settings
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from pinecone import Pinecone
from ..helpers.agent_prompts import system_prompt
from ...schemas.data_schemas import GemResponseSchema
import json
from ..helpers.agent_functions import AgentFunctionCalls

genai.configure(api_key=server_settings.GEMINI_API_KEY)
embedding_model = server_settings.EMBEDDING_MODEL
pinecone_db = Pinecone(api_key=server_settings.PINECONE_API_KEY)
index_name = server_settings.PINECONE_INDEX_NAME

class AgentGraph:
    def __init__(self):
        self.graph = StateGraph(State)
        self.pinecone_db = pinecone_db
        self.embedding_model = SentenceTransformer(embedding_model, device="cpu")
        self.data_analysis_model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=system_prompt)
        self.state = State()
        self.agent_functions = AgentFunctionCalls

    def get_regulatory_context(self, state: State) -> State:
        """Fetch regulatory context based on facility metadata"""
        config = {
        'temperature': 0.2
        }

        prompt = f"""
        You are conducting a SEMANTIC SEARCH QUERY for a vector database that contains some official
        regulatory text of 40 CFR Part 98 and 40 CFR Part 75 (GHG Reporting Rule).
        There are NO labels like "power plant" or "facility type" in the database. 
        You must infer relevant regulatory sections and concepts based on the following metadata.

        IMPORTANT:
        Do NOT copy the metadata directly into the query.
        Instead, infer from the metadata a precise, meaningful regulatory search phrase
        that will retrieve the most relevant regulatory rules, definitions, calculations,
        monitoring methods, reporting requirements, or QA/QC procedures. From the search results obtained
        determine whether you have sufficient information by doing one of two things,
        either A, gain further clarity by calling another search or B, determine that you have sufficient
        information and write a summary of everything you've learned and steps to proceed with with the
        given data analysis. This includes equations, totals and anything else.

        Focus on topics such as:
        - Emission calculation methods and equations
        - Monitoring requirements (e.g., CEMS, fuel flow)
        - Equipment-specific rules (boilers, turbines, flares, etc.)
        - Unit-level reporting fields and definitions (e.g., unit_id, emissions)
        - Recordkeeping or QA/QC requirements
        - Applicability rules for different subparts
        - Validation and verification
        """
        user_input = f"""
            Facility Metadata:
            Facility Type: {state['fac_metadata']['facility_type']}
            Subparts: {', '.join(state['fac_metadata']['subparts'])}
            Description: {state['fac_metadata'].get('facility_description', 'N/A')}
            NAICS Code: {state['fac_metadata'].get('naics_code', 'N/A')}
            Monitoring Method: {state['fac_metadata'].get('monitoring_method', 'N/A')}
            Equipment Types:
            {chr(10).join([f"- {eq.get('type', 'Unknown')} (Fuel: {eq.get('fuel', 'N/A')}, Capacity: {eq.get('capacity', 'N/A')})" for eq in state['fac_metadata'].get('equipment_types', [])])}

            Uploaded Data Fields:
            {', '.join(state['doc_metadata'].get('fields', []))}

            Data Snapshot:
            {state['data_snapshot']}

            Now, use the prepared function to run the semantic search with a highly focused semantic search query that will retrieve 
            the most relevant regulatory compliance text. You may query the regulatory database as many times as needed until you
            have gathered sufficient information to analyze the data based on the given metadata.
            Begin!
        """

        messages = [{"role": "model", "parts": f"{prompt}"}]
        messages.append({"role": "user", "parts": f"{user_input}"})

        final_summary = ""
        search_count = 0
        while search_count < 6:
            search_count+=1
            print(search_count)
            search_results = []
            response = self.data_analysis_model.generate_content(
                contents=messages,
                generation_config=config,
                tools=[self.agent_functions.use_similarity_search]
            )
            for part in response.parts:
                if hasattr(part, "function_call") and part.function_call:
                    fc = part.function_call
                    vector_query = fc.args.get("vector_query", "")
                    result = self.agent_functions.use_similarity_search(vector_query)
                    search_results.append(result)
                elif hasattr(part, "text") and part.text:
                    final_summary = part.text
            aggregated_results = "\n#############\n".join(search_results)
            messages.append({"role": "user", "parts": f"YOUR SEARCH {search_count} RESULTS:\n{aggregated_results}"})

        if search_count == 6:
            messages.append({"role": "user", "parts": f"""You have completed all necessary semantic searches. Now, write a 
                            final regulatory context summary for this facility and the uploaded data. Include:

                            - All relevant **emission calculation equations**.
                            - Applicable **monitoring requirements** and methods (e.g., CEMS, fuel flow).
                            - Equipment-specific rules (boilers, turbines, flares, etc.).
                            - Unit-level reporting fields and definitions (e.g., unit_id, emissions).
                            - QA/QC, recordkeeping, and validation requirements.
                            - Regulatory thresholds, limits, or applicability conditions for the subparts.
                            - Any other guidance that downstream agents would need to **validate, calculate, and report** the emissions correctly.
                            """})
            response = self.data_analysis_model.generate_content(
                    contents=messages,
                    generation_config=config,
                    tools=[self.agent_functions.use_similarity_search]
                )
            final_summary = response.text
    
        regulatory_context = final_summary
        state['regulatory_context'] = regulatory_context
        return state

    def analyze_document(self, state: State) -> State:
        """Analyze data inside document"""
        # Step 1: fetch context from epa regulation db  
        subparts = ', '.join(subpart for subpart in state["subparts"])
        context = f"""The following data is from a facility with the following characteristics:
        Facility Type: {state['facility_type']} 
        Data Type: {state['data_type']}
        Applicable Subparts: {subparts}
        """
        embedding = self.embedding_model.encode(context).tolist()
        index = self.pinecone_db.Index(index_name)
        results = index.query(
            vector=embedding,
            top_k=10,
            namespace="onus_regulations_epa_regulations",
            include_metadata=True
        )
        gemini_prompt = f"""
        APPLICABLE REGULATIONS: {'\n###########\n'.join([text['metadata']['text'] for text in results['matches']])}

        DATA: {state['chunk']}
        """

        response = self.data_analysis_model.generate_content( 
             contents=gemini_prompt,
             generation_config={
        "response_mime_type": "application/json",
        "response_schema": GemResponseSchema,
        },
            )
        raw_text = response.text
        data = json.loads(raw_text)
        for key in ['flag', 'validation_status', 'errors', 'suggestions']:
            if key in data:
                state[key] = data[key]

        return state

    def combine(self, state: State) -> State:
        """
        Combine results across multiple chunks.
        If any chunk has errors -> FAILED
        If any chunk has warnings or suggestions -> PARTIALLY_FAILED
        If no issues -> PASSED
        """

        errors = state.get("errors", {})
        suggestions = state.get("suggestions", {})

        has_errors = any(
            isinstance(v, list) and len(v) > 0 
            for v in errors.values()
        ) if errors else False

        has_suggestions = any(
            isinstance(v, list) and len(v) > 0 
            for v in suggestions.values()
        ) if suggestions else False

        if has_errors:
            state["flag"] = "INVALID"
            state["validation_status"] = "FAILED"
        elif has_suggestions:
            state["flag"] = "WARNING"
            state["validation_status"] = "PARTIALLY_FAILED"
        else:
            state["flag"] = "VALID"
            state["validation_status"] = "PASSED"
        print(state['notes'])
        return state

    def build_graph(self) -> StateGraph:
        """Build the agent graph with defined nodes and transitions"""
        self.graph.add_node("get_regulatory_context", self.get_regulatory_context)
        self.graph.add_node("analyze_document", self.analyze_document)
        self.graph.add_edge(START, "get_regulatory_context")
        self.graph.add_edge("get_regulatory_context", END)
        return self.graph
        