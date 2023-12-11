import os

def get_mongo_connection_string():
    ATLAS_USERNAME = os.getenv("ATLAS_USERNAME")
    ATLAS_PASSWORD = os.getenv("ATLAS_PASSWORD")
    ATLAS_CLUSTER = os.getenv("ATLAS_CLUSTER")
    ATLAS_DB_NAME = os.getenv("ATLAS_DB_NAME")
    ATLAS_COLLECTION_NAME = os.getenv("ATLAS_COLLECTION_NAME")

    # Формирование строки подключения к MongoDB Atlas
    ATLAS_CONNECTION_URL = f"mongodb+srv://{ATLAS_USERNAME}:{ATLAS_PASSWORD}@{ATLAS_CLUSTER}/{ATLAS_DB_NAME}?retryWrites=true&w=majority"
    
    return ATLAS_CONNECTION_URL, ATLAS_DB_NAME, ATLAS_COLLECTION_NAME