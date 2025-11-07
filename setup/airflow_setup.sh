#!/bin/bash

# Airflow Setup Script for WSL
# This script will set up Apache Airflow in your WSL environment

echo "=========================================="
echo "Apache Airflow Setup Script"
echo "=========================================="
echo ""

# Step 1: Update Ubuntu and install Python tools
echo "Step 1: Updating Ubuntu and installing Python tools..."
sudo apt update && sudo apt install python3-pip python3-venv -y

if [ $? -ne 0 ]; then
    echo "Error: Failed to update or install packages"
    exit 1
fi

echo "✓ Ubuntu updated and Python tools installed"
echo ""

# Step 2: Create Airflow project directory
echo "Step 2: Creating Airflow project directory..."
mkdir -p ~/airflow_project
cd ~/airflow_project

echo "✓ Created ~/airflow_project"
echo ""

# Step 3: Create and activate virtual environment
echo "Step 3: Creating Python virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
source venv/bin/activate

# Set AIRFLOW_HOME (use absolute path for compatibility)
export AIRFLOW_HOME="/home/hi/airflow_project"
echo "✓ Set AIRFLOW_HOME to: $AIRFLOW_HOME"
echo ""

# Step 4: Install Airflow and dependencies
echo "Step 4: Installing Apache Airflow and dependencies..."
echo "This may take several minutes..."
pip install --upgrade pip
# Install stable version 2.10.3 to avoid compatibility issues
pip install "apache-airflow[celery,postgres,redis]==2.10.3" pandas wbgapi

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Airflow"
    exit 1
fi

echo "✓ Airflow and dependencies installed"
echo ""

# Step 5: Initialize Airflow database
echo "Step 5: Initializing Airflow database..."
airflow db init

if [ $? -ne 0 ]; then
    echo "Error: Failed to initialize Airflow database"
    exit 1
fi

echo "✓ Airflow database initialized"
echo ""

# Step 6: Create admin user
echo "Step 6: Creating Airflow admin user..."
echo "Username: admin"
echo "Password: admin"
echo "Note: You should change this password after first login!"

airflow users create \
    --username admin \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email admin@example.com \
    --password admin

if [ $? -ne 0 ]; then
    echo "Error: Failed to create admin user"
    exit 1
fi

echo "✓ Admin user created"
echo ""

# Create activation script for future sessions
echo "Creating activation script for future sessions..."
cat > ~/airflow_project/activate_airflow.sh << 'EOF'
#!/bin/bash
cd ~/airflow_project
source venv/bin/activate
export AIRFLOW_HOME="/home/hi/airflow_project"
echo "Airflow environment activated!"
echo "AIRFLOW_HOME: $AIRFLOW_HOME"
EOF

chmod +x ~/airflow_project/activate_airflow.sh

echo "✓ Created activation script: ~/airflow_project/activate_airflow.sh"
echo ""

echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. To start Airflow in the FUTURE, you need TWO terminals:"
echo ""
echo "   Terminal 1 - Webserver:"
echo "   $ cd ~/airflow_project"
echo "   $ source activate_airflow.sh"
echo "   $ airflow webserver -p 8080"
echo ""
echo "   Terminal 2 - Scheduler:"
echo "   $ cd ~/airflow_project"
echo "   $ source activate_airflow.sh"
echo "   $ airflow scheduler"
echo ""
echo "2. Access Airflow UI at: http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "=========================================="
echo ""
echo "Would you like to start Airflow now? (y/n)"
read -p "Start Airflow webserver and scheduler? " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "Starting Airflow webserver on port 8080..."
    echo "The scheduler will need to be started in a separate terminal."
    echo ""
    echo "Run this in a NEW WSL terminal:"
    echo "  cd ~/airflow_project && source activate_airflow.sh && airflow scheduler"
    echo ""
    airflow webserver -p 8080
fi
