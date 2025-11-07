import sqlite3
import pandas as pd
from datetime import datetime

def generate_dashboard():
    """Generate comprehensive dashboard with extensive analysis and visualizations"""
    
    # Connect to database
    conn = sqlite3.connect('/tmp/movies.db')
    
    # Add timestamp for cache busting
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Get data
    hollywood_df = pd.read_sql_query("SELECT * FROM movie_roi_analytics", conn)
    indian_df = pd.read_sql_query("SELECT * FROM indian_movies_roi", conn)
    
    conn.close()
    
    # Convert to JSON for embedding
    hollywood_json = hollywood_df.to_json(orient='records')
    indian_json = indian_df.to_json(orient='records')
    
    # Calculate extensive statistics
    total_movies = len(hollywood_df) + len(indian_df)
    hollywood_count = len(hollywood_df)
    indian_count = len(indian_df)
    tamil_count = len(indian_df[indian_df['language'] == 'Tamil']) if len(indian_df) > 0 else 0
    
    # Hollywood stats
    hollywood_avg_roi = hollywood_df['roi'].mean() if len(hollywood_df) > 0 else 0
    hollywood_avg_rating = hollywood_df['vote_average'].mean() if len(hollywood_df) > 0 else 0
    hollywood_total_budget = hollywood_df['budget'].sum() / 83 if len(hollywood_df) > 0 else 0  # Convert to INR
    hollywood_total_revenue = hollywood_df['revenue'].sum() / 83 if len(hollywood_df) > 0 else 0
    hollywood_profitable = len(hollywood_df[hollywood_df['roi'] > 0]) if len(hollywood_df) > 0 else 0
    
    # Indian stats
    indian_avg_roi = indian_df['roi'].mean() if len(indian_df) > 0 else 0
    indian_avg_rating = indian_df['vote_average'].mean() if len(indian_df) > 0 else 0
    indian_total_budget = indian_df['budget'].sum() if len(indian_df) > 0 else 0
    indian_total_revenue = indian_df['revenue'].sum() if len(indian_df) > 0 else 0
    indian_profitable = len(indian_df[indian_df['roi'] > 0]) if len(indian_df) > 0 else 0
    
    # HTML with extensive visualizations
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Movie Profit Data Pipeline - Analytics Dashboard</title>
    <style>
        /* BASIC STYLING */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            border: 3px solid #2d7a2f;
        }}
        
        .header h1 {{
            font-size: 32px;
        }}
        
        .export-section {{
            background-color: #ffeb3b;
            padding: 20px;
            margin-bottom: 20px;
            border: 3px solid #ffc107;
        }}
        
        .export-section h2 {{
            color: #333;
            margin-bottom: 15px;
        }}
        
        .button {{
            background-color: #2196F3;
            color: white;
            padding: 15px 30px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            font-weight: bold;
            border: 3px solid #0d47a1;
        }}
        
        .button:hover {{
            background-color: #0d47a1;
        }}
        
        .button-green {{
            background-color: #4CAF50;
            border: 3px solid #2d7a2f;
        }}
        
        .button-green:hover {{
            background-color: #2d7a2f;
        }}
        
        .button-orange {{
            background-color: #ff9800;
            border: 3px solid #e65100;
        }}
        
        .button-orange:hover {{
            background-color: #e65100;
        }}
        
        .stats-container {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-box {{
            flex: 1;
            min-width: 200px;
            padding: 20px;
            text-align: center;
            border: 3px solid;
        }}
        
        .stat-box.blue {{
            background-color: #2196F3;
            border-color: #0d47a1;
            color: white;
        }}
        
        .stat-box.green {{
            background-color: #4CAF50;
            border-color: #2d7a2f;
            color: white;
        }}
        
        .stat-box.orange {{
            background-color: #ff9800;
            border-color: #e65100;
            color: white;
        }}
        
        .stat-box.red {{
            background-color: #f44336;
            border-color: #b71c1c;
            color: white;
        }}
        
        .stat-box.purple {{
            background-color: #9c27b0;
            border-color: #6a1b9a;
            color: white;
        }}
        
        .stat-number {{
            font-size: 48px;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            font-size: 14px;
            margin-top: 5px;
        }}
        
        .viz-section {{
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border: 3px solid #333;
        }}
        
        .viz-section h2 {{
            color: #333;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: 3px solid #2d7a2f;
        }}
        
        .viz-section h3 {{
            color: #333;
            margin: 20px 0 10px 0;
            padding: 8px;
            background-color: #2196F3;
            color: white;
            border: 3px solid #0d47a1;
        }}
        
        .bar-chart {{
            margin: 20px 0;
        }}
        
        .bar-item {{
            margin: 10px 0;
        }}
        
        .bar-label {{
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }}
        
        .bar-container {{
            background-color: #ddd;
            height: 40px;
            border: 2px solid #333;
            position: relative;
        }}
        
        .bar-fill {{
            height: 100%;
            text-align: right;
            padding-right: 10px;
            color: white;
            font-weight: bold;
            line-height: 40px;
        }}
        
        .bar-fill.green {{
            background-color: #4CAF50;
        }}
        
        .bar-fill.blue {{
            background-color: #2196F3;
        }}
        
        .bar-fill.orange {{
            background-color: #ff9800;
        }}
        
        .bar-fill.red {{
            background-color: #f44336;
        }}
        
        .bar-fill.purple {{
            background-color: #9c27b0;
        }}
        
        .bar-fill.yellow {{
            background-color: #ffc107;
            color: #333;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
        }}
        
        th {{
            background-color: #2196F3;
            color: white;
            padding: 12px;
            text-align: left;
            border: 2px solid #0d47a1;
        }}
        
        td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .positive {{
            color: green;
            font-weight: bold;
        }}
        
        .negative {{
            color: red;
            font-weight: bold;
        }}
        
        .section {{
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border: 3px solid #333;
        }}
        
        .section h2 {{
            color: white;
            padding: 10px;
            margin: -20px -20px 20px -20px;
            background-color: #2196F3;
            border-bottom: 3px solid #0d47a1;
        }}
        
        .analysis-box {{
            background-color: #e3f2fd;
            padding: 15px;
            margin: 10px 0;
            border: 3px solid #2196F3;
        }}
        
        .analysis-box h4 {{
            color: #0d47a1;
            margin-bottom: 10px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .info-card {{
            background-color: white;
            padding: 15px;
            border: 3px solid #2196F3;
        }}
        
        .info-card h4 {{
            color: #2196F3;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        
        .info-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
    </style>
</head>
<body>

<div class="header">
    <h1>🎬 MOVIES PROFIT DATA PIPELINE</h1>
    <p style="font-size: 18px; margin-top: 10px;"><strong>Real-time Movie ROI Analytics Dashboard</strong></p>
    <div style="margin-top: 15px; font-size: 14px; line-height: 1.6;">
        <p><strong>Jagadeesh S</strong> (1RUA24CSE7008) | <strong>Gandavaram Prudhvi Sai</strong> (1RUA24CSE7007) | <strong>Mukund S Ganig</strong> (1RVU23CSE290)</p>
        <p>B.Tech (Hons) Computer Science & Engineering | RV University, Bangalore</p>
    </div>
    <p style="font-size: 11px; margin-top: 10px; opacity: 0.8;">Last Updated: {current_time}</p>
</div>

<div class="export-section">
    <h2>📥 EXPORT DATA</h2>
    <button class="button button-green" onclick="exportCSV('hollywood')">Download Hollywood CSV</button>
    <button class="button button-green" onclick="exportCSV('indian')">Download Indian CSV</button>
    <button class="button button-orange" onclick="exportPowerBI()">Export for Power BI</button>
    <button class="button" onclick="exportJSON()">Download JSON</button>
</div>

<div class="stats-container">
    <div class="stat-box blue">
        <div>TOTAL MOVIES</div>
        <div class="stat-number">{total_movies}</div>
        <div class="stat-label">All Regions</div>
    </div>
    <div class="stat-box green">
        <div>HOLLYWOOD</div>
        <div class="stat-number">{hollywood_count}</div>
        <div class="stat-label">Now Playing</div>
    </div>
    <div class="stat-box orange">
        <div>INDIAN</div>
        <div class="stat-number">{indian_count}</div>
        <div class="stat-label">5 Languages</div>
    </div>
    <div class="stat-box red">
        <div>TAMIL</div>
        <div class="stat-number">{tamil_count}</div>
        <div class="stat-label">Regional</div>
    </div>
</div>

<!-- FINANCIAL OVERVIEW -->
<div class="viz-section">
    <h2>💰 FINANCIAL OVERVIEW</h2>
    <div class="info-grid">
        <div class="info-card">
            <h4>Hollywood Total Budget</h4>
            <div class="info-value">₹{hollywood_total_budget/10000000:.1f} Cr</div>
        </div>
        <div class="info-card">
            <h4>Hollywood Total Revenue</h4>
            <div class="info-value">₹{hollywood_total_revenue/10000000:.1f} Cr</div>
        </div>
        <div class="info-card">
            <h4>Indian Total Budget</h4>
            <div class="info-value">₹{indian_total_budget/10000000:.1f} Cr</div>
        </div>
        <div class="info-card">
            <h4>Indian Total Revenue</h4>
            <div class="info-value">₹{indian_total_revenue/10000000:.1f} Cr</div>
        </div>
    </div>
</div>

<!-- ROI COMPARISON -->
<div class="viz-section">
    <h2>📊 ROI COMPARISON ANALYSIS</h2>
    <div class="bar-chart">
        <div class="bar-item">
            <div class="bar-label">Hollywood Average ROI: {hollywood_avg_roi:.1f}%</div>
            <div class="bar-container">
                <div class="bar-fill green" style="width: {min(abs(hollywood_avg_roi), 100)}%">
                    {hollywood_avg_roi:.1f}%
                </div>
            </div>
        </div>
        <div class="bar-item">
            <div class="bar-label">Indian Average ROI: {indian_avg_roi:.1f}%</div>
            <div class="bar-container">
                <div class="bar-fill blue" style="width: {min(abs(indian_avg_roi), 100)}%">
                    {indian_avg_roi:.1f}%
                </div>
            </div>
        </div>
    </div>
    
    <h3>Profitability Analysis</h3>
    <div class="bar-chart">
        <div class="bar-item">
            <div class="bar-label">Hollywood Profitable Movies: {hollywood_profitable} of {hollywood_count}</div>
            <div class="bar-container">
                <div class="bar-fill green" style="width: {(hollywood_profitable/max(hollywood_count,1))*100}%">
                    {(hollywood_profitable/max(hollywood_count,1))*100:.0f}%
                </div>
            </div>
        </div>
        <div class="bar-item">
            <div class="bar-label">Indian Profitable Movies: {indian_profitable} of {indian_count}</div>
            <div class="bar-container">
                <div class="bar-fill blue" style="width: {(indian_profitable/max(indian_count,1))*100}%">
                    {(indian_profitable/max(indian_count,1))*100:.0f}%
                </div>
            </div>
        </div>
    </div>
</div>

<!-- RATING COMPARISON -->
<div class="viz-section">
    <h2>⭐ RATING ANALYSIS</h2>
    <div class="bar-chart">
        <div class="bar-item">
            <div class="bar-label">Hollywood Average Rating: {hollywood_avg_rating:.2f}/10</div>
            <div class="bar-container">
                <div class="bar-fill orange" style="width: {hollywood_avg_rating*10}%">
                    {hollywood_avg_rating:.2f}/10
                </div>
            </div>
        </div>
        <div class="bar-item">
            <div class="bar-label">Indian Average Rating: {indian_avg_rating:.2f}/10</div>
            <div class="bar-container">
                <div class="bar-fill orange" style="width: {indian_avg_rating*10}%">
                    {indian_avg_rating:.2f}/10
                </div>
            </div>
        </div>
    </div>
</div>

<!-- LANGUAGE BREAKDOWN -->
<div class="viz-section">
    <h2>🌍 MOVIES BY LANGUAGE</h2>
    <div class="bar-chart" id="languageChart"></div>
</div>

<!-- TOP PERFORMERS -->
<div class="viz-section">
    <h2>🏆 TOP 10 MOVIES BY ROI</h2>
    <div class="bar-chart" id="topMoviesChart"></div>
</div>

<!-- HIGHEST RATED -->
<div class="viz-section">
    <h2>⭐ TOP 10 HIGHEST RATED MOVIES</h2>
    <div class="bar-chart" id="topRatedChart"></div>
</div>

<!-- BIGGEST BUDGET -->
<div class="viz-section">
    <h2>💵 TOP 10 BIGGEST BUDGET MOVIES</h2>
    <div class="bar-chart" id="biggestBudgetChart"></div>
</div>

<!-- HIGHEST REVENUE -->
<div class="viz-section">
    <h2>💰 TOP 10 HIGHEST REVENUE MOVIES</h2>
    <div class="bar-chart" id="highestRevenueChart"></div>
</div>

<!-- LANGUAGE-WISE ROI -->
<div class="viz-section">
    <h2>📈 AVERAGE ROI BY LANGUAGE</h2>
    <div class="bar-chart" id="languageROIChart"></div>
</div>

<!-- LANGUAGE-WISE RATING -->
<div class="viz-section">
    <h2>⭐ AVERAGE RATING BY LANGUAGE</h2>
    <div class="bar-chart" id="languageRatingChart"></div>
</div>

<!-- RELEASE YEAR ANALYSIS -->
<div class="viz-section">
    <h2>📅 MOVIES BY RELEASE YEAR</h2>
    <div class="bar-chart" id="yearChart"></div>
</div>

<!-- KEY INSIGHTS -->
<div class="viz-section">
    <h2>💡 KEY INSIGHTS & ANALYSIS</h2>
    <div id="insightsSection"></div>
</div>

<!-- HOLLYWOOD TABLE -->
<div class="section">
    <h2>🎥 HOLLYWOOD MOVIES - DETAILED DATA</h2>
    <table id="hollywoodTable"></table>
</div>

<!-- INDIAN TABLE -->
<div class="section">
    <h2>🇮🇳 INDIAN MOVIES - DETAILED DATA</h2>
    <table id="indianTable"></table>
</div>

<script>
var hollywoodData = {hollywood_json};
var indianData = {indian_json};

var languageColors = {{
    'Hindi': 'orange',
    'Tamil': 'red',
    'Telugu': 'blue',
    'Kannada': 'green',
    'Malayalam': 'purple'
}};

// Language breakdown chart
function createLanguageChart() {{
    var languageCounts = {{}};
    indianData.forEach(function(movie) {{
        var lang = movie.language;
        languageCounts[lang] = (languageCounts[lang] || 0) + 1;
    }});
    
    var maxCount = Math.max(...Object.values(languageCounts));
    var html = '';
    
    for (var lang in languageCounts) {{
        var count = languageCounts[lang];
        var percentage = (count / maxCount) * 100;
        var color = languageColors[lang] || 'blue';
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + lang + ': ' + count + ' movies</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill ' + color + '" style="width: ' + percentage + '%">' + count + '</div>';
        html += '</div></div>';
    }}
    
    document.getElementById('languageChart').innerHTML = html;
}}

// Top 10 movies by ROI
function createTopMoviesChart() {{
    var allMovies = [];
    
    hollywoodData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            roi: movie.roi,
            type: 'Hollywood'
        }});
    }});
    
    indianData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            roi: movie.roi,
            type: movie.language
        }});
    }});
    
    allMovies.sort(function(a, b) {{ return b.roi - a.roi; }});
    var top10 = allMovies.slice(0, 10);
    
    var maxROI = Math.max(...top10.map(m => Math.abs(m.roi)));
    var html = '';
    
    top10.forEach(function(movie, index) {{
        var percentage = (Math.abs(movie.roi) / maxROI) * 100;
        var color = movie.roi >= 0 ? 'green' : 'red';
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + (index + 1) + '. ' + movie.title + ' (' + movie.type + ') - ROI: ' + movie.roi.toFixed(1) + '%</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill ' + color + '" style="width: ' + percentage + '%">' + movie.roi.toFixed(1) + '%</div>';
        html += '</div></div>';
    }});
    
    document.getElementById('topMoviesChart').innerHTML = html;
}}

