import pickle
import pandas as pd

salary_cap = {2019:188200000,
              2018:177200000,
              2017:167000000,
              2016:155270000,
              2015:143280000,
              2014:133000000,
              2013:123000000,
              2012:120600000,
              2011:120000000,
              2010:123000000,
              2009:123000000,
              2008:116000000,
              2007:109000000,
              2006:102000000,
              2005:85500000,
              2004:80582000,
              2003:75007000,
              2002:71101000,
              2001:67405000,
              2000:62172000,
              1999:57288000,
              1998:52388000,
              1997:41454000,
              1996:40753000,
              1995:37100000,
              1994:34608000}

def fix_team_names(df,col='Tm'):
    '''
    Corrects team names acording to name_cleaning dictionary.
    '''
    # Fix names of old teams
    name_cleaning = {'PHO':'ARI','RAM':'LAR','RAI':'OAK','STL':'LAR','SDG':'LAC'}

    for old, new in name_cleaning.items():
        df[col] = df[col].replace(old, new)
    return df

def change_number_types(df,to_int,to_float):
    '''
    Convert specified columns to int or float in bulk. Blank values 
    are changed to 0 before converting.
    '''
    
    # Convert columns to Ints
    df[to_int] = df[to_int].replace('','0')
    df[to_int] = df[to_int].astype(int).copy()

    # Convert columns to Floats
    df[to_float] = df[to_float].replace('','0')
    df[to_float] = df[to_float].astype(float).copy()
    
    return df

def scale_data(row):
    '''
    Used to scale stats, so max value is 1 and min is 0.
    '''
    return (row - row.min()) / (row.max() - row.min())

def scale_per_year(df,cols,year,name='_adj'):
    '''
    Given a list of columns, loops through and scales
    each column.  Adds a new column by modifying the name
    of the original.
    '''
    for col in cols:
        df[col+name] = df.groupby([year])[col].transform(scale_data)


def engineer_passing_df(pkl_file):
    # Create df for passing stats
    with open('../pickle_data/{}.pkl'.format(pkl_file), 'rb') as picklefile: 
        df = pd.DataFrame(pickle.load(picklefile))

    # First split the record
    df['pass_QBrec'] = df['pass_QBrec'].replace('','0-0-0',)
    df[['pass_wins','pass_loses','pass_ties']] = df['pass_QBrec'].str.split('-',expand=True)

    # Convert columns to Ints and Floats
    col_to_int = ['Age','G','GS','Year','pass_4QC','pass_Att','pass_Cmp','pass_GWD','pass_Int','pass_Lng','pass_Sk','pass_TD','pass_Yds','pass_wins','pass_loses','pass_ties']
    col_to_float =  ['pass_ANY/A','pass_AY/A','pass_Cmp%', 'pass_Int%', 'pass_NY/A', 'pass_Rate', 'pass_TD%', 'pass_Y/A','pass_Y/C','pass_Y/G','pass_Sk%']

    df = change_number_types(df,col_to_int,col_to_float)

    # Move year forward, so compairing 2018 contract vs 2017 stats
    df['Analysis_Year'] = df['Year'] + 1

    # Fix team name for traded players
    df['Tm'] = df['Tm'].replace(['3TM','2TM'],'multi')

    # Fix team name for teams that moved
    df = fix_team_names(df)

    # Drop unnececery columns
    col_drop =  ['Pos','Year','pass_QBR','pass_QBrec']
    df.drop(columns=col_drop,inplace=True)

    # Create columns scaled between 1 and 0 for each year, 1 is the max for that year.
    cols_to_scale = ['pass_4QC','pass_Att','pass_Cmp','pass_GWD','pass_Int',
                    'pass_Lng','pass_Sk','pass_TD','pass_Yds','pass_ANY/A',
                    'pass_AY/A','pass_Cmp%','pass_Int%','pass_NY/A','pass_Rate',
                    'pass_TD%','pass_Y/A','pass_Y/C','pass_Y/G','pass_Sk%']

    scale_per_year(df,cols_to_scale,year='Analysis_Year')

    return df


def engineer_rushing_df(pkl_file):
    # Create df for rushing stats
    with open('../pickle_data/{}.pkl'.format(pkl_file), 'rb') as picklefile: 
        df = pd.DataFrame(pickle.load(picklefile))

    # Convert columns to Ints and Floats
    col_to_int = ['Age','G','GS','Year','rush_Att','rush_Fmb','rush_Lng','rush_TD','rush_Yds']
    col_to_float = ['rush_Y/A','rush_Y/G']

    df = change_number_types(df,col_to_int,col_to_float)

    # Move year forward, so compairing 2018 contract vs 2017 stats
    df['Analysis_Year'] = df['Year'] + 1

    # Fix team name for traded players
    df['Tm'] = df['Tm'].replace(['3TM','2TM'],'multi')

    # Fix team name for teams that moved
    df = fix_team_names(df)

    # Drop unnececery columns
    col_drop =  ['Pos','Year']
    df.drop(columns=col_drop,inplace=True)

    # Create columns scaled between 1 and 0 for each year, 1 is the max for that year.
    cols_to_scale = ['rush_Att','rush_Fmb',
                    'rush_Lng','rush_TD',
                    'rush_Yds','rush_Y/A',
                    'rush_Y/G']

    scale_per_year(df,cols_to_scale,year='Analysis_Year')

    return df


