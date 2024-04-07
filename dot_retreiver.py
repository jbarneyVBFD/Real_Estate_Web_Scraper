from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os
import shutil
import time
import random
import csv
import requests

def download_pdf(url, destination_folder, filename):
    # Ensure the destination directory exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, filename)

    headers = {
        'Accept': 'application/pdf',  # Indicates a preference for PDF files
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # This will raise an HTTPError if the download failed
    
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content of the response to a new file in the destination folder
        with open(destination_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded '{filename}' to '{destination_folder}'")
    else:
        print(f"Failed to download file from {url}")

def get_user_agents():  
    # Path to your CSV file
    csv_file_path = 'whatismybrowser-user-agent-database.csv'

    # Initialize an empty list to hold User-Agent strings
    user_agents = []

    # Open the CSV file and read its contents into the list
    with open(csv_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header row if there is one
        for row in csvreader:
            # Assuming the User-Agent string is in the first column of each row
            user_agents.append(row[0])

    return user_agents

def initialize_driver(custom_options=None):
    # Setup Chrome options
    chrome_options = Options()
    if custom_options:
        # These automatically revert to default when the webdriver session is closed
        for option_key, option_value in custom_options.items():
            chrome_options.add_experimental_option(option_key, option_value)

    # Get user agents
    user_agents = get_user_agents()

    # # Specify headless mode and other arguments for running Chrome
    # chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    # chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, WARNING: only use this if you understand implications
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource problems
    # chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
         
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def moveFile(addy, source_directory, DOT):
    # Move files to final directory
    for filename in os.listdir(source_directory):
        # Create full source path
        source_path = os.path.join(source_directory, filename)

        # Check if Deed of Trust or Details Page, then create full path of target directory
        if DOT:
            target_directory = f"/Users/johnbarney/Desktop/Web_Scraper/Documents/{addy}/DOT"
        else: 
            target_directory = f"/Users/johnbarney/Desktop/Web_Scraper/Documents/{addy}/deets"
        
        # Make sure target directory exists
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
            
        # Create full path of destination, then move files there
        target_path = os.path.join(target_directory, filename)
        shutil.move(source_path, target_path)


def download_files(addy, download_folder):
    download_folder = os.path.abspath(download_folder)
    print(download_folder)
    # Make sure folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Initialize driver with custom download settings
    custom_options = {
        'prefs': {
            "download.default_directory": download_folder,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": False
        }
    }
    driver = initialize_driver(custom_options)
    wait = WebDriverWait(driver,10)

    # The URL to which the form submits (replace this with the actual form action URL)
    url = 'https://www.tccsearch.org/RealEstate/SearchEntry.aspx#close'

    # Navigate to the search page
    driver.get(url)

    # Wait for disclaimer
    WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "cph1_lnkAccept"))
    )

    # Acknowledge disclaimer to enter the site
    disclaimer = driver.find_element(By.ID, "cph1_lnkAccept")
    disclaimer.click()

    # Wait for the address input to be visible
    WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "cphNoMargin_f_txtLDStreetAddress"))
    )

    # Fill in the address
    address_input = driver.find_element(By.ID, "cphNoMargin_f_txtLDStreetAddress")
    address_input.clear()
    address_input.send_keys(addy)

    # Select the "DEED OF TRUST" checkbox if not already selected
    checkbox = driver.find_element(By.NAME, "ctl00$cphNoMargin$f$dclDocType$42")
    if not checkbox.is_selected():
        checkbox.click()    

    # Submit the form by clicking the search button
    search_button = driver.find_element(By.ID, "cphNoMargin_SearchButtons2_btnSearch")
    search_button.click()

    # Wait for the navigation to complete or for Selected Details link to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cphNoMargin_cphNoMargin_OptionsBar1_lnkDetail"))
    )   

    # Find the checkbox by its ID and click it to select
    checkbox = driver.find_element(By.ID, "chkAll")
    if not checkbox.is_selected():
        checkbox.click()
        
    # Now, find the link by its ID and click it
    details_link = driver.find_element(By.ID, "cphNoMargin_cphNoMargin_OptionsBar1_lnkDetail")
    images_link = driver.find_element(By.ID, "cphNoMargin_cphNoMargin_OptionsBar1_lnkDld")

    details_link.click()

    # After clicking the details link, handle the new window
    original_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrOptionWindow"))
    )

    # Click the "Get Item(s) Now" button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnProcessNow"))
    ).click()

    # Wait for the select element to be loaded.
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "lstDeliveryItems"))
    )
    # Create a Select object
    select_obj = Select(select_element)

    # Loop through the options and select each one by its visible text or value
    for index, option in enumerate(select_obj.options):
        
        # Select by index since the options list gets refreshed each time you switch iframes
        select_obj.select_by_index(index)
        
        # Switch to pdf window
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrPDFWindow"))
        )

        # Extract the pdf link
        pdf = driver.find_element(By.ID, "pdf").get_attribute('data')
        print(pdf)
        download_pdf(url=pdf, destination_folder=f"/Users/johnbarney/Desktop/Web_Scraper/Documents/{addy}/deets/", filename=f"deets_{index}.pdf")
        # print(pdf)
        # driver.get(pdf)
        time.sleep(5)

        # Switch back to option window i-frame 
        driver.switch_to.window(original_window)
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrOptionWindow"))
        )

    # Move files to their respective locations
    # moveFile(addy=addy, source_directory=download_folder, DOT=False)

    # Clean-up: Switch back to the original window
    driver.switch_to.window(original_window)

    # Now navigate to images link
    images_link.click()
    time.sleep(5)
    # After clicking the images link, handle the new window
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrOptionWindow"))
    )

    # Click the "Get Item(s) Now" button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnProcessNow"))
    ).click()

    # Wait for the select element to be loaded.
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "lstDeliveryItems"))
    )

    # Create a Select object
    select_obj = Select(select_element)

    
    # Loop through the options and select each one by its visible text or value
    for index, option in enumerate(select_obj.options):
        # Select by index since the options list gets refreshed each time you switch iframes
        select_obj.select_by_index(index)
       
        # Switch to pdf window
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrPDFWindow"))
        )
    
        # Extract the pdf link
        pdf = driver.find_element(By.ID, "pdf").get_attribute('data')
        download_pdf(url=pdf, destination_folder=f"/Users/johnbarney/Desktop/Web_Scraper/Documents/{addy}/DOT/", filename=f"DOT_{index}.pdf")
        print(pdf)
        # driver.get(pdf)
        time.sleep(5)

        driver.switch_to.window(original_window)
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrOptionWindow"))
        )

    # Move files to their respective locations
    # moveFile(addy=addy, source_directory=download_folder, DOT=True)

    driver.quit()

addy = "603 W 17TH ST"
download_files(addy=addy, download_folder="/Users/johnbarney/Downloads/Temp")