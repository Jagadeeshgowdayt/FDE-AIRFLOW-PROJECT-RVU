# Movies Profit Data Pipeline

**Real-time Movie ROI Analytics using Apache Airflow & TMDB API**

---

## 👥 Team Members

| Name | Roll Number | Program |
|------|-------------|---------|
| **Jagadeesh S** | 1RUA24CSE7008 | B.Tech (Hons) CSE |
| **Gandavaram Prudhvi Sai** | 1RUA24CSE7007 | B.Tech (Hons) CSE |
| **Mukund S Ganig** | 1RVU23CSE290 | B.Tech (Hons) CSE |

**Institution:** RV University, Bangalore

---

## 📋 Project Overview

An automated data pipeline built with **Apache Airflow** that fetches, processes, and analyzes movie financial data from **The Movie Database (TMDB) API**. The system provides real-time ROI analytics for Hollywood and Indian regional cinema (Hindi, Tamil, Kannada, Telugu, Malayalam).

### Key Features

- 🎬 **Automated Data Ingestion**: Scheduled DAGs fetch latest movie data
- 💰 **ROI Analysis**: Calculate profit margins and return on investment
- 📊 **Interactive Dashboard**: Visualize trends with 12+ charts
- 🌍 **Multi-language Support**: Analyze Indian regional cinema
- 📤 **Export Capabilities**: CSV, JSON, and Power BI formats
- ⚡ **Real-time Updates**: Live data refresh from TMDB API

---

## 🏗️ Architecture

```
TMDB API → Airflow DAGs → SQLite → Dashboard
    ↓           ↓            ↓         ↓
  Fetch    Transform    Store    Visualize
```

### Components

1. **Data Source**: TMDB API (Bearer Token Authentication)
2. **Orchestration**: Apache Airflow 2.10.3
3. **Storage**: SQLite Database
4. **Visualization**: HTML/CSS/JavaScript Dashboard
5. **Environment**: WSL2 (Ubuntu) on Windows

---

## 📁 Project Structure

```
FDE-AIRFLOW-PROJECT-RVU/
├── dags/
│   ├── movie_roi_pipeline.py          # Hollywood movies pipeline
│   ├── indian_movies_pipeline.py      # Indian regional cinema pipeline
│   └── movie_dashboard.py             # Dashboard generator
├── scripts/
│   ├── check-pipeline.bat             # Pipeline helper commands
│   ├── start-airflow.bat              # Airflow startup script
│   └── access-database.bat            # Database access utility
├── setup/
│   ├── activate_airflow.sh            # Environment activation
│   └── airflow_setup.sh               # Initial setup script
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Windows 10/11** with WSL2 (Ubuntu)
- **Python 3.10+**
- **TMDB API Key** (Bearer Token)

### Step 1: Clone Repository

```bash
git clone https://github.com/Jagadeeshgowdayt/FDE-AIRFLOW-PROJECT-RVU.git
cd FDE-AIRFLOW-PROJECT-RVU
```

### Step 2: Setup Airflow (WSL)

```bash
# Create project directory
mkdir -p ~/airflow_project
cd ~/airflow_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Airflow
pip install apache-airflow==2.10.3 pandas requests

# Set Airflow home
export AIRFLOW_HOME=~/airflow_project

