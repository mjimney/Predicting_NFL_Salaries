import requests
import pickle
from bs4 import BeautifulSoup


# Define url's
url_base = 'https://www.pro-football-reference.com/years/'

passing_url = '/passing.htm'
rushing_url = '/rushing.htm'
receiving_url = '/receiving.htm'
defense_url = '/defense.htm'
kick_ret_url = '/returns.htm'

target_urls = [passing_url,rushing_url,receiving_url]


# Function to scrape pro-football-refrence.com
def stats_scrape(url_tail, year, header_row = 0, header_prefix = '', status = False, review_headers = False):
    combined_url = url_base + str(year) + url_tail
    response = requests.get(combined_url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    tables = soup.find_all('table')
    if status == True:
        if len(tables) > 0:
            return 'Ok'
        else:
            return 'Error'

    else:
        rows = [row for row in tables[0].find_all('tr')]
        
        # Define table headers
        table_headers = []
        cells = [cell for cell in rows[header_row].find_all('th')]
        for cell in cells:
            table_headers.append(cell.text)

        # Clean-up headers
        table_headers.pop(0)  # Remove the rank column
        table_headers = table_headers[:6] + [header_prefix + label for label in table_headers[6:]] # First 6 columns are generic, update header for other columns
        table_headers.append('Year') # add a column for year
        if review_headers == True:
            return table_headers
        
        # Build data table
        stats_list_per_player = []
        for row in rows[header_row:]:
            data_row = []
            cells = [cell for cell in row]

            try:  # Ignores header rows placed every 30 rows in the table
                for cell in cells[1:]: # skipping first column, which is rank
                    data_row.append(cell.text.replace('*','').replace('+',''))
                data_row.append(year)
                player_dict = dict([stat for stat in zip(table_headers,data_row)])
                stats_list_per_player.append(player_dict)    
            except:
                pass
        return stats_list_per_player


# Test all pages can connect
def check_connections(years):
    for year in years:
        failures = []
        for url in target_urls:
            site_status = stats_scrape(url,year,status=True)
            if site_status == 'Error':
                failures.append((year,url))
        if len(failures) == 0:
            print ('{}  No Errors'.format(year))
        else:
            print ('Errors for the following: {}'.format(failures))


# Scrape passing stats for each year.  Each player is a dict.
def save_comp_data(years,url_ext,prefix):
    stats_by_year = []
    for year in years:
        annual_count = len(stats_by_year)
        passing_by_year += stats_scrape(passing_url,year,header_prefix = prefix)
        print ('{} Complete  -  New Entries = {}'.format(year,len(stats_by_year) - annual_count))
    print ('Finished')

    with open('../pickle_data/{}stats.pkl'.format(prefix), 'wb') as picklefile:
        pickle.dump(stats_by_year, picklefile)


# Define years to analyze
target_years_stats = list(range(1993,2019))

# Run once to confirm connections are working
# check_connections(target_years_stats)

# Save passing data
save_comp_data(years = target_years_stats, url_ext = passing_url, prefix = 'pass_')
# Save rushing data
save_comp_data(years = target_years_stats, url_ext = rushing_url, prefix = 'rush_')
# Save receiving data
save_comp_data(years = target_years_stats, url_ext = receiving_url, prefix = 'rec_')