def engineer_receiving_df(pkl_file):
    # Create df for receiving stats
    with open('../pickle_data/{}.pkl'.format(pkl_file), 'rb') as picklefile: 
        df = pd.DataFrame(pickle.load(picklefile))
        
    # Convert columns to Ints and Floats
    col_to_int = ['Age','G','GS','Year','rec_Fmb','rec_Lng','rec_Rec','rec_TD','rec_Tgt','rec_Yds']       
    col_to_float = ['rec_Ctch%','rec_R/G', 'rec_Y/G','rec_Y/R','rec_Y/Tgt']

    df['rec_Ctch%'] = df['rec_Ctch%'].str.replace('%','')
    df = change_number_types(df,col_to_int,col_to_float)

    # Move year forward, so compairing 2018 contract vs 2017 stats
    df['Analysis_Year'] = df['Year'] + 1

    # Fix team name for traded players
    df['Tm'] = df['Tm'].replace(['3TM','2TM'],'multi')

    # Fix team name for teams that moved
    df = fix_team_names(df)

    # Drop unnececery columns
    col_drop =  ['Pos','Year']
    df.drop(columns=col_drop,inplace=True)

    # Create columns scaled between 1 and 0 for each year, 1 is the max for that year.
    cols_to_scale = ['rec_Fmb','rec_Lng',
                    'rec_Rec','rec_TD',
                    'rec_Tgt','rec_Yds',
                    'rec_Ctch%','rec_R/G',
                    'rec_Y/G','rec_Y/R',
                    'rec_Y/Tgt']

    scale_per_year(df,cols_to_scale,year='Analysis_Year')

    return df


def engineer_comp_df(pkl_file):
    # Create df for comp data
    with open('../pickle_data/{}.pkl'.format(pkl_file), 'rb') as picklefile: 
        df = pd.DataFrame(pickle.load(picklefile))

    # Drop unnececery columns
    col_drop =  ['base_salary', 'misc_bonus',
                'option_bonus','restruc_bonus',
                'roster_bonus', 'signing_bonus',
                'workout_bonus']

    df.drop(columns=col_drop,inplace=True)

    # Filter for only QBs, RBs, and WRs

    mask = df['pos'].isin(['QB', 'RB', 'WR'])
    df_filtered = df[mask].copy()

    for name,year in duplicates_to_remove_from_comp:
        name_filter = df_filtered['name'] == name
        year_filter = df_filtered['year'] == year
        df_filtered.drop(df_filtered[name_filter & year_filter].index,inplace=True)

    # Combine compensation split across teams (if traded, you can be paid by 2 teams in a year)
    df_filtered['comp'] = df_filtered.groupby(['year','name'])['cap_hit'].transform(sum)
    df_filtered.drop_duplicates(subset=['year', 'name'], inplace=True)

    # Calculate Salary Cap % with cleaned data
    df_filtered['cap_pct'] = df_filtered['comp'] / df_filtered['year'].map(salary_cap)

    return df_filtered




pass_df = engineer_passing_df(pkl_file = 'pass_stats')
rush_df = engineer_rushing_df(pkl_file = 'rush_stats')
rec_df = engineer_receiving_df(pkl_file = 'rec_stats')




# Merge pass, rush, and rec stats together
col_overlap = ['Age', 'G', 'GS', 'Player', 'Tm', 'Analysis_Year']
stat_df = pd.merge(pass_df,rush_df,how='outer',left_on=col_overlap,right_on=col_overlap)
stat_df = stat_df.merge(rec_df,how='outer',left_on=col_overlap,right_on=col_overlap).copy()
stat_df.fillna(0,inplace=True)
del(pass_df,rush_df,rec_df)


# Filter for players with same name in same year
duplicate_player_mask = stat_df.duplicated(['Player','Analysis_Year'],keep=False)

# List of tuples, to be used to remove data from compensation data
duplicates_to_remove_from_comp = list(stat_df[stat_df.duplicated(['Player','Analysis_Year'])][['Player','Analysis_Year']].apply(tuple,axis=1))

# Retrieve index of duplicate players, eliminate duplicate players in the same year
stat_df.drop(stat_df[duplicate_player_mask].index,inplace=True)

# Merge compensation with stats data
comp_df = engineer_comp_df(pkl_file = 'player_comp')
player_df = pd.merge(left=comp_df,right=stat_df,how='left',left_on=['name','year'],right_on=['Player','Analysis_Year'])
del(comp_df,stat_df)


# Remove redundant data
cols_to_remove = ['Player','team','Analysis_Year','cap_hit']
player_df.drop(columns=cols_to_remove,inplace=True)

# Drop NaN's, AKA players with no stats
player_df.dropna(inplace=True)
player_df.reset_index(drop=True,inplace=True)

# Remove outliers
outliers = {'Jeff Blake':1995}  # Error with 1995 salary
for name,year in outliers.items():
    name_filter = player_df['name'] == name
    year_filter = player_df['year'] == year
    player_df.drop(player_df[name_filter & year_filter].index,inplace=True)

# Pickle complete dataset
with open('../pickle_data/player_df.pkl', 'wb') as picklefile:
    pickle.dump(player_df, picklefile)