# Initialize database
airflow db init
```

### Step 3: Copy DAG Files

```bash
# Copy pipeline files to dags folder
cp dags/*.py ~/airflow_project/dags/
```

### Step 4: Configure TMDB API

Edit the DAG files and add your TMDB Bearer Token:

```python
bearer_token = "YOUR_TMDB_BEARER_TOKEN_HERE"
```

### Step 5: Start Airflow

```bash
# Start scheduler
airflow scheduler &

# Start webserver
airflow webserver --port 8080 &
```

Access UI: http://localhost:8080

---

## 💻 Usage

### Start Airflow (Windows PowerShell)

```powershell
# Start Airflow services
wsl bash -ic "cd ~/airflow_project && source activate_airflow.sh && nohup airflow scheduler > /tmp/airflow-scheduler.log 2>&1 &"
wsl bash -ic "cd ~/airflow_project && source activate_airflow.sh && nohup airflow webserver --port 8080 > /tmp/airflow-webserver.log 2>&1 &"

# Open Airflow UI
start "http://localhost:8080"
```

### Trigger Pipelines

```powershell
# Hollywood movies
wsl bash -ic "cd ~/airflow_project && source activate_airflow.sh && airflow dags trigger tmdb_movie_roi_pipeline"

# Indian regional cinema
wsl bash -ic "cd ~/airflow_project && source activate_airflow.sh && airflow dags trigger indian_movies_roi_pipeline"
```

### Generate Dashboard

```powershell
# Generate and open dashboard
wsl bash -ic "cd ~/airflow_project && source activate_airflow.sh && python dags/movie_dashboard.py"
wsl bash -ic "cp /tmp/movie_dashboard.html /mnt/c/Users/YOUR_USERNAME/Downloads/movie_dashboard.html"
start movie_dashboard.html
```

---

## 📊 Pipeline Details

### 1. Hollywood Movies Pipeline (`tmdb_movie_roi_pipeline`)

**Schedule**: Daily  
**Tasks**:
1. Fetch "now playing" movies from TMDB
2. Get detailed financial data (budget, revenue, ratings)
3. Calculate ROI and profit margins
4. Store in `movie_roi_analytics` table

**Metrics**:
- Budget & Revenue (USD → INR)
- ROI Percentage
- Profit Margin
- Rating & Popularity

### 2. Indian Regional Cinema Pipeline (`indian_movies_roi_pipeline`)

**Schedule**: Daily  
**Languages**: Hindi, Tamil, Kannada, Telugu, Malayalam  
**Tasks**:
1. Fetch latest releases by language
2. Get financial data + director info
3. Calculate ROI in Indian Crores (₹)
4. Store in `indian_movies_roi` table

**Special Features**:
- Broader date range for Tamil movies
- Popularity-based sorting
- Enhanced metadata (genres, runtime, directors)

---

## 📈 Dashboard Features

### Visualizations (12 Charts)

1. **ROI Comparison** - Hollywood vs Indian
2. **Profitability Analysis** - Success rate percentages
3. **Rating Analysis** - Average ratings by region
4. **Language Distribution** - Movie counts
5. **Top 10 ROI** - Best performing movies
6. **Top 10 Rated** - Highest rated films
7. **Top 10 Budget** - Biggest productions
8. **Top 10 Revenue** - Highest earners
9. **ROI by Language** - Regional performance
10. **Rating by Language** - Quality metrics
11. **Release Year Timeline** - Distribution
12. **Key Insights** - Automated analysis

### Export Options

- **CSV**: Hollywood & Indian movies separately
- **JSON**: Combined dataset with metadata
- **Power BI**: Direct import ready

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| **Orchestration** | Apache Airflow 2.10.3 |
| **Language** | Python 3.10 |
| **API** | TMDB REST API |
| **Database** | SQLite |
| **Data Processing** | Pandas |
| **Visualization** | HTML/CSS/JavaScript |
| **Environment** | WSL2 Ubuntu |

---

## 📊 Database Schema

### Table: `movie_roi_analytics` (Hollywood)

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | TMDB Movie ID |
| title | TEXT | Movie title |
| budget | INTEGER | Budget (USD) |
| revenue | INTEGER | Revenue (USD) |
| vote_average | REAL | Rating (0-10) |
| profit | INTEGER | Revenue - Budget |
| roi | REAL | ROI Percentage |

### Table: `indian_movies_roi` (Indian Regional)

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | TMDB Movie ID |
| title | TEXT | English title |
| original_title | TEXT | Original language title |
| language | TEXT | Language name |
| release_year | INTEGER | Year |
| director | TEXT | Director name |
| genres | TEXT | Genre list |
| runtime | INTEGER | Duration (minutes) |
| budget | INTEGER | Budget |
| revenue | INTEGER | Revenue |
| roi | REAL | ROI % |
| budget_crores | REAL | Budget (₹ Crores) |
| revenue_crores | REAL | Revenue (₹ Crores) |

---

## 🧪 Testing

### Check DAG Status

```bash
airflow dags list
airflow dags list-runs -d tmdb_movie_roi_pipeline
```

### Test Individual Tasks

```bash
airflow tasks test tmdb_movie_roi_pipeline ingest_movie_ids 2025-01-01
```

### Query Database

```bash
sqlite3 /tmp/movies.db "SELECT COUNT(*) FROM movie_roi_analytics;"
sqlite3 /tmp/movies.db "SELECT * FROM indian_movies_roi WHERE language='Tamil';"
```

---

## 🎓 Learning Outcomes

- Hands-on experience with **Apache Airflow** DAG design
- Real-world **ETL pipeline** development
- **API integration** and authentication
- **Data transformation** with Pandas
- **Database design** and querying
- **Dashboard development** for data visualization
- **Version control** with Git/GitHub

---

## 📝 Future Enhancements

- [ ] Add more data sources (IMDb, Box Office Mojo)
- [ ] Implement ML models for ROI prediction
- [ ] Add email/Slack notifications
- [ ] Deploy to cloud (AWS/GCP)
- [ ] Add user authentication
- [ ] Expand to more languages/regions
- [ ] Implement data quality checks
- [ ] Add streaming analytics

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for educational purposes as part of the **Foundations of Data Engineering** course at RV University.

---

## 📧 Contact

For questions or feedback, reach out to the team members via their university emails.

---

## 🙏 Acknowledgments

- **RV University** - For providing the learning environment
- **TMDB** - For the comprehensive movie database API
- **Apache Airflow Community** - For excellent documentation
- **Course Instructor** - For guidance and support

---

**⭐ Star this repository if you found it helpful!**

---

*Last Updated: November 2025*
