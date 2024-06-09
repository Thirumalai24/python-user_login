import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables from .env file, overriding existing variables
load_dotenv(override=True)

# Initialize a global variable to store the database client
db_client: AsyncIOMotorClient = None

# Asynchronous function to connect and initialize the database
async def get_db_conn():
    global db_client
    try:
        # Create a database client with the configured MongoDB URL
        db_client = AsyncIOMotorClient(
            os.getenv('MONGO_URL'),
            
        )
        return db_client[os.getenv('MONGO_DBNAME')]
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise e
