from flask import Flask, render_template, redirect, url_for, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

def create_app():
    load_dotenv()
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder='../static',
        template_folder='../templates'
    )
    app.secret_key = os.getenv('SECRET_KEY', 'devsecret')
    CORS(app)

    # Register blueprints
    from src.routes.main import main_bp
    from src.auth import auth_bp, login_required
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Landing page
    @app.route('/')
    def landing():
        return render_template('landing.html', year=datetime.now().year)

    # Protected chat route
    @app.route('/chat')
    @login_required
    def chat():
        return render_template('index.html')

    return app

# For legacy support if someone runs this file directly
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)