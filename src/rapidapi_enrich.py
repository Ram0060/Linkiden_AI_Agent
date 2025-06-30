from typing import List, Dict
import requests
import time
from urllib.parse import quote
import os
from dotenv import load_dotenv
load_dotenv()




def enrich_profiles_with_rapidapi(linkedin_urls: List[str], config: dict, limit: int = 10) -> List[Dict]:
    """
    Enriches LinkedIn profiles using RapidAPI. Returns a list of profile data dicts.
    Only processes up to `limit` profiles (default 10 for testing).
    Always wraps the returned profile in a {'data': ...} dictionary for consistency.
    """
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    rapidapi_host = os.getenv("RAPIDAPI_HOST")
    endpoint = f"https://{rapidapi_host}/get-linkedin-profile"
    results = []
    for url in linkedin_urls[:limit]:
        encoded_url = quote(url, safe='')
        full_url = f"{endpoint}?linkedin_url={encoded_url}&include_skills=true"
        try:
            response = requests.get(
                full_url,
                headers={
                    "X-RapidAPI-Key": rapidapi_key,
                    "X-RapidAPI-Host": rapidapi_host
                }
            )
            if response.status_code == 200:
                profile_data = response.json()
                results.append({"data": profile_data})  # Always wrap in 'data' key
            else:
                print(f"RapidAPI failed for {url}: {response.status_code} - {response.text}")
            time.sleep(1)  # Respect rate limits
        except Exception as e:
            print(f"Error processing {url}: {e}")
    return results 