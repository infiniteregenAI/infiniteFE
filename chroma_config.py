import chromadb

def get_chroma_client():
    """
        This method returns a chromadb client.
        
        Returns :
            chromadb.PersistentClient : The chromadb client.
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