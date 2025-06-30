
# LinkedIn AI Sourcing Agent ��

An intelligent AI-powered tool that automates the entire candidate sourcing pipeline from job description to personalized LinkedIn outreach messages.

## �� Features

### Core Pipeline
- **Job Description Processing**: Upload and analyze job descriptions with intelligent text chunking and embedding
- **Structured Information Extraction**: Extract job titles, locations, and required skills using KOR (Knowledge-Oriented Retrieval)
- **Alternate Title Generation**: Generate multiple job title variations for broader candidate search
- **LinkedIn Profile Discovery**: Search for relevant candidates using Tavily search API
- **Profile Enrichment**: Enhance candidate profiles with detailed information via RapidAPI
- **AI-Powered Scoring**: Score candidates using custom rubrics and OpenAI GPT-4
- **Personalized Messaging**: Generate tailored LinkedIn outreach messages for each candidate

### User Interface
- **Streamlit Web App**: Interactive web interface for easy pipeline execution
- **Step-by-Step Process**: Visual progress through each stage of the sourcing pipeline
- **Real-time Results**: View extracted information, found profiles, scores, and messages
- **File Upload Support**: Upload custom job descriptions in TXT format

## 🛠️ Technology Stack

- **AI/ML**: OpenAI GPT-4, LangChain, KOR
- **Search**: Tavily Search API
- **Data Enrichment**: RapidAPI LinkedIn Profile Data
- **Vector Database**: ChromaDB for embeddings
- **Web Framework**: Streamlit
- **Language**: Python 3.x

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key
- RapidAPI key (for LinkedIn profile enrichment)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkinden_AI_Agnet
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   RAPIDAPI_KEY=your_rapidapi_key
   RAPIDAPI_HOST=fresh-linkedin-profile-data.p.rapidapi.com
   ```

## 🎯 Usage

### Web Interface (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

### Command Line
```bash
python src/main.py
```

## 📊 Pipeline Overview

1. **Job Description Upload**: Upload a TXT file containing the job description
2. **Information Extraction**: Extract structured job information (title, location, skills)
3. **Title Generation**: Generate alternate job titles for broader search
4. **Profile Discovery**: Search LinkedIn for relevant candidates
5. **Profile Enrichment**: Enhance candidate profiles with detailed information
6. **Candidate Scoring**: Score candidates using AI-powered rubric evaluation
7. **Message Generation**: Create personalized LinkedIn outreach messages

## 🎯 Scoring System

The AI scoring system evaluates candidates across multiple dimensions:

- **Education (20%)**: University prestige and academic progression
- **Career Trajectory (20%)**: Professional growth and advancement
- **Company Relevance (15%)**: Experience at relevant companies
- **Experience Match (25%)**: Skills alignment with job requirements
- **Location Match (10%)**: Geographic proximity to job location
- **Tenure (10%)**: Job stability and career progression patterns







