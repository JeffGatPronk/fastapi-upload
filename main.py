from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

TMS_UPLOAD_URL = "https://fhbio.stage.tmsonline.com/tms/tmsconnect/fileexchange"
TMS_USER = "Yjgoldstein@pronktech.com"
TMS_PASS = "Welcome1!"

@app.post("/uploadfile")
async def upload_file(workorder: str = Form(...), pdffile: UploadFile = None):
    if not pdffile:
        return {"status": "No file selected"}

    file_content = await pdffile.read()
    files = {"File": (pdffile.filename, file_content, "application/pdf")}
    data = {"WorkOrderID": workorder, "DocumentType": "ProcedureReading"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                TMS_UPLOAD_URL,
                files=files,
                data=data,
                auth=(TMS_USER, TMS_PASS),
                timeout=30
            )
        except Exception as e:
            return {"status": "Failed", "detail": str(e)}

    return {
        "status": "Uploaded" if response.status_code == 200 else "Failed",
        "detail": response.text
    }
