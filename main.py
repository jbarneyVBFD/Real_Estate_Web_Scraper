import logging
from Form import get_file_paths
from Real_Estate_Data import RealEstateDataFetcher

if __name__ == "__main__":
    input_path, output_path = get_file_paths()
    if not input_path or not output_path:
        print("Operation cancelled by the user.")
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        RealEstateDataFetcher.generate_grantor_grantee_csv(input_file_path=input_path, output_file_path=output_path)