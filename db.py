import os, dotenv
import motor.motor_asyncio

dotenv.load_dotenv(".env")

uri = os.getenv("DB_URI")
# Create a new client and connect to the server
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)