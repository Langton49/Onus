from typing import TypedDict, Optional

class EquipmentDetail(TypedDict):
    type: str                                       # Boiler, Turbine, Flare, etc.
    fuel: Optional[str]
    capacity: Optional[str]
    unit_id: Optional[str]

class FacilityMetadata(TypedDict):
    facility_type: str
    subparts: list[str]
    facility_description: Optional[str]
    naics_code: Optional[str]
    reporting_year: Optional[int]
    equipment_types: Optional[list[EquipmentDetail]]

class DocumentMetadata(TypedDict):
    doc_type: str                                   # JSON, CSV, XML, EXCEL
    file_hash: str
    fields: Optional[list[str]]

class State(TypedDict, total=False):
    fac_metadata: Optional[FacilityMetadata]                  # Context for facility
    doc_metadata: Optional[DocumentMetadata]
    data_snapshot: Optional[str]
    regulatory_context: Optional[str]                         # AI generated context
    
    validation_status: Optional[str]                # PASSED, WARNING, FAILED
    
    errors: Optional[dict[str, list[str]]]          # Errors with explanations
    suggestions: Optional[dict[str, list[str]]]     # Quality or improvement suggestions
    notes: Optional[dict[str, list[str]]]           # Other observations / regulatory insights





