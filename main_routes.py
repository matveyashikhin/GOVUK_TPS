from flask import Blueprint
from base_template import BaseTemplate  # Changed from templates.base_template
import pandas as pd

class MainRoutes:
    """Handles main application routes"""
    
    def __init__(self, data_loader, analytics):
        self.data_loader = data_loader
        self.analytics = analytics
        self.base_template = BaseTemplate()
    
    def dashboard(self):
        """Dashboard route handler"""
        stats = self.data_loader.get_data_stats()
        
        content = f"""
        <div class="section-header">
            <h1><i class="fas fa-tachometer-alt me-3"></i>Dashboard Overview</h1>
            <p class="text-muted">Complete overview of your trademark database</p>
        </div>
        <div class="row">
            <div class="col-md-3">
                <div class="card stat-card stat-card-blue">
                    <div class="card-body text-center">
                        <i class="fas fa-table fa-3x mb-3"></i>
                        <h5>Total Records</h5>
                        <h2>{stats['total_records']:,}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card stat-card-green">
                    <div class="card-body text-center">
                        <i class="fas fa-font fa-3x mb-3"></i>
                        <h5>Unique Words</h5>
                        <h2>{stats['unique_words']:,}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card stat-card-purple">
                    <div class="card-body text-center">
                        <i class="fas fa-user fa-3x mb-3"></i>
                        <h5>Unique Owners</h5>
                        <h2>{stats['unique_owners']:,}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card stat-card-orange">
                    <div class="card-body text-center">
                        <i class="fas fa-link fa-3x mb-3"></i>
                        <h5>With Links</h5>
                        <h2>{stats['links_count']:,}</h2>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-rocket me-2"></i>Quick Actions</h5>
                        <div class="d-grid gap-2">
                            <a href="/search" class="btn btn-primary btn-lg"><i class="fas fa-search me-2"></i>Start Searching</a>
                            <a href="/analytics" class="btn btn-success btn-lg"><i class="fas fa-chart-bar me-2"></i>View Analytics</a>
                            <a href="/stocks" class="btn btn-warning btn-lg"><i class="fas fa-chart-line me-2"></i>Stock Analysis</a>
                            <a href="/export" class="btn btn-info btn-lg"><i class="fas fa-download me-2"></i>Export Data</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-info-circle me-2"></i>Database Info</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between"><span>Data Source:</span><span>GOV.UK</span></li>
                            <li class="list-group-item d-flex justify-content-between"><span>Records with Links:</span><span>{stats['links_count']:,}</span></li>
                            <li class="list-group-item d-flex justify-content-between"><span>File Format:</span><span>CSV</span></li>
                            <li class="list-group-item d-flex justify-content-between"><span>Status:</span><span class="text-success">Active</span></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return self.base_template.get_template().format(
            title="Dashboard", content=content, home_active="active",
            search_active="", analytics_active="", stocks_active="",
            export_active="", about_active="", extra_js=""
        )
    
    def search_page(self):
        """Search page route handler"""
        content = """
        <div class="section-header">
            <h1><i class="fas fa-search me-3"></i>Advanced Search</h1>
            <p class="text-muted">Search through trademark records with powerful filters</p>
        </div>
        <div class="card mb-4" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6">
                        <input type="text" id="search-input" class="form-control form-control-lg" placeholder="Enter search term...">
                    </div>
                    <div class="col-md-3">
                        <select id="field-select" class="form-select form-select-lg">
                            <option value="all">All Fields</option>
                            <option value="Word">Word</option>
                            <option value="Classes">Classes</option>
                            <option value="Owner">Owner</option>
                            <option value="Date">Date</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <button id="search-button" class="btn btn-primary btn-lg w-100">
                            <i class="fas fa-search me-2"></i>Search
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div id="results-summary" class="mb-3 d-none">
            <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                Found <strong><span id="results-count">0</span></strong> results
            </div>
        </div>
        <div id="loading" class="text-center py-5" style="display: none;">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
            <p class="mt-3">Searching...</p>
        </div>
        <div id="results-container" class="card d-none">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5><i class="fas fa-list me-2"></i>Results</h5>
                </div>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th class="sortable-header" data-column="Word">Word <i class="fas fa-sort sort-icon"></i></th>
                                <th class="sortable-header" data-column="Classes">Classes <i class="fas fa-sort sort-icon"></i></th>
                                <th class="sortable-header" data-column="Owner">Owner <i class="fas fa-sort sort-icon"></i></th>
                                <th class="sortable-header" data-column="Date">Date <i class="fas fa-sort sort-icon"></i></th>
                                <th>Link</th>
                            </tr>
                        </thead>
                        <tbody id="results-table"></tbody>
                    </table>
                </div>
            </div>
        </div>
        <div id="no-results" class="card d-none">
            <div class="card-body text-center py-5">
                <i class="fas fa-search fa-4x mb-4 text-muted"></i>
                <h3>No results found</h3>
                <p class="text-muted">Try different search terms</p>
            </div>
        </div>
        """
        
        # Include the search JavaScript
        search_js = self._get_search_javascript()
        
        return self.base_template.get_template().format(
            title="Search", content=content, home_active="",
            search_active="active", analytics_active="", stocks_active="",
            export_active="", about_active="", extra_js=search_js
        )
    
    def analytics_page(self):
        """Analytics page route handler with clickable owner links"""
        top_owners = self.analytics.get_top_owners(10)
        top_classes = self.analytics.get_top_classes(10)
        summary_stats = self.analytics.get_summary_stats()
        
        # Format the data for display WITH CLICKABLE LINKS
        owners_rows = ''
        if top_owners:
            for owner, count in top_owners.items():
                # URL encode the owner name for safe linking
                import urllib.parse
                encoded_owner = urllib.parse.quote(owner)
                owners_rows += f'''
                    <tr>
                        <td>
                            <a href="/owner/{encoded_owner}" class="trademark-link" title="View all trademarks for {owner}">
                                {owner}
                            </a>
                        </td>
                        <td><span class="badge bg-primary">{count}</span></td>
                    </tr>
                '''
        else:
            owners_rows = '<tr><td colspan="2">No data available</td></tr>'
        
        # Classes remain the same (no links needed)
        classes_rows = ''.join([f'<tr><td>{cls}</td><td>{count}</td></tr>' 
                            for cls, count in top_classes.items()]) if top_classes else '<tr><td colspan="2">No data available</td></tr>'
        
        content = f"""
        <div class="section-header">
            <h1><i class="fas fa-chart-bar me-3"></i>Data Analytics</h1>
            <p class="text-muted">Insights and trends from the trademark database</p>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-crown me-2"></i>Top Trademark Owners</h5>
                        <p class="text-muted small">Click on any owner name to view their trademarks</p>
                        <div class="table-responsive">
                            <table class="table table-sm table-hover">
                                <thead><tr><th>Owner</th><th>Count</th></tr></thead>
                                <tbody>{owners_rows}</tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-tags me-2"></i>Top Classes</h5>
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead><tr><th>Class</th><th>Count</th></tr></thead>
                                <tbody>{classes_rows}</tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title"><i class="fas fa-info-circle me-2"></i>Database Statistics</h5>
                        <div class="row text-center">
                            <div class="col-md-3">
                                <h3 class="text-primary">{summary_stats['total_records']:,}</h3>
                                <p class="text-muted">Total Records</p>
                            </div>
                            <div class="col-md-3">
                                <h3 class="text-success">{summary_stats['unique_words']:,}</h3>
                                <p class="text-muted">Unique Words</p>
                            </div>
                            <div class="col-md-3">
                                <h3 class="text-warning">{summary_stats['unique_owners']:,}</h3>
                                <p class="text-muted">Unique Owners</p>
                            </div>
                            <div class="col-md-3">
                                <h3 class="text-info">{summary_stats['unique_classes']:,}</h3>
                                <p class="text-muted">Unique Classes</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return self.base_template.get_template().format(
            title="Analytics", content=content, home_active="",
            search_active="", analytics_active="active", stocks_active="",
            export_active="", about_active="", extra_js=""
        )

    def owner_details_page(self, owner_name):
        """Show detailed trademark listing for a specific owner"""
        import urllib.parse
        
        # Decode the owner name from URL
        decoded_owner = urllib.parse.unquote(owner_name)
        
        # Get all trademarks for this owner
        owner_trademarks = self.data_loader.df[
            self.data_loader.df['Owner'].str.contains(decoded_owner, case=False, na=False, regex=False)
        ].copy()
        
        if owner_trademarks.empty:
            content = f"""
            <div class="section-header">
                <h1><i class="fas fa-user me-3"></i>No Trademarks Found</h1>
                <p class="text-muted">No trademarks found for "{decoded_owner}"</p>
            </div>
            <div class="text-center">
                <a href="/analytics" class="btn btn-primary">
                    <i class="fas fa-arrow-left me-2"></i>Back to Analytics
                </a>
            </div>
            """
        else:
            # Sort by date if available, otherwise by word
            if 'Date_sort' in owner_trademarks.columns:
                owner_trademarks = owner_trademarks.sort_values('Date_sort', ascending=False, na_position='last')
            else:
                owner_trademarks = owner_trademarks.sort_values('Word', na_position='last')
            
            # Remove the sorting column for display
            display_df = owner_trademarks.drop('Date_sort', axis=1) if 'Date_sort' in owner_trademarks.columns else owner_trademarks
            
            # Create table rows
            table_rows = ""
            for _, row in display_df.iterrows():
                link_cell = ""
                if pd.notna(row.get('Link')) and str(row['Link']).strip():
                    link_cell = f'<a href="{row["Link"]}" target="_blank" class="trademark-link"><i class="fas fa-external-link-alt me-1"></i>View</a>'
                else:
                    link_cell = '<span class="text-muted">-</span>'
                
                table_rows += f"""
                    <tr>
                        <td><strong>{row.get('Word', 'N/A')}</strong></td>
                        <td>{row.get('Classes', 'N/A')}</td>
                        <td>{row.get('Date', 'N/A')}</td>
                        <td>{link_cell}</td>
                    </tr>
                """
            
            content = f"""
            <div class="section-header">
                <h1><i class="fas fa-user me-3"></i>{decoded_owner}</h1>
                <p class="text-muted">{len(owner_trademarks)} trademark(s) found</p>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-6">
                    <a href="/analytics" class="btn btn-outline-primary">
                        <i class="fas fa-arrow-left me-2"></i>Back to Analytics
                    </a>
                </div>
                <div class="col-md-6 text-end">
                    <button onclick="exportOwnerData()" class="btn btn-outline-success">
                        <i class="fas fa-download me-2"></i>Export These Trademarks
                    </button>
                </div>
            </div>
            
            <div class="card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5><i class="fas fa-list me-2"></i>Trademarks</h5>
                        <span class="badge bg-info fs-6">{len(owner_trademarks)} total</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Trademark Word</th>
                                    <th>Classes</th>
                                    <th>Date</th>
                                    <th>Link</th>
                                </tr>
                            </thead>
                            <tbody>
                                {table_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            """
        
        # JavaScript for export functionality
        export_js = f"""
        <script>
            function exportOwnerData() {{
                const ownerName = "{decoded_owner}";
                const encodedOwner = encodeURIComponent(ownerName);
                window.open(`/api/export/owner/${{encodedOwner}}`, '_blank');
            }}
        </script>
        """
        
        return self.base_template.get_template().format(
            title=f"Trademarks - {decoded_owner}", content=content, 
            home_active="", search_active="", analytics_active="active", 
            stocks_active="", export_active="", about_active="", 
            extra_js=export_js
        )
    
    def export_page(self):
        """Export page route handler"""
        content = """
        <div class="section-header">
            <h1><i class="fas fa-download me-3"></i>Export Data</h1>
            <p class="text-muted">Download and export trademark data in various formats</p>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="fas fa-file-csv fa-4x text-success mb-3"></i>
                        <h5>Export as CSV</h5>
                        <p class="text-muted">Download the complete dataset as CSV file</p>
                        <a href="/api/export/csv" class="btn btn-success btn-lg">
                            <i class="fas fa-download me-2"></i>Download CSV
                        </a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="fas fa-file-excel fa-4x text-primary mb-3"></i>
                        <h5>Export as Excel</h5>
                        <p class="text-muted">Download as Excel file with formatting</p>
                        <a href="/api/export/excel" class="btn btn-primary btn-lg">
                            <i class="fas fa-download me-2"></i>Download Excel
                        </a>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return self.base_template.get_template().format(
            title="Export", content=content, home_active="",
            search_active="", analytics_active="", stocks_active="",
            export_active="active", about_active="", extra_js=""
        )
    
    def about_page(self):
        """About page route handler"""
        content = """
        <div class="section-header">
            <h1><i class="fas fa-info-circle me-3"></i>About</h1>
            <p class="text-muted">Information about this trademark database explorer</p>
        </div>
        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h5>Project Overview</h5>
                        <p>This Trademark Data Explorer is a comprehensive tool for searching and analyzing trademark data scraped from GOV.UK. The application provides powerful search capabilities, data analytics, stock market integration, and export functionality.</p>

                        <h5 class="mt-4">Features</h5>
                        <ul>
                            <li><strong>Advanced Search:</strong> Search across all fields or specific columns</li>
                            <li><strong>Real-time Analytics:</strong> View statistics and trends</li>
                            <li><strong>Enhanced Stock Market Integration:</strong> Match trademark owners to public companies with 500+ mappings</li>
                            <li><strong>Data Export:</strong> Download data in CSV or Excel format</li>
                            <li><strong>Class Guide:</strong> Built-in IPO class reference</li>
                            <li><strong>Direct Links:</strong> Access original trademark pages</li>
                            <li><strong>Responsive Design:</strong> Works on desktop and mobile devices</li>
                        </ul>

                        <h5 class="mt-4">Technology Stack</h5>
                        <ul>
                            <li><strong>Backend:</strong> Python Flask</li>
                            <li><strong>Data Processing:</strong> Pandas</li>
                            <li><strong>Stock Data:</strong> yfinance with comprehensive ticker database</li>
                            <li><strong>String Matching:</strong> FuzzyWuzzy with multiple algorithms</li>
                            <li><strong>Frontend:</strong> Bootstrap 5, JavaScript</li>
                            <li><strong>Architecture:</strong> Modular design with separate components</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5><i class="fas fa-database me-2"></i>Data Source</h5>
                        <p><strong>Source:</strong> GOV.UK Trademark Database</p>
                        <p><strong>Records:</strong> 159,000+</p>
                        <p><strong>Last Updated:</strong> June 2025</p>
                        <p><strong>Format:</strong> CSV with Links</p>
                    </div>
                </div>

                <div class="card mt-3">
                    <div class="card-body">
                        <h5><i class="fas fa-chart-line me-2"></i>Enhanced Stock Integration</h5>
                        <p><strong>Company Mappings:</strong> 500+ including subsidiaries</p>
                        <p><strong>Match Rate:</strong> Significantly improved with fuzzy logic</p>
                        <p><strong>Brand Recognition:</strong> Includes popular brands and their parent companies</p>
                    </div>
                </div>

                <div class="card mt-3">
                    <div class="card-body">
                        <h5><i class="fas fa-envelope me-2"></i>Contact</h5>
                        <p>For questions or support, please contact the development team.</p>
                        <p><strong>Version:</strong> 4.0 Modular</p>
                        <p><strong>Status:</strong> Active</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return self.base_template.get_template().format(
            title="About", content=content, home_active="",
            search_active="", analytics_active="", stocks_active="",
            export_active="", about_active="active", extra_js=""
        )
    
    def _get_search_javascript(self):
        """Get the search page JavaScript"""
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const searchInput = document.getElementById('search-input');
                const fieldSelect = document.getElementById('field-select');
                const searchButton = document.getElementById('search-button');
                const resultsTable = document.getElementById('results-table');
                const resultsContainer = document.getElementById('results-container');
                const resultsSummary = document.getElementById('results-summary');
                const resultsCount = document.getElementById('results-count');
                const loadingElement = document.getElementById('loading');
                const noResultsElement = document.getElementById('no-results');

                let currentResults = [];
                let currentSort = { column: null, direction: 'asc' };

                function performSearch() {
                    const query = searchInput.value.trim();
                    const field = fieldSelect.value;

                    if (!query) {
                        hideAllResults();
                        return;
                    }

                    showLoading();

                    const url = `/api/search?query=${encodeURIComponent(query)}&field=${field}` +
                               (currentSort.column ? `&sort_by=${currentSort.column}&sort_order=${currentSort.direction}` : '');

                    fetch(url)
                        .then(response => response.json())
                        .then(data => {
                            hideLoading();
                            currentResults = data.results || [];

                            if (data.results && data.results.length > 0) {
                                displayResults(data.results, query, field);
                                showResultsSummary(data.count);
                            } else {
                                showNoResults();
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            hideLoading();
                            showError();
                        });
                }

                function sortResults(column) {
                    if (currentSort.column === column) {
                        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
                    } else {
                        currentSort.column = column;
                        currentSort.direction = 'asc';
                    }
                    updateSortIcons();
                    if (currentResults.length > 0) {
                        performSearch();
                    }
                }

                function updateSortIcons() {
                    document.querySelectorAll('.sort-icon').forEach(icon => {
                        icon.className = 'fas fa-sort sort-icon';
                    });
                    if (currentSort.column) {
                        const activeHeader = document.querySelector(`[data-column="${currentSort.column}"] .sort-icon`);
                        if (activeHeader) {
                            activeHeader.className = `fas fa-sort-${currentSort.direction === 'asc' ? 'up' : 'down'} sort-icon active`;
                        }
                    }
                }

                function hideAllResults() {
                    resultsContainer.classList.add('d-none');
                    resultsSummary.classList.add('d-none');
                    noResultsElement.classList.add('d-none');
                }

                function showLoading() {
                    loadingElement.style.display = 'block';
                    hideAllResults();
                }

                function hideLoading() {
                    loadingElement.style.display = 'none';
                }

                function displayResults(results, query, field) {
                    resultsTable.innerHTML = '';
                    results.forEach((result, index) => {
                        const row = document.createElement('tr');

                        const highlightText = (text, searchTerm) => {
                            if (!text) return '';
                            text = String(text);
                            const regex = new RegExp(searchTerm, 'gi');
                            return text.replace(regex, match => `<span style="background: linear-gradient(135deg, #ffeaa7, #fab1a0); padding: 2px 4px; border-radius: 4px; font-weight: 600;">${match}</span>`);
                        };

                        const wordText = (field === 'Word' || field === 'all') ? highlightText(result.Word, query) : (result.Word || '');
                        const classesText = (field === 'Classes' || field === 'all') ? highlightText(result.Classes, query) : (result.Classes || '');
                        const ownerText = (field === 'Owner' || field === 'all') ? highlightText(result.Owner, query) : (result.Owner || '');
                        const dateText = (field === 'Date' || field === 'all') ? highlightText(result.Date, query) : (result.Date || '');

                        let linkText = '';
                        if (result.Link && result.Link.trim() !== '') {
                            linkText = `<a href="${result.Link}" target="_blank" class="trademark-link"><i class="fas fa-external-link-alt me-1"></i>View</a>`;
                        } else {
                            linkText = '<span class="text-muted">-</span>';
                        }

                        row.innerHTML = `
                            <td>${wordText}</td>
                            <td>${classesText}</td>
                            <td>${ownerText}</td>
                            <td>${dateText}</td>
                            <td>${linkText}</td>
                        `;
                        resultsTable.appendChild(row);
                    });
                    resultsContainer.classList.remove('d-none');
                }

                function showResultsSummary(count) {
                    resultsCount.textContent = count.toLocaleString();
                    resultsSummary.classList.remove('d-none');
                }

                function showNoResults() {
                    noResultsElement.classList.remove('d-none');
                }

                function showError() {
                    resultsTable.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading results</td></tr>';
                    resultsContainer.classList.remove('d-none');
                }

                searchButton.addEventListener('click', performSearch);
                searchInput.addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') {
                        performSearch();
                    }
                });

                document.querySelectorAll('.sortable-header').forEach(header => {
                    header.addEventListener('click', function() {
                        const column = this.getAttribute('data-column');
                        sortResults(column);
                    });
                });

                searchInput.focus();
            });
        </script>
        """