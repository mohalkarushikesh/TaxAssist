# TaxAssist - Cotality Property Tax Chatbot

TaxAssist is an intelligent chatbot designed to handle property-related tax queries for Cotality.com. It uses the Gemini API to provide accurate, timely, and user-friendly responses about property taxes, calculations, regulations, and guidance.

## Features

- Real-time property tax assistance
- Natural language understanding
- Tax calculation estimates
- Regulatory guidance
- Filing assistance
- Deadline reminders
- Escalation to human support
- Mobile-responsive interface
- Accessibility-compliant design
- **User authentication (register/login/logout)**
- **Beautiful landing page and modern UI**
- **Local SQLite database for user management**
- **Modular, scalable Flask project structure**

## Technical Stack

- Backend: Python Flask, SQLAlchemy (SQLite)
- Frontend: HTML5, CSS3, JavaScript
- AI: Google's Gemini API
- Styling: Tailwind CSS, custom CSS (Monaco font)
- Icons: Font Awesome

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd taxassist
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
GEMINI_API_KEY=your_gemini_api_key
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your_secret_key
```

5. Run the application:
```bash
python src/app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Open the application in a web browser
2. Register a new account or log in
3. Access the chatbot via the "Get Started" or "Login" button
4. Type your property tax-related question in the chat input
5. Receive instant, formatted responses from TaxAssist
6. Use the "Clear Chat" button to start a new conversation
7. Click the headset icon to escalate to human support if needed

## Project Structure

- `src/app.py` - Main Flask app, blueprint registration, route protection
- `src/auth.py` - Authentication (register, login, logout, session)
- `src/db.py` - Local SQLite DB setup (SQLAlchemy)
- `src/models/` - Data models (User, Property, etc.)
- `src/routes/` - API/chatbot routes (Gemini integration)
- `src/services/` - Business logic (e.g., tax calculation)
- `src/utils/` - Utility functions (e.g., formatting)
- `templates/` - Jinja2 HTML templates (landing, login, register, chat)
- `static/` - CSS, JS, images

## Support

For support inquiries, contact:
- Email: supportUK@cotality.com
- Phone (UK): 0333 123 1417

## License

Copyright © 2024 Cotality.com. All rights reserved.

## Application Screenshots

Below are screenshots of the TaxAssist application UI:

### Landing Page (Top)
![Landing Page Top](static/images/Landing%20Page%20top.png)

### Landing Page (Bottom)
![Landing Page Bottom](static/images/Landing%20Page%20bottom.png)

### Registration Page
![Registration Page](static/images/Registeration%20Page%20UI.png)

### Login Page
![Login Page](static/images/Login%20Page%20UI.png)

### Chatbot UI (Light Mode)
![Chatbot UI 1](static/images/Updated%20Chatbot%20UI1.png)

### Chatbot UI (Dark Mode)
![Chatbot UI 2](static/images/Updated%20Chatbot%20UI2.png)

### Chatbot UI (Dark Mode)
![Chatbot UI 2](static/images/Updated%20Chatbot%20UI3.png)

---

## Future Enhancements

- **Admin dashboard** for user and chat management
- **Password reset and email verification**
- **User profile and settings page**
- **File upload and document analysis (e.g., Form 16 parsing)**
- **Multi-language support**
- **Advanced analytics and reporting**
- **Integration with payment gateways for premium features**
- **Push/email notifications for deadlines and updates**
- **Progressive Web App (PWA) support for offline use**
- **More chatbot personalities and customization**