// Top 10 highest rated
function createTopRatedChart() {{
    var allMovies = [];
    
    hollywoodData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            rating: movie.vote_average,
            type: 'Hollywood'
        }});
    }});
    
    indianData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            rating: movie.vote_average,
            type: movie.language
        }});
    }});
    
    allMovies.sort(function(a, b) {{ return b.rating - a.rating; }});
    var top10 = allMovies.slice(0, 10);
    
    var html = '';
    
    top10.forEach(function(movie, index) {{
        var percentage = (movie.rating / 10) * 100;
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + (index + 1) + '. ' + movie.title + ' (' + movie.type + ') - ⭐ ' + movie.rating.toFixed(1) + '/10</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill orange" style="width: ' + percentage + '%">' + movie.rating.toFixed(1) + '/10</div>';
        html += '</div></div>';
    }});
    
    document.getElementById('topRatedChart').innerHTML = html;
}}

// Biggest budget movies
function createBiggestBudgetChart() {{
    var allMovies = [];
    
    hollywoodData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            budget: movie.budget / 83,  // Convert USD to INR
            type: 'Hollywood'
        }});
    }});
    
    indianData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            budget: movie.budget,
            type: movie.language
        }});
    }});
    
    allMovies.sort(function(a, b) {{ return b.budget - a.budget; }});
    var top10 = allMovies.slice(0, 10);
    
    var maxBudget = top10[0].budget;
    var html = '';
    
    top10.forEach(function(movie, index) {{
        var percentage = (movie.budget / maxBudget) * 100;
        var budgetCr = (movie.budget / 10000000).toFixed(1);
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + (index + 1) + '. ' + movie.title + ' (' + movie.type + ') - ₹' + budgetCr + ' Cr</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill blue" style="width: ' + percentage + '%">₹' + budgetCr + ' Cr</div>';
        html += '</div></div>';
    }});
    
    document.getElementById('biggestBudgetChart').innerHTML = html;
}}

