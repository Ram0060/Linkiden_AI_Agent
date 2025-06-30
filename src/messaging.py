from typing import List, Dict
import os
from openai import OpenAI

def craft_linkedin_messages(candidates: List[Dict], config: dict) -> List[Dict]:
    """
    Generates personalized LinkedIn outreach messages for each candidate using OpenAI LLM.
    Returns a list of dicts with name, linkedin_url, and message.
    """
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    client = OpenAI()
    messages = []
    for candidate in candidates:
        name = candidate.get("name", "Candidate")
        url = candidate.get("linkedin_url", "")
        prompt = f"""
You are an AI sourcing assistant.

Craft a short and friendly LinkedIn message to reach out to this candidate for an ML Research Engineer role in Mountain View, CA.

Use the candidate's name. Avoid sounding too formal or robotic. Make the message feel personal and warm.

Candidate name: {name}
LinkedIn: {url}

Format your reply with ONLY the message text.
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You're a recruiter writing LinkedIn connection messages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
            if not content:
                message = ""
            else:
                message = content.strip()
            messages.append({
                "name": name,
                "linkedin_url": url,
                "message": message
            })
        except Exception as e:
            print(f"Error generating message for {name}: {e}")
            messages.append({
                "name": name,
                "linkedin_url": url,
                "message": ""
            })
    return messages 