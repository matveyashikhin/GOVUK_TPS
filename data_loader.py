# File: data_loader.py (Updated for flat structure)
import pandas as pd
import os
from pathlib import Path
from sample_data import IPOClassGenerator  # Changed from .sample_data

class TrademarkDataLoader:
    """Handles loading and managing trademark data"""
    
    def __init__(self, config):
        self.config = config
        self._df = None
        self._classes_df = None
        
    def load_main_data(self):
        """Load the main trademark CSV data"""
        data_path = self.config.data_file_path
        
        if data_path.exists():
            print(f"✓ CSV file found at: {data_path}")
            df = pd.read_csv(data_path)
            
            # Process date column if it exists
            if 'Date' in df.columns:
                try:
                    df['Date_sort'] = pd.to_datetime(df['Date'], format='%d %B %Y', errors='coerce')
                    print("✓ Date column converted for proper sorting")
                except Exception as e:
                    print(f"⚠ Could not convert dates: {e}")
                    
            print(f"✓ CSV loaded successfully. Shape: {df.shape}")
            self._df = df
            return df
        else:
            print(f"✗ CSV file NOT found at: {data_path}")
            return pd.DataFrame(columns=['Word', 'Classes', 'Owner', 'Link', 'Date'])
    
    def load_classes_data(self):
        """Load the IPO classes data"""
        classes_path = self.config.classes_file_path
        
        # Try to load existing file first
        if classes_path.exists():
            try:
                print(f"✓ Classes file found at: {classes_path}")
                classes_df = pd.read_csv(classes_path)
                print(f"✓ Classes loaded successfully. Shape: {classes_df.shape}")
                self._classes_df = classes_df
                return classes_df
            except Exception as e:
                print(f"✗ Error loading classes file: {e}")
        
        # Create sample data if file doesn't exist or failed to load
        print("Creating sample IPO classes data...")
        generator = IPOClassGenerator()
        classes_df = generator.create_sample_classes(classes_path)
        self._classes_df = classes_df
        return classes_df
    
    @property
    def df(self):
        """Get the main dataframe, loading if necessary"""
        if self._df is None:
            self._df = self.load_main_data()
        return self._df
    
    @property
    def classes_df(self):
        """Get the classes dataframe, loading if necessary"""
        if self._classes_df is None:
            self._classes_df = self.load_classes_data()
        return self._classes_df
    
    def get_data_stats(self):
        """Get basic statistics about the loaded data"""
        df = self.df
        return {
            'total_records': len(df),
            'unique_words': df['Word'].nunique() if 'Word' in df.columns else 0,
            'unique_owners': df['Owner'].nunique() if 'Owner' in df.columns else 0,
            'links_count': df['Link'].notna().sum() if 'Link' in df.columns else 0,
            'unique_classes': df['Classes'].nunique() if 'Classes' in df.columns else 0
        }
    
    def search_data(self, query, field='all', sort_by='', sort_order='asc', limit=100):
        """Search the trademark data"""
        df = self.df
        
        if not query.strip():
            return {'results': [], 'count': 0}
        
        try:
            # Apply search filter
            if field == 'all':
                mask = df.apply(lambda row: any(
                    query.lower() in str(val).lower() for val in row if pd.notna(val)
                ), axis=1)
                results = df[mask]
            else:
                if field in df.columns:
                    mask = df[field].astype(str).str.lower().str.contains(query.lower(), na=False)
                    results = df[mask]
                else:
                    raise ValueError(f"Column '{field}' not found")
            
            # Apply sorting if requested
            if sort_by and sort_by in df.columns:
                ascending = sort_order == 'asc'
                if sort_by == 'Date' and 'Date_sort' in results.columns:
                    results = results.sort_values(by='Date_sort', ascending=ascending, na_position='last')
                else:
                    results = results.sort_values(by=sort_by, ascending=ascending, na_position='last')
            
            # Remove sorting column before returning
            if 'Date_sort' in results.columns:
                results = results.drop('Date_sort', axis=1)
            
            # Limit results
            results_dict = results.head(limit).to_dict('records')
            
            return {
                'results': results_dict,
                'count': len(results),
                'total': len(df),
                'truncated': len(results) > limit,
                'sorted_by': sort_by,
                'sort_order': sort_order
            }
            
        except Exception as e:
            raise Exception(f'Search failed: {str(e)}')