import logging
from typing import Dict, Any
import yaml
import google.generativeai as genai
import os
from datetime import datetime
import json
import requests

class TaxProcessor:
    def __init__(self):
        """Initialize TaxProcessor with configuration and models"""
        # Load configuration
        with open("config/config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

        # Setup logger
        self.logger = logging.getLogger("taxassist")

        # Initialize Gemini configuration
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # System prompt for tax assistance
        self.system_prompt = """You are TaxAssist, a knowledgeable tax assistant for Cotality.com, 
        specializing in property tax matters. Provide accurate, helpful responses to tax-related queries.
        Focus on property tax calculations, rates, and regional variations."""

    def _call_gemini_api(self, query: str) -> str:
        """Make API call to Gemini model"""
        try:
            full_url = f"{self.gemini_url}?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{self.system_prompt}\n\nUser query: {query}"
                    }]
                }]
            }

            response = requests.post(
                full_url,
                headers={"Content-Type": "application/json"},
                json=payload
            )

            if response.status_code != 200:
                self.logger.error(f"Gemini API error: {response.text}")
                raise Exception("Failed to get response from Gemini API")

            result = response.json()
            if "candidates" in result:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            return "I apologize, but I couldn't process that request at the moment."

        except Exception as e:
            self.logger.error(f"Error calling Gemini API: {str(e)}")
            raise

    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a tax-related query"""
        try:
            # Log incoming query
            self.logger.info(f"Processing query: {query}")

            # Get response from Gemini model
            response = self._call_gemini_api(query)

            return {
                "response": response,
                "confidence": self.config["nlp"]["confidence_threshold"],
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            raise

    def calculate_tax_estimate(self, property_value: float, location: str) -> Dict[str, Any]:
        """Calculate estimated property tax based on value and location"""
        try:
            # Log estimation request
            self.logger.info(f"Calculating tax estimate for property value: {property_value} in {location}")

            # Create a structured query for tax estimation
            query = f"""Calculate property tax estimate for:
            Property Value: ${property_value:,.2f}
            Location: {location}
            
            Please provide:
            1. Estimated tax rate for the location
            2. Calculated annual property tax
            3. Any relevant exemptions or special considerations
            """

            # Get response from Gemini model
            response = self._call_gemini_api(query)

            # For now, use a simple calculation as fallback
            estimated_rate = 0.01  # 1% placeholder rate
            estimated_tax = property_value * estimated_rate

            return {
                "estimated_tax": estimated_tax,
                "tax_rate": estimated_rate,
                "location": location,
                "property_value": property_value,
                "ai_response": response,
                "note": "This is an estimate and may not reflect actual tax obligations.",
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error calculating tax estimate: {str(e)}")
            raise 