from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__, 
           static_url_path='/static',
           static_folder='../static',
           template_folder='../templates')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCDGdoZrW4V10rnTCCGRu6vWNs-AddIsfY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# System prompt for TaxAssist
SYSTEM_PROMPT = """You are TaxAssist, Cotality.com's expert property tax chatbot. 
You provide accurate, friendly, and concise responses about property taxes. 
Focus on property tax calculations, regulations, and guidance.
Always maintain a professional yet approachable tone.

Your capabilities include:
1. Property tax calculations and estimates
2. Information about tax laws and regulations
3. Guidance on filing property tax returns
4. Tax compliance checks and deadlines
5. Updates on tax-related news and legislative changes

When providing estimates, use typical property tax rates and indicate they are based on Cotality's insights."""

@app.route("/")
def home():
    """Serve the chatbot interface"""
    return render_template('index.html')

@app.route("/api/chat", methods=["POST"])
def chat():
    """Process chat messages"""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing message in request"}), 400

        user_message = data["message"]
        prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nTaxAssist:"
        
        # Generate response using Gemini
        response = model.generate_content(prompt)
        
        return jsonify({
            "response": response.text,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "error": "An error occurred while processing your request.",
            "details": str(e)
        }), 500

@app.route("/api/tax-estimate", methods=["POST"])
def tax_estimate():
    """Calculate property tax estimates"""
    try:
        data = request.json
        property_value = data.get('value', 0)
        location = data.get('location', '')
        property_type = data.get('type', '')
        
        prompt = f"{SYSTEM_PROMPT}\n\nCalculate estimated property tax for:\nValue: ${property_value:,}\nLocation: {location}\nType: {property_type}\n\nTaxAssist:"
        response = model.generate_content(prompt)
        
        return jsonify({
            'estimate': response.text,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': 'Unable to calculate tax estimate.',
            'details': str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug) 