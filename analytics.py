import pandas as pd

class TrademarkAnalytics:
    """Handles analytics calculations for trademark data"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def get_top_owners(self, limit=10):
        """Get top trademark owners by count"""
        df = self.data_loader.df
        if 'Owner' not in df.columns:
            return {}
        return df['Owner'].value_counts().head(limit).to_dict()
    
    def get_top_classes(self, limit=10):
        """Get top classes by count"""
        df = self.data_loader.df
        if 'Classes' not in df.columns:
            return {}
        return df['Classes'].value_counts().head(limit).to_dict()
    
    def get_class_distribution(self):
        """Get distribution of trademark classes"""
        df = self.data_loader.df
        if 'Classes' not in df.columns:
            return {}
        
        # Handle multiple classes per record (comma-separated)
        all_classes = []
        for classes_str in df['Classes'].dropna():
            if isinstance(classes_str, str):
                # Split by comma and clean
                classes = [cls.strip() for cls in classes_str.split(',')]
                all_classes.extend(classes)
        
        return pd.Series(all_classes).value_counts().to_dict()
    
    def get_owner_distribution(self):
        """Get distribution of trademarks by owner"""
        df = self.data_loader.df
        if 'Owner' not in df.columns:
            return {}
        return df['Owner'].value_counts().to_dict()
    
    def get_temporal_trends(self):
        """Get temporal trends in trademark registrations"""
        df = self.data_loader.df
        if 'Date_sort' not in df.columns:
            return {}
        
        # Group by year
        df_with_dates = df.dropna(subset=['Date_sort'])
        df_with_dates['Year'] = df_with_dates['Date_sort'].dt.year
        yearly_counts = df_with_dates['Year'].value_counts().sort_index()
        
        return yearly_counts.to_dict()
    
    def get_summary_stats(self):
        """Get comprehensive summary statistics"""
        stats = self.data_loader.get_data_stats()
        
        # Add additional analytics
        df = self.data_loader.df
        
        # Average trademarks per owner
        if 'Owner' in df.columns:
            owner_counts = df['Owner'].value_counts()
            stats['avg_trademarks_per_owner'] = owner_counts.mean()
            stats['median_trademarks_per_owner'] = owner_counts.median()
        
        # Most active class
        if 'Classes' in df.columns:
            top_class = df['Classes'].value_counts().index[0] if len(df) > 0 else None
            stats['most_active_class'] = top_class
        
        # Date range
        if 'Date_sort' in df.columns:
            valid_dates = df['Date_sort'].dropna()
            if len(valid_dates) > 0:
                stats['earliest_date'] = valid_dates.min().strftime('%Y-%m-%d')
                stats['latest_date'] = valid_dates.max().strftime('%Y-%m-%d')
        
        return stats
    
    def search_analytics(self, query, field='all'):
        """Get analytics for search results"""
        search_results = self.data_loader.search_data(query, field, limit=10000)
        
        if not search_results['results']:
            return {
                'total_matches': 0,
                'top_owners': {},
                'top_classes': {},
                'match_percentage': 0
            }
        
        # Convert to DataFrame for analysis
        results_df = pd.DataFrame(search_results['results'])
        
        analytics = {
            'total_matches': len(results_df),
            'match_percentage': (len(results_df) / len(self.data_loader.df)) * 100,
            'top_owners': results_df['Owner'].value_counts().head(5).to_dict() if 'Owner' in results_df.columns else {},
            'top_classes': results_df['Classes'].value_counts().head(5).to_dict() if 'Classes' in results_df.columns else {}
        }
        
        return analytics