# LinkedIn Profile Finder

An AI-powered tool to find suitable LinkedIn profiles that match job requirements. This project uses LangChain and OpenAI to extract job requirements from job descriptions and find matching LinkedIn profiles.

## Features

- 🔍 **Job Requirement Extraction**: Automatically extracts job title, location, required skills, experience, and education requirements from job descriptions
- 🎯 **Profile Matching**: Finds LinkedIn profiles that match job requirements using multiple search strategies
- 📊 **Scoring System**: Scores profiles based on title match, location match, skills match, experience, and education
- 📈 **Detailed Analysis**: Provides strengths, weaknesses, and recommendations for each candidate
- 💾 **Export Results**: Save results in JSON format or export as CSV
- 🌐 **Web Interface**: Streamlit-based web application for easy interaction

## Project Structure

```
linkinden_AI_Agnet/
├── src/
│   ├── enhanced_linkedin_finder.py    # Main LinkedIn profile finder
│   ├── linkedin_scraper.py            # LinkedIn web scraping utilities
│   ├── linkedin_profile_finder.py     # Original profile finder
│   ├── job_description/
│   │   └── jd1.txt                    # Sample job description
│   └── experiments.py/
│       ├── exp1.ipynb                 # Jupyter notebook experiments
│       └── extracted_job_info*.json   # Extracted job information
├── demo_linkedin_finder.py            # Demo script
├── app.py                             # Streamlit web application
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd linkinden_AI_Agnet
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Method 1: Command Line Demo

Run the demo script to see the LinkedIn profile finder in action:

```bash
python demo_linkedin_finder.py
```

This will:
- Load the sample job description
- Extract job requirements using OpenAI
- Search for matching LinkedIn profiles
- Display results with scoring and analysis
- Save results to `linkedin_search_results.json`

### Method 2: Streamlit Web Application

Launch the web interface:

```bash
streamlit run app.py
```

The web app provides:
- Job description input (upload file, manual entry, or use sample)
- Interactive profile search with configurable parameters
- Detailed results with expandable profile information
- Export functionality (JSON and CSV)

### Method 3: Programmatic Usage

```python
from src.enhanced_linkedin_finder import EnhancedLinkedInFinder

# Initialize finder
finder = EnhancedLinkedInFinder(api_key="your_openai_api_key")

# Load job description
with open("job_description.txt", "r") as f:
    job_description = f.read()

# Extract job requirements
job_req = finder.extract_job_requirements(job_description)

# Search for profiles
profiles = finder.search_profiles(job_req, max_results=10)

# Analyze and save results
for profile in profiles:
    analysis = finder.analyze_profile_fit(profile, job_req)
    print(f"{profile.name}: {profile.match_score}/100")

finder.save_results(profiles, "results.json")
```

## How It Works

### 1. Job Requirement Extraction

The system uses OpenAI's GPT-4 to extract structured job requirements from natural language job descriptions:

- **Job Title**: The specific role being offered
- **Location**: Where the job is located
- **Required Skills**: Technical and soft skills needed
- **Experience Years**: Minimum years of experience required
- **Education Requirements**: Required educational background
- **Keywords**: Important terms and technologies mentioned

### 2. Profile Search Strategies

The finder uses multiple search strategies to find relevant profiles:

- **Keyword Search**: Search by job title and location
- **Skills Search**: Search by required skills
- **Location Search**: Focus on specific geographic areas
- **Company Search**: Search within specific companies
- **Mock Search**: For testing and demonstration purposes

### 3. Profile Scoring

Each profile is scored on a 100-point scale based on:

- **Title Match (30 points)**: How well the profile title matches the job title
- **Location Match (20 points)**: Geographic proximity to the job location
- **Skills Match (25 points)**: Overlap between required and profile skills
- **Experience Match (15 points)**: Whether experience meets requirements
- **Education Match (10 points)**: Educational background alignment

### 4. Analysis and Recommendations

For each profile, the system provides:

- **Strengths**: What makes the candidate a good fit
- **Weaknesses**: Areas where the candidate may fall short
- **Recommendations**: Whether to consider for interview

## Sample Job Description

The project includes a sample job description for a "Software Engineer, ML Research" position at Windsurf in Mountain View, CA. This demonstrates how the system extracts requirements from real job postings.

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Search Parameters

- `max_results`: Maximum number of profiles to return (default: 10)
- `min_match_score`: Minimum match score to include (default: 50)
- `search_strategies`: Which search strategies to use

## Output Format

Results are saved in JSON format with the following structure:

```json
{
  "profiles": [
    {
      "name": "John Doe",
      "title": "Senior Software Engineer",
      "location": "Mountain View, CA",
      "company": "Tech Corp",
      "profile_url": "https://linkedin.com/in/johndoe",
      "summary": "Experienced software engineer...",
      "experience": [
        {
          "title": "Software Engineer",
          "company": "Tech Corp",
          "duration": "3 years"
        }
      ],
      "education": [
        {
          "degree": "BS Computer Science",
          "school": "Stanford University"
        }
      ],
      "skills": ["Python", "Machine Learning", "AI"],
      "match_score": 85.5,
      "match_reasons": ["Title match", "Location match", "3 skills match"]
    }
  ]
}
```

## Limitations and Considerations

1. **LinkedIn Scraping**: The current implementation uses mock data for demonstration. Real LinkedIn scraping requires:
   - Proper authentication
   - Compliance with LinkedIn's terms of service
   - Rate limiting to avoid being blocked

2. **API Costs**: Using OpenAI's API incurs costs based on usage. Monitor your API usage to control expenses.

3. **Data Privacy**: Ensure compliance with data protection regulations when processing personal information.

4. **Accuracy**: The matching algorithm is based on text similarity and may not capture all nuances of job requirements.

## Future Enhancements

- [ ] Integration with real LinkedIn API
- [ ] Advanced filtering options
- [ ] Email outreach automation
- [ ] Candidate tracking system
- [ ] Integration with ATS systems
- [ ] Multi-language support
- [ ] Advanced analytics and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and demonstration purposes. Please ensure compliance with LinkedIn's terms of service and applicable data protection laws when using this tool.

## Support

For questions or issues, please open an issue in the repository or contact the development team. 