# TaxAssist

A modern AI-powered tax assistant chatbot built with Flask and Google's Gemini API.

## Features

- Interactive chat interface for tax-related queries
- Real-time responses using Google's Gemini AI
- Clean, modern UI with typing indicators and animations
- Mobile-responsive design

## Tech Stack

- Python 3.8+
- Flask
- Google Gemini API
- HTML5/CSS3
- JavaScript

## Setup

1. Clone the repository:
```bash
git clone https://github.com/mohalkarushikesh/TaxAssist.git
cd TaxAssist
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Windows
set GOOGLE_API_KEY=your_api_key
# Linux/Mac
export GOOGLE_API_KEY=your_api_key
```

5. Run the application:
```bash
python -m src.taxassist.app
```

The application will be available at `http://localhost:5000`

## Project Structure

```
taxassist/
├── config/
│   └── config.yaml       # Configuration settings
├── src/
│   └── taxassist/
│       ├── app.py        # Main application
│       └── utils/
│           ├── logger.py # Logging setup
│           └── tax_processor.py # Tax processing logic
├── logs/                 # Application logs
└── requirements.txt      # Dependencies
```

## Contributing

Feel free to open issues and pull requests for any improvements.

## License

MIT License