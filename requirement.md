# Taxly, your AI-powered Tax Assistant Chatbot Prompt for Taxly.com

## Objective
Develop an independent chatbot named **Taxly, your AI-powered Tax Assistant** for [taxly.com](https://taxly.com)'s tax team to efficiently handle property-related tax queries. The chatbot uses the Gemini API (gemini-2.0-flash) with the API key `YOUR_GEMINI_API_KEY` for generating responses. It serves internal users (tax team members) and external users (clients or partners) by providing accurate, timely, and user-friendly responses, referencing Taxly’s property data systems for real-time tax information. The chatbot incorporates real-world use cases, advanced features, and a modern, Taxly-branded user interface.

## Key Requirements

### Purpose
Handle a wide range of property-related tax queries, including:
- Answering questions about property tax calculations, factors, and regional variations.
- Providing estimates for property taxes based on user inputs (e.g., location, value, type).
- Offering information on tax laws, regulations, and recent changes affecting property owners or businesses.
- Guiding users through filing property tax returns or other tax-related forms, including step-by-step instructions or links to Taxly resources.
- Assisting with compliance checks, ensuring users are aware of tax obligations and deadlines.
- Providing real-time updates on tax-related news or legislative changes impacting property taxes.

### API Integration
- Use the Gemini API (`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`) with the provided API key (`YOUR_GEMINI_API_KEY`) for conversational responses.
- Structure API requests with a system prompt configuring the chatbot as TaxAssist, an expert in property taxes for Taxly, ensuring concise, friendly, and relevant responses.
- Handle API errors gracefully, displaying user-friendly messages (e.g., “Oops, something went wrong! Please try again.”).

### Cotality Data Reference
- Reference Taxly’s property data systems for accurate tax information (e.g., tax rates, exemptions, regional data). Use mock data or publicly available Taxly resources (e.g., [Taxly Insights](https://taxly.com)) as placeholders, simulating real-time integration.
- Example: For “Tax rate for Irvine, CA,” respond with an estimated rate (e.g., 1%) sourced from Taxly’s insights.
- Prepare for future integration with Taxly’s API or database for real-time data retrieval.

### Real-World Use Cases
- **Property Tax Estimation**: A user inputs property details (e.g., $500,000 home in Irvine, CA), and TaxAssist estimates annual tax based on current rates.
- **Tax Law Updates**: A client asks about recent tax law changes, and TaxAssist summarizes updates with links to Taxly resources.
- **Filing Assistance**: A user seeks help filing a tax return, and TaxAssist provides step-by-step guidance or links to forms.
- **Deadline Reminders**: TaxAssist proactively reminds users of upcoming tax deadlines (e.g., April 15, 2025).
- **Internal Team Support**: A tax team member queries regional tax rates, and TaxAssist delivers quick, accurate data.

### Features
- **Natural Language Processing (NLP)**: Leverages Gemini API’s NLP capabilities to understand varied query phrasings.
- **Database Integration (Mock)**: Simulates connection to Taxly’s property data for tax calculations, using mock data until real API access is provided.
- **Multi-Language Support**: Supports English, with placeholders for additional languages (e.g., Spanish, German) to reflect Taxly’s global operations.
- **Secure Data Handling**: Ensures user inputs are processed securely, with no storage of sensitive data, complying with GDPR and CCPA.
- **Escalation to Human Agents**: Includes a button or command (e.g., “Talk to a human”) to escalate complex queries to Taxly’s support (e.g., [supportUK@taxly.com](mailto:supportUK@taxly.com) or 0333 123 1417 for UK).
- **Message History Toggle**: Allows users to show/hide chat history for privacy or clarity.
- **Clear Chat Button**: Resets the chat session, retaining only the welcome message.
- **Visual Data Support**: Displays tax trends or estimates as text-based tables (e.g., historical rates) or links to Taxly visualizations.
- **Conversational Tone**: Maintains a friendly, professional tone (e.g., “Happy to help with your tax query!”).
- **24/7 Availability**: Accessible anytime via a web interface.
- **Typing Animation**: Shows a typing indicator for a natural conversation flow.

### User Interface
- **Branding**: Uses a Taxly-branded light theme with colors inspired by their website (e.g., blue, white, gray).
- **Typography**: Uses “Amazon Ember” or a similar professional font (fallback to Arial).
- **Layout**: Includes a header with Taxly’s logo, a scrollable chatbox, and an input area with send/escalation buttons.
- **Responsiveness**: Mobile-friendly with stacked layouts on smaller screens.
- **Accessibility**: Includes ARIA labels and high-contrast focus states.

### Name
The chatbot is named **Taxly, your AI-powered Tax Assistant**, reflecting its tax expertise and alignment with Taxly’s property focus.

## Implementation
- **Platform**: A Flask-based web application with a single-page interface (`index.html`).
- **Dependencies**: Flask for the backend, Tailwind CSS for styling, Font Awesome for icons.
- **Gemini API Call**: Sends user queries to the Gemini API with a system prompt, processes responses, and formats them for display.

## Additional Considerations
- **Scalability**: Handles increasing query volumes as Taxly grows.
- **Security**: Avoids storing sensitive data client-side; uses HTTPS for API calls.
- **Testing**: Validates API key functionality and response accuracy with mock tax queries.
- **Future Enhancements**: Integrate Taxly’s real API for data access, add voice input, or support additional languages.

## Sample Interaction
**User**: “What’s the property tax for a $750,000 condo in Toronto?”  
**Taxly, your AI-powered Tax Assistant**: “Based on Taxly’s data, the estimated property tax for a $750,000 condo in Toronto is ~$4,500 (0.6% rate). Want a detailed breakdown or filing help?”  

**User**: “Any new tax laws in Ontario?”  
**Taxly, your AI-powered Tax Assistant**: “In 2025, Ontario introduced a first-time buyer tax credit, saving up to $4,000. Check details at [Taxly Insights](https://taxly.com). Need assistance applying it?”

## Conclusion
TaxAssist will streamline Taxly’s tax team operations by automating property tax queries using the Gemini API and referencing Taxly’s data. Its advanced features, real-world use cases, and Taxly-branded interface will enhance efficiency and user satisfaction, aligning with Taxly’s mission of delivering actionable property insights.