// Highest revenue movies
function createHighestRevenueChart() {{
    var allMovies = [];
    
    hollywoodData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            revenue: movie.revenue / 83,  // Convert USD to INR
            type: 'Hollywood'
        }});
    }});
    
    indianData.forEach(function(movie) {{
        allMovies.push({{
            title: movie.title,
            revenue: movie.revenue,
            type: movie.language
        }});
    }});
    
    allMovies.sort(function(a, b) {{ return b.revenue - a.revenue; }});
    var top10 = allMovies.slice(0, 10);
    
    var maxRevenue = top10[0].revenue;
    var html = '';
    
    top10.forEach(function(movie, index) {{
        var percentage = (movie.revenue / maxRevenue) * 100;
        var revenueCr = (movie.revenue / 10000000).toFixed(1);
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + (index + 1) + '. ' + movie.title + ' (' + movie.type + ') - ₹' + revenueCr + ' Cr</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill green" style="width: ' + percentage + '%">₹' + revenueCr + ' Cr</div>';
        html += '</div></div>';
    }});
    
    document.getElementById('highestRevenueChart').innerHTML = html;
}}

// Average ROI by language
function createLanguageROIChart() {{
    var languageROI = {{}};
    var languageCounts = {{}};
    
    indianData.forEach(function(movie) {{
        var lang = movie.language;
        if (!languageROI[lang]) {{
            languageROI[lang] = 0;
            languageCounts[lang] = 0;
        }}
        languageROI[lang] += movie.roi;
        languageCounts[lang]++;
    }});
    
    var avgROI = {{}};
    for (var lang in languageROI) {{
        avgROI[lang] = languageROI[lang] / languageCounts[lang];
    }}
    
    var maxROI = Math.max(...Object.values(avgROI).map(Math.abs));
    var html = '';
    
    for (var lang in avgROI) {{
        var roi = avgROI[lang];
        var percentage = (Math.abs(roi) / maxROI) * 100;
        var color = roi >= 0 ? 'green' : 'red';
        var langColor = languageColors[lang] || 'blue';
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + lang + ' Average ROI: ' + roi.toFixed(1) + '%</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill ' + color + '" style="width: ' + percentage + '%">' + roi.toFixed(1) + '%</div>';
        html += '</div></div>';
    }}
    
    document.getElementById('languageROIChart').innerHTML = html;
}}

