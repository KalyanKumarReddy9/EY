import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import json
from datetime import datetime
from functools import wraps
import jwt
import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.binary import Binary
import uuid

# Import agents
from agents import exim_agent, trials_agent, iqvia_agent, patent_agent, webintel_agent, internal_agent
from reports import report_generator
# Import the master agent from local_langchain instead of langchain
from local_langchain.master_agent import run_master_agent

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get port from environment or default to 4000
PORT = int(os.environ.get("PORT", 4000))

# JWT Secret
JWT_SECRET = os.environ.get("JWT_SECRET", "change_this_secret")

def get_mongo_client():
    """Create and return a MongoDB client"""
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    return MongoClient(MONGO_URI)

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                parts = auth_header.split(' ')
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]
            except:
                pass
        
        if not token:
            return jsonify({'msg': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            current_user_id = data['id']
        except:
            return jsonify({'msg': 'Token is invalid!'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "Pharma Mind Nexus API is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', '')
        
        if not name or not email or not password:
            return jsonify({"msg": "Missing fields"}), 400
        
        client = get_mongo_client()
        db = client["pharma_hub"]
        users_collection = db["users"]
        
        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return jsonify({"msg": "Email already in use"}), 400
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = users_collection.insert_one(user)
        user_id = str(result.inserted_id)
        
        # Create JWT token
        token = jwt.encode({'id': user_id}, JWT_SECRET, algorithm="HS256")
        
        # Return user data without password
        user_response = {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role
        }
        
        return jsonify({
            "user": user_response,
            "token": token
        }), 200
        
    except Exception as e:
        return jsonify({"msg": "Server error"}), 500
    finally:
        if 'client' in locals():
            client.close()

@app.route('/api/auth/signin', methods=['POST'])
def signin():
    """User signin endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"msg": "Missing fields"}), 400
        
        client = get_mongo_client()
        db = client["pharma_hub"]
        users_collection = db["users"]
        
        # Find user
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"msg": "Invalid credentials"}), 400
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({"msg": "Invalid credentials"}), 400
        
        # Create JWT token
        token = jwt.encode({'id': str(user['_id'])}, JWT_SECRET, algorithm="HS256")
        
        # Return user data without password
        user_response = {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "role": user.get('role', '')
        }
        
        return jsonify({
            "user": user_response,
            "token": token
        }), 200
        
    except Exception as e:
        return jsonify({"msg": "Server error"}), 500
    finally:
        if 'client' in locals():
            client.close()

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_user(current_user_id):
    """Get current user profile"""
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        users_collection = db["users"]
        
        # Find user
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        # Return user data without password
        user_response = {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "role": user.get('role', '')
        }
        
        return jsonify({"user": user_response}), 200
        
    except Exception as e:
        return jsonify({"msg": "Server error"}), 500
    finally:
        if 'client' in locals():
            client.close()

@app.route('/api/auth/me', methods=['PUT'])
@token_required
def update_user(current_user_id):
    """Update current user profile"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        role = data.get('role')
        
        client = get_mongo_client()
        db = client["pharma_hub"]
        users_collection = db["users"]
        
        # Find user
        user = users_collection.find_one({"_id": ObjectId(current_user_id)})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        # Update fields
        update_data = {}
        if name:
            update_data['name'] = name
        if email:
            update_data['email'] = email
        if role is not None:
            update_data['role'] = role
            
        # Update user
        users_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {"$set": update_data}
        )
        
        # Return updated user data
        updated_user = users_collection.find_one({"_id": ObjectId(current_user_id)})
        user_response = {
            "id": str(updated_user['_id']),
            "name": updated_user['name'],
            "email": updated_user['email'],
            "role": updated_user.get('role', '')
        }
        
        return jsonify({"user": user_response}), 200
        
    except Exception as e:
        return jsonify({"msg": "Server error"}), 500
    finally:
        if 'client' in locals():
            client.close()

@app.route('/api/exim', methods=['GET'])
def get_exim_data():
    """Get EXIM trade data"""
    try:
        hs_code = request.args.get('hs_code')
        year_from = request.args.get('year_from')
        year_to = request.args.get('year_to')
        top_n = request.args.get('top_n', 10)
        
        # If no HS code provided, use a default one for pharmaceutical products
        if not hs_code:
            hs_code = "3004"  # Default HS code for pharmaceutical products
        
        data = exim_agent.get_trade_by_hs(
            hs_code=hs_code,
            year_from=year_from,
            year_to=year_to,
            top_n=int(top_n)
        )
        
        return jsonify({
            "query": f"EXIM data for HS code {hs_code}",
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        # Return mock data as fallback
        try:
            mock_data = exim_agent.get_mock_trade_data(hs_code or "3004", int(top_n))
            return jsonify({
                "query": f"EXIM data for HS code {hs_code or '3004'}",
                "data": mock_data,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as mock_e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/trials', methods=['GET'])
def get_trials_data():
    """Get clinical trials data"""
    try:
        condition = request.args.get('condition')
        phase = request.args.get('phase')
        status = request.args.get('status')
        top_n = request.args.get('top_n', 10)
        
        # If no condition provided, use a default one
        if not condition:
            condition = "diabetes"  # Default condition
        
        result = trials_agent.search_trials(
            condition=condition,
            phase=phase,
            status=status,
            top_n=int(top_n)
        )
        
        # Handle both old and new return formats
        if isinstance(result, dict):
            # New format with metadata
            data = result.get("data", [])
            source = result.get("source", "Unknown")
        else:
            # Old format (just data list)
            data = result
            source = "API"
        
        return jsonify({
            "query": f"Clinical trials for {condition}",
            "data": data,
            "source": source,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        # Return mock data as fallback
        try:
            mock_data = trials_agent.get_mock_trials(condition or "diabetes", phase, status, int(top_n))
            return jsonify({
                "query": f"Clinical trials for {condition or 'diabetes'}",
                "data": mock_data,
                "source": "Mock Data",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as mock_e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/iqvia', methods=['GET'])
def get_iqvia_data():
    """Get IQVIA market data"""
    try:
        therapy_area = request.args.get('therapy_area')
        
        stats = iqvia_agent.get_market_stats(therapy_area=therapy_area)
        competitors = iqvia_agent.get_competitor_analysis(therapy_area=therapy_area)
        trends = iqvia_agent.get_therapy_trends(therapy_area=therapy_area)
        
        data = {
            "market_stats": stats,
            "competitors": competitors,
            "trends": trends
        }
        
        return jsonify({
            "query": f"IQVIA data for {therapy_area or 'general market'}",
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patents', methods=['GET'])
def get_patent_data():
    """Get patent data"""
    try:
        query = request.args.get('query')
        assignee = request.args.get('assignee')
        ipc_code = request.args.get('ipc_code')
        top_n = request.args.get('top_n', 10)
        
        # Use at least one search parameter
        if not query and not assignee and not ipc_code:
            # For gene therapy query, provide a default search
            if request.args.get('query', '').lower() == 'find recent patents related to gene therapy':
                query = 'gene therapy'
            else:
                query = "pharmaceutical"  # Default search term
        
        data = patent_agent.search_patents(
            query=query or "",
            assignee=assignee,
            ipc_code=ipc_code,
            top_n=int(top_n)
        )
        
        # Include text_summary in response if available
        response_data = {
            "query": f"Patent search for {query or assignee or ipc_code}",
            "data": data.get("data", []),
            "text_summary": data.get("text_summary", ""),
            "source": data.get("source", "Unknown"),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add error info if present
        if "error" in data:
            response_data["error"] = data["error"]
        
        return jsonify(response_data)
    except Exception as e:
        # Even if there's an exception, try to return mock data
        try:
            mock_data = patent_agent.get_mock_patent_data(query or "gene therapy", int(top_n))
            text_representation = "\n\n".join([patent_agent.format_patent_as_text(patent) for patent in mock_data])
            return jsonify({
                "query": f"Patent search for {query or assignee or ipc_code}",
                "data": mock_data,
                "text_summary": text_representation,
                "source": "Mock Data",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as mock_e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/web-intel', methods=['GET'])
def get_web_intel_data():
    """Get web intelligence data"""
    try:
        query = request.args.get('query')
        num_results = request.args.get('num_results', 5)
        
        if not query:
            return jsonify({"error": "query parameter is required"}), 400
        
        data = webintel_agent.search_web(
            query=query,
            num_results=int(num_results)
        )
        
        return jsonify({
            "query": f"Web search for {query}",
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/internal-docs', methods=['GET'])
def get_internal_docs():
    """Get internal documents"""
    try:
        query = request.args.get('query')
        top_n = request.args.get('top_n', 5)
        
        if not query:
            return jsonify({"error": "query parameter is required"}), 400
        
        data = internal_agent.search_internal_documents(
            query=query,
            top_n=int(top_n)
        )
        
        return jsonify({
            "query": f"Internal documents for {query}",
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/master-agent', methods=['POST'])
def run_master_agent_endpoint():
    """Run the master agent with a query"""
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({"error": "query parameter is required"}), 400
        
        # Run master agent
        response = run_master_agent(query)
        
        return jsonify({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate a report from collected data and store it in MongoDB"""
    client = None
    try:
        data = request.get_json()
        query = data.get('query')
        results = data.get('results')
        report_type = data.get('type', 'text')  # text, pdf, or excel
        user_id = data.get('user_id')  # Optional user ID
        
        print(f"Generating report: query={query}, type={report_type}, user_id={user_id}")
        
        if not query or not results:
            return jsonify({"error": "query and results are required"}), 400
        
        # Filter out empty sections
        filtered_results = {k: v for k, v in results.items() if v}
        print(f"Filtered results keys: {list(filtered_results.keys())}")
        
        # Generate report
        filepath = None
        summary = None
        if report_type == 'pdf':
            filepath = report_generator.generate_pdf_report(query, filtered_results)
            print(f"PDF report generated: {filepath}")
        elif report_type == 'excel':
            filepath = report_generator.generate_excel_report(query, filtered_results)
            print(f"Excel report generated: {filepath}")
        elif report_type == 'text':
            summary = report_generator.generate_text_summary(query, filtered_results)
            print(f"Text summary generated: {len(summary) if summary else 0} characters")
        else:
            return jsonify({"error": "Invalid report type. Use 'pdf', 'excel', or 'text'"}), 400
            
        # Store report in MongoDB
        print("Storing report in MongoDB...")
        client = get_mongo_client()
        db = client["pharma_hub"]
        reports_collection = db["reports"]
        
        # Create report record
        report_id = str(uuid.uuid4())
        report_record = {
            "report_id": report_id,
            "query": query,
            "report_type": report_type,
            "file_path": filepath if report_type in ['pdf', 'excel'] else None,
            "generated_at": datetime.now().isoformat(),
            "generated_by": user_id,
            "metadata": {
                "sections": list(filtered_results.keys()),
                "data_points": sum(len(v) if isinstance(v, list) else 1 for v in filtered_results.values())
            }
        }
        print(f"Report record prepared: {report_record}")
        
        # For PDF and Excel reports, store the binary data
        if report_type in ['pdf', 'excel'] and filepath:
            try:
                print(f"Reading file data from: {filepath}")
                with open(filepath, 'rb') as f:
                    binary_data = f.read()
                report_record["file_data"] = Binary(binary_data)
                print(f"Binary data read: {len(binary_data)} bytes")
            except Exception as file_error:
                print(f"Warning: Could not read file data: {file_error}")
                import traceback
                traceback.print_exc()
        
        # For text reports, store the summary
        if report_type == 'text' and summary:
            report_record["text_summary"] = summary
            
        # Insert report record into database
        print("Inserting report record into database...")
        result = reports_collection.insert_one(report_record)
        print(f"Report record inserted with ID: {result.inserted_id}")
        
        # Return appropriate response
        print("Returning response...")
        if report_type == 'pdf' and filepath:
            # For PDF, return download info instead of sending file directly
            return jsonify({
                "report_id": report_id,
                "query": query,
                "report_type": report_type,
                "message": "PDF report generated successfully",
                "download_url": f"/api/reports/{report_id}/download"
            })
        elif report_type == 'excel' and filepath:
            # For Excel, return download info instead of sending file directly
            return jsonify({
                "report_id": report_id,
                "query": query,
                "report_type": report_type,
                "message": "Excel report generated successfully",
                "download_url": f"/api/reports/{report_id}/download"
            })
        elif report_type == 'text' and summary:
            return jsonify({
                "query": query,
                "summary": summary,
                "report_id": report_id,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": "Invalid report type or missing data"}), 400
            
    except Exception as e:
        print(f"Error generating report: {str(e)}")  # Log the error for debugging
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500
    finally:
        # Close MongoDB connection
        if client:
            try:
                client.close()
                print("MongoDB connection closed")
            except Exception as close_error:
                print(f"Error closing MongoDB connection: {close_error}")

@app.route('/api/reports', methods=['GET'])
def list_reports():
    """List all stored reports"""
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        reports_collection = db["reports"]
        
        # Find all reports
        reports = list(reports_collection.find({}, {
            "report_id": 1, 
            "query": 1, 
            "report_type": 1, 
            "generated_at": 1, 
            "generated_by": 1, 
            "metadata": 1,
            "_id": 0
        }))
        
        # Close MongoDB connection
        client.close()
        
        # Return reports list
        return jsonify({
            "reports": reports,
            "count": len(reports)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    """Retrieve a stored report by ID"""
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        reports_collection = db["reports"]
        
        # Find report
        report = reports_collection.find_one({"report_id": report_id})
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        # Close MongoDB connection
        client.close()
        
        # Return report metadata
        return jsonify({
            "report_id": report["report_id"],
            "query": report["query"],
            "report_type": report["report_type"],
            "generated_at": report["generated_at"],
            "generated_by": report.get("generated_by"),
            "metadata": report.get("metadata")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/<report_id>/download', methods=['GET'])
def download_report(report_id):
    """Download a stored report by ID"""
    try:
        client = get_mongo_client()
        db = client["pharma_hub"]
        reports_collection = db["reports"]
        
        # Find report
        report = reports_collection.find_one({"report_id": report_id})
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        # Close MongoDB connection
        client.close()
        
        # For text reports, return the summary
        if report["report_type"] == "text":
            return jsonify({
                "query": report["query"],
                "summary": report["text_summary"],
                "timestamp": report["generated_at"]
            })
        
        # For PDF and Excel reports, return the file data
        if report["report_type"] in ["pdf", "excel"] and "file_data" in report:
            from flask import Response
            import io
            
            # Return binary data as file
            return Response(
                report["file_data"],
                mimetype='application/pdf' if report["report_type"] == "pdf" else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers={
                    "Content-Disposition": f"attachment; filename=report_{report_id}.{report['report_type']}"
                }
            )
        
        return jsonify({"error": "Report data not available"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Pharma Mind Nexus API server on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)