import chromadb

def get_chroma_client():
    """
    Create a ChromaDB client with consistent settings.
    """
    settings = chromadb.Settings(
        anonymized_telemetry=False,
        allow_reset=True,
        is_persistent=True,
        persist_directory="db"
    )
    
    return chromadb.PersistentClient(
        path="db",
        settings=settings
    )