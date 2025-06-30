from config import load_config
from jd_processing import load_jd, split_jd, embed_and_save_chunks
from kor_extraction import extract_structured_info
from title_generation import generate_alternate_titles
from tavily_search import search_linkedin_profiles
from rapidapi_enrich import enrich_profiles_with_rapidapi
from scoring import score_candidates
from messaging import craft_linkedin_messages
import json
import os


def main():
    # 1. Load config
    config = load_config()
    print("Loaded config.")

    # 2. Load and process job description
    jd_text = load_jd(config['JD_PATH'])
    print("Loaded job description.")
    split_docs = split_jd(jd_text)
    print(f"Split JD into {len(split_docs)} chunks.")
    embed_and_save_chunks(split_docs, config)
    print("Embedded and saved JD chunks to ChromaDB.")

    # 3. Extract structured info
    structured_info = extract_structured_info(jd_text, config)
    print("Extracted structured job info:")
    print(json.dumps(structured_info, indent=2))
    with open(os.path.join(config['OUTPUT_DIR'], 'extracted_job_info.json'), 'w') as f:
        json.dump(structured_info, f, indent=2)

    # 4. Generate alternate job titles
    titles = generate_alternate_titles(structured_info, config)
    print("Generated alternate job titles:")
    print(titles)
    with open(os.path.join(config['OUTPUT_DIR'], 'combined_titles.json'), 'w') as f:
        json.dump(titles, f, indent=2)

    # 5. Search LinkedIn profiles with Tavily
    linkedin_urls = search_linkedin_profiles(titles, config)
    print(f"Found {len(linkedin_urls)} unique LinkedIn profiles.")
    with open(os.path.join(config['OUTPUT_DIR'], 'final_linkedin_profiles.json'), 'w') as f:
        json.dump(linkedin_urls, f, indent=2)

    # 6. Enrich profiles with RapidAPI
    enriched_profiles = enrich_profiles_with_rapidapi(linkedin_urls, config, limit=10)
    print(f"Enriched {len(enriched_profiles)} profiles with RapidAPI.")
    with open(os.path.join(config['OUTPUT_DIR'], 'enriched_profiles_rapidapi.json'), 'w') as f:
        json.dump(enriched_profiles, f, indent=2)

    # 7. Load scoring rubric
    with open(config['SCORE_RUBRIC_PATH'], 'r') as f:
        rubric = f.read()

    # 8. Score candidates
    scored_candidates = score_candidates(enriched_profiles, rubric, config)
    print(f"Scored {len(scored_candidates)} candidates.")
    with open(os.path.join(config['OUTPUT_DIR'], 'scored_candidates.json'), 'w') as f:
        json.dump(scored_candidates, f, indent=2)

    # 9. Craft LinkedIn messages
    messages = craft_linkedin_messages(scored_candidates, config)
    print(f"Generated {len(messages)} LinkedIn outreach messages.")
    with open(os.path.join(config['OUTPUT_DIR'], 'linkedin_outreach_messages.json'), 'w') as f:
        json.dump(messages, f, indent=2)

    print("Pipeline complete!")

if __name__ == "__main__":
    main() 