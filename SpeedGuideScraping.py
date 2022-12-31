import requests
import csv
import time
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
r = requests.Session()
r.auth = ('user', 'pass')
# Use a normal Chromium browser user agent to reduce the chance to get banned by websites
r.headers.update({'x-test': 'true', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
rows=[]
fields=['Port','Protocol','Service','Detail']

# Looping through port 0-65535 with tqdm progress bar. range(65536) covers 0-65535
for p in tqdm(range(65536),desc='Working on it...'):
    # Use requests to get SpeedGuide's port info pages
    data = r.get(url=f'https://www.speedguide.net/port.php?port={p}').text
    # Use BeautifulSoup to parse the page got
    soup = bs(data, 'html.parser')
    # Find i tags with text 'SG' (<i>SG</i>) on page
    # This step eliminates random port info and keeps only SpeedGuide ones
    rowsWithSg = soup.find_all('i', text='SG')
    for row in rowsWithSg:
        # Find all siblings of the parent td tag of <i>SG</i>
        # <i>SG</i> is inside of a td tag. The sibling (other) td tags contain the port, protocol, service, and detail info
        # The i tag is in the last td column, so find_previous_sibling() will get the previous td tags following the sequence below
        detail=row.parent.find_previous_sibling().text.strip()
        service=row.parent.find_previous_sibling().find_previous_sibling().text.strip()
        protocol=row.parent.find_previous_sibling().find_previous_sibling().find_previous_sibling().text.strip()
        port=row.parent.find_previous_sibling().find_previous_sibling().find_previous_sibling().find_previous_sibling().text.strip()
        # Insert the info in an array, and then add the array insided of the rows array
        rows.append([port,protocol,service,detail])
    # Wait for 0.5 seconds so SpeedGuide doesn't ban the process. This is not necessary
    time.sleep(0.5)

# Open a new file 'SpeedGuideScraping.csv'
with open('SpeedGuideScraping.csv','w') as csvfile:
    csvwriter=csv.writer(csvfile)
    # Write header
    csvwriter.writerow(fields)
    # Write rows into CSV
    csvwriter.writerows(rows)
print('Done!')