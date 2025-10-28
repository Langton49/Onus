from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import re
from .enums import FacilityType, EPASubpart

class LocationSchema(BaseModel):
    """Location information for a facility"""
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State or province")
    zip_code: str = Field(..., description="ZIP or postal code")
    country: str = Field(default="USA", description="Country code")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")

    @field_validator("zip_code")
    def validate_zip_code(cls, v):
        pattern = r"^\d{5}(-\d{4})?$"
        if not re.match(pattern, v):
            raise ValueError("Invalid ZIP code format. Use 12345 or 12345-6789.")
        return v

    @field_validator("latitude", mode="before")
    @classmethod
    def validate_latitude(cls, v):
        if v is not None and (v < -90 or v > 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return v
    
    @field_validator("longitude", mode="before")
    @classmethod
    def validate_longitude(cls, v):
        if v is not None and (v < -180 or v > 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v

class CreateFacilityRequest(BaseModel):
    """Request object to create a new facility"""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the facility")
    ghgrp_id: str = Field(..., min_length=1, max_length=100, description="GHGRP ID")
    description: Optional[str] = Field(None, min_length=10, max_length=1000, description="Facility description")
    facility_type: FacilityType = Field(..., description="Type of facility")
    naics_code: Optional[str] = Field(None, description="NAICS industry classification code")
    location: LocationSchema = Field(..., description="Facility location")
    applicable_subparts: List[EPASubpart] = Field(default_factory=list, description="Applicable EPA subparts for emissions reporting")
    
    @field_validator("naics_code", mode="before")
    @classmethod
    def validate_naics_code(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError("NAICS code must contain only digits.")
        return v
    
    class Config:
        use_enum_values = True

class UpdateFacilityRequest(BaseModel):
    """Request object for updating an existing facility"""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Facility name")
    facility_type: Optional[FacilityType] = Field(None, description="Type of facility")
    naics_code: Optional[str] = Field(None, description="NAICS industry classification code")
    location: Optional[LocationSchema] = Field(None, description="Facility location information")
    applicable_subparts: Optional[List[EPASubpart]] = Field(None, description="Applicable EPA subparts for emissions reporting")
    is_active: Optional[bool] = Field(None, description="Whether the facility is active")

    @field_validator('naics_code', mode="before")
    @classmethod
    def validate_naics_code(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('NAICS code must contain only digits')
        return v

    class Config:
        use_enum_values = True

class SearchFacilityRequest(BaseModel):
    """Request object for advanced facility search"""
    name: Optional[str] = Field(None, description="Search by facility name (partial match)")
    facility_type: Optional[FacilityType] = Field(None, description="Filter by facility type")
    naics_code: Optional[str] = Field(None, description="Filter by NAICS code")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    subpart: Optional[EPASubpart] = Field(None, description="Filter by applicable EPA subpart")
    state: Optional[str] = Field(None, description="Filter by state/province")
    city: Optional[str] = Field(None, description="Filter by city")

    @field_validator('naics_code', mode="before")
    @classmethod
    def validate_naics_code(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('NAICS code must contain only digits')
        return v

    class Config:
        use_enum_values = True

class GeneralFacilityResponse(BaseModel):
    """Response object for facility response data"""
    id: uuid.UUID
    name: str
    ghgrp_id: str
    facility_type: FacilityType
    naics_code: Optional[str]
    location: Optional[Dict[str, Any]]
    applicable_subparts: List[EPASubpart]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

class ListFacilityResponse(BaseModel):
    """Schema for paginated facility list response"""
    facilities: List[GeneralFacilityResponse]
    total_results: int = Field(..., description="Total number of facilities")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

    @model_validator(mode="after")
    def set_total_pages(self):
        self.total_pages = (self.total_results + self.page_size - 1) // self.page_size
        return self