// Average rating by language
function createLanguageRatingChart() {{
    var languageRating = {{}};
    var languageCounts = {{}};
    
    indianData.forEach(function(movie) {{
        var lang = movie.language;
        if (!languageRating[lang]) {{
            languageRating[lang] = 0;
            languageCounts[lang] = 0;
        }}
        languageRating[lang] += movie.vote_average;
        languageCounts[lang]++;
    }});
    
    var avgRating = {{}};
    for (var lang in languageRating) {{
        avgRating[lang] = languageRating[lang] / languageCounts[lang];
    }}
    
    var html = '';
    
    for (var lang in avgRating) {{
        var rating = avgRating[lang];
        var percentage = (rating / 10) * 100;
        var color = languageColors[lang] || 'blue';
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + lang + ' Average Rating: ' + rating.toFixed(2) + '/10</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill ' + color + '" style="width: ' + percentage + '%">' + rating.toFixed(2) + '/10</div>';
        html += '</div></div>';
    }}
    
    document.getElementById('languageRatingChart').innerHTML = html;
}}

// Movies by release year
function createYearChart() {{
    var yearCounts = {{}};
    
    hollywoodData.forEach(function(movie) {{
        if (movie.release_year) {{
            yearCounts[movie.release_year] = (yearCounts[movie.release_year] || 0) + 1;
        }}
    }});
    
    indianData.forEach(function(movie) {{
        if (movie.release_year) {{
            yearCounts[movie.release_year] = (yearCounts[movie.release_year] || 0) + 1;
        }}
    }});
    
    var years = Object.keys(yearCounts).sort();
    var maxCount = Math.max(...Object.values(yearCounts));
    var html = '';
    
    years.forEach(function(year) {{
        var count = yearCounts[year];
        var percentage = (count / maxCount) * 100;
        html += '<div class="bar-item">';
        html += '<div class="bar-label">' + year + ': ' + count + ' movies</div>';
        html += '<div class="bar-container">';
        html += '<div class="bar-fill blue" style="width: ' + percentage + '%">' + count + '</div>';
        html += '</div></div>';
    }});
    
    document.getElementById('yearChart').innerHTML = html;
}}

