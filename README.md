# Real Estate Data Scraper - README

## Overview
The Real Estate Data Scraper is a Python-based tool designed to scrape grantor and grantee information, along with the date of each deed of trust, from a specified real estate website. This tool takes a list of addresses from a provided CSV file and outputs another CSV file containing detailed transaction information for each address. This is particularly useful for users needing detailed property transaction records for legal, business, or research purposes.

## Prerequisites
To use this scraper, you will need:
- Python 3.7 or newer
- pip (Python package installer)
- Google Chrome or Chromium Browser
- ChromeDriver compatible with your browser version

## Installation
1. **Clone the repository:**
```
git clone https://github.com/jbarneyVBFD/Real_Estate_Web_Scraper.git
cd Real_Estate_Web_Scraper
```


2. **Set up a virtual environment (optional but recommended):**
```
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```


3. **Install the required Python packages:**
```
pip install -r requirements.txt
```


4. **ChromeDriver Setup:**
- Download ChromeDriver from [ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads) matching your Chrome version.
- Place the ChromeDriver executable in a directory within your PATH or specify the path in the script.

## Input File Format
Prepare a CSV file containing the addresses for which you want to fetch data. The CSV file must have a header named `Address`. Example of the input CSV format:
```
Address
123 Example St
456 Another Ln
789 Sample Blvd
```


## Usage
1. **Run the scraper:**
```
python main.py
```

When prompted, a window will appear allowing you to select the input CSV file containing addresses and specify the desired location for the output CSV file.

2. **Input and Output:**
- **Input:** Path to the CSV file containing addresses.
- **Output:** Path where the resultant CSV file will be saved. This file will include columns for Address, Grantor, Grantee, and Date.

## Output File Description
The output CSV file will contain the following columns:
- `Address`: The property address as provided in the input file.
- `Grantor`: The name of the person or entity transferring the property.
- `Grantee`: The name of the person or entity receiving the property.
- `Date`: The date on which the deed of trust was recorded.

## Example Output
```
Address,Grantor,Grantee,Date
123 Example St,John Doe,Jane Smith,01/01/2020
456 Another Ln,Alice Johnson,Bob Lee,02/02/2021
```


## Troubleshooting
- **Selenium WebDriver Errors:** Ensure your ChromeDriver matches your version of Chrome and is correctly placed.
- **Python or Dependency Issues:** Make sure all dependencies are installed as specified in `requirements.txt`. If errors occur, try setting up a new virtual environment and reinstalling the dependencies.

## Support
For issues not resolved by the troubleshooting steps, please open an issue on the project's GitHub repository page or contact the repository maintainer directly via email.