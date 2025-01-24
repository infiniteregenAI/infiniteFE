from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.knowledge.text import TextKnowledgeBase
from phi.document.chunking.semantic import SemanticChunking
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.knowledge.combined import CombinedKnowledgeBase
from phi.vectordb.pgvector import PgVector
import os 
from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DB_URL")

climate_ai_pdf_knowledge_base = PDFKnowledgeBase(
    path="data/climate_ai_data/pdfs",  
    vector_db=PgVector(
        table_name="climate_ai_pdf_vectors",  
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
    reader=PDFReader(chunk=True),  
)

climate_ai_txt_knowledge_base = TextKnowledgeBase(
    path="data/climate_ai_data/txts",
    vector_db=PgVector(
        table_name="climate_ai_txt_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)
    
climate_ai_website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://science.nasa.gov/climate-change/","https://www.unep.org/publications-data","https://www.ipcc.ch/reports/"],
    max_depth=10,
    vector_db=PgVector(
        table_name="climate_ai_websites_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)

climate_ai_knowledge_base = CombinedKnowledgeBase(
    sources=[
        climate_ai_pdf_knowledge_base, 
        climate_ai_txt_knowledge_base,
        climate_ai_website_knowledge_base
    ],
    vector_db=PgVector(
        table_name="climate_ai_combined_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)

green_pill_ai_pdf_knowledge_base = PDFKnowledgeBase(
    path="data/green_pill_ai_pdfs",  
    vector_db=PgVector(
        table_name="green_pill_ai_pdf_vectors",  
        db_url=DB_URL, 
    ),
    reader=PDFReader(chunk=True),
    chunking_strategy=SemanticChunking(),
)

green_pill_ai_website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://greenpill.network/","https://refi.gitbook.io/docs","https://www.investopedia.com/what-is-regenerative-finance-refi-7098179","https://www.pwc.com/m1/en/publications/carbon-credit-tokenization.html"],
    max_depth=10,
    vector_db=PgVector(
        table_name="green_pill_ai_websites_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)

green_pill_ai_knowledge_base = CombinedKnowledgeBase(
    sources=[
        green_pill_ai_pdf_knowledge_base,
        green_pill_ai_website_knowledge_base
    ],
    vector_db=PgVector(
        table_name="green_pill_ai_combined_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)

owocki_ai_pdf_knowledge_base = PDFKnowledgeBase(
    path="data/owocki_ai_pdfs",  
    vector_db=PgVector(
        table_name="owocki_ai_pdf_vectors",  
        db_url=DB_URL, 
    ),
    reader=PDFReader(chunk=True),
    chunking_strategy=SemanticChunking(),
)

owocki_ai_txt_knowledge_base = TextKnowledgeBase(
    path="data/owocki_ai_data/txts",
    vector_db=PgVector(
        table_name="owocki_ai_txt_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)

owocki_ai_website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://owocki.com/","https://impactdaos.xyz/","https://gov.gitcoin.co/"],
    max_depth=10,
    vector_db=PgVector(
        table_name="owocki_ai_websites_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking(),
)

owocki_ai_knowledge_base = CombinedKnowledgeBase(
    sources=[
        owocki_ai_pdf_knowledge_base,
        owocki_ai_txt_knowledge_base,
        owocki_ai_website_knowledge_base
    ],
    vector_db=PgVector(
        table_name="owocki_ai_combined_vectors",
        db_url=DB_URL, 
    ),
    chunking_strategy=SemanticChunking()
)    
    
gitcoin_ai_pdf_knowledge_base = PDFKnowledgeBase(
    path="data/gitcoin_ai_pdfs",  
    vector_db=PgVector(
        table_name="gitcoin_ai_pdf_vectors",  
        db_url=DB_URL, 
    ),
    reader=PDFReader(chunk=True),
)

gitcoin_ai_website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://science.nasa.gov/climate-change/"],
    max_depth=10,
    vector_db=PgVector(
        table_name="gitcoin_ai_websites_vectors",
        db_url=DB_URL, 
    ),
)

gitcoin_ai_knowledge_base = CombinedKnowledgeBase(
    sources=[
        gitcoin_ai_pdf_knowledge_base,
        gitcoin_ai_website_knowledge_base
    ],
    vector_db=PgVector(
        table_name="gitcoin_ai_combined_vectors",
        db_url=DB_URL, 
    )
)