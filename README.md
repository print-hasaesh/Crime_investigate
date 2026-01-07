# Crime Investigation Dashboard

This project is a Python-based crime data analysis dashboard designed to demonstrate data cleaning, duplicate handling, and interactive visualization using Plotly. It is suitable for academic projects, hackathons, and demonstrations of data preprocessing and UI-driven analytics.

The dashboard reads crime data from a CSV file, performs automatic cleaning and normalization, and presents interactive charts through a Tkinter-based interface.

---

## Project Structure

The project folder must contain the following files:

dashboard.py  
crime_data.csv  
README.md  
requirements.txt  

---

## System Requirements

Python version required:
Python 3.9 or higher

Supported operating systems:
Windows, Linux, macOS

---

Download the ZIP file from the repository, extract it, and open a terminal or PowerShell inside the extracted folder.

Verify that Python is installed:

python --version


If Python is not installed, download it from https://www.python.org
 and ensure that "Add Python to PATH" is enabled during installation.

(Optional but recommended) Create a virtual environment:

    python -m venv venv
    venv\Scripts\activate


Install required dependencies:

    pip install -r requirements.txt


If requirements.txt is not used:

    pip install pandas plotly


If multiple Python versions are installed:

    python -m pip install pandas plotly


Verify Plotly installation (optional):

    python -c "import plotly; print(plotly.__version__)"


If no error appears, the installation was successful.

Running the Application
Ensure you are inside the project directory:

    cd Crime_investigate


Run the dashboard:

    python dashboard.py


A Tkinter window will open displaying multiple tabs.