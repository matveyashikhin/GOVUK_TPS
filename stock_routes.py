from flask import Blueprint
from base_template import BaseTemplate  # Changed from templates.base_template

class StockRoutes:
    """Handles stock-related routes"""
    
    def __init__(self, data_loader, stock_matcher):
        self.data_loader = data_loader
        self.stock_matcher = stock_matcher
        self.base_template = BaseTemplate()
    
    def stocks_page(self):
        """Stock analysis page route handler"""
        content = """
        <div class="section-header">
            <h1><i class="fas fa-chart-line me-3"></i>Stock Market Analysis</h1>
            <p class="text-muted">Discover which trademark owners are publicly traded companies</p>
        </div>

        <div class="row mb-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h5><i class="fas fa-cog me-2"></i>Analysis Settings</h5>
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label>Number of top companies to analyze:</label>
                                <select id="company-limit" class="form-select">
                                    <option value="100">Top 100</option>
                                    <option value="250">Top 250</option>
                                    <option value="500" selected>Top 500</option>
                                    <option value="1000">Top 1000</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label>&nbsp;</label>
                                <button id="analyze-button" class="btn btn-primary w-100">
                                    <i class="fas fa-search me-2"></i>Analyze Companies
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="fas fa-shield-alt fa-3x text-success mb-3"></i>
                        <h6>Improved Accuracy</h6>
                        <p class="small text-muted">Enhanced matching with blacklist filtering to prevent false positives like entertainment companies.</p>
                    </div>
                </div>
            </div>
        </div>

        <div id="loading-stocks" class="text-center py-5" style="display: none;">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
            <p class="mt-3">Analyzing companies and fetching stock data...</p>
            <p class="text-muted">This may take a few minutes</p>
        </div>

        <div id="stock-results" class="d-none">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5><i class="fas fa-building me-2"></i>Public Companies Found</h5>
                        <div class="btn-group">
                            <button id="show-public" class="btn btn-outline-success active">Public Only</button>
                            <button id="show-all" class="btn btn-outline-secondary">All Companies</button>
                        </div>
                    </div>
                    <div id="stock-summary" class="row mb-3"></div>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Trademark Owner</th>
                                    <th>Trademarks</th>
                                    <th>Ticker</th>
                                    <th>Stock Price</th>
                                    <th>Market Cap</th>
                                    <th>Sector</th>
                                    <th>Match Quality</th>
                                </tr>
                            </thead>
                            <tbody id="stock-table"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Include the stock analysis JavaScript
        stocks_js = self._get_stocks_javascript()
        
        return self.base_template.get_template().format(
            title="Stock Analysis", content=content, home_active="",
            search_active="", analytics_active="", stocks_active="active",
            export_active="", about_active="", extra_js=stocks_js
        )
    
    def _get_stocks_javascript(self):
        """Get the stock analysis JavaScript"""
        return """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const analyzeButton = document.getElementById('analyze-button');
                const companyLimit = document.getElementById('company-limit');
                const loadingElement = document.getElementById('loading-stocks');
                const resultsElement = document.getElementById('stock-results');
                const stockTable = document.getElementById('stock-table');
                const stockSummary = document.getElementById('stock-summary');
                const showPublicBtn = document.getElementById('show-public');
                const showAllBtn = document.getElementById('show-all');

                let allResults = [];

                analyzeButton.addEventListener('click', function() {
                    const limit = companyLimit.value;
                    analyzeStocks(limit);
                });

                showPublicBtn.addEventListener('click', function() {
                    showPublicBtn.classList.add('active');
                    showAllBtn.classList.remove('active');
                    displayResults(allResults.filter(r => r.ticker));
                });

                showAllBtn.addEventListener('click', function() {
                    showAllBtn.classList.add('active');
                    showPublicBtn.classList.remove('active');
                    displayResults(allResults);
                });

                function analyzeStocks(limit) {
                    loadingElement.style.display = 'block';
                    resultsElement.classList.add('d-none');
                    analyzeButton.disabled = true;
                    analyzeButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';

                    fetch(`/api/analyze-stocks?limit=${limit}`)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status}`);
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log('API Response:', data);
                            loadingElement.style.display = 'none';
                            analyzeButton.disabled = false;
                            analyzeButton.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Companies';

                            if (data.error) {
                                alert('Error: ' + data.error);
                                return;
                            }

                            if (data.results && data.results.length > 0) {
                                allResults = data.results;
                                displaySummary(data.summary);
                                displayResults(allResults.filter(r => r.ticker));
                                resultsElement.classList.remove('d-none');
                            } else {
                                alert('No results found. Check the console for errors.');
                            }
                        })
                        .catch(error => {
                            console.error('Fetch Error:', error);
                            loadingElement.style.display = 'none';
                            analyzeButton.disabled = false;
                            analyzeButton.innerHTML = '<i class="fas fa-search me-2"></i>Analyze Companies';
                            alert('Error analyzing stocks: ' + error.message);
                        });
                }

                function displaySummary(summary) {
                    stockSummary.innerHTML = `
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4 class="text-success">${summary.public_companies}</h4>
                                <small class="text-muted">Public Companies</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4 class="text-primary">${summary.total_trademarks}</h4>
                                <small class="text-muted">Total Trademarks</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4 class="text-info">$${summary.total_market_cap}</h4>
                                <small class="text-muted">Combined Market Cap</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="text-center">
                                <h4 class="text-warning">${summary.top_sector}</h4>
                                <small class="text-muted">Top Sector</small>
                            </div>
                        </div>
                    `;
                }

                function displayResults(results) {
                    stockTable.innerHTML = '';

                    if (!results || results.length === 0) {
                        stockTable.innerHTML = '<tr><td colspan="7" class="text-center">No results to display</td></tr>';
                        return;
                    }

                    results.forEach(result => {
                        const row = document.createElement('tr');

                        const trademarkOwner = result.trademark_owner || 'N/A';
                        const trademarkCount = result.trademark_count || 0;
                        const ticker = result.ticker || null;
                        const currentPrice = result.current_price || null;
                        const marketCap = result.market_cap || null;
                        const sector = result.sector || null;
                        const matchConfidence = result.match_confidence || 'No Match';

                        const marketCapFormatted = marketCap ?
                            `$${(marketCap / 1e9).toFixed(1)}B` : '-';
                        const priceFormatted = currentPrice ?
                            `${parseFloat(currentPrice).toFixed(2)}` : '-';

                        const matchBadge = matchConfidence === 'Exact' ?
                            '<span class="badge bg-success">Exact</span>' :
                            matchConfidence === 'High' ?
                            '<span class="badge bg-success">High</span>' :
                            matchConfidence === 'Medium' ?
                            '<span class="badge bg-warning">Medium</span>' :
                            '<span class="badge bg-secondary">No Match</span>';

                        row.innerHTML = `
                            <td>${trademarkOwner}</td>
                            <td><span class="badge bg-primary">${trademarkCount}</span></td>
                            <td>${ticker ? `<strong>${ticker}</strong>` : '-'}</td>
                            <td>${priceFormatted}</td>
                            <td>${marketCapFormatted}</td>
                            <td>${sector || '-'}</td>
                            <td>${matchBadge}</td>
                        `;

                        stockTable.appendChild(row);
                    });
                }
            });
        </script>
        """