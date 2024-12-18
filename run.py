from app import create_app
import os
from dotenv import load_dotenv

# Add the project root directory to Python path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)