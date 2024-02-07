from fastapi import FastAPI, UploadFile, HTTPException
from io import BytesIO
import PyPDF2

from model_req import generate

app = FastAPI()

allowed_files = ["pdf", "txt"]

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # Read the contents of the uploaded file as bytes
        # file content read file 
        f_content : file = await file.read()
        # Create a BytesIO object from the file content
        f_stream : BytesIO = BytesIO(f_content)

        # Initialize an empty string to store the text
        text : str = ''

        if file.filename.endswith(allowed_files[0]):
        
            # Create a PDF reader object
            pdf_reader : PyPDF2 = PyPDF2.PdfReader(f_stream)
        
            # Get the number of pages in the PDF
            n_pages : int = len(pdf_reader.pages)
        
        
            # Iterate through each page and extract text
            for page_num in range(n_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
            # Close the file stream
            f_stream.close()

            # Return the filename and extracted text and pass the context
            return {"filename": file.filename, "text": await generate(f"generate a resume strictly bassed on this document : {text}", [])}

        elif file.filename.endswith(allowed_files[1]):
            text = f_stream.read().decode("utf-8")
            return {"filename": file.filename, "text": await generate(f"generate a resume strictly bassed on this document only 100 chars: {text}", [])}

        else:
            raise HTTPException(status_code=404, detail="Extension file not allowed")
            
