import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

class RealEstateDataFetcher:
    def __init__(self):
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        """Initializes and returns a headless Chrome WebDriver."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox") # Recommended for running as root/user in docker
        chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=chrome_options)
        return driver

    def get_rows(self, addy):
        """Fetches rows of grantor and grantee data for a given address."""
        try:
            url = 'https://www.tccsearch.org/RealEstate/SearchEntry.aspx#close'
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "cph1_lnkAccept")))
            self.driver.find_element(By.ID, "cph1_lnkAccept").click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "cphNoMargin_f_txtLDStreetAddress")))
            address_input = self.driver.find_element(By.ID, "cphNoMargin_f_txtLDStreetAddress")
            address_input.clear()
            address_input.send_keys(addy)
            checkbox = self.driver.find_element(By.NAME, "ctl00$cphNoMargin$f$dclDocType$42")
            if not checkbox.is_selected():
                checkbox.click()
            self.driver.find_element(By.ID, "cphNoMargin_SearchButtons2_btnSearch").click()
            num_rows = self.get_number_of_rows()
            if num_rows == 0:
                return [], [], []
            return self.extract_grantor_grantee_data(num_rows)
        except Exception as e:
            logging.error(f"An error occurred while processing {addy}: {e}")
            return None, None
        finally:
            self.driver.quit()

    def get_number_of_rows(self):
        """Returns the number of rows available for the current search."""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "cphNoMargin_cphNoMargin_SearchCriteriaTop_TotalRows")))
        num_rows_element = self.driver.find_element(By.ID, "cphNoMargin_cphNoMargin_SearchCriteriaTop_TotalRows")
        return int(num_rows_element.text)

    def extract_grantor_grantee_data(self, num_rows):
        """Extracts grantor and grantee data from the search results."""
        grantors, grantees, dates = [], [], []
        for i in range(num_rows):
            grantor_element = self.driver.find_element(By.ID, f"ctl00_ctl00_cphNoMargin_cphNoMargin_g_G1_ctl00_it11_{i % 20}_lblTor")
            grantee_element = self.driver.find_element(By.ID, f"ctl00_ctl00_cphNoMargin_cphNoMargin_g_G1_ctl00_it11_{i % 20}_lblTee")
            date_xpath = f"//*[@id='ctl00_ctl00_cphNoMargin_cphNoMargin_g_G1_ctl00']/table/tbody/tr[2]/td/table/tbody[2]/tr/td/div[2]/table/tbody/tr[{i % 20 + 2}]/td[9]"
            date_element = self.driver.find_element(By.XPATH, date_xpath)
            grantors.append(grantor_element.text)
            grantees.append(grantee_element.text)
            dates.append(date_element.text)
            if (i + 1) % 20 == 0 and i + 1 < num_rows:
                self.navigate_to_next_page()
        return grantors, grantees, dates

    def navigate_to_next_page(self):
        """Navigates to the next page of the search results if applicable."""
        next_page_button = self.driver.find_element(By.ID, "OptionsBar2_imgNext") 
        next_page_button.click()

    @staticmethod
    def generate_grantor_grantee_csv(input_file_path, output_file_path):
        """Generates a CSV file with grantor and grantee data for a list of addresses."""
        df = pd.read_csv(input_file_path)
        # Create an empty DataFrame with the necessary columns
        expanded_df = pd.DataFrame(columns=['Address', 'Grantor', 'Grantee', 'Date'])

        for i, row in df.iterrows():
            fetcher = RealEstateDataFetcher()
            address = row['Address']
            grantors, grantees, dates = fetcher.get_rows(address)
        
            # Iterate through each grantor, grantee, and date, adding each as a new row
            for grantor, grantee, date in zip(grantors, grantees, dates):
                new_row = {'Address': address, 'Grantor': grantor, 'Grantee': grantee, 'Date': date}
                new_row_df = pd.DataFrame([new_row])  # Convert the dictionary to a DataFrame
                expanded_df = pd.concat([expanded_df, new_row_df], ignore_index=True)
    
        # Filter out any rows that didn't get data (if any)
        expanded_df.dropna(subset=['Grantor', 'Grantee', 'Date'], inplace=True)

        # Save the expanded DataFrame to CSV
        expanded_df.to_csv(output_file_path, index=False)