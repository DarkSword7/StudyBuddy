from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Import routes here to avoid circular imports
    from .routes import init_routes
    init_routes(app)
    
    return app