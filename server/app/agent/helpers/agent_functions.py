from ....config import server_settings
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import hashlib
import time
from typing import Dict, Any

embedding_model = SentenceTransformer(server_settings.EMBEDDING_MODEL, device="cpu")
pinecone_db = Pinecone(api_key=server_settings.PINECONE_API_KEY)
index_name = server_settings.PINECONE_INDEX_NAME
search_cache: Dict[str, Dict[str, Any]] = {}
cache_ttl = 3600

class AgentFunctionCalls:

    @staticmethod
    def use_semantic_search(vector_query: str) -> str:
        """Run semantic search on pinecone db"""
        try:
            if not vector_query:
                return "No search query provided."
            
            cache_hash = hashlib.md5(vector_query.encode()).hexdigest()
            curr_time = time.time()
            if cache_hash in search_cache:
                cached_res = search_cache[cache_hash]
                if curr_time - cached_res['timestamp'] < cache_ttl:
                    return cached_res['result']
                else:
                    del search_cache[cache_hash]
            
            if not embedding_model:
                return "Embedding model not initialized."
            embedding = embedding_model.encode(vector_query).tolist()

            if not pinecone_db or not index_name:
                return "Vector db not initialized."
            index = pinecone_db.Index(index_name)

            results = index.query(
                vector=embedding,
                top_k=10,
                namespace="onus_regulations_epa_regulations",
                include_metadata=True
            )
            if not results or 'matches' not in results or not results['matches']:
                return "No regulatory information found for this query. Please try a different search term."
            
            result_text = '\n\n ############### \n\n'.join(r['metadata']['text'] for r in results['matches'])

            search_cache[cache_hash] = {
                'result': result_text,
                'timestamp': curr_time,
                'query': vector_query
            }

            if len(search_cache) > 100:
                AgentFunctionCalls.clean_cache()

        except Exception as e:
            return f"Error during semantic search: {str(e)}"  

    @staticmethod
    def clean_cache():
        try:
            current_time = time.time()
            expired_keys = [
                key for key, value in search_cache.items()
                if current_time - value['timestamp'] > cache_ttl
            ]
            for key in expired_keys:
                del search_cache[key]
        except Exception as e:
            return f"Error during cache clean up"
        
    @staticmethod
    def end_analysis(
        equation_names_list: list[str],
        flag: str,
        validation_status: str,
        errors: dict,
        summary: str
    ):
        """Call this when you have gathered sufficient regulatory information.
        
        Args:
            equation_names_list: List of relevant equation names found
            flag: Quality flag for the analysis
            validation_status: Overall validation status
            errors: Any errors or issues identified
            summary: Complete summary of regulatory requirements
        """
        return {
            "equation_names_list": equation_names_list,
            "flag": flag,
            "validation_status": validation_status,
            "errors": errors,
            "summary": summary
        }
    
    @staticmethod
    def end_calculations(data_value_map: dict[str, float]) -> dict[str, float]:
        return data_value_map
    
    @staticmethod
    def analysis_error(error_map: dict[str, str]) -> dict[str, str]:
        return error_map