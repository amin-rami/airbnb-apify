from apify_client import ApifyClientAsync
import math
import asyncio
from tqdm import tqdm


async def get_price_range_results(
    client: ApifyClientAsync,
    actor_id: str,
    run_config: dict,
    start_price: int,
) -> dict:
    run_input = dict(run_config)
    run_input["priceMin"] = start_price
    run_input["priceMax"] = start_price + 1
    run = await client.actor(actor_id).call(run_input=run_input)
    return run


async def push_data_to_target_dataset(
    client: ApifyClientAsync,
    origin_dataset_id: str,
    destination_dataset_id: str
) -> None:
    data = await client.dataset(origin_dataset_id).list_items()
    data = data.items
    await client.dataset(destination_dataset_id).push_items(data)


async def scrape(
    client: ApifyClientAsync,
    actor_id: str,
    run_config: str,
    start_price: int,
    end_price: int,
    number_of_runners: int,
    destination_dataset_id: str
) -> None:
    number_of_rounds = math.ceil((end_price - start_price + 1) / number_of_runners)
    for i in tqdm(range(number_of_rounds)):
        start = start_price + i * number_of_runners
        end = min(start_price + (i + 1) * number_of_runners, end_price)
        tasks = [
            get_price_range_results(client, actor_id, run_config, price) 
            for price in range(start, end)
        ]
        runs = await asyncio.gather(*tasks)
        
        tasks = [push_data_to_target_dataset(client, run["defaultDatasetId"], destination_dataset_id) for run in runs]
        await asyncio.gather(*tasks)
