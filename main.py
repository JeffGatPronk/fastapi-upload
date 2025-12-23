from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
import httpx  # Async HTTP client

app = FastAPI()

# === Replace with your TMS credentials ===
TMS_UPLOAD_URL = "https://fhbio.stage.tmsonline.com/tms/tmsconnect/fileexchange"
TMS_USER = "jgoldstein@pronktech.com"
TMS_PASS = "Welcome1!"


@app.get("/upload", response_class=HTMLResponse)
async def upload_form(workorder: str):
    """
    Display an HTML form to pick a PDF file for the given work order.
    """
    return f"""
    <h3>Upload PDF for Work Order {workorder}</h3>
    <form action="/uploadfile" method="post" enctype="multipart/form-data">
        <input type="file" name="pdffile" accept=".pdf" required />
        <input type="hidden" name="workorder" value="{workorder}" />
        <input type="submit" value="Upload PDF" />
    </form>
    """


@app.post("/uploadfile")
async def upload_file(workorder: str = Form(...), pdffile: UploadFile = None):
    """
    Receives PDF file and posts it to TMS Procedure Readings asynchronously.
    """
    if not pdffile:
        return {"status": "No file selected"}

    # Read file content asynchronously
    file_content = await pdffile.read()
    files = {"File": (pdffile.filename, file_content, "application/pdf")}
    data = {"WorkOrderID": workorder, "DocumentType": "ProcedureReading"}

    # Async POST to TMS
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(
                TMS_UPLOAD_URL,
                files=files,
                data=data,
                auth=(TMS_USER, TMS_PASS)
            )
        except Exception as e:
            return {"status": "Failed", "detail": str(e)}

    return {
        "status": "Uploaded" if response.status_code == 200 else "Failed",
        "detail": response.text
    }
