from flask import render_template, request, jsonify
from .search_engine import SearchEngine

# Create search engine instance
search_engine = SearchEngine()

def init_routes(app):
    """Initialize routes for the Flask application"""
    
    @app.route('/')
    def index():
        """Render the main page"""
        return render_template('index.html')

    @app.route('/search', methods=['POST'])
    def search():
        """Handle search requests"""
        query = request.json.get('query', '')
        
        if not query:
            return jsonify({
                'error': 'No search query provided',
                'results': {}
            }), 400
        
        # Perform comprehensive search
        search_results = search_engine.perform_comprehensive_search(query)
        
        return jsonify({
            'query': query,
            'results': search_results
        })