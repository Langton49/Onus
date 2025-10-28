from .graph import AgentGraph
from .graph_state import State

agent_graph = AgentGraph()

example_state = {
    "fac_metadata": {
        "facility_type": "Power Plant",
        "subparts": ["C", "D"],
        "facility_description": "Coal-fired electricity generating facility",
        "naics_code": "221112",
        "monitoring_method": "CEMS",
        "reporting_year": 2024,
        "equipment_types": [
            {
                "type": "Boiler",
                "fuel": "Coal",
                "capacity": "500 MW",
                "unit_id": "B-101"
            },
            {
                "type": "Turbine",
                "fuel": None,
                "capacity": "450 MW",
                "unit_id": "T-201"
            }
        ]
    },
    "doc_metadata": {
        "doc_type": "CSV",
        "file_hash": "abc123def456...",
        "fields": ["date", "emissions", "unit_id"]
    },
    "data_snapshot": """        date  emissions unit_id
0  2024-01-01      10.5   B-101
1  2024-01-02      11.0   B-101
2  2024-01-03       9.8   B-101
3  2024-01-01       0.0   T-201
4  2024-01-02       0.0   T-201"""
}

example_state_2 = {
    "fac_metadata": {
        "facility_type": "Power Plant",
        "subparts": ["C", "D", "G"],
        "facility_description": "Coal-fired electricity generating facility with auxiliary gas turbines",
        "naics_code": "221112",
        "monitoring_method": "CEMS",
        "reporting_year": 2024,
        "equipment_types": [
            {
                "type": "Boiler",
                "fuel": "Coal",
                "capacity": "500 MW",
                "unit_id": "B-101"
            },
            {
                "type": "Turbine",
                "fuel": "Natural Gas",
                "capacity": "150 MW",
                "unit_id": "T-301"
            },
            {
                "type": "Flare",
                "fuel": "Waste Gas",
                "capacity": "50 MW",
                "unit_id": "F-401"
            }
        ]
    },
    "doc_metadata": {
        "doc_type": "CSV",
        "file_hash": "abc123def456...",
        "fields": ["date", "emissions", "unit_id", "heat_input", "fuel_type"]
    },
    "data_snapshot": """        date  emissions unit_id  heat_input fuel_type
0  2024-01-01      10.5   B-101       2000       Coal
1  2024-01-02      11.0   B-101       2100       Coal
2  2024-01-03       9.8   B-101       1950       Coal
3  2024-01-01       0.0   T-301        500       Gas
4  2024-01-02       0.0   T-301        520       Gas
5  2024-01-01       1.2   F-401         50     Waste Gas""",
    "regulatory_context": None,
    "chunk_index": 0,
    "total_chunks": 1,
    "validation_status": None,
    "errors": {},
    "suggestions": {},
    "notes": {}
}


print(agent_graph.get_regulatory_context(example_state_2))
