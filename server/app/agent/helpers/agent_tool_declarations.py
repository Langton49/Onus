from google.generativeai.types import FunctionDeclaration
from schemas.enums import Equations

class AgentToolDeclarations:
    use_similarity_search_dec = FunctionDeclaration(
        name="use_similarity_search",
        description="""Search the regulatory database for specific EPA regulatory text.
        
        SEARCH QUERY GUIDELINES:
        - Always include "40 CFR Part 98" for greenhouse gas reporting rules
        - Include specific subpart letters (C, D, AA, DD, NN, OO, RR)
        - Use exact regulatory terminology: "emission calculation equations", "monitoring requirements"
        - Include equipment types: "boiler", "turbine", "generator", "CEMS"
        - Search for specific equations: "Equation C-1", "Equation AA-1"
        - Include validation terms: "QA/QC", "data validation", "quality assurance"
        
        GOOD EXAMPLES:
        - "40 CFR Part 98 Subpart C boiler CO2 emission calculation equations"
        - "40 CFR Part 98 CEMS continuous monitoring data validation requirements"
        - "40 CFR Part 98 Equation C-6 hourly CO2 mass emission rate calculation"
        
        AVOID: Generic terms, facility names, or non-regulatory language""",
        parameters={
            "type": "object",
            "properties": {
                "vector_query": {
                    "type": "string",
                    "description": "Specific regulatory search query following the guidelines above"
                }
            },
            "required": ["vector_query"]
        }
        )
    
    end_analysis_dec = FunctionDeclaration(
        name="end_analysis",
        description="""CRITICAL: Call this function to complete regulatory validation analysis.
        
        VALIDATION REQUIREMENTS:
        - Set validation_status to "FAILED" if you cannot find specific regulatory equations
        - Set validation_status to "FAILED" if data cannot be properly verified
        - Set validation_status to "FAILED" if monitoring requirements are unclear
        - Only set "PASSED" if you have complete regulatory framework for validation
        
        You MUST use this function - never return JSON text directly.""",
        parameters={
            "type": "object",
            "properties": {
                "equation_names_list": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [e.value for e in Equations]
                        },
                    "description": "List of all relevant emission calculation equation names/references found"
                },
                "flag": {
                    "type": "string",
                    "description": "Quality flag for data completeness",
                    "enum": ["VALID", "ESTIMATED", "MISSING", "OUTLIER", "INVALID"]
                },
                "validation_status": {
                    "type": "string",
                    "description": "Overall validation status",
                    "enum": ["PENDING", "PASSED", "FAILED", "REQUIRES_REVIEW"]
                },
                "errors": {
                    "type": "object",
                    "description": "Dictionary of any errors, missing data, or compliance issues",
                    "properties": {
                        "missing_fields": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "validation_errors": {
                            "type": "array", 
                            "items": {"type": "string"}
                        },
                        "compliance_issues": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
                "summary": {
                    "type": "string",
                    "description": """Comprehensive summary including: emission equations, monitoring requirements, 
                    equipment rules, reporting fields, QA/QC procedures, regulatory thresholds, and next steps"""
                }
            },
            "required": ["equation_names_list", "flag", "validation_status", "summary"]
        }
    )
        
    end_calculations_dec = FunctionDeclaration(
    name="end_calculations",
    description=(
        "Return final calculated greenhouse gas emissions data values along with their descriptive labels. "
        "Use this function to present the final results of emissions calculations with clear descriptions "
        "of what each value represents."
    ),
    parameters={
        "type": "object",
        "properties": {
            "data_value_map": {
                "type": "object",
                "description": (
                    "Dictionary mapping descriptive labels to calculated emissions values. "
                    "Keys should be clear descriptions of the emission type/source, and values should be "
                    "the calculated amounts in metric tons or metric tons CO2e."
                ),
                "properties": {
                    "example_key": {
                        "type": "number",
                        "description": "Example numeric emission value (metric tons)."
                    }
                }
            }
        },
        "required": ["data_value_map"],
    },
    )

    analysis_error_dec = FunctionDeclaration(
    name="analysis_error",
    description=(
        "Report errors encountered during greenhouse gas emissions analysis. "
        "Use this function when calculations cannot be completed due to missing data, invalid values, "
        "inappropriate parameters, or other issues that prevent accurate emissions quantification."
    ),
    parameters={
        "type": "object",
        "properties": {
            "error_map": {
                "type": "object",
                "description": (
                    "Dictionary containing error details with descriptive keys explaining what went wrong. "
                    "Keys should identify the specific issue or missing data, and values should provide clear explanations."
                ),
                "properties": {
                    "example_error": {
                        "type": "string",
                        "description": "Example error description (e.g., missing data, invalid value)."
                    }
                }
            }
        },
        "required": ["error_map"],
    },
    )
