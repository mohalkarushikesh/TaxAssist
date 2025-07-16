from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder='../static',
        template_folder='../templates'
    )
    CORS(app)

    # Register blueprints
    from src.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app

# For legacy support if someone runs this file directly
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)