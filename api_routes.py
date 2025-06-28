from flask import Blueprint, request, jsonify, Response
import io
import re
import pandas as pd

api_bp = Blueprint('api', __name__, url_prefix='/api')

class APIRoutes:
    """Handles API endpoints"""
    
    def __init__(self, data_loader, stock_matcher):
        self.data_loader = data_loader
        self.stock_matcher = stock_matcher
    
    def search(self):
        """Search API endpoint"""
        query = request.args.get('query', '').strip()
        field = request.args.get('field', 'all')
        sort_by = request.args.get('sort_by', '')
        sort_order = request.args.get('sort_order', 'asc')
        
        try:
            result = self.data_loader.search_data(query, field, sort_by, sort_order)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def class_guide(self):
        """Class guide API endpoint"""
        try:
            classes_df = self.data_loader.classes_df
            classes_dict = classes_df.to_dict('records')
            
            return jsonify({
                'classes': classes_dict,
                'count': len(classes_dict),
                'status': 'success'
            })
        except Exception as e:
            print(f"Error in class_guide API: {str(e)}")
            return jsonify({
                'error': f'Failed to load class guide: {str(e)}',
                'classes': [],
                'count': 0,
                'status': 'error'
            }), 500
    
    def download_class_guide(self):
        """Download class guide as CSV"""
        try:
            classes_df = self.data_loader.classes_df
            output = io.StringIO()
            classes_df.to_csv(output, index=False, header=['Class Number', 'Description'])
            output.seek(0)
            
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=ipo_class_guide.csv'}
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def export_csv(self):
        """Export main data as CSV"""
        try:
            df = self.data_loader.df
            output = io.StringIO()
            
            # Remove sorting column if it exists
            export_df = df.drop('Date_sort', axis=1) if 'Date_sort' in df.columns else df
            export_df.to_csv(output, index=False)
            output.seek(0)
            
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=trademark_data.csv'}
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def export_excel(self):
        """Export main data as Excel"""
        try:
            import pandas as pd
            
            df = self.data_loader.df
            output = io.BytesIO()
            
            # Remove sorting column if it exists
            export_df = df.drop('Date_sort', axis=1) if 'Date_sort' in df.columns else df
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_df.to_excel(writer, sheet_name='Trademark Data', index=False)
            output.seek(0)
            
            return Response(
                output.getvalue(),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers={'Content-Disposition': 'attachment; filename=trademark_data.xlsx'}
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

    def export_owner_data(self, owner_name):
        """Export trademarks for a specific owner as CSV"""
        import urllib.parse
        
        try:
            # Decode the owner name
            decoded_owner = urllib.parse.unquote(owner_name)
            
            # Get trademarks for this owner
            owner_trademarks = self.data_loader.df[
                self.data_loader.df['Owner'].str.contains(decoded_owner, case=False, na=False, regex=False)
            ].copy()
            
            if owner_trademarks.empty:
                return jsonify({'error': 'No trademarks found for this owner'}), 404
            
            # Remove sorting column if present
            export_df = owner_trademarks.drop('Date_sort', axis=1) if 'Date_sort' in owner_trademarks.columns else owner_trademarks
            
            # Create CSV
            output = io.StringIO()
            export_df.to_csv(output, index=False)
            output.seek(0)
            
            # Safe filename
            safe_filename = re.sub(r'[^\w\s-]', '', decoded_owner).strip()[:50]
            filename = f"trademarks_{safe_filename}.csv"
            
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def analyze_stocks(self):
        """Stock analysis API endpoint"""
        limit = int(request.args.get('limit', 100))
        
        try:
            print(f"Starting stock analysis for top {limit} companies...")
            results_df = self.stock_matcher.analyze_trademark_companies(self.data_loader.df, limit)
            
            if results_df.empty:
                print("No results found")
                return jsonify({
                    'results': [], 
                    'summary': {
                        'total_companies': 0, 
                        'public_companies': 0, 
                        'total_trademarks': 0, 
                        'total_market_cap': '0', 
                        'top_sector': 'N/A'
                    }
                })
            
            print(f"Analysis complete. Results shape: {results_df.shape}")
            
            # Calculate summary statistics
            public_companies = results_df[results_df['ticker'].notna()]
            print(f"Found {len(public_companies)} public companies out of {len(results_df)} total")
            
            # Handle market cap calculation safely
            valid_market_caps = public_companies['market_cap'].dropna()
            total_market_cap = valid_market_caps.sum() if len(valid_market_caps) > 0 else 0
            
            if total_market_cap > 1e12:
                market_cap_str = f"{total_market_cap/1e12:.1f}T"
            elif total_market_cap > 1e9:
                market_cap_str = f"{total_market_cap/1e9:.1f}B"
            elif total_market_cap > 1e6:
                market_cap_str = f"{total_market_cap/1e6:.1f}M"
            else:
                market_cap_str = f"{total_market_cap:.0f}"
            
            # Handle top sector safely
            valid_sectors = public_companies['sector'].dropna()
            if len(valid_sectors) > 0:
                top_sector = valid_sectors.mode().iloc[0] if not valid_sectors.empty else "N/A"
            else:
                top_sector = "N/A"
            
            summary = {
                'total_companies': int(len(results_df)),
                'public_companies': int(len(public_companies)),
                'total_trademarks': int(results_df['trademark_count'].sum()),
                'total_market_cap': market_cap_str,
                'top_sector': top_sector
            }
            
            print(f"Summary: {summary}")
            
            # Convert DataFrame to dict, handling NaN values
            results_dict = results_df.fillna('').to_dict('records')
            
            return jsonify({
                'results': results_dict,
                'summary': summary
            })
            
        except Exception as e:
            print(f"Error in stock analysis: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500