// Generate insights
function createInsights() {{
    var allMovies = hollywoodData.concat(indianData);
    
    var bestROI = allMovies.reduce((max, m) => m.roi > max.roi ? m : max, allMovies[0]);
    var worstROI = allMovies.reduce((min, m) => m.roi < min.roi ? m : min, allMovies[0]);
    var bestRated = allMovies.reduce((max, m) => m.vote_average > max.vote_average ? m : max, allMovies[0]);
    var highestBudget = allMovies.reduce((max, m) => m.budget > max.budget ? m : max, allMovies[0]);
    var highestRevenue = allMovies.reduce((max, m) => m.revenue > max.revenue ? m : max, allMovies[0]);
    
    var html = '';
    
    html += '<div class="analysis-box">';
    html += '<h4>🏆 Best Performing Movie (ROI)</h4>';
    html += '<p><strong>' + bestROI.title + '</strong> with ' + bestROI.roi.toFixed(1) + '% ROI</p>';
    html += '<p>Budget: ₹' + (bestROI.budget/10000000).toFixed(1) + ' Cr | Revenue: ₹' + (bestROI.revenue/10000000).toFixed(1) + ' Cr</p>';
    html += '</div>';
    
    html += '<div class="analysis-box">';
    html += '<h4>📉 Worst Performing Movie (ROI)</h4>';
    html += '<p><strong>' + worstROI.title + '</strong> with ' + worstROI.roi.toFixed(1) + '% ROI</p>';
    html += '<p>Budget: ₹' + (worstROI.budget/10000000).toFixed(1) + ' Cr | Revenue: ₹' + (worstROI.revenue/10000000).toFixed(1) + ' Cr</p>';
    html += '</div>';
    
    html += '<div class="analysis-box">';
    html += '<h4>⭐ Highest Rated Movie</h4>';
    html += '<p><strong>' + bestRated.title + '</strong> with ' + bestRated.vote_average.toFixed(1) + '/10 rating</p>';
    html += '<p>ROI: ' + bestRated.roi.toFixed(1) + '% | Revenue: ₹' + (bestRated.revenue/10000000).toFixed(1) + ' Cr</p>';
    html += '</div>';
    
    html += '<div class="analysis-box">';
    html += '<h4>💵 Biggest Budget Movie</h4>';
    html += '<p><strong>' + highestBudget.title + '</strong> with ₹' + (highestBudget.budget/10000000).toFixed(1) + ' Cr budget</p>';
    html += '<p>Revenue: ₹' + (highestBudget.revenue/10000000).toFixed(1) + ' Cr | ROI: ' + highestBudget.roi.toFixed(1) + '%</p>';
    html += '</div>';
    
    html += '<div class="analysis-box">';
    html += '<h4>💰 Highest Revenue Movie</h4>';
    html += '<p><strong>' + highestRevenue.title + '</strong> with ₹' + (highestRevenue.revenue/10000000).toFixed(1) + ' Cr revenue</p>';
    html += '<p>Budget: ₹' + (highestRevenue.budget/10000000).toFixed(1) + ' Cr | ROI: ' + highestRevenue.roi.toFixed(1) + '%</p>';
    html += '</div>';
    
    document.getElementById('insightsSection').innerHTML = html;
}}

