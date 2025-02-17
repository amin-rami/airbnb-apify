from apify_client import ApifyClientAsync
from dotenv import load_dotenv
import os
import asyncio
from utils import scrape

load_dotenv()

API_TOKEN = os.getenv("APIFY_API_TOKEN")
DATASET_ID = os.getenv("DATASET_ID")
ACTOR_ID = os.getenv("ACTOR_ID")
MAX_RUNNER_INSTANCES= int(os.getenv("MAX_RUNNER_INSTANCES"))
MIN_PRICE = int(os.getenv("MIN_PRICE"))
MAX_PRICE = int(os.getenv("MAX_PRICE"))


client = ApifyClientAsync(token=API_TOKEN)


run_config = {
    "currency": "USD",
    "locale": "en-US",
    "locationQueries": [
        "Dubai"
    ],
}


asyncio.run(scrape(
    client,
    ACTOR_ID,
    run_config,
    MIN_PRICE,
    MAX_PRICE,
    MAX_RUNNER_INSTANCES,
    DATASET_ID
    )
)
