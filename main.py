from apify_client import ApifyClient
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

API_TOKEN = os.getenv("APIFY_API_TOKEN")
DATASET_ID = os.getenv("DATASET_ID")
min_price = int(os.getenv("MIN_PRICE"))
max_price = int(os.getenv("MAX_PRICE"))


client = ApifyClient(token=API_TOKEN)


template = {
    "currency": "USD",
    "locale": "en-US",
    "locationQueries": [
        "Dubai"
    ],
}


for price in tqdm(range(min_price, max_price)):
    run_input = dict(template)
    run_input["priceMin"] = price
    run_input["priceMax"] = price + 1
    run = client.actor("GsNzxEKzE2vQ5d9HN").call(run_input=run_input)

    run_dataset_id = run["defaultDatasetId"]
    run_results = client.dataset(run_dataset_id).list_items().items
    client.dataset(DATASET_ID).push_items(run_results)
