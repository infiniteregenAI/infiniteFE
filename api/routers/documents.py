from fastapi import APIRouter, HTTPException , UploadFile, File 
import tempfile
import traceback
from core.document_generator import DocumentGenerator
from core.document_processor import DocumentProcessor
from api.models import (  
    GenerateSummaryRequest,
)

document_generator = DocumentGenerator()

router = APIRouter()

@router.post("/generate_summary")
async def generate_summary(request: GenerateSummaryRequest):
    """
        This api endpoint is used to generate a summary from the conversation. 
        
        Args :
            request (GenerateSummaryRequest) : The request details.
            
        Returns :
            str : The generated summary.
    """
    try:
        return document_generator.generate_summary(request.messages)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/process_document/{agent_id}")
async def process_document(agent_id: str,file: UploadFile = File(...)):
    """
        This api endpoint is used to process a document.
        
        Args :
            agent_id (str) : The id of the agent.
            file (UploadFile) : The document file.            
        Returns :
            Dict : The processed document details.
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        document_processor = DocumentProcessor(agent_id)
        content = await file.read()
        return document_processor.process_document(content, file.filename)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/extract_text_from_pdf/{agent_id}")
async def extract_text_from_pdf(agent_id: str, file: UploadFile = File(...)):
    """
        This api endpoint is used to extract text from a pdf.
        
        Args :
            agent_id (str) : The id of the agent.
            request (ExtractTextFromPDFRequest) : The request details.
            
        Returns :
            str : The extracted text.
    """
    try:
        if not file or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Uploaded file must be a PDF")
        
        content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(content)
            file_path = tmp_file.name
            
        document_processor = DocumentProcessor(agent_id)
        return document_processor._extract_text_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add_document/{agent_id}")
async def add_document(agent_id: str, file: UploadFile = File(...)):
    """
        This api endpoint is used to add a document to the agent's knowledge base.
        
        Args :
            agent_id (str) : The id of the agent.
            request (AddDocumentRequest) : The request details.
            
        Returns :
            Tuple[bool, str] : The result of the operation.
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        document_processor = DocumentProcessor(agent_id)
        content = await file.read()
        return document_processor.add_document(content=content, filename= file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))