# File: app.py (Updated for flat structure)
#!/usr/bin/env python3
"""
Trademark Data Explorer - Main Application
A modular Flask application for exploring and analyzing trademark data.
"""

from flask import Flask
from pathlib import Path

# Import configuration and components (UPDATED FOR FLAT STRUCTURE)
from config import Config
from data_loader import TrademarkDataLoader  # Changed from data.data_loader
from analytics import TrademarkAnalytics     # Changed from models.analytics
from stock_matcher import StockMatcher       # Changed from models.stock_matcher
from main_routes import MainRoutes           # Changed from routes.main_routes
from api_routes import APIRoutes             # Changed from routes.api_routes
from stock_routes import StockRoutes         # Changed from routes.stock_routes

class TrademarkExplorerApp:
    """Main application class that orchestrates all components"""
    
    def __init__(self, base_path=None):
        # Initialize configuration
        self.config = Config(base_path)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
        
        # Initialize core components
        self._initialize_components()
        
        # Register routes
        self._register_routes()
        
        print("✓ Trademark Explorer initialized successfully!")
        print(f"✓ Data directory: {self.config.base_path}")
        print(f"✓ Configuration loaded")
    
    def _initialize_components(self):
        """Initialize all application components"""
        print("Initializing application components...")
        
        # Initialize data loader
        self.data_loader = TrademarkDataLoader(self.config)
        print("✓ Data loader initialized")
        
        # Load data
        print("Loading trademark data...")
        self.data_loader.load_main_data()
        self.data_loader.load_classes_data()
        print("✓ Data loaded successfully")
        
        # Initialize analytics
        self.analytics = TrademarkAnalytics(self.data_loader)
        print("✓ Analytics module initialized")
        
        # Initialize stock matcher
        self.stock_matcher = StockMatcher(self.config)
        print("✓ Stock matcher initialized")
        
        # Initialize route handlers
        self.main_routes = MainRoutes(self.data_loader, self.analytics)
        self.api_routes = APIRoutes(self.data_loader, self.stock_matcher)
        self.stock_routes = StockRoutes(self.data_loader, self.stock_matcher)
        print("✓ Route handlers initialized")
    
    def _register_routes(self):
        """Register all application routes"""
        print("Registering routes...")
        
        # Main application routes
        self.app.route('/')(self.main_routes.dashboard)
        self.app.route('/search')(self.main_routes.search_page)
        self.app.route('/analytics')(self.main_routes.analytics_page)
        self.app.route('/export')(self.main_routes.export_page)
        self.app.route('/about')(self.main_routes.about_page)
        
        # NEW ROUTE: Owner details page - with proper method reference
        @self.app.route('/owner/<path:owner_name>')
        def owner_details_route(owner_name):
            return self.main_routes.owner_details_page(owner_name)
        
        # Stock routes
        self.app.route('/stocks')(self.stock_routes.stocks_page)
        
        # API routes
        self.app.route('/api/search')(self.api_routes.search)
        self.app.route('/api/class-guide')(self.api_routes.class_guide)
        self.app.route('/api/class-guide/download')(self.api_routes.download_class_guide)
        self.app.route('/api/export/csv')(self.api_routes.export_csv)
        self.app.route('/api/export/excel')(self.api_routes.export_excel)
        self.app.route('/api/analyze-stocks')(self.api_routes.analyze_stocks)
        
        # NEW API ROUTE: Export owner-specific data - with proper method reference
        @self.app.route('/api/export/owner/<path:owner_name>')
        def export_owner_route(owner_name):
            return self.api_routes.export_owner_data(owner_name)
        
        print("✓ Routes registered successfully")
    
    def run(self, debug=None, host=None, port=None):
        """Run the Flask application"""
        # Use config defaults if not specified
        debug = debug if debug is not None else self.config.FLASK_DEBUG
        host = host or self.config.FLASK_HOST
        port = port or self.config.FLASK_PORT
        
        print(f"\n🚀 Starting Trademark Explorer...")
        print(f"   Server: http://{host}:{port}")
        print(f"   Debug mode: {debug}")
        print(f"   Records loaded: {len(self.data_loader.df):,}")
        print(f"   Classes loaded: {len(self.data_loader.classes_df):,}")
        print("   Press Ctrl+C to stop\n")
        
        self.app.run(host=host, port=port, debug=debug)
    
    def get_app(self):
        """Get the Flask app instance (useful for deployment)"""
        return self.app
    
    def get_stats(self):
        """Get application statistics"""
        return {
            'config': {
                'data_path': str(self.config.data_file_path),
                'classes_path': str(self.config.classes_file_path),
                'cache_path': str(self.config.stock_cache_path)
            },
            'data': self.data_loader.get_data_stats(),
            'stock_mappings': len(self.stock_matcher.manual_mappings),
            'blacklisted_companies': len(self.stock_matcher.company_blacklist)
        }

def create_app(base_path=None):
    """Factory function to create the Flask app (useful for deployment)"""
    explorer = TrademarkExplorerApp(base_path)
    return explorer.get_app()

def main():
    """Main entry point for running the application"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Trademark Data Explorer')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run on')
    parser.add_argument('--port', type=int, default=2000, help='Port to run on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--data-path', help='Path to data directory')
    parser.add_argument('--stats', action='store_true', help='Show app statistics and exit')
    
    args = parser.parse_args()
    
    try:
        # Initialize the application
        app = TrademarkExplorerApp(args.data_path)
        
        if args.stats:
            # Show statistics and exit
            stats = app.get_stats()
            print("\n📊 Application Statistics:")
            print("=" * 50)
            print(f"Data file: {stats['config']['data_path']}")
            print(f"Classes file: {stats['config']['classes_path']}")
            print(f"Cache file: {stats['config']['cache_path']}")
            print(f"Total records: {stats['data']['total_records']:,}")
            print(f"Unique words: {stats['data']['unique_words']:,}")
            print(f"Unique owners: {stats['data']['unique_owners']:,}")
            print(f"Unique classes: {stats['data']['unique_classes']:,}")
            print(f"Records with links: {stats['data']['links_count']:,}")
            print(f"Stock mappings: {stats['stock_mappings']:,}")
            print(f"Blacklisted terms: {stats['blacklisted_companies']:,}")
            return
        
        # Run the application
        app.run(debug=args.debug, host=args.host, port=args.port)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()