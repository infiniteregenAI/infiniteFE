from typing import List, Dict, Tuple
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings  
import chromadb
import PyPDF2
import tempfile

class DocumentProcessor:
    def __init__(self, agent_id: str):
        """
        This constructor initializes the document processor.

        Args :
            agent_id (str): The id of the agent.

        Returns :
            None
        """
        self.agent_id = agent_id
        self.db_path = f"agent_knowledge/{agent_id}"
        os.makedirs(self.db_path, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name=f"agent_{agent_id}_knowledge"
        )

        self.embeddings = OpenAIEmbeddings()  # Updated to the new class
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def process_document(self, content: bytes, filename: str) -> Dict[str, List]:
        """
        This method processes a document.

        Args :
            content (bytes): The document content.
            filename (str): The document filename.

        Returns :
            Dict[str, List]: The processed document details.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
            tmp_file.write(content)
            file_path = tmp_file.name

        try:
            if filename.lower().endswith('.pdf'):
                text = self._extract_text_from_pdf(file_path)
            else:
                text = content.decode('utf-8')

            chunks = self.text_splitter.split_text(text)
            return {
                "chunks": chunks,
                "metadatas": [{"source": filename, "index": i} for i in range(len(chunks))]
            }
        finally:
            os.unlink(file_path)

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """
        This method extracts text from a pdf.

        Args :
            file_path (str): The path to the pdf file.

        Returns :
            str: The extracted text.
        """
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return "\n".join(page.extract_text() for page in pdf_reader.pages)

    def add_document(self, content: bytes, filename: str) -> Tuple[bool, str]:
        """
        This method adds a document to the knowledge base.

        Args :
            content (bytes): The document content.
            filename (str): The document filename.

        Returns :
            Tuple[bool, str]: The result of the operation.
        """
        try:
            doc_data = self.process_document(content, filename)
            embeddings = self.embeddings.embed_documents(doc_data["chunks"])

            self.collection.add(
                embeddings=embeddings,
                documents=doc_data["chunks"],
                metadatas=doc_data["metadatas"],
                ids=[f"{filename}_{i}" for i in range(len(doc_data["chunks"]))]
            )
            return True, f"Successfully processed {filename}"
        except Exception as e:
            return False, str(e)

    def get_relevant_context(self, query: str, k: int = 3) -> List[str]:
        """
        This method gets the relevant context for a query.

        Args :
            query (str): The query.
            k (int): The number of results to return.

        Returns :
            List[str]: The relevant context.
        """
        query_embedding = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results["documents"][0] if results["documents"] else []

