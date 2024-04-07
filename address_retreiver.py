import requests
import csv

commercial_endpoint = 'https://data.austintexas.gov/resource/nbzi-qabm.json?$query=SELECT%20%60full_street_name%60%2C%20%60base_zone_category%60%0AWHERE%0A%20%20%60base_zone_category%60%20IN%20(%0A%20%20%20%20%22%22%2C%0A%20%20%20%20%22Central%20Business%20District%22%2C%0A%20%20%20%20%22Commercial%20Highway%22%2C%0A%20%20%20%20%22Commercial-Liquor%20Sales%22%2C%0A%20%20%20%20%22Commercial%20Recreation%22%2C%0A%20%20%20%20%22Community%20Commercial%22%2C%0A%20%20%20%20%22General%20Commercial%20Services%22%2C%0A%20%20%20%20%22Lake%20Commercial%22%2C%0A%20%20%20%20%22Neighborhood%20Commercial%22%2C%0A%20%20%20%20%22Downtown%20Mixed%20Use%22%2C%0A%20%20%20%20%22East%20Riverside%20Corridor%22%2C%0A%20%20%20%20%22Industrial%20Park%22%2C%0A%20%20%20%20%22Major%20Industry%22%2C%0A%20%20%20%20%22Limited%20Industrial%20Services%22%2C%0A%20%20%20%20%22Research%20and%20Development%22%2C%0A%20%20%20%20%22Unzoned%22%0A%20%20)'
office_endpoint = 'https://data.austintexas.gov/resource/nbzi-qabm.json?$query=SELECT%20%60full_street_name%60%2C%20%60base_zone_category%60%0AWHERE%0A%20%20%60base_zone_category%60%20IN%20(%0A%20%20%20%20%22%22%2C%0A%20%20%20%20%22Warehouse%20Limited%20Office%22%2C%0A%20%20%20%20%22Neighborhood%20Office%22%2C%0A%20%20%20%20%22General%20Office%22%2C%0A%20%20%20%20%22Limited%20Office%22%0A%20%20)'

def get_addresses(api_url):
    # increase limit to retreive all available addresses
    limit = 100000
    updated_url = f"{api_url} LIMIT {limit}"

    # Send a GET request to the API endpoint
    response = requests.get(updated_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()
    
        # Extract and print the addresses
        addresses = [item['full_street_name'] for item in data if 'full_street_name' in item]
        zones = [item['base_zone_category'] for item in data if 'base_zone_category' in item]
        return addresses, zones

    else:
        print(f"Failed to fetch data, status code: {response.status_code}") 

addresses, zones = get_addresses(commercial_endpoint)
print(len(addresses))
print(len(zones))

def save_addresses_zones_to_csv(addresses, zones, filename="addresses_zones.csv"):
    """
    Saves a list of addresses and their corresponding zones to a CSV file.

    Parameters:
    - addresses: List of addresses to save.
    - zones: List of zones corresponding to each address.
    - filename: Name of the CSV file to save the data to (default is "addresses_zones.csv").
    
    Note: `addresses` and `zones` must have the same length.
    """
    
    # Check if both lists have the same length
    if len(addresses) != len(zones):
        raise ValueError("The lengths of addresses and zones lists must match.")
    
    # Open or create the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['Address', 'Zone'])
        
        # Write the addresses and zones to the CSV, each pair on its own row
        for address, zone in zip(addresses, zones):
            writer.writerow([address, zone])

    print(f"Addresses and zones have been saved to {filename}.")

# Call the function to save the addresses and zones"
save_addresses_zones_to_csv(addresses, zones, "commercial_zoned_addresses.csv")

