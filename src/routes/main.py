import re
import markdown2
from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import google.generativeai as genai

main_bp = Blueprint('main', __name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# System prompt for Taxly, your AI-powered Tax Assistant
SYSTEM_PROMPT = """You are Taxly, your AI-powered Tax Assistant, Taxly.com's expert property tax chatbot. \
You provide accurate, friendly, and concise responses about property taxes. \
Focus on property tax calculations, regulations, and guidance.\
Always maintain a professional yet approachable tone.\
\
Your capabilities include:\
1. Property tax calculations and estimates\
2. Information about tax laws and regulations\
3. Guidance on filing property tax returns\
4. Tax compliance checks and deadlines\
5. Updates on tax-related news and legislative changes\
\
When providing estimates, use typical property tax rates and indicate they are based on Taxly's insights."""

def starts_with_greeting(text):
    greetings = [
        r'^hi\b', r'^hello\b', r'^hey\b', r'^greetings\b', r'^welcome\b'
    ]
    text = text.strip().lower()
    return any(re.match(greet, text) for greet in greetings)

# Removed the '/' route that rendered index.html

@main_bp.route("/api/chat", methods=["POST"])
def chat():
    """Process chat messages with formatted responses"""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing message in request"}), 400

        user_message = data["message"].strip().lower()
        is_first = data.get("is_first", False)
        capabilities_triggers = [
            "what are your capabilities",
            "what can you do",
            "your capabilities",
            "can you help me",
            "how can you help"
        ]

        if any(trigger in user_message for trigger in capabilities_triggers):
            formatted_response = (
                "<b>Here are my capabilities as Taxly, your AI-powered Tax Assistant:</b><br><br>"
                "<ul>"
                "<li>Calculating property tax estimates</li>"
                "<li>Explaining tax laws and regulations</li>"
                "<li>Guiding you through filing property tax returns</li>"
                "<li>Checking compliance or deadlines</li>"
                "<li>Providing updates on tax-related news and legislative changes</li>"
                "</ul>"
                "Just let me know how I can assist you further!"
            )
        else:
            prompt = f"{SYSTEM_PROMPT}\n\nUser: {data['message']}\nTaxAssist:"
            response = model.generate_content(prompt)
            llm_text = response.text.strip()
            llm_html = markdown2.markdown(llm_text)
            if is_first:
                if starts_with_greeting(llm_text):
                    formatted_response = (
                        f"{llm_html}<br><br>"
                        "Just let me know how I can assist you further!"
                    )
                else:
                    formatted_response = (
                        "<b>Hello! I'm Taxly, your AI-powered Tax Assistant from Taxly.com. How can I help you today?</b><br><br>"
                        f"{llm_html}<br><br>"
                        "Just let me know how I can assist you further!"
                    )
            else:
                formatted_response = (
                    f"{llm_html}<br><br>"
                    "Just let me know how I can assist you further!"
                )

        return jsonify({
            "response": formatted_response,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "error": "An error occurred while processing your request.",
            "details": str(e)
        }), 500

@main_bp.route("/api/tax-estimate", methods=["POST"])
def tax_estimate():
    """Calculate property tax estimates"""
    try:
        data = request.json
        property_value = data.get('value', 0)
        location = data.get('location', '')
        property_type = data.get('type', '')
        prompt = f"{SYSTEM_PROMPT}\n\nCalculate estimated property tax for:\nValue: ${property_value:,}\nLocation: {location}\nType: {property_type}\n\nTaxAssist:"
        response = model.generate_content(prompt)
        llm_html = markdown2.markdown(response.text.strip())
        formatted_response = (
            "<b>Hello! I'm Taxly, your AI-powered Tax Assistant from Taxly.com. Here's your property tax estimate:</b><br><br>"
            f"{llm_html}<br><br>"
            "Need a detailed breakdown or help with filing? Let me know!"
        )
        return jsonify({
            'estimate': formatted_response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': 'Unable to calculate tax estimate.',
            'details': str(e)
        }), 500

@main_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })
