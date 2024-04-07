from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import csv
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

def initialize_driver():
    # Setup Chrome options
    chrome_options = Options()

    # Specify headless mode and other arguments for running Chrome
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
         
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_grantors(addy):
    # Initialize driver
    driver = initialize_driver()

    # The URL to which the form submits
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

    num_rows = get_number_of_rows(driver=driver)

    if num_rows == 0:
        # Clean Up: Quit driver
        try:
            driver.quit()

        except Exception as e:
            print(f"Failed to quit driver with error: {e}")
        
        return [],[]
    
    # Create empty grantors and grantees lists
    grantors = []
    grantees = []

    page = 0

    for i in range(num_rows):
        # Change the page after 20 iterations
        if i % 20 == 0 and i > 0:
            next_page_button = driver.find_element(By.ID, "OptionsBar2_imgNext") 
            next_page_button.click()
            page += 1

        # Change i to correspond with page
        if page > 0:
            i = i - (20 * page)

        # Wait for the navigation to complete or for grantor text to be loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, f"ctl00_ctl00_cphNoMargin_cphNoMargin_g_G1_ctl00_it11_{i}_lblTor"))
        )   

        # Get grantor name
        grantor_element = driver.find_element(By.ID, f"ctl00_ctl00_cphNoMargin_cphNoMargin_g_G1_ctl00_it11_{i}_lblTor")
        grantor = grantor_element.text

        # Get grantee name
        grantee_element = driver.find_element(By.ID, f"ctl00_ctl00_cphNoMargin_cphNoMargin_g_G1_ctl00_it11_{i}_lblTee")
        grantee = grantee_element.text

        # Append grantor and grantee to respective lists
        grantors.append(grantor)
        grantees.append(grantee)


    # Clean Up: Quit driver
    try:
        driver.quit()

    except Exception as e:
        print(f"Failed to quit driver with error: {e}")


    # Return grantors and grantees lists
    return grantors, grantees

def get_number_of_rows(driver):
    # Wait for the navigation to complete or for number of rows to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cphNoMargin_cphNoMargin_SearchCriteriaTop_TotalRows"))
    )  

    # Get number of rows element and text
    num_rows_element = driver.find_element(By.ID, "cphNoMargin_cphNoMargin_SearchCriteriaTop_TotalRows")
    num_rows = num_rows_element.text

    # Convert to int and return
    return int(num_rows)

def generate_grantor_grantee_csv(input_file_path, output_file_path):
    # Create dataframe from cvs file path
    df = pd.read_csv(input_file_path)
    lost_df = pd.DataFrame(columns=['Address','Main_Index'])

    # Add empty columns for grantors and grantees
    df['Grantors'] = None
    df['Grantees'] = None

    # Loop through each address and insert grantors and grantees 
    for i, address in enumerate(df['Address']):
        try:
            # Get grantors and grantees lists
            grantors, grantees = get_grantors(addy=address)
            
        except Exception as e:
            # Log the error
            print(f"Error ({e}), processing address {address} at index: {i}")
            
            # Update and save missed address in lost_df
            lost_df.loc[len(lost_df.index)] = [address, i]
            lost_df.to_csv('Temp/missed_addresses.csv')

            # continue to next address
            continue

        # Put grantors and grantees in their respective cells
        df['Grantors'][i] = grantors
        df['Grantees'][i] = grantees

        # Save to csv output file
        df.to_csv(output_file_path)


generate_grantor_grantee_csv(input_file_path="commercial_zoned_addresses.csv", output_file_path="Temp/addresses_commercial.csv")

# lost_df = pd.read_csv('Temp/missed_addresses.csv')
# for address in lost_df['Address']:
#     grantor, grantee = get_grantors(addy=address)
#     print(f"address: {address} \n grantors: {grantor} \n grantees: {grantee}")
# print(lost_df)
