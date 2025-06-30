from typing import Dict, List
import os
from openai import OpenAI

def generate_alternate_titles(structured_info: Dict, config: dict) -> List[str]:
    """
    Generates alternate job titles using OpenAI's GPT model based on structured job info.
    Returns a list of suggested titles.
    """
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    client = OpenAI()
    job_data = structured_info["job_info"][0]
    title = job_data["title"]
    location = job_data["location"]
    keywords = job_data["keywords"]

    prompt = f"""
You are a technical recruiter.

Here is a job description summary:
- Title: {title}
- Location: {location}
- Keywords: {keywords}

Tasks:
1. Suggest 5 alternate job titles.
   Only return a list like:
   - Title 1
   - Title 2
   - Title 3
   - Title 4
   - Title 5
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a sourcing assistant helping find candidates on LinkedIn."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    content = response.choices[0].message.content
    if not content:
        # If the LLM response is empty, return an empty list
        return []
    suggested_titles = [
        f"{line.lstrip('- ').strip()}, {location}"
        for line in content.splitlines()
        if line.strip().startswith("-")
    ]
    return suggested_titles 