// Create tables
function createHollywoodTable() {{
    var html = '<tr><th>Title</th><th>Year</th><th>Director</th><th>Genres</th><th>Runtime</th><th>Budget</th><th>Revenue</th><th>ROI %</th><th>Rating</th></tr>';
    
    hollywoodData.forEach(function(movie) {{
        var roiClass = movie.roi >= 0 ? 'positive' : 'negative';
        html += '<tr>';
        html += '<td>' + movie.title + '</td>';
        html += '<td>' + (movie.release_year || 'N/A') + '</td>';
        html += '<td>' + (movie.director || 'N/A') + '</td>';
        html += '<td>' + (movie.genres || 'N/A') + '</td>';
        html += '<td>' + (movie.runtime ? movie.runtime + ' min' : 'N/A') + '</td>';
        html += '<td>₹' + (movie.budget_inr / 10000000).toFixed(1) + ' Cr</td>';
        html += '<td>₹' + (movie.revenue_inr / 10000000).toFixed(1) + ' Cr</td>';
        html += '<td class="' + roiClass + '">' + movie.roi.toFixed(1) + '%</td>';
        html += '<td>⭐ ' + movie.vote_average.toFixed(1) + '</td>';
        html += '</tr>';
    }});
    
    document.getElementById('hollywoodTable').innerHTML = html;
}}

