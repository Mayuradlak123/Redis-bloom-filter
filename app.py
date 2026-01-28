import os
from dotenv import load_dotenv
from flask import Flask, render_template
from api.routes.auth import auth_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    print(f"🚀 Starting Flask server on http://127.0.0.1:{PORT}")
    app.run(debug=DEBUG, port=PORT)
