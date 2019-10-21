import requests
import pandas as pd
import matplotlib.pyplot as plt

#read in game ids of 18/19 WSL, 2019 WWC, 2018 NWSL matches
wsl = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/37/4.json"
nwsl = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/49/3.json"
wwc = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/72/30.json"

#read in competition info, get list of match ids, append to master list
all_match_ids = []
for competition in [wsl,nwsl,wwc]:
    
    games = requests.get(url=competition).json()
    match_ids = [g['match_id'] for g in games]
    for id_val in match_ids:
        all_match_ids.append(id_val)

#create master df
all_passes = pd.DataFrame()

#iterate over all matches, parse data,append pass data to master df
for matchidval in all_match_ids:

    print(matchidval)
    #read in events dataframe
    match_data_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{}.json".format(matchidval)
        
    all_events = requests.get(url=match_data_url.format(matchidval)).json()
    event_df = pd.DataFrame(all_events)
    
    #iterate over rows and create new cols 
    event_df["event"]=""
    event_df["team"]=""
    event_df["player_name"]=""
    
    for index, row in event_df.iterrows():
        event_df.at[index,'event'] = row['type']['name']
        event_df.at[index,'team'] = row['possession_team']['name']
        
        if str(row['player']) != "nan":
            event_df.at[index,'player_name'] = row['player']['name']   
     
    #filter to just passes       
    pass_df = event_df[(event_df["event"]=="Pass")]
    
    pass_df["start_x"]=""
    pass_df["start_y"]=""
    pass_df["end_x"]=""
    pass_df["end_y"]=""
    pass_df["outcome"] = ""
    pass_df["length"]=""
    pass_df["angle"]=""
    pass_df["height"]=""
    pass_df["backheel"]=""
    pass_df["deflected"]=""
    pass_df["cross"]=""
    pass_df["cut_back"]=""
    pass_df["switch"]=""
    pass_df["body_part"]=""
    pass_df["type"]=""
    pass_df["technique"]=""
    pass_df["pressure"]=""
        
    for index, row in pass_df.iterrows():
        pass_df.at[index,'start_x'] = row['location'][0]
        pass_df.at[index,'start_y'] = row['location'][1]
    
        pass_df.at[index,'end_x'] = row['pass']['end_location'][0]
        pass_df.at[index,'end_y'] = row['pass']['end_location'][1]
        
        if "outcome" in row['pass']:
            pass_df.at[index,'outcome'] = 0
        else:
            pass_df.at[index,'outcome'] = 1
        
        if 'type' in row['pass']:
            pass_df.at[index,'type'] = row['pass']['type']['name']
        else:
            pass_df.at[index,'type'] = "Normal"
    
        if 'technique' in row['pass']:
            pass_df.at[index,'technique'] = row['pass']['technique']['name']
        else:
            pass_df.at[index,'technique'] = "Normal"
        
        if "body_part" in row['pass']:
            pass_df.at[index,'body_part'] = row['pass']['body_part']['name']
        else:
            pass_df.at[index,'body_part'] = "N/A"
            
        pass_df.at[index,'height'] = row['pass']['height']['name']
        
        pass_df.at[index,'length'] = row['pass']['length']
        pass_df.at[index,'angle'] = row['pass']['angle']
        
        if row["under_pressure"] == True:
            pass_df.at[index,'pressure'] = 1
        else:
            pass_df.at[index,'pressure'] = 0
        
        if "backheel" in row['pass']:
            pass_df.at[index,'backheel'] = 1
        else:
            pass_df.at[index,'backheel'] = 0
            
        if "deflected" in row['pass']:
            pass_df.at[index,'deflected'] = 1
        else:
            pass_df.at[index,'deflected'] = 0
    
        if "cross" in row['pass']:
            pass_df.at[index,'cross'] = 1
        else:
            pass_df.at[index,'cross'] = 0
            
        if "cut_back" in row['pass']:
            pass_df.at[index,'cut_back'] = 1
        else:
            pass_df.at[index,'cut_back'] = 0
    
        if "switch" in row['pass']:
            pass_df.at[index,'switch'] = 1
        else:
            pass_df.at[index,'switch'] = 0
       
    
    details = ['id','player_name', 'team','start_x',
               'start_y', 'end_x', 'end_y', 'outcome',
               'length','angle','height','backheel','deflected',
               'cross','cut_back','switch','body_part','type','technique',
               'pressure']
        
    pass_details = pass_df[details]
    
    all_passes = all_passes.append(pass_details)
    
all_passes.to_csv("sb_passes.csv")