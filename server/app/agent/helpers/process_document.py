from fastapi import UploadFile
import pandas as pd
from pandas import DataFrame
from schemas.enums import FileExtension

class DocumentParser:
    """Helper class to parse and chunk documents based on file type"""
    
    @staticmethod
    def get_file_ext(doc: UploadFile) -> FileExtension:
        try:
            file_ext = None
            if doc.filename.endswith('.csv'):
                file_ext = FileExtension.CSV
            elif doc.filename.endswith('.xlsx'):
                file_ext = FileExtension.XLSX
            else:
                raise ValueError("Unsupported file type")
            return file_ext
        except Exception as e:
            raise ValueError(f"Error determining file type: {e}")
        
    @staticmethod
    def extract_fields(doc: UploadFile) -> list[str]:
        """Extract column names from the document"""
        try:
            file_ext = DocumentParser.get_file_ext(doc)
            doc.file.seek(0)  # Reset file pointer
            if file_ext == FileExtension.CSV:
                df = pd.read_csv(doc.file, nrows=0)
                return df.columns.tolist()
            elif file_ext == FileExtension.XLSX:
                df = pd.read_excel(doc.file, engine="openpyxl", nrows=0)
                return df.columns.tolist()
            else:
                raise ValueError("Unsupported file type for extracting columns")
        except Exception as e:
            raise ValueError(f"Error extracting columns: {e}")
        
    @staticmethod
    def get_snapshot(doc:UploadFile) -> DataFrame:
        """Convert the first 5 rows of the document into a dataframe"""
        try:
            file_ext = DocumentParser.get_file_ext(doc)
            doc.file.seek(0) 

            if file_ext == FileExtension.CSV:
                df = pd.read_csv(doc.file, nrows=5)
                return df.to_string()
            
            elif file_ext == FileExtension.XLSX:
                df = pd.read_excel(doc.file, engine="openpyxl", nrows=5)
                return df.to_string()
            
            else:
                raise ValueError("Unsupported file type for dataframe conversion")
        except Exception as e:
            raise ValueError(f"Error converting document to dataframe: {e}")