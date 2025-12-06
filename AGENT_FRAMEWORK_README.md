# Pharma Mind Nexus Agent AI Framework

## Overview
This document describes the implemented Agent AI Framework for the Pharma Mind Nexus platform. The framework consists of a Master Agent that orchestrates specialized Worker Agents to provide comprehensive pharmaceutical research capabilities.

## Implemented Worker Agents

### 1. IQVIA Insights Agent
- **Endpoint**: `/api/iqvia`
- **Functionality**: Provides market size data, growth trends, and competitive intelligence
- **Data Sources**: Mock data (IQVIA dataset not publicly available)
- **Output**: Market size tables, CAGR trends, therapy-level competitor summaries

### 2. EXIM Trade Data Agent
- **Endpoint**: `/api/exim`
- **Functionality**: Analyzes international pharmaceutical trade flows and supply chain dynamics
- **Data Sources**: UN Comtrade API with mock data fallback
- **Output**: Trade volume charts, sourcing insights, import dependency tables

### 3. Patent Landscape Agent
- **Endpoint**: `/api/patents`
- **Functionality**: Searches patent databases for intellectual property insights
- **Data Sources**: PubMed API with mock data fallback
- **Output**: Patent status tables, competitive filing heatmaps

### 4. Clinical Trials Agent
- **Endpoint**: `/api/clinical-trials`
- **Functionality**: Tracks ongoing clinical trials and drug development pipelines
- **Data Sources**: ClinicalTrials.gov API with rate limiting handling
- **Output**: Tables of active trials, sponsor profiles, trial phase distributions

### 5. Web Intelligence Agent
- **Endpoint**: `/api/web-search`
- **Functionality**: Performs real-time web search for guidelines and scientific publications
- **Data Sources**: Google Custom Search API with mock data fallback
- **Output**: Hyperlinked summaries, quotations from credible sources

### 6. Report Generator Agent
- **Endpoint**: `/api/generate-report`
- **Functionality**: Formats synthesized responses into polished PDF reports
- **Data Sources**: Sudo.Dev LLM API with mock processing fallback
- **Output**: PDF summaries with charts/tables

## API Improvements

### Rate Limiting Handling
- Implemented exponential backoff for ClinicalTrials.gov API
- Added retry mechanisms for transient failures
- Increased timeouts for better reliability

### Mock Data System
- Comprehensive mock data implementations for all agents
- Automatic fallback when real APIs are unavailable
- Realistic data structures matching expected output formats

### Error Handling
- Enhanced error handling with detailed logging
- Graceful degradation to mock data when APIs fail
- Clear error messages for debugging

## Frontend Enhancements

### Improved Data Presentation
- Structured display of agent responses
- Collapsible sections for better organization
- Formatted data views for different agent types

### Report Generation
- PDF report download functionality
- Visual feedback during report generation
- Proper file naming with timestamps

## How to Use

### Starting the Backend
```bash
cd crewai-system
pip install -r requirements.txt
python -m api.server
```

### Starting the Frontend
```bash
npm install
npm run dev
```

### Querying Agents
The system automatically queries all available agents when you submit a question through the chat interface. You can ask about:
- Market insights for specific molecules or therapeutic areas
- Clinical trial activity and sponsors
- Patent landscapes and intellectual property
- Trade flows and supply chain dynamics
- Regulatory updates and safety signals

### Generating Reports
After receiving agent responses, you can click "Generate Report" to create a PDF summary of all findings.

## Configuration

### Environment Variables
Create a `.env` file in the `crewai-system` directory with the following variables:

```
# Required DB + server
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
PORT=4000
JWT_SECRET=your_jwt_secret_here

# Embeddings / Vector DB
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=us-west1-gcp

# Hugging Face Token
HF_TOKEN=your_hugging_face_token_here

# PubMed API Key
PUBMED_API_KEY=your_pubmed_api_key_here

# Google API keys
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_custom_search_engine_id_here

# Alternative APIs (optional)
GEMINI_API_KEY=your_gemini_api_key_here
SUDO_DEV_API_KEY=your_sudo_dev_api_key_here
OPENFDA_API_KEY=your_openfda_api_key_here
```

### Obtaining API Keys

#### 1. MongoDB
- Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a cluster and database user
- Obtain your connection string from the Atlas dashboard

#### 2. Pinecone
- Sign up at [Pinecone](https://www.pinecone.io/)
- Create an API key in your dashboard
- Note the environment region for the PINECONE_ENV variable

#### 3. Hugging Face
- Sign up at [Hugging Face](https://huggingface.co/)
- Create an access token in your account settings
- Use the token as your HF_TOKEN

#### 4. PubMed (NCBI)
- Visit [NCBI API Keys](https://www.ncbi.nlm.nih.gov/account/settings/)
- Sign in or create an account
- Generate an API key in your account settings

#### 5. Google APIs
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select an existing one
- Enable the Custom Search API
- Create credentials (API key)
- For Google Custom Search Engine (CSE):
  - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
  - Create a new search engine
  - Configure it to search the entire web
  - Obtain the Search Engine ID

#### 6. Sudo.Dev (Optional)
- Sign up at [Sudo.Dev](https://sudo.dev/)
- Obtain an API key for enhanced LLM processing

If these are not provided, the system will automatically fall back to mock data.

## Future Enhancements

1. **Internal Knowledge Agent**: Implementation for processing internal documents
2. **Safety Signal Agent**: Integration with FAERS/EudraVigilance databases
3. **Regulatory Monitor Agent**: Automated tracking of regulatory guidance
4. **Supply Chain Risk Agent**: Advanced supply chain analytics
5. **Clinical Evidence Summarizer**: Document ingestion and summarization

## Troubleshooting

### API Connection Issues
- Check environment variables are properly configured
- Verify API keys are valid and have sufficient quotas
- Review console logs for detailed error messages

### Mock Data Usage
- The system automatically falls back to mock data when real APIs are unavailable
- Mock data provides realistic examples matching expected output formats
- All agent functionalities can be tested with mock data

### Report Generation Problems
- Ensure Sudo.Dev API key is configured for enhanced reports
- Check network connectivity for external API calls
- Review backend logs for processing errors