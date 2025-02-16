from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("APIFY_API_TOKEN")
client = ApifyClient(token=API_TOKEN)
run_id = "1DPJlsIhQtfekMyV5"

run = client.run(run_id)
print(run.dataset().list_items().items)
