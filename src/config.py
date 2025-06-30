import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    """
    Loads environment variables and important file paths for the project.
    Returns a dictionary with config values.
    """
    config = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'TAVILY_API_KEY': os.getenv('TAVILY_API_KEY'),
        'RAPIDAPI_KEY': os.getenv('RAPIDAPI_KEY'),
        'RAPIDAPI_HOST': os.getenv('RAPIDAPI_HOST', 'fresh-linkedin-profile-data.p.rapidapi.com'),
        'JD_PATH': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'job_description', 'jd1.txt'),
        'CHROMA_DB_PATH': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'chroma_db'),
        'SCORE_RUBRIC_PATH': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'score_fit_rubics', 'SWE_ML.txt'),
        'OUTPUT_DIR': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'experiments.py'),
    }
    return config 