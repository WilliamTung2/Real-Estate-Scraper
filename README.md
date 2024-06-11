### Real Estate Data Scraper for Trulia ###

This script scrapes real estate data from Trulia and saves it to an Excel file. It uses Python libraries such as `requests`, `BeautifulSoup`, and `pandas` to fetch and process the data. The script also handles potential blocking by rotating user agents and adding delays between requests.

## Prerequisites

Before running the script, ensure you have the following Python libraries installed:

- `requests`
- `beautifulsoup4`
- `pandas`
- `openpyxl`

You can install them using pip:

pip install requests beautifulsoup4 pandas openpyxl



###Functions

# get_random_user_agent()
Returns a random User-Agent from the list to mimic different browsers.

# get_page_content(url)
Fetches the page content for a given URL, using a random User-Agent and handling potential request errors.

# parse_page(content)
Parses the HTML content of a page to extract real estate data such as address, beds, baths, and price.

# scrape_trulia(base_url, num_pages)
Scrapes multiple pages of data from Trulia, iterating through the specified number of pages and collecting the data.

##Main Function
The main() function orchestrates the scraping process, cleans the data to remove N/A values, and saves the data to an Excel file.

###Notes
Adjust the number of pages to scrape by changing the num_pages variable in the main() function.
Inspect page_content.html if the script fails to scrape data correctly. This file logs the HTML content for debugging purposes.
