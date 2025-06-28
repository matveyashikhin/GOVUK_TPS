import os
from pathlib import Path

class Config:
    """Configuration class for the Trademark Explorer application"""
    
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = Path(__file__).parent
        else:
            base_path = Path(base_path)
        
        self.base_path = base_path
        
    @property
    def data_file_path(self):
        """Path to the main CSV data file"""
        return self.base_path / "data" / "consolidated_table_with_links.csv"
    
    @property
    def classes_file_path(self):
        """Path to the IPO classes CSV file"""
        return self.base_path / "data" / "ipoclasses.csv"
    
    @property
    def stock_cache_path(self):
        """Path to the stock cache JSON file"""
        return self.base_path / "data" / "stock_cache.json"
    
    # Flask settings
    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = 2000
    FLASK_DEBUG = False
    
    # Data settings
    DEFAULT_SEARCH_LIMIT = 100
    DEFAULT_STOCK_ANALYSIS_LIMIT = 500
    STOCK_CACHE_HOURS = 1
    
    # UI settings
    MAX_DISPLAY_RESULTS = 100
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        data_dir = self.base_path / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir