from typing import List
import os
import requests

def search_linkedin_profiles(titles: List[str], config: dict, max_results_per_title: int = 4) -> List[str]:
    """
    Searches LinkedIn profiles using the Tavily API for each title/location combination.
    Returns a list of unique LinkedIn profile URLs.
    """
    tavily_api_key = config['TAVILY_API_KEY']
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY not set in config.")

    all_linkedin_urls = []
    for title in titles:
        # Split title and location (if comma is present)
        if "," in title:
            short_title, short_location = title.split(",", 1)
        else:
            short_title = title
            short_location = ""
        query = f'site:linkedin.com/in/ {short_title.strip()} {short_location.strip()}'
        response = requests.post(
            "https://api.tavily.com/search",
            headers={
                "Authorization": f"Bearer {tavily_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "query": query,
                "search_depth": "basic",
                "include_answer": False,
                "max_results": max_results_per_title
            }
        )
        if response.status_code == 200:
            data = response.json()
            urls = [r["url"] for r in data.get("results", []) if "linkedin.com/in/" in r["url"]]
            all_linkedin_urls.extend(urls)
        else:
            print(f"Tavily API failed for '{title}': {response.status_code} - {response.text}")
    # Deduplicate
    unique_urls = list(set(all_linkedin_urls))[:7]
    return unique_urls 