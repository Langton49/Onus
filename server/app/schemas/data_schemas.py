from pydantic import BaseModel, Field
from typing import List, Optional, Literal

from .enums import ValidationStatus, QualityFlag
    
class Errors(BaseModel):
    missing_fields: list[str]
    invalid_format: list[str]
    other: list[str]

class EquipmentDetail(BaseModel):
    type: str 
    fuel: Optional[str]
    capacity: Optional[str]
    unit_id: Optional[str]

class FileUploadForm(BaseModel):
    reporting_year: str = Field(..., description="Reporting year")
    equipment_types: Optional[List[EquipmentDetail]] = Field(None, default_factory=list)

class FileUploadResponse(BaseModel):
    success: bool
    message: str
    records_processed: int
    records_created: int
    errors: List[Errors] = Field(default_factory=list)
    file_hash: Optional[str] = None
    task_id: Optional[str] = None

class ModelResponseSchema(BaseModel):
    equation_names_list: list[str]
    flag: QualityFlag
    validation_status: ValidationStatus
    errors: Errors
    summary: str

    class Config:
        use_enum_values = True

"""
Below is the different parts of the CEMS reporting form that are filled out by the AI model
"""

class ProcessUnit(BaseModel):
    """Process/Unit table entry"""
    name_or_id: Optional[str] = Field(None, description="Name or ID of process/unit monitored by CEMS")
    description: Optional[str] = Field(None, description="Description of process/unit (optional)")
    fuel_name: Optional[str] = Field(None, description="Name of each fuel combusted in unit")

class CMLMonitoringLocation(BaseModel):
    """Single CML monitoring location"""
    cml_name_or_id: Optional[str] = Field(None, description="CML Name or ID")
    description: Optional[str] = Field(None, description="Description or label (optional)")
    configuration: Optional[Literal[
        "Single industrial process or process unit that exhausts to a dedicated stack",
        "Multiple industrial processes or process units share a common stack",
        "Industrial process or process unit shares a common stack with one or more stationary fuel combustion units"
    ]] = Field(..., description="Configuration type")

    process_unit_1: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 1")
    process_unit_2: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 2")
    process_unit_3: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 3")
    process_unit_4: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 4")
    process_unit_5: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 5")
    process_unit_6: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 6")
    process_unit_7: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 7")
    process_unit_8: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 8")
    process_unit_9: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 9")
    process_unit_10: Optional[str] = Field(None, description="Name or ID of Process/Unit Monitored by this CML - 10")
    
    quarter_1_co2_emissions: Optional[float] = Field(None, ge=0, description="Q1 Cumulative CO2 Emissions (metric tons)")
    quarter_2_co2_emissions: Optional[float] = Field(None, ge=0, description="Q2 Cumulative CO2 Emissions (metric tons)")
    quarter_3_co2_emissions: Optional[float] = Field(None, ge=0, description="Q3 Cumulative CO2 Emissions (metric tons)")
    quarter_4_co2_emissions: Optional[float] = Field(None, ge=0, description="Q4 Cumulative CO2 Emissions (metric tons)")
    
    methodology_start_date: Optional[str] = Field(None, description="Methodology Start Date (mm/dd/yyyy)")
    methodology_end_date: Optional[str] = Field(None, description="Methodology End Date (mm/dd/yyyy)")
    
    total_annual_biogenic_co2_emissions: Optional[float] = Field(None, ge=0, description="Total Annual Biogenic CO2 Emissions (metric tons)")
    total_annual_non_biogenic_co2_emissions: Optional[float] = Field(None, ge=0, description="Total Annual Non-Biogenic CO2 Emissions (metric tons)")
    total_annual_co2_measured: Optional[float] = Field(None, ge=0, description="Total Annual CO2 Measured by CEMS (metric tons)")
    total_annual_ch4: Optional[float] = Field(None, ge=0, description="Total Annual CH4 Emissions (metric tons)")
    total_annual_n2o: Optional[float] = Field(None, ge=0, description="Total Annual N2O Emissions (metric tons)")
    
    total_annual_operating_hours: Optional[float] = Field(None, ge=0, description="Total Annual Source Operating Hours")
    total_hours_substitute_data_co2_concentration: Optional[float] = Field(None, ge=0, description="Hours substitute data used for CO2 concentration")
    total_hours_substitute_data_stack_gas_flow_rate: Optional[float] = Field(None, ge=0, description="Hours substitute data used for stack gas flow rate")
    total_hours_substitute_data_moisture_content: Optional[float] = Field(None, ge=0, description="Hours substitute data used for moisture content")
    
    includes_bypass_emissions: Optional[Literal["Yes", "No"]] = Field(
        None, 
        description="Do emissions include slipstream that bypassed CEMS per 98.33(a)(4)(viii)?"
    )

class CEMSReportingForm(BaseModel):
    """Complete CEMS Reporting Form structure"""
    
    # Facility Information (C9-C12)
    facility_name: Optional[str] = Field(None, description="Facility Name")
    ghgrp_id: Optional[str] = Field(None, description="GHGRP ID")
    subpart: Optional[Literal[
        "Subpart R", "Subpart S", "Subpart Z", "Subpart BB", 
        "Subpart CC", "Subpart EE", "Subpart GG"
    ]] = Field(None, description="Applicable Subpart")
    reporting_period: Optional[Literal[
        "2016", "2017", "2018", "2019", "2020", 
        "2021", "2022", "2023", "2024", "2025"
    ]] = Field(None, description="Reporting Period (Year)")
    
    # Process Units Table (B26-D45, max 20 entries)
    process_units: List[ProcessUnit] = Field(
        default_factory=list,
        max_items=20,
        description="List of process/units monitored by CEMS"
    )
    
    # CML Monitoring Locations (up to 10 sections)
    cml_locations: List[CMLMonitoringLocation] = Field(
        default_factory=list,
        max_items=10,
        description="CML (Continuous Monitoring Location) sections"
    )
    
    # Metadata for traceability
    class Config:
        json_schema_extra = {
            "description": "EPA GHGRP CEMS Reporting Form - Structured data matching Excel template",
            "source_file": "https://uat.ccdsupport.com/sites/default/files/2025-01/CEMS%20Reporting%20Form%20for%20RY2019%20-%20RY2024.xlsx",
        }