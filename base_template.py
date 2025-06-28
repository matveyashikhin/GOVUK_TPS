class BaseTemplate:
    """Generates the base HTML template for the application"""
    
    @staticmethod
    def get_template():
        """Return the base HTML template with proper JavaScript escaping"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title} - Trademark Data Explorer</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
        .navbar {{ background: rgba(255,255,255,0.95) !important; backdrop-filter: blur(10px); }}
        .navbar-brand {{ font-weight: 800; color: #2c3e50 !important; }}
        .nav-link {{ color: #495057 !important; font-weight: 600; }}
        .nav-link:hover {{ color: #667eea !important; }}
        .nav-link.active {{ color: #667eea !important; background: rgba(102, 126, 234, 0.1); border-radius: 8px; }}
        .main-container {{ background: white; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin: 2rem auto; padding: 2rem; max-width: 1400px; }}
        .section-header {{ text-align: center; margin-bottom: 2rem; color: #2c3e50; }}
        .stat-card {{ border: none; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 1.5rem; transition: transform 0.3s ease; }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-card-blue {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        .stat-card-green {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }}
        .stat-card-purple {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }}
        .stat-card-orange {{ background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }}
        .class-guide-btn {{ background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); border: none; color: white; font-weight: 600; transition: all 0.3s ease; }}
        .class-guide-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px rgba(250, 112, 154, 0.4); color: white; }}
        .trademark-link {{ color: #667eea; text-decoration: none; font-weight: 600; }}
        .trademark-link:hover {{ color: #764ba2; text-decoration: underline; }}
        .sortable-header {{ cursor: pointer; user-select: none; transition: all 0.2s ease; position: relative; padding-right: 20px !important; }}
        .sortable-header:hover {{ background-color: #e9ecef !important; }}
        .sort-icon {{ position: absolute; right: 5px; top: 50%; transform: translateY(-50%); font-size: 0.8rem; opacity: 0.5; }}
        .sort-icon.active {{ opacity: 1; color: #667eea; }}
        .export-btn {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border: none; color: white; font-weight: 600; transition: all 0.3s ease; }}
        .export-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4); color: white; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .fade-in {{ animation: fadeIn 0.5s ease-out; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/"><i class="fas fa-database me-2"></i>Trademark Explorer</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link {home_active}" href="/"><i class="fas fa-home me-1"></i>Dashboard</a></li>
                    <li class="nav-item"><a class="nav-link {search_active}" href="/search"><i class="fas fa-search me-1"></i>Search</a></li>
                    <li class="nav-item"><a class="nav-link {analytics_active}" href="/analytics"><i class="fas fa-chart-bar me-1"></i>Analytics</a></li>
                    <li class="nav-item"><a class="nav-link {stocks_active}" href="/stocks"><i class="fas fa-chart-line me-1"></i>Stocks</a></li>
                    <li class="nav-item"><a class="nav-link {export_active}" href="/export"><i class="fas fa-download me-1"></i>Export</a></li>
                    <li class="nav-item"><a class="nav-link {about_active}" href="/about"><i class="fas fa-info-circle me-1"></i>About</a></li>
                    <li class="nav-item"><button class="nav-link btn btn-link class-guide-btn" data-bs-toggle="modal" data-bs-target="#classGuideModal"><i class="fas fa-book me-1"></i>Class Guide</button></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="main-container">{content}</div>
    </div>

    <!-- Class Guide Modal -->
    <div class="modal fade" id="classGuideModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <h5 class="modal-title"><i class="fas fa-book me-2"></i>IPO Class Guide</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <input type="text" id="classSearch" class="form-control mb-3" placeholder="Search by class number or description...">
                    <div id="classGuideContent" style="max-height: 400px; overflow-y: auto;"></div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <a href="/api/class-guide/download" class="btn btn-primary"><i class="fas fa-download me-1"></i>Download Guide</a>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, setting up class guide modal');
            
            const classGuideModal = document.getElementById('classGuideModal');
            const classSearch = document.getElementById('classSearch');
            const classGuideContent = document.getElementById('classGuideContent');
            let allClasses = [];

            if (classGuideModal) {{
                console.log('Class guide modal found');
                
                classGuideModal.addEventListener('show.bs.modal', function() {{
                    console.log('Modal opening, loading class guide');
                    if (allClasses.length === 0) {{
                        loadClassGuide();
                    }} else {{
                        console.log('Classes already loaded, displaying');
                        displayClasses(allClasses);
                    }}
                }});
            }} else {{
                console.error('Class guide modal not found!');
            }}

            if (classSearch) {{
                classSearch.addEventListener('input', function() {{
                    console.log('Search input changed:', this.value);
                    filterClasses(this.value.toLowerCase());
                }});
            }}

            function loadClassGuide() {{
                console.log('Fetching class guide from API...');
                classGuideContent.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p class="mt-2">Loading classes...</p></div>';
                
                fetch('/api/class-guide')
                    .then(response => {{
                        console.log('API response status:', response.status);
                        if (!response.ok) {{
                            throw new Error(`HTTP error! status: ${{response.status}}`);
                        }}
                        return response.json();
                    }})
                    .then(data => {{
                        console.log('API response data:', data);
                        
                        if (data.error) {{
                            throw new Error(data.error);
                        }}
                        
                        allClasses = data.classes || [];
                        console.log(`Loaded ${{allClasses.length}} classes`);
                        
                        if (allClasses.length === 0) {{
                            classGuideContent.innerHTML = '<div class="alert alert-warning">No class data available</div>';
                        }} else {{
                            displayClasses(allClasses);
                        }}
                    }})
                    .catch(error => {{
                        console.error('Error loading class guide:', error);
                        classGuideContent.innerHTML = `
                            <div class="alert alert-danger">
                                <strong>Error loading class guide:</strong><br>
                                ${{error.message}}
                            </div>
                        `;
                    }});
            }}

            function displayClasses(classes) {{
                console.log(`Displaying ${{classes.length}} classes`);
                
                if (!classes || classes.length === 0) {{
                    classGuideContent.innerHTML = '<div class="alert alert-info">No classes to display</div>';
                    return;
                }}
                
                let html = '';
                classes.forEach(cls => {{
                    html += `
                        <div style="border-bottom: 1px solid #eee; padding: 0.75rem;">
                            <div style="font-weight: bold; color: #667eea;">
                                Class ${{cls.Class || 'N/A'}}
                            </div>
                            <div style="color: #495057; margin-top: 0.25rem;">
                                ${{cls.Description || 'No description available'}}
                            </div>
                        </div>
                    `;
                }});
                
                classGuideContent.innerHTML = html;
            }}

            function filterClasses(searchTerm) {{
                console.log('Filtering classes with term:', searchTerm);
                
                if (!searchTerm) {{
                    displayClasses(allClasses);
                    return;
                }}
                
                const filtered = allClasses.filter(cls => {{
                    const classMatch = (cls.Class || '').toString().toLowerCase().includes(searchTerm);
                    const descMatch = (cls.Description || '').toLowerCase().includes(searchTerm);
                    return classMatch || descMatch;
                }});
                
                console.log(`Filtered to ${{filtered.length}} classes`);
                displayClasses(filtered);
            }}
        }});
    </script>
    {extra_js}
</body>
</html>"""