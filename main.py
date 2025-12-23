from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Replace these with your TMS credentials
TMS_UPLOAD_URL = "https://fhbio.stage.tmsonline.com/tms/tmsconnect/fileexchange"
TMS_USER = "jgoldstein@pronktech.com"
TMS_PASS = "Welcome1!"

@app.get("/upload", response_class=HTMLResponse)
def upload_form(workorder: str):
    return f"""
    <h3>Upload PDF for Work Order {workorder}</h3>
    <form action="/uploadfile" method="post" enctype="multipart/form-data">
        <input type="file" name="pdffile" accept=".pdf" required />
        <input type="hidden" name="workorder" value="{workorder}" />
        <input type="submit" value="Upload PDF" />
    </form>
    """

@app.post("/uploadfile")
def upload_file(workorder: str = Form(...), pdffile: UploadFile = None):
    if not pdffile:
        return {"status": "No file selected"}

    files = {"File": (pdffile.filename, pdffile.file, "application/pdf")}
    data = {"WorkOrderID": workorder, "DocumentType": "ProcedureReading"}
    response = requests.post(TMS_UPLOAD_URL, files=files, data=data, auth=(TMS_USER, TMS_PASS))

    return {
        "status": "Uploaded" if response.status_code == 200 else "Failed",
        "detail": response.text
    }
