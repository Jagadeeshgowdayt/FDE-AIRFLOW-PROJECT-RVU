#!/bin/bash
cd ~/airflow_project
source venv/bin/activate
export AIRFLOW_HOME="/home/hi/airflow_project"
echo "Airflow environment activated!"
echo "AIRFLOW_HOME: $AIRFLOW_HOME"
