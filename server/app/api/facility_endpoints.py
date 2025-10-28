from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid
from utils.auth import Auth
from database.base import get_db
from ..models.facility_model import Facility
from ..schemas.facility_schemas import (
    GeneralFacilityResponse, 
    ListFacilityResponse, 
    UpdateFacilityRequest, 
    CreateFacilityRequest, 
    SearchFacilityRequest
    )

router = APIRouter(prefix="/api/facilities", tags=["facilities"])

@router.get('/', response_model=ListFacilityResponse, status_code=200)
async def list_facilities(
    page: int = Query(1, ge=1, description="Page number"), 
    page_size: int = Query(10, ge=5, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    List all facilities with pagination
    """
    try:
        query = db.query(Facility)
        total_results = query.count()

        # Apply pagination
        offset = (page - 1) * page_size
        facilities = query.offset(offset).limit(page_size).all()

        return ListFacilityResponse(
            facilities=facilities,
            total_results=total_results,
            page=page,
            page_size=page_size,
            total_pages=(total_results + page_size - 1) // page_size
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to list facilities: {str(e)}")

@router.post('/register', response_model=GeneralFacilityResponse, status_code=201, dependencies=[Depends(Auth.require_role('DESIGNATED_REP'))])
async def register_facility(facility_data: CreateFacilityRequest, db: Session = Depends(get_db)):
    try:
        location_dict = facility_data.location.model_dump() # Turn location to a dict
        
        # Create new record
        facililty = Facility(
            name = facility_data.name,
            ghgrp_id = facility_data.ghgrp_id,
            facility_type = facility_data.facility_type,
            description = facility_data.description,
            naics_code = facility_data.naics_code,
            location = location_dict,
            applicable_subparts = facility_data.applicable_subparts,
        )
        
        # Push to db and fetch record with default and auto-configured fields
        db.add(facililty)
        db.commit()
        db.refresh(facililty)

        return facililty
    
    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=400, detail="Facility with this name or identifier already exists")
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occured while registering new facility")

@router.put('/{facility_id}', response_model=GeneralFacilityResponse, status_code=200, dependencies=[Depends(Auth.require_role('DESIGNATED_REP'))])
async def update_facility(facility_id: uuid.UUID, facility_data: UpdateFacilityRequest, db: Session = Depends(get_db)):
    """Update existing facility"""
    try:
        facility = db.query(Facility).filter(Facility.id == facility_id).first() # Get the facility from db

        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
        
        update_data = facility_data.model_dump(exclude_unset=True)
    
        for field, value in update_data.items():
            if field == "location" and value:
                setattr(facility, field, value.model_dump() if hasattr(value, 'model_dump') else value)
            elif field == "applicable_subparts" and value:
                setattr(facility, field, [item.value for item in value])
            else:
                setattr(facility, field, value)
        
        db.commit()
        db.refresh(facility)

        return facility

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occured while updating facility")
    
@router.post('/search', response_model=ListFacilityResponse, status_code=200)
async def search_facilities(search_data: SearchFacilityRequest, 
                            page: int = Query(1, ge=1, description="Page number"), 
                            page_size: int = Query(10, ge=5, le=100, description="number of records per page"),
                            db: Session = Depends(get_db)):
    try:
        query = db.query(Facility)
        
        # Apply each filter in the search request
        if search_data.name:
            query = query.filter(Facility.name.ilike(f"%{search_data.name}%"))
        
        if search_data.facility_type:
            query = query.filter(Facility.facility_type == search_data.facility_type.value)
        
        if search_data.naics_code:
            query = query.filter(Facility.naics_code == search_data.naics_code)
        
        if search_data.is_active is not None:
            query = query.filter(Facility.is_active == search_data.is_active)

        if search_data.subpart:
            query = query.filter(Facility.applicable_subparts.contains([search_data.subpart.value]))
        
        if search_data.city:
            query = query.filter(Facility.location['city'].astext.ilike(f"%{search_data.city}%"))
        
        if search_data.state:
            query = query.filter(Facility.location['state'].astext.ilike(f"%{search_data.state}%"))
        
        total_results = query.count()

         # Apply pagination
        offset = (page - 1) * page_size
        facilities = query.offset(offset).limit(page_size).all()

        return ListFacilityResponse(
            facilities=facilities,
            total_results=total_results,
            page=page,
            page_size=page_size,
            total_pages=(total_results + page_size - 1) // page_size
        )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to search facilities: {str(e)}")
    

