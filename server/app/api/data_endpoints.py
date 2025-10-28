from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import AsyncGenerator
import json
import hashlib
import uuid
import asyncio
import redis
import pandas as pd

from agent.graph.graph_state import State, DocumentMetadata, FacilityMetadata
from database.base import get_db
from ..models.facility_model import Facility
from ..agent.helpers.process_document import DocumentParser, FileExtension
from ..schemas.data_schemas import FileUploadResponse, FileUploadForm

router = APIRouter(prefix="/api/data", tags=["Data Ingestion"])
document_parser = DocumentParser()

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

@router.post("/upload", response_model=FileUploadResponse)
async def upload_data(
    facility_id: uuid.UUID,
    file: UploadFile = File(...),
    form_data: FileUploadForm = Form(...),
    db: Session = Depends(get_db),
):
    """Upload data to Langgraph agent"""
    try:
        # Validate facility exists
        facility = db.query(Facility).filter(Facility.id == facility_id).first()
        if not facility:
            raise HTTPException(status_code=404, detail="Not associated with any facility")
        
        # Read file content once and reset pointer
        data_snapshot = document_parser.get_snapshot(file)
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer to beginning

        file_hash = hashlib.sha256(file_content).hexdigest()
        doc_fields = document_parser.extract_fields(file)
        file_ext = document_parser.get_file_ext(file)
        
        fac_metadata = FacilityMetadata(
            facility_type=facility.facility_type,
            facility_description=facility.description or "",
            subparts=facility.applicable_subparts,
            naics_code=facility.naics_code,
            reporting_year=form_data.reporting_year,
            equipment_types=form_data.equipment_types
        )

        doc_metadata = DocumentMetadata(
            doc_type=file_ext.value,
            file_hash=file_hash,
            fields=doc_fields
        )

        init_state = State(
            fac_metadata=fac_metadata,
            doc_metadata=doc_metadata,
            data_snapshot=data_snapshot
        )

        task_id = str(uuid.uuid4())

        return FileUploadResponse(
            success=True,
            message="File uploaded and is being processed",
            records_processed=0,
            records_created=0,
            file_hash=file_hash,
            task_id=task_id
        )
    except Exception as e:
        return FileUploadResponse(
            success=False,
            message="Error processing file",
            error=e,
            file_hash=None
        )
