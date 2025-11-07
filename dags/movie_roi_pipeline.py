# import pandas, requests, sqlite3
# import DAG, PythonOperator, and datetime from airflow
import pandas as pd
import requests
import sqlite3
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


# define a python function named 'ingest_movie_ids'
# inside the function, print "Fetching 'now playing' movie IDs..."
# call the TMDB api url "https://api.themoviedb.org/3/movie/now_playing?api_key=YOUR_KEY"
# get the json response
# extract the 'id' from each movie in 'results' into a list called 'movie_ids'
# return the 'movie_ids' list
def ingest_movie_ids():
    """Fetch movie IDs from TMDB 'now playing' endpoint"""
    print("Fetching 'now playing' movie IDs...")
    
    # TMDB Bearer token (Authorization header)
    bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDA1ZDNhMzFkMjQ3NTQyM2EwMTRmMTNhODc5MDgyMCIsIm5iZiI6MTc1NTI5MTc3Mi4wODcwMDAxLCJzdWIiOiI2ODlmYTA3Yzg3M2U4ODhhMTJjZDAyNzIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.XUQhU6FIVch63DeLEx9Gg9LFnBj_XfZPJKOfIgIhc7w"
    
    url = "https://api.themoviedb.org/3/movie/now_playing"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Extract movie IDs from results
    movie_ids = [movie['id'] for movie in data.get('results', [])]
    
    print(f"✓ Fetched {len(movie_ids)} movie IDs")
    return movie_ids


# define a python function named 'get_details_and_transform' that takes 'ti' as an argument
# inside the function, pull the 'movie_ids' list from the 'ingest_task' using xcom
# create an empty list called 'movie_data_list'
# loop through each 'movie_id' in the 'movie_ids' list
# inside the loop, call the tmdb api url f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_KEY"
# get the json response and call it 'movie_details'
# if 'budget' > 0 and 'revenue' > 0 in 'movie_details':
#   append the id, title, budget, revenue, and vote_average to the 'movie_data_list'
#
# convert 'movie_data_list' to a pandas dataframe called 'df'
# create a new column 'profit' by subtracting 'budget' from 'revenue'
# create a new column 'roi' by calculating (profit / budget) * 100
# return the dataframe as json
def get_details_and_transform(ti):
    """Fetch movie details, clean data, and calculate ROI metrics"""
    print("Fetching movie details and transforming data...")
    
    # Pull movie_ids from previous task using XCom
    movie_ids = ti.xcom_pull(task_ids='ingest_task')
    
    # TMDB Bearer token (Authorization header)
    bearer_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDA1ZDNhMzFkMjQ3NTQyM2EwMTRmMTNhODc5MDgyMCIsIm5iZiI6MTc1NTI5MTc3Mi4wODcwMDAxLCJzdWIiOiI2ODlmYTA3Yzg3M2U4ODhhMTJjZDAyNzIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.XUQhU6FIVch63DeLEx9Gg9LFnBj_XfZPJKOfIgIhc7w"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "accept": "application/json"
    }
    
    # Create empty list to store movie data
    movie_data_list = []
    
    # Loop through each movie_id
    for movie_id in movie_ids:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            response = requests.get(url, headers=headers)
            movie_details = response.json()
            
            # Only include movies with valid budget and revenue
            if movie_details.get('budget', 0) > 0 and movie_details.get('revenue', 0) > 0:
                movie_data_list.append({
                    'id': movie_details['id'],
                    'title': movie_details['title'],
                    'budget': movie_details['budget'],
                    'revenue': movie_details['revenue'],
                    'vote_average': movie_details.get('vote_average', 0)
                })
                print(f"  ✓ Processed: {movie_details['title']}")
        except Exception as e:
            print(f"  ✗ Error processing movie {movie_id}: {e}")
            continue
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(movie_data_list)
    
    if len(df) > 0:
        # Create new column 'profit' by subtracting budget from revenue
        df['profit'] = df['revenue'] - df['budget']
        
        # Create new column 'roi' by calculating (profit / budget) * 100
        df['roi'] = (df['profit'] / df['budget']) * 100
        
        print(f"\n✓ Transformed {len(df)} movies with valid financial data")
        print(f"  Average ROI: {df['roi'].mean():.2f}%")
        
        # Return as JSON for XCom
        return df.to_json()
    else:
        print("\n⚠️ No movies with valid financial data found")
        return pd.DataFrame().to_json()


# define a python function named 'store_movie_data' that takes 'ti' as an argument
# inside the function, pull the json data from the 'process_and_transform_task' using xcom
# convert the json back to a pandas dataframe
# connect to a sqlite database at "/tmp/movies.db"
# save the dataframe to a sql table named 'movie_roi_analytics', replacing it if it exists
def store_movie_data(ti):
    """Store processed movie data in SQLite database"""
    print("Storing movie data in SQLite database...")
    
    # Pull JSON data from previous task using XCom
    json_data = ti.xcom_pull(task_ids='process_and_transform_task')
    
    # Convert JSON back to pandas DataFrame
    df = pd.read_json(json_data)
    
    if len(df) > 0:
        # Connect to SQLite database
        conn = sqlite3.connect("/tmp/movies.db")
        
        # Save DataFrame to SQL table, replacing if it exists
        df.to_sql('movie_roi_analytics', conn, if_exists='replace', index=False)
        
        print(f"✓ Stored {len(df)} movies in database")
        print(f"  Database: /tmp/movies.db")
        print(f"  Table: movie_roi_analytics")
        
        # Close connection
        conn.close()
    else:
        print("⚠️ No data to store")


# create an airflow DAG with dag_id 'tmdb_movie_roi_pipeline', start_date of today, and a '@daily' schedule
# create a PythonOperator for 'ingest_task' that calls 'ingest_movie_ids'
# create a PythonOperator for 'process_and_transform_task' that calls 'get_details_and_transform'
# create a PythonOperator for 'store_task' that calls 'store_movie_data'
#
# set the task dependencies: ingest_task >> process_and_transform_task >> store_task

# Default arguments for the DAG
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
    dag_id='tmdb_movie_roi_pipeline',
    default_args=default_args,
    description='TMDB Movie ROI Analytics Pipeline - Ingest, Transform, and Store',
    schedule_interval='@daily',
    catchup=False,
    tags=['tmdb', 'movies', 'roi', 'analytics'],
) as dag:
    
    # Create PythonOperator for ingest_task
    ingest_task = PythonOperator(
        task_id='ingest_task',
        python_callable=ingest_movie_ids,
    )
    
    # Create PythonOperator for process_and_transform_task
    process_and_transform_task = PythonOperator(
        task_id='process_and_transform_task',
        python_callable=get_details_and_transform,
    )
    
    # Create PythonOperator for store_task
    store_task = PythonOperator(
        task_id='store_task',
        python_callable=store_movie_data,
    )
    
    # Set task dependencies
    ingest_task >> process_and_transform_task >> store_task
