from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
from langchain_openai import ChatOpenAI
from typing import Dict
import os

def get_kor_schema() -> Object:
    """
    Returns the KOR schema for extracting job title, location, and skills from a job description.
    """
    schema = Object(
        id="job_info",
        description="Extract job title, location, and skills from a job description.",
        attributes=[
            Text(
                id="title",
                description="The job title",
                examples=[
                    ("We are looking for an AI Engineer to join our team.", "AI Engineer"),
                    ("As a Machine Learning Engineer, you will work on cutting-edge models.", "Machine Learning Engineer"),
                ],
            ),
            Text(
                id="location",
                description="Job location",
                examples=[
                    ("This is a remote role based in the US.", "Remote - US"),
                    ("The position is in San Francisco, CA.", "San Francisco, CA"),
                ],
            ),
            Text(
                id="keywords",
                description="Comma-separated list of required skills or tools",
                examples=[
                    ("Required skills: Python, LangChain, OpenAI", "Python, LangChain, OpenAI"),
                    ("Must know NLP, embeddings, and ChromaDB", "NLP, embeddings, ChromaDB"),
                ],
            ),
        ],
        many=False,
    )
    return schema


def extract_structured_info(jd_text: str, config: dict) -> Dict:
    """
    Extracts structured job info from the job description text using KOR and an LLM.
    """
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    schema = get_kor_schema()
    chain = create_extraction_chain(llm, schema)
    result = chain.invoke(jd_text)
    return result["data"] 