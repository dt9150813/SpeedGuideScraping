import requests
import csv
import time
import sys
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
rows = []
fields = ['Port', 'Protocol', 'Service', 'Detail']
r = requests.Session()
# Use a normal Chromium browser user agent to reduce the chance to get banned by websites
r.headers.update({'x-test': 'true', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
# Open a new file 'SpeedGuideScraping.csv'
with open('SpeedGuideScraping.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header
    csvwriter.writerow(fields)
    # Looping through port 0-65535 with tqdm progress bar. range(65536) covers 0-65535
    for p in tqdm(range(65536), desc='Working on it...'):
        # Use requests to get SpeedGuide's port info pages
        try:
            data = r.get(url=f'http://api.scraperapi.com/?api_key=d56c4f9c92778d1ab5fa3cc315a97366&url=https://www.speedguide.net/port.php?port={p}').text
            # Use BeautifulSoup to parse the page got
            soup = bs(data, 'html.parser')
            # Find i tags with text 'SG' (<i>SG</i>) on page
            # This step eliminates random port info and keeps only SpeedGuide ones
            rowsWithSg = soup.find_all('i', text='SG')
            for row in rowsWithSg:
                # Find all siblings of the parent td tag of <i>SG</i>
                # <i>SG</i> is inside of a td tag. The sibling (other) td tags contain the port, protocol, service, and detail info
                # The i tag is in the last td column, so find_previous_sibling() will get the previous td tags following the sequence below
                detail = row.parent.find_previous_sibling().text.strip()
                service = row.parent.find_previous_sibling().find_previous_sibling().text.strip()
                protocol = row.parent.find_previous_sibling(
                ).find_previous_sibling().find_previous_sibling().text.strip()
                port = row.parent.find_previous_sibling().find_previous_sibling(
                ).find_previous_sibling().find_previous_sibling().text.strip()
                # Insert the info in an array, and then add the array insided of the rows array
                # rows.append([port,protocol,service,detail])
                # Write rows into CSV
                csvwriter.writerow([port, protocol, service, detail])
        except:
            print(f'An error occured (prob got banned). Last scraped info was on port {p-1}.')
            sys.exit()
        time.sleep(5)
print('Done!')
