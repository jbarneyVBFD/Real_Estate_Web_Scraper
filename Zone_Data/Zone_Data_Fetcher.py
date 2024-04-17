import requests
import csv
import logging

class ZoneDataFetcher:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.logger = logging.getLogger(__name__)

    def get_addresses(self):
        """Fetches addresses and their zones from the API."""
        limit = 1000000  # Increase limit to retrieve all available addresses
        updated_url = f"{self.endpoint} LIMIT {limit}"

        try:
            response = requests.get(updated_url)

            if response.status_code == 200:
                data = response.json()
                addresses = [item['full_street_name'] for item in data if 'full_street_name' in item]
                zones = [item['base_zone_category'] for item in data if 'base_zone_category' in item]
                return addresses, zones
            else:
                self.logger.error(f"Failed to fetch data, status code: {response.status_code}")
                return None, None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None, None

    @staticmethod
    def save_addresses_zones_to_csv(addresses, zones, filename="addresses_zones.csv"):
        """Saves addresses and their zones to a CSV file."""
        if len(addresses) != len(zones):
            raise ValueError("The lengths of addresses and zones lists must match.")

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Address', 'Zone'])
            for address, zone in zip(addresses, zones):
                writer.writerow([address, zone])
        
        logging.info(f"Addresses and zones have been saved to {filename}.")


# Example usage
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     commercial_endpoint = 'https://data.austintexas.gov/resource/nbzi-qabm.json?$query=SELECT%20%60full_street_name%60%2C%20%60base_zone_category%60%0AWHERE%0A%20%20%60base_zone_category%60%20IN%20(%0A%20%20%20%20%22%22%2C%20... <remaining query>'

#     fetcher = ZoneDataFetcher(commercial_endpoint)
#     addresses, zones = fetcher.get_addresses()
    
#     if addresses is not None and zones is not None:
#         fetcher.save_addresses_zones_to_csv(addresses, zones, "commercial_zoned_addresses.csv")
#     else:
#         logging.error("Failed to fetch addresses and zones.")
