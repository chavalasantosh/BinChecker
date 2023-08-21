import requests
import csv
from concurrent.futures import ThreadPoolExecutor

# Define the range of BINs to search
start_bin = 100000
end_bin = 700000

# Create a list to store the retrieved BINs
retrieved_bins = []

# Function to fetch BIN information
def fetch_bin_info(bin_num):
    url = f"https://bin-info.herokuapp.com/bin/{bin_num}"
    response = requests.get(url)
    
    if response.status_code == 200:
        bin_info = response.json()
        return bin_info
    else:
        return None

# Function to save retrieved BIN information to CSV
def save_to_csv(bins):
    fieldnames = bins[0].keys()

    with open("retrieved_bins.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(bins)

# Perform the BIN lookup for each BIN in the range using multithreading
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_bin_info, bin_num) for bin_num in range(start_bin, end_bin + 1)]

    for future in futures:
        bin_info = future.result()
        if bin_info is not None:
            retrieved_bins.append(bin_info)
        
        # Save the retrieved BIN information to a file instantly
        if len(retrieved_bins) >= 100:
            save_to_csv(retrieved_bins)
            retrieved_bins = []

    # Save the remaining retrieved BIN information to the CSV file
    if retrieved_bins:
        save_to_csv(retrieved_bins)


#Change url if u have your own. :)
