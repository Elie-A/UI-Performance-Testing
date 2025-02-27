# setup.py
import os
import sys
import subprocess

def install_requirements():
    """Install required packages for the dashboard."""
    requirements = [
        'flask',
        'watchdog',
    ]
    
    print("Installing required packages...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + requirements)
    print("Installation complete!")

def create_directories():
    """Create necessary directories for the dashboard."""
    directories = [
        'templates',
        'static',
        'results'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
            
def create_placeholder():
    """Create a placeholder metrics file for testing."""
    placeholder_path = os.path.join('results', 'example_metrics.json')
    placeholder_content = """
    {
        "test_case_id": "Example Test",
        "start_time": "2025-02-27T10:00:00",
        "actions": [
            {
                "action": "Login",
                "start_time": "2025-02-27T10:00:01",
                "duration": 1.5,
                "parameters": {},
                "step_order": 1,
                "cpu_usage": "23%",
                "memory_usage": "345.67 MB"
            },
            {
                "action": "Navigate",
                "start_time": "2025-02-27T10:00:03",
                "duration": 0.8,
                "parameters": {},
                "step_order": 2,
                "cpu_usage": "25%",
                "memory_usage": "348.92 MB"
            }
        ],
        "system_info": {
            "os": "Windows",
            "os_version": "10.0.19045",
            "cpu": "30%",
            "memory": "16.0 GB"
        },
        "execution_context": {
            "robot_version": "6.1.1",
            "python_version": "3.10.0",
            "browser": "chromium",
            "headless_mode": false
        },
        "summary": {
            "Login": {
                "count": 1,
                "total_duration": 1.5,
                "min_duration": 1.5,
                "max_duration": 1.5,
                "avg_duration": 1.5
            },
            "Navigate": {
                "count": 1,
                "total_duration": 0.8,
                "min_duration": 0.8,
                "max_duration": 0.8,
                "avg_duration": 0.8
            }
        }
    }
    """
    
    with open(placeholder_path, 'w') as f:
        f.write(placeholder_content)
    
    print(f"Created placeholder metrics file at {placeholder_path}")

def setup():
    """Run all setup steps."""
    install_requirements()
    create_directories()
    
    # Move the dashboard.html template to the templates directory
    dashboard_source = 'dashboard.html'  # You'll need to create this file from the HTML code provided
    dashboard_dest = os.path.join('templates', 'dashboard.html')
    
    print("Setup complete!")
    print("\nTo start the dashboard, run:")
    print("    python app.py")
    print("\nThen open a web browser and go to:")
    print("    http://localhost:5000")

if __name__ == "__main__":
    setup()