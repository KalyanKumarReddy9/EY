const express = require('express');
const router = express.Router();
const axios = require('axios');
const { PDFDocument, rgb, StandardFonts } = require('pdf-lib');

// ClinicalTrials.gov API
const CLINICAL_TRIALS_API = 'https://clinicaltrials.gov/api/v2/studies';
router.get('/clinical-trials', async (req, res) => {
    try {
        const { query } = req.query;
        if (!query) {
            return res.status(400).json({ msg: 'Query parameter is required' });
        }
        const response = await axios.get(`${CLINICAL_TRIALS_API}?query.term=${query}`);
        res.json(response.data);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// PatentsView API (USPTO)
const PATENTSVIEW_API = 'https://search.patentsview.org/api/v1/patent/';
router.get('/patents', async (req, res) => {
    try {
        const { query } = req.query;
        if (!query) {
            return res.status(400).json({ msg: 'Query parameter is required' });
        }
        // Correctly format the query for PatentsView API
        const q = JSON.stringify({ "_text_any": { "patent_title": query, "patent_abstract": query } });
        const response = await axios.get(PATENTSVIEW_API, { 
            params: { q },
            // Adding a timeout
            timeout: 10000 
        });
        res.json(response.data);
    } catch (err) {
        // Improved error logging
        if (err.response) {
            console.error('Patents API Error:', err.response.status, err.response.data);
            res.status(err.response.status).json(err.response.data);
        } else if (err.request) {
            console.error('Patents API No Response:', err.request);
            res.status(504).send('Server Error: No response from Patents API');
        } else {
            console.error('Patents API Setup Error:', err.message);
            res.status(500).send('Server Error');
        }
    }
});

// PubMed API
const PUBMED_SEARCH_API = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi';
const PUBMED_SUMMARY_API = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi';
const PUBMED_API_KEY = process.env.PUBMED_API_KEY;
router.get('/pubmed', async (req, res) => {
    try {
        const { query } = req.query;
        if (!query) {
            return res.status(400).json({ msg: 'Query parameter is required' });
        }
        
        // Step 1: Search for article IDs
        const searchResponse = await axios.get(PUBMED_SEARCH_API, {
            params: { db: 'pubmed', term: query, retmode: 'json', api_key: PUBMED_API_KEY }
        });

        const idList = searchResponse.data.esearchresult.idlist;
        if (!idList || idList.length === 0) {
            return res.json({ esearchresult: { count: "0", idlist: [] }, result: {} });
        }

        // Step 2: Fetch summaries for the found IDs
        const ids = idList.join(',');
        const summaryResponse = await axios.get(PUBMED_SUMMARY_API, {
            params: { db: 'pubmed', id: ids, retmode: 'json', api_key: PUBMED_API_KEY }
        });

        res.json(summaryResponse.data);
    } catch (err) {
        if (err.response) {
            console.error('PubMed API Error:', err.response.status, err.response.data);
            res.status(err.response.status).json(err.response.data);
        } else if (err.request) {
            console.error('PubMed API No Response:', err.request);
            res.status(504).send('Server Error: No response from PubMed API');
        } else {
            console.error('PubMed API Setup Error:', err.message);
            res.status(500).send('Server Error');
        }
    }
});

// Google Custom Search API (Web Intelligence)
const GOOGLE_SEARCH_API = 'https://www.googleapis.com/customsearch/v1';
const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY;
const GOOGLE_CSE_ID = process.env.GOOGLE_CSE_ID;
router.get('/web-search', async (req, res) => {
    try {
        const { query } = req.query;
        if (!query) {
            return res.status(400).json({ msg: 'Query parameter is required' });
        }
        const response = await axios.get(GOOGLE_SEARCH_API, {
            params: {
                key: GOOGLE_API_KEY,
                cx: GOOGLE_CSE_ID,
                q: query
            }
        });
        res.json(response.data);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// OpenFDA API
const OPENFDA_API = 'https://api.fda.gov/drug/label.json';
const OPENFDA_API_KEY = process.env.OPENFDA_API_KEY;
router.get('/openfda', async (req, res) => {
    try {
        const { query } = req.query;
        if (!query) {
            return res.status(400).json({ msg: 'Query parameter is required' });
        }
        const response = await axios.get(OPENFDA_API, {
            params: {
                search: query,
                api_key: OPENFDA_API_KEY
            }
        });
        res.json(response.data);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// UN Comtrade API for EXIM Trends
const UN_COMTRADE_API_GET = 'https://comtradeapi.un.org/data/v1/get/C/A/HS';
const UN_COMTRADE_API_LOOKUP = 'https://comtradeapi.un.org/files/v1/app/reference/HS.json';

router.get('/exim', async (req, res) => {
    try {
        const { query } = req.query;
        if (!query) {
            return res.status(400).json({ msg: 'Query parameter is required' });
        }

        // Step 1: Look up the commodity code from the text query
        const lookupResponse = await axios.get(UN_COMTRADE_API_LOOKUP);
        const commodities = lookupResponse.data.results;
        const foundCommodity = commodities.find(c => c.text.toLowerCase().includes(query.toLowerCase()));

        if (!foundCommodity) {
            return res.json({ validation: { status: 'warning', message: `Could not find a specific commodity code for "${query}". Results may be broad.` }, data: [] });
        }

        // Step 2: Fetch trade data using the found commodity code
        const response = await axios.get(UN_COMTRADE_API_GET, {
            params: {
                reporterCode: 'all',
                partnerCode: '0', // World
                period: '2022',
                cmdCode: foundCommodity.id,
                flowCode: 'M,X' // Imports and Exports
            }
        });
        res.json(response.data);
    } catch (err) {
        if (err.response) {
            console.error('UN Comtrade API Error:', err.response.status, err.response.data);
            res.status(err.response.status).json(err.response.data);
        } else {
            console.error('UN Comtrade API Error:', err.message);
            res.status(500).send('Server Error');
        }
    }
});


// Report Generator Agent
const SUDO_DEV_API_URL = 'https://api.sudo.dev/v1/chat/completions';
const SUDO_DEV_API_KEY = process.env.SUDO_DEV_API_KEY;

router.post('/generate-report', async (req, res) => {
    try {
        const { query, results } = req.body;

        if (!query || !results) {
            return res.status(400).json({ msg: 'Query and results are required' });
        }

        const prompt = `
            As a pharmaceutical research analyst, synthesize the following data into a coherent summary report.
            The initial query was: "${query}".

            Here is the data collected from various sources:
            - Clinical Trials: ${JSON.stringify(results['Clinical Trials'], null, 2)}
            - Patents: ${JSON.stringify(results['Patents'], null, 2)}
            - PubMed: ${JSON.stringify(results['Pubmed'], null, 2)}
            - Web Search: ${JSON.stringify(results['Web Search'], null, 2)}
            - OpenFDA: ${JSON.stringify(results['Openfda'], null, 2)}
            - EXIM: ${JSON.stringify(results['Exim'], null, 2)}

            Please provide a summary that addresses the following:
            1.  **Unmet Medical Needs:** Based on the literature and clinical trials, what are the current unmet needs related to the query?
            2.  **Innovation Opportunities:** Are there any opportunities for new drug formulations, repurposing, or new indications?
            3.  **Patent Landscape:** What is the current patent situation? Are there any key patents expiring soon?
            4.  **Clinical Trial Activity:** What is the current state of clinical trials? Are there many active trials? Who are the key sponsors?

            Generate a concise, well-structured report based on this data.
        `;

        const response = await axios.post(SUDO_DEV_API_URL, {
            model: 'mistral-7b-instruct',
            messages: [{ role: 'user', content: prompt }],
        }, {
            headers: {
                'Authorization': `Bearer ${SUDO_DEV_API_KEY}`
            }
        });

        const reportText = response.data.choices[0]?.message?.content || "Could not generate report.";

        // Create a new PDF document
        const pdfDoc = await PDFDocument.create();
        const page = pdfDoc.addPage();
        const { width, height } = page.getSize();
        const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
        const fontSize = 12;

        page.drawText(reportText, {
            x: 50,
            y: height - 4 * fontSize,
            font,
            size: fontSize,
            maxWidth: width - 100,
            lineHeight: 15,
            color: rgb(0, 0, 0),
        });

        // Serialize the PDF to bytes
        const pdfBytes = await pdfDoc.save();

        // Send the PDF as a response
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', 'attachment; filename=report.pdf');
        res.send(Buffer.from(pdfBytes));

    } catch (err) {
        if (err.response) {
            console.error('Report Generation Error:', err.response.status, err.response.data);
            res.status(err.response.status).json(err.response.data);
        } else {
            console.error('Report Generation Error:', err.message);
            res.status(500).send('Server Error');
        }
    }
});


module.exports = router;
