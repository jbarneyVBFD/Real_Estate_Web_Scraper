# Austin Zoned Addresses Scraper

## Overview

This script is designed to fetch addresses and their corresponding zoning categories from the Austin, Texas, government database for commercial and office zones. It utilizes the Socrata Open Data API to access two distinct datasets:

- Commercial properties
- Office locations

The script then saves this data into a CSV file for easy access and analysis. This can be particularly useful for researchers, urban planners, and data analysts interested in property zoning information in Austin.

## Installation

### Prerequisites

Before you can run this script, you'll need:

- Python 3.x installed on your machine. Python can be downloaded from [python.org](https://www.python.org/downloads/).
- The `requests` library installed, which the script uses to make HTTP requests. If you don't have `requests` installed, you can install it using pip:

  ```bash
  pip install requests

## Getting the Script

- Download the Python script to your local machine.
- Place the script in a suitable directory where you wish to run it from.

## Running the Script

To run the script, follow these steps:

1. Open your command line interface (CLI).
2. Navigate to the directory where the script is saved.
3. Run the script using Python by typing the following command:

   ```bash
   python address_retreiver.py

## How It Works

The script is structured as follows:

- **API Endpoints**: It defines two API endpoints that target different zoning data within the Austin, Texas, open data portal:
  - `commercial_endpoint` for commercial zoning data.
  - `office_endpoint` for office zoning data.

- **Fetching Data**: The `get_addresses` function sends a GET request to the specified API endpoint. It appends a high `limit` parameter to the query to ensure retrieval of all available data. The function then parses the JSON response to extract addresses and zoning categories.

- **Saving Data**: Using the `save_addresses_zones_to_csv` function, the script saves the fetched addresses and zones into a CSV file named `commercial_zoned_addresses.csv`. This file includes two columns: `Address` and `Zone`.

## Customization

You can customize the script by modifying the API endpoint URLs to target different datasets or by changing the output CSV file's name in the `save_addresses_zones_to_csv` function.

## Troubleshooting

- **API Fetch Limit**: The script sets a high limit to ensure all data is fetched. However, if the dataset exceeds this limit, consider implementing pagination in the `get_addresses` function.

- **HTTP Request Failures**: If the script fails to fetch data (e.g., due to network issues or API endpoint changes), verify your internet connection and the validity of the API URLs.
