# Indian Regional Movies ROI Pipeline - Kannada, Tamil, Telugu, Hindi
import pandas as pd
import requests
import sqlite3
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def fetch_indian_movies():
    """Fetch popular Indian movies from multiple regions"""
    print("Fetching Indian movies (Hindi, Tamil, Kannada, Telugu, Malayalam)...")
    
    # TMDB Bearer token
    bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDA1ZDNhMzFkMjQ3NTQyM2EwMTRmMTNhODc5MDgyMCIsIm5iZiI6MTc1NTI5MTc3Mi4wODcwMDAxLCJzdWIiOiI2ODlmYTA3Yzg3M2U4ODhhMTJjZDAyNzIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.XUQhU6FIVch63DeLEx9Gg9LFnBj_XfZPJKOfIgIhc7w"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "accept": "application/json"
    }
    
    # Language codes for Indian cinema
    # hi = Hindi, ta = Tamil, kn = Kannada, te = Telugu, ml = Malayalam
    languages = {
        'hi': 'Hindi',
        'ta': 'Tamil', 
        'kn': 'Kannada',
        'te': 'Telugu',
        'ml': 'Malayalam'
    }
    
    all_movies = {}
    
    # Fetch popular movies for each language
    for lang_code, lang_name in languages.items():
        print(f"\n📽️  Fetching {lang_name} movies...")
        
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            'with_original_language': lang_code,
            'sort_by': 'popularity.desc',
            'page': 1,
            'vote_count.gte': 10  # At least 10 votes to ensure quality
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            movies = data.get('results', [])
            for movie in movies[:10]:  # Get top 10 from each language
                all_movies[movie['id']] = {
                    'id': movie['id'],
                    'language': lang_name,
                    'language_code': lang_code
                }
            
            print(f"  ✓ Found {len(movies[:10])} {lang_name} movies")
            
        except Exception as e:
            print(f"  ✗ Error fetching {lang_name} movies: {e}")
    
    print(f"\n✓ Total unique movies fetched: {len(all_movies)}")
    return all_movies


def process_indian_movies(ti):
    """Fetch details and calculate ROI for Indian movies"""
    print("Processing Indian movie details...")
    
    # Pull movie data from previous task
    movies_dict = ti.xcom_pull(task_ids='fetch_indian_movies_task')
    
    # TMDB Bearer token
    bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDA1ZDNhMzFkMjQ3NTQyM2EwMTRmMTNhODc5MDgyMCIsIm5iZiI6MTc1NTI5MTc3Mi4wODcwMDAxLCJzdWIiOiI2ODlmYTA3Yzg3M2U4ODhhMTJjZDAyNzIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.XUQhU6FIVch63DeLEx9Gg9LFnBj_XfZPJKOfIgIhc7w"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "accept": "application/json"
    }
    
    # Handle case where XCom data might be None
    if not movies_dict:
        print("⚠️  No movie data received from fetch task! Returning empty dataset.")
        return pd.DataFrame().to_json()
    
    movie_data_list = []
    
    for movie_id, movie_info in movies_dict.items():
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            response = requests.get(url, headers=headers)
            details = response.json()
            
            # Only include movies with valid budget and revenue
            if details.get('budget', 0) > 0 and details.get('revenue', 0) > 0:
                movie_data_list.append({
                    'id': details['id'],
                    'title': details['title'],
                    'original_title': details.get('original_title', details['title']),
                    'language': movie_info['language'],
                    'language_code': movie_info['language_code'],
                    'budget': details['budget'],
                    'revenue': details['revenue'],
                    'vote_average': details.get('vote_average', 0),
                    'release_date': details.get('release_date', 'Unknown'),
                    'popularity': details.get('popularity', 0)
                })
                print(f"  ✓ {movie_info['language']}: {details['title']}")
        
        except Exception as e:
            print(f"  ✗ Error processing movie {movie_id}: {e}")
            continue
    
    # Convert to DataFrame
    df = pd.DataFrame(movie_data_list)
    
    if len(df) > 0:
        # Calculate financial metrics
        df['profit'] = df['revenue'] - df['budget']
        df['roi'] = (df['profit'] / df['budget']) * 100
        df['profit_margin'] = (df['profit'] / df['revenue']) * 100
        
        # Format currency columns to crores (Indian standard)
        df['budget_crores'] = df['budget'] / 10000000  # Convert to crores
        df['revenue_crores'] = df['revenue'] / 10000000
        df['profit_crores'] = df['profit'] / 10000000
        
        print(f"\n✓ Processed {len(df)} movies with valid financial data")
        print(f"\nBy Language:")
        print(df.groupby('language')['title'].count().to_string())
        print(f"\nAverage ROI by Language:")
        print(df.groupby('language')['roi'].mean().round(2).to_string())
        
        return df.to_json()
    else:
        print("\n⚠️ No movies with valid financial data found")
        return pd.DataFrame().to_json()


def store_indian_movies(ti):
    """Store Indian movie data in separate database table"""
    print("Storing Indian movie data...")
    
    # Pull JSON data from previous task
    json_data = ti.xcom_pull(task_ids='process_indian_movies_task')
    
    # Handle case where no data is available
    if not json_data:
        print("⚠️  No processed data received! Skipping database storage.")
        return
    
    # Convert JSON back to DataFrame
    df = pd.read_json(json_data)
    
    if len(df) > 0:
        # Connect to SQLite database
        conn = sqlite3.connect("/tmp/movies.db")
        
        # Save to separate table for Indian movies
        df.to_sql('indian_movies_roi', conn, if_exists='replace', index=False)
        
        print(f"✓ Stored {len(df)} Indian movies")
        print(f"  Database: /tmp/movies.db")
        print(f"  Table: indian_movies_roi")
        print(f"\nBreakdown by Language:")
        print(df.groupby('language')['title'].count().to_string())
        
        conn.close()
    else:
        print("⚠️ No data to store")


# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
with DAG(
    dag_id='indian_movies_roi_pipeline',
    default_args=default_args,
    description='Indian Regional Cinema ROI Analytics - Hindi, Tamil, Kannada, Telugu, Malayalam',
    schedule_interval='@daily',
    catchup=False,
    tags=['indian-cinema', 'kannada', 'tamil', 'hindi', 'telugu', 'malayalam', 'roi'],
) as dag:
    
    # Task 1: Fetch Indian movies from multiple languages
    fetch_task = PythonOperator(
        task_id='fetch_indian_movies_task',
        python_callable=fetch_indian_movies,
    )
    
    # Task 2: Process and calculate ROI
    process_task = PythonOperator(
        task_id='process_indian_movies_task',
        python_callable=process_indian_movies,
    )
    
    # Task 3: Store in database
    store_task = PythonOperator(
        task_id='store_indian_movies_task',
        python_callable=store_indian_movies,
    )
    
    # Set dependencies
    fetch_task >> process_task >> store_task
