# Pharma Mind Nexus - Python Implementation

This is a Python-based implementation of the Pharma Mind Nexus system using Flask, MongoDB, Pinecone, and LangChain.

## System Architecture

The system follows a hybrid architecture:
1. **ETL/Scrapers** - Batch-run processes to store CSV/structured data in MongoDB
2. **Vector Embeddings** - Precompute embeddings for documents/rows and upsert into Pinecone
3. **Worker Agents** - Specialized agents for different data sources
4. **LangChain Master Agent** - Orchestrates worker functions/tools
5. **Report Generator** - Composes PDF/Excel from returned data
6. **Flask API** - Exposes endpoints to query agents, upload CSVs, and kick off scrapes

## Folder Structure

```
/crewai-system/
├─ /scrapers/                # scraping + CSV download + ETL to Mongo
│   ├─ csv_to_mongo.py
│   ├─ comtrade_loader.py
│   └─ clinicaltrials_loader.py
├─ /agents/                  # Worker agents
│   ├─ exim_agent.py
│   ├─ trials_agent.py
│   ├─ iqvia_agent.py
│   ├─ patent_agent.py
│   ├─ webintel_agent.py
│   └─ internal_agent.py
├─ /vector/                  # Vector embeddings and Pinecone integration
│   ├─ embeddings.py
│   └─ pinecone_client.py
├─ /api/                     # Flask API server
│   └─ server.py
├─ /reports/                 # Report generation
│   └─ report_generator.py
├─ /langchain/               # LangChain master agent
│   └─ master_agent.py
├─ main.py                   # Main application entry point
├─ init_db.py                # Database initialization
├─ example_usage.py          # Example usage demonstrations
├─ requirements.txt          # Python dependencies
├─ .env                      # Environment variables (not committed to git)
└─ database_schema.py        # MongoDB schema definitions
```

## Prerequisites

1. Python 3.7+
2. MongoDB Atlas account
3. Pinecone account
4. Hugging Face account
5. (Optional) Google Custom Search API credentials

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd crewai-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   # Required DB + server
   MONGO_URI=mongodb+srv://username:password@cluster.example.mongodb.net/
   PORT=4000
   JWT_SECRET=change_this_secret

   # Embeddings / Vector DB
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENV=us-west1-gcp

   # Hugging Face Token
   HF_TOKEN=your_hugging_face_token

   # Optional API keys
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_CSE_ID=your_google_custom_search_id
   ```

## Running the System

1. Initialize the database:
   ```bash
   python init_db.py
   ```

2. Start the Flask server:
   ```bash
   python main.py
   ```

3. The API will be available at `http://localhost:4000`

## API Endpoints

- `GET /api/exim` - Get EXIM trade data
- `GET /api/trials` - Get clinical trials data
- `GET /api/iqvia` - Get IQVIA market data
- `GET /api/patents` - Get patent data
- `GET /api/web-intel` - Get web intelligence data
- `GET /api/internal-docs` - Search internal documents
- `POST /api/master-agent` - Run the master agent
- `POST /api/generate-report` - Generate reports

## Worker Agents

1. **EXIM Agent** - Trade data analysis
2. **Clinical Trials Agent** - Clinical trial data
3. **IQVIA Agent** - Market intelligence (using mock data)
4. **Patent Agent** - Intellectual property analysis
5. **Web Intelligence Agent** - Online research
6. **Internal Documents Agent** - Internal knowledge processing

## Running Examples

To see the system in action, run:
```bash
python example_usage.py
```

This will demonstrate all the agents and functionality.

## Data Sources

- **MongoDB** - Structured data storage
- **Pinecone** - Vector database for semantic search
- **Hugging Face** - Language models via LangChain
- **ClinicalTrials.gov** - Clinical trial data
- **Comtrade API** - International trade data
- **Google Custom Search** - Web intelligence (optional)

## Features

- Modular agent architecture
- Database indexing for performance
- Vector embeddings for semantic search
- PDF and Excel report generation
- Text summarization
- Error handling and fallbacks
- RESTful API endpoints
- CORS support

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.