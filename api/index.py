from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import agents, conversation, documents

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the origins as per your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}


app.include_router(agents.router , prefix="/api/py" , tags=["agents"]) 
app.include_router(conversation.router , prefix="/api/py" , tags=["conversation"])
app.include_router(documents.router , prefix="/api/py" , tags=["documents"])