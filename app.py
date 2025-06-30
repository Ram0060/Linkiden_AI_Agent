import streamlit as st
import os
import json
from src.config import load_config
from src.jd_processing import load_jd, split_jd, embed_and_save_chunks
from src.kor_extraction import extract_structured_info
from src.title_generation import generate_alternate_titles
from src.tavily_search import search_linkedin_profiles
from src.rapidapi_enrich import enrich_profiles_with_rapidapi
from src.scoring import score_candidates
from src.messaging import craft_linkedin_messages

def get_profile_name(profile):
    # Try common name fields
    for key in ['name', 'full_name']:
        if key in profile and profile[key]:
            return profile[key]
    # Try first_name + last_name
    if profile.get('first_name') or profile.get('last_name'):
        return f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
    # Fallback: use headline or 'N/A'
    return profile.get('headline', 'N/A')

st.title("LinkedIn AI Sourcing Agent (Text Output)")
st.write("""
Upload a job description and run the sourcing pipeline. Results will be shown in a readable text format at each step.
""")

config = load_config()

# Step 1: Upload JD file
jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])
jd_text = None
if jd_file:
    jd_text = jd_file.read().decode("utf-8")
    st.markdown("**Job Description Preview:**")
    st.write(jd_text[:1000] + ("..." if len(jd_text) > 1000 else ""))

# Step 2: Extract structured info
if st.button("Extract Structured Info") and jd_text:
    structured_info = extract_structured_info(jd_text, config)
    st.markdown("**Extracted Info:**")
    for job in structured_info.get("job_info", []):
        st.write(f"Title: {job.get('title', '')}")
        st.write(f"Location: {job.get('location', '')}")
        st.write(f"Keywords: {job.get('keywords', '')}")

# Step 3: Generate alternate titles
    suggested_titles = generate_alternate_titles(structured_info, config)
    st.markdown("**Suggested Titles:**")
    for t in suggested_titles:
        st.write(f"- {t}")

# Step 4: Tavily search
    linkedin_urls = search_linkedin_profiles(suggested_titles, config)
    st.markdown("**LinkedIn URLs Found:**")
    for url in linkedin_urls:
        st.write(url)

# Step 5: RapidAPI enrich (first 10 links)
    enriched_profiles = enrich_profiles_with_rapidapi(linkedin_urls[:10], config)
    # Flatten the structure to handle double 'data' nesting
    flattened_profiles = []
    for p in enriched_profiles:
        if isinstance(p, dict) and 'data' in p:
            if isinstance(p['data'], dict) and 'data' in p['data']:
                flattened_profiles.append(p['data']['data'])
            else:
                flattened_profiles.append(p['data'])
        else:
            flattened_profiles.append(p)
    # Filter for valid profiles with a linkedin_url
    valid_profiles = [p for p in flattened_profiles if p.get('linkedin_url')]
    if not valid_profiles:
        st.warning("No valid enriched profiles were returned from RapidAPI. Scoring and messaging steps will be skipped.")
    else:
        st.markdown("**Enriched Profiles (first 10):**")
        for idx, profile in enumerate(valid_profiles, 1):
            name = get_profile_name(profile)
            url = profile.get('linkedin_url', 'N/A')
            headline = profile.get('headline', 'N/A')
            st.write(f"{idx}. {name} | {headline}")
            st.write(f"   {url}")

        # Step 6: Score candidates
        rubric_path = os.path.join("src", "score_fit_rubics", "SWE_ML.txt")
        with open(rubric_path, "r") as f:
            rubric = f.read()
        scored_candidates = score_candidates(valid_profiles, rubric, config)
        st.markdown("**Scored Candidates:**")
        for cand in scored_candidates:
            name = get_profile_name(cand)
            score = cand.get('fit_score', 'N/A')
            url = cand.get('linkedin_url', 'N/A')
            breakdown = cand.get('score_breakdown', {})
            explanation = cand.get('explanation', None)
            st.write(f"{name} | Score: {score}")
            st.write(f"   {url}")
            if breakdown:
                st.markdown("**Score Breakdown:**")
                for k, v in breakdown.items():
                    st.write(f"- {k.capitalize()}: {v}")
            if explanation:
                st.markdown("**Explanation:**")
                st.write(explanation)

        # Step 7: Craft messages
        messages = craft_linkedin_messages(scored_candidates, config)
        st.markdown("**Outreach Messages:**")
        for msg in messages:
            name = msg.get('name', 'N/A')
            url = msg.get('linkedin_url', 'N/A')
            message = msg.get('message', '')
            st.write(f"To: {name} ({url})")
            st.write(message)
            st.markdown("---")

    if valid_profiles:
        st.write("DEBUG: First enriched profile:", valid_profiles[0])
    else:
        st.write("DEBUG: No profiles returned at all.")

    st.write("DEBUG: Raw enriched_profiles:", enriched_profiles) 