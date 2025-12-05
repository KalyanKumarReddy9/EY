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
- **Data Sources**: PatentsView API with mock data fallback
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
cd backend
npm install
npm run dev
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
Create a `.env` file in the backend directory with the following variables:

```
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
SUDO_DEV_API_KEY=your_sudo_dev_api_key
PUBMED_API_KEY=your_pubmed_api_key
OPENFDA_API_KEY=your_openfda_api_key
MONGO_URI=your_mongodb_connection_string
```

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