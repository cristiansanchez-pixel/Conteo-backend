from ..mysql import Database
from ..models.file_model import FileModel, getFileModel
from ..utils.audit import save_audit_file
from pathlib import Path
from ..config import get_env
from uuid import uuid4 as uuid
from datetime import datetime
from fastapi.responses import FileResponse
import os
import openpyxl

class FileController: 
  
    async def upload_file(self, file: FileModel):
      MAX_FILE_SIZE = get_env().MICROS_FILE_SIZE
      ALLOWED_EXTENSIONS = get_env().ALLOWED_EXTENSIONS.split(",")
      with Database() as db:
        try:
            file_content = await file.read()
            file_size = len(file_content)
            if file_size > MAX_FILE_SIZE:
                return "File too large"
            file_extension = Path(file.filename).suffix
            if file_extension not in ALLOWED_EXTENSIONS:
                return "File type not allowed"

            original_filename = Path(file.filename).stem
            path = f"C:\Users\pope0\OneDrive\Escritorio\arcivhos_conteo{str(uuid())}.{file_extension}"
            Path( path).mkdir(parents=True, exist_ok=True)
            with open(f"{ path}/{file.filename}", "wb") as buffer:
                buffer.write(file_content)
                
            wb_obj = openpyxl.load_workbook(path)
            
            sheet_obj = wb_obj.activate
            
            headers = [sheet_obj.cell(row=1, clumn=col).value for col in range(1, sheet_obj.max_column + 1)]
            
            stock_col = headers.index("stock") + 1
            codigo_barras_col = headers.index("codigo_barras") + 1
            
            for row in range(2, sheet_obj.max_row + 1):
              row_data = {}
              
              for col_index, header in enumerate(headers, start=1):
                row_data[header] = sheet_obj.cell(row=row, column=col_index).value


            query = """
                INSERT INTO file
                
            """

            db.execute(
                query,
                (
                ),
            )

            save_audit_file(
                
            )
            return True
        except Exception as e:
            print(e)
            db.rollback()
        return None