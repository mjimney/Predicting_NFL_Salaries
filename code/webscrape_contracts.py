import requests
import pickle
from bs4 import BeautifulSoup

# String cleaning logic
number_cleaning = {'$':'','(':'',')':'',',':'','-':'0'}
clean_mapping = str.maketrans(number_cleaning)

# url team Mapping
team_mapping = {'san-francisco-49ers': 'SFO',
                'chicago-bears': 'CHI',
                'cincinnati-bengals': 'CIN',
                'buffalo-bills': 'BUF',
                'denver-broncos': 'DEN',
                'cleveland-browns': 'CLE',
                'tampa-bay-buccaneers': 'TAM',
                'arizona-cardinals': 'ARI',
                'los-angeles-chargers': 'LAC',
                'kansas-city-chiefs': 'KAN',
                'indianapolis-colts': 'IND',
                'dallas-cowboys': 'DAL',
                'miami-dolphins': 'MIA',
                'philadelphia-eagles': 'PHI',
                'atlanta-falcons': 'ATL',
                'new-york-giants': 'NYG',
                'jacksonville-jaguars': 'JAX',
                'new-york-jets': 'NYJ',
                'detroit-lions': 'DET',
                'green-bay-packers': 'GNB',
                'carolina-panthers': 'CAR',
                'new-england-patriots': 'NWE',
                'oakland-raiders': 'OAK',
                'los-angeles-rams': 'LAR',
                'baltimore-ravens': 'BAL',
                'washington-redskins': 'WAS',
                'new-orleans-saints': 'NOR',
                'seattle-seahawks': 'SEA',
                'pittsburgh-steelers': 'PIT',
                'houston-texans': 'HOU',
                'tennessee-titans': 'TEN',
                'minnesota-vikings': 'MIN'}

# Function to scrape spotrac.com
def comp_scrape(team, year, status = False):
    # Connect to url
    url = 'https://www.spotrac.com/nfl/{}/cap/{}/'.format(team,year)
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    
    # Test connection
    if status == True:
        if len(soup.find_all('table')) > 0:
            return 'Ok'
        else:
            return 'Error'

    # Build data table for all players, looping through active, injured, etc
    player_comp_list = []
    try:
        for table in soup.find_all('table')[:-2]:
            rows = [row for row in table.find_all('tr')]
            rows = rows[1:]
            try:
                for row in rows:
                    player_comp = {}
                    player_comp['year'] = year
                    player_comp['team'] = team_mapping[team]
                    player_comp['name'] = row.find('a').text
                    player_comp['pos'] = row.find_all(class_ = 'cap')[0].text
                    player_comp['base_salary'] = int(row.find_all(class_ = 'cap')[1].text.translate(clean_mapping))
                    player_comp['signing_bonus'] = int(row.find_all(class_ = 'cap')[2].text.translate(clean_mapping))
                    player_comp['roster_bonus'] = int(row.find_all(class_ = 'cap')[3].text.translate(clean_mapping))
                    player_comp['option_bonus'] = int(row.find_all(class_ = 'cap')[4].text.translate(clean_mapping))
                    player_comp['workout_bonus'] = int(row.find_all(class_ = 'cap')[5].text.translate(clean_mapping))
                    player_comp['restruc_bonus'] = int(row.find_all(class_ = 'cap')[6].text.translate(clean_mapping))
                    player_comp['misc_bonus'] = int(row.find_all(class_ = 'cap')[7].text.translate(clean_mapping))
                    try:
                        player_comp['cap_hit'] = int(row.find(title = 'Cap Hit').text.translate(clean_mapping))
                    except:
                        player_comp['cap_hit'] = int(row.find_all(class_ = 'cap info')[-1].text.translate(clean_mapping))
                    player_comp['cap_pct'] = float(row.find_all(class_ = 'center')[1].text.translate(clean_mapping))

                    player_comp_list.append(player_comp)
            except:
                pass
        return player_comp_list
    except:
        return player_comp_list

def check_connections(years):
    for year in years:
        failures = []
        for team in list(team_mapping.keys()):
            site_status = comp_scrape(team,year,status=True)
            if site_status == 'Error':
                failures.append((year,team))
        if len(failures) == 0:
            print ('{}  No Errors'.format(year))
        else:
            print ('Errors for the following: {}'.format(failures))

def save_comp_data(years):
    comp_data = []
    for year in target_years_comp:
        annual_count = len(comp_data)
        for team in list(team_mapping.keys()):
            comp_data += comp_scrape(team,year)
        print ('{} Complete  -  New Entries = {}'.format(year,len(comp_data) - annual_count))
    print ('Finished')

    # Pickle data
    with open('../pickle_data/player_comp.pkl', 'wb') as picklefile:
        pickle.dump(comp_data, picklefile)


# Define years to analyze
target_years_comp = list(range(1994,2019))

# Run once to confirm connections are working
# check_connections(target_years_comp)

# Save compensation data to pickle file
save_comp_data(target_years_comp)
