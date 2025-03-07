from ..mysql import Database
from ..models.file_model import FileModel
# from ..utils.audit import save_audit_file
from pathlib import Path
from ..config import get_env
from uuid import uuid4 as uuid
from datetime import datetime 
# from fastapi.responses import FileResponse
import os
import openpyxl
import json
class FileController:   
    async def upload_file(self, file: FileModel):
      MAX_FILE_SIZE = get_env().MAX_FILE_SIZE
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

            folder_path = "C:\\Users\\pope0\\OneDrive\\Escritorio\\arcivhos_conteo"
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            file_path = f"{folder_path}\\{str(uuid())}.{file_extension}"
            
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
                
            wb_obj = openpyxl.load_workbook(file_path)
            sheet_obj = wb_obj.active
            
            wb_obj.close()
            
            headers = [sheet_obj.cell(row=1, column=col).value for col in range(
                1, sheet_obj.max_column + 1
                )]
            
            for row in range(2, sheet_obj.max_row + 1):
                
                data = {}               
                row_data = {}
                    
                for col_index, header in enumerate(headers, start=1):
                    row_data[header] = sheet_obj.cell(row=row, column=col_index).value
                    
                codigo_barras = row_data.get("codigo de barras")
                stock = row_data.get("stock")
                
                if codigo_barras is None or stock is None:
                    return "Data realmente invalida o faltan datos en el excel :("
                
                for key, value in row_data.items():
                    if key != "stock" and key != "codigo de barras":
                        data[key] = value          
                    
                    
            


            query = """
                INSERT INTO productos (codigo_barras, stock, data)
                VALUES (%s, %s, %s)
                
            """

            db.execute(
                query,
                (
                    row_data["codigo de barras"],
                    row_data["stock"],
                    json.dumps(data)
                ),
            )

            # save_audit_file(
                
            # )
            return True
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}