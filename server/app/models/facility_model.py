from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from database.base import Base

class Facility(Base):
    __tablename__ = "facilities"

    # Table columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ghgrp_id = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    facility_type = Column(String(50), nullable=False)  # FacilityType enum
    description = Column(String(1000), nullable=True)
    naics_code = Column(String(10), nullable=True)
    location = Column(JSON, nullable=False)  # {"latitude": float, "longitude": float, "address": str}
    applicable_subparts = Column(JSON, nullable=False, default=list)  # List of EPASubpart enums
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    
    # Relationship 
    users = relationship("User", back_populates="facility", cascade="all, delete-orphan", passive_deletes=True)