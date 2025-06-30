from typing import List, Dict
import os
import json
from openai import OpenAI

def score_candidates(profiles: List[Dict], rubric: str, config: dict) -> List[Dict]:
    """
    Scores each candidate profile using OpenAI LLM and the provided rubric.
    Returns a list of scored candidate dicts.
    Expects each profile to be a flat dict (not nested under 'data').
    """
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    client = OpenAI()
    results = []
    for profile in profiles:
        url = profile.get('linkedin_url', '')
        prompt = f"""
You are an expert technical recruiter.

Your task is to rate a candidate based on the provided LinkedIn profile data and the scoring rubric below.

Rubric:
{rubric}

Profile Data: {json.dumps(profile)}

Return **only** a valid JSON object in this format:
{{
  "name": "Full Name (or 'Unknown' if not present)",
  "linkedin_url": "{url}",
  "fit_score": <float from 1.0 to 10.0>,
  "score_breakdown": {{
    "education": <float>,
    "trajectory": <float>,
    "company": <float>,
    "skills": <float>,
    "location": <float>,
    "tenure": <float>
  }}
}}

Only return the JSON. Do not include explanations, markdown, or commentary.
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a JSON-only evaluator assistant. You return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            content = response.choices[0].message.content
            if not content:
                # If the LLM response is empty, append a default result
                results.append({
                    "name": "Unknown",
                    "linkedin_url": url,
                    "fit_score": 0.0,
                    "score_breakdown": {
                        "education": 0.0,
                        "trajectory": 0.0,
                        "company": 0.0,
                        "skills": 0.0,
                        "location": 0.0,
                        "tenure": 0.0
                    }
                })
                continue
            results.append(json.loads(content.strip()))
        except json.JSONDecodeError:
            print(f"LLM output was not valid JSON for: {url}")
            results.append({
                "name": "Unknown",
                "linkedin_url": url,
                "fit_score": 0.0,
                "score_breakdown": {
                    "education": 0.0,
                    "trajectory": 0.0,
                    "company": 0.0,
                    "skills": 0.0,
                    "location": 0.0,
                    "tenure": 0.0
                }
            })
        except Exception as e:
            print(f"Unexpected error for {url}: {e}")
            results.append({
                "name": "Unknown",
                "linkedin_url": url,
                "fit_score": 0.0,
                "score_breakdown": {
                    "education": 0.0,
                    "trajectory": 0.0,
                    "company": 0.0,
                    "skills": 0.0,
                    "location": 0.0,
                    "tenure": 0.0
                }
            })
    return results 

def get_profile_name(profile):
    # Try common name fields
    for key in ['name', 'full_name', 'first_name', 'last_name']:
        if key in profile and profile[key]:
            return profile[key]
    # Fallback: use headline or 'N/A'
    return profile.get('headline', 'N/A') 