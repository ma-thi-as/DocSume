from fastapi import FastAPI, UploadFile
from io import BytesIO
import PyPDF2

from model_req import generate

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # Read the contents of the uploaded file as bytes
    f_content = await file.read()

    # Create a BytesIO object from the file content
    f_stream = BytesIO(f_content)

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(f_stream)

    # Get the number of pages in the PDF
    n_pages = len(pdf_reader.pages)

    # Initialize an empty string to store the text
    text = ''

    # Iterate through each page and extract text
    for page_num in range(n_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    # Close the file stream
    f_stream.close()

    

    # Return the filename and extracted text
    return {"filename": file.filename, "text": await generate(f"generate a resume strictly bassed on this document: {text}", [])}
