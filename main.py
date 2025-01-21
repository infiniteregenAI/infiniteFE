from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import agents, conversation , documents

app = FastAPI(title="Agent Conversation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(conversation.router, prefix="/api", tags=["conversation"])
app.include_router(documents.router, prefix="/api", tags=["documents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)