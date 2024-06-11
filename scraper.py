import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# List of User-Agents to rotate through
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
]

# Function to get a random User-Agent
def get_random_user_agent():
    return random.choice(user_agents)

# Function to get page content with headers and delay
def get_page_content(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'
    }
    try:
        time.sleep(random.uniform(3, 7)) 
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to parse and extract data from a single page
def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    # Log the page content for inspection
    with open("page_content.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    listings = soup.find_all('li', class_='Grid__CellBox-sc-a8dff4e9-0')


    addresses = []
    beds = []
    baths = []
    prices = []

    for listing in listings:
        try:
            address = listing.find('div', {'data-testid':'property-address'}).get_text(strip=True)

        except AttributeError:
            address = 'N/A'

        try:
            bed = listing.find('div', {'data-testid':'property-beds'}).get_text(strip=True)

        except AttributeError:
            bed = 'N/A'

        try:
            bath = listing.find('div', {'data-testid':'property-baths'}).get_text(strip=True)
        except AttributeError:
            bath = 'N/A'

        try:
            price = listing.find('div', {'data-testid':'property-price'}).get_text(strip=True)
        except AttributeError:
            price = 'N/A'

        addresses.append(address)
        beds.append(bed)
        baths.append(bath)
        prices.append(price)

    return addresses, beds, baths, prices

# Scrape data from multiple pages on Trulia
def scrape_trulia(base_url, num_pages):
    all_addresses = []
    all_beds = []
    all_baths = []
    all_prices = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}_p/"
        print(f"Scraping page {page}: {url}")

        content = get_page_content(url)
        time.sleep(random.uniform(1, 3)) 
        if content:
            addresses, beds, baths, prices = parse_page(content)
            all_addresses.extend(addresses)
            all_beds.extend(beds)
            all_baths.extend(baths)
            all_prices.extend(prices)

        # Sleep between requests to mimic human behavior
        time.sleep(random.uniform(3, 7))  # Sleep for 3 to 7 seconds randomly

    return all_addresses, all_beds, all_baths, all_prices

# Main function to run the scraper
def main():
    base_url = 'https://www.trulia.com/NY/New_York/'
    num_pages = 10  # Set the number of pages to scrape

    addresses, beds, baths, prices = scrape_trulia(base_url, num_pages)

    # Create a DataFrame
    real_estate = pd.DataFrame({
        'Address': addresses,
        'Beds': beds,
        'Baths': baths,
        'Price': prices
    })
    real_estate.replace('N/A', pd.NA, inplace=True)
    real_estate.dropna(inplace=True)

    # Output the DataFrame
    print(real_estate)

    # Save to a CSV file
    real_estate.to_csv('real_estate_trulia.csv', index=False)

if __name__ == "__main__":
    main()