function createIndianTable() {{
    var html = '<tr><th>Title</th><th>Original Title</th><th>Language</th><th>Year</th><th>Director</th><th>Genres</th><th>Runtime</th><th>Budget</th><th>Revenue</th><th>ROI %</th><th>Rating</th></tr>';
    
    indianData.forEach(function(movie) {{
        var roiClass = movie.roi >= 0 ? 'positive' : 'negative';
        html += '<tr>';
        html += '<td>' + movie.title + '</td>';
        html += '<td>' + movie.original_title + '</td>';
        html += '<td>' + movie.language + '</td>';
        html += '<td>' + (movie.release_year || 'N/A') + '</td>';
        html += '<td>' + (movie.director || 'N/A') + '</td>';
        html += '<td>' + (movie.genres || 'N/A') + '</td>';
        html += '<td>' + (movie.runtime ? movie.runtime + ' min' : 'N/A') + '</td>';
        html += '<td>₹' + (movie.budget_inr / 10000000).toFixed(1) + ' Cr</td>';
        html += '<td>₹' + (movie.revenue_inr / 10000000).toFixed(1) + ' Cr</td>';
        html += '<td class="' + roiClass + '">' + movie.roi.toFixed(1) + '%</td>';
        html += '<td>⭐ ' + movie.vote_average.toFixed(1) + '</td>';
        html += '</tr>';
    }});
    
    document.getElementById('indianTable').innerHTML = html;
}}

// Export functions
function exportCSV(type) {{
    var data = type === 'hollywood' ? hollywoodData : indianData;
    var filename = type + '_movies.csv';
    
    if (data.length === 0) {{
        alert('No data available for ' + type);
        return;
    }}
    
    var csv = Object.keys(data[0]).join(',') + '\\n';
    
    data.forEach(function(row) {{
        var values = Object.values(row).map(function(val) {{
            return '"' + (val || '').toString().replace(/"/g, '""') + '"';
        }});
        csv += values.join(',') + '\\n';
    }});
    
    var blob = new Blob([csv], {{ type: 'text/csv' }});
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
}}

function exportPowerBI() {{
    alert('Downloading both CSV files for Power BI!\\n\\n1. Hollywood movies\\n2. Indian movies\\n\\nOpen Power BI Desktop and import both CSV files.');
    exportCSV('hollywood');
    setTimeout(function() {{ exportCSV('indian'); }}, 500);
}}

function exportJSON() {{
    var combined = {{
        generated_at: new Date().toISOString(),
        total_movies: hollywoodData.length + indianData.length,
        hollywood: hollywoodData,
        indian: indianData
    }};
    
    var json = JSON.stringify(combined, null, 2);
    var blob = new Blob([json], {{ type: 'application/json' }});
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'movie_analytics.json';
    a.click();
}}

// Initialize all charts and tables
createLanguageChart();
createTopMoviesChart();
createTopRatedChart();
createBiggestBudgetChart();
createHighestRevenueChart();
createLanguageROIChart();
createLanguageRatingChart();
createYearChart();
createInsights();
createHollywoodTable();
createIndianTable();
</script>

</body>
</html>"""
    
    # Write to file
    output_path = '/tmp/movie_dashboard.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Comprehensive dashboard generated: {output_path}")
    return output_path

if __name__ == '__main__':
    generate_dashboard()
