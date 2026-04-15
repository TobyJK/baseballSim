import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pybaseball as pb

def savePitchingData(
        startDate: str = "2025-03-17", 
        endDate: str = "2025-09-29", 
        pitchers: list[str] = ['Cristopher Sánchez', 'Brendon Little', 
                               'Cam Schlittler', 'Yoshinobu Yamamoto', 
                               'Carlos Rodón', 'Max Fried', 'Paul Skenes', 
                               'Tarik Skubal', 'Shohei Ohtani', 'Kodai Senga']
    ) -> None:

    """
    Creates a csv file of statcast pitch data for given pitchers.
    Defaults to data for some set pitchers from the 2025 regular season.

    startDate : YYYY-MM-DD : the first date for which you want data
    endDate : YYYY-MM-DD : the final date for which you want data
    pitchers : List(STR) : the names of pitchers
    """

    correctNames = [x.lower().split(" ")[::-1] for x in pitchers]
    pitcherIDs = [pb.playerid_lookup(x[0], x[1]).key_mlbam.iloc[0] for x in correctNames]

    result = pd.concat([pb.statcast_pitcher(startDate, endDate, x) for x in pitcherIDs])

    result.drop(inplace=True, columns=["game_date", "spin_dir", "spin_rate_deprecated", "break_angle_deprecated", "break_length_deprecated", 
                "game_type", "home_team", "away_team", "tfs_deprecated", "tfs_zulu_deprecated", "umpire", "sv_id", "if_fielding_alignment", "of_fielding_alignment",
                "game_pk", "fielder_2", "fielder_3", "fielder_4", "fielder_6", "fielder_7", "fielder_8", "fielder_9", "des", "game_year",
                "pitcher_days_since_prev_game", "batter_days_since_prev_game", "pitcher_days_until_next_game", "batter_days_until_next_game"])
    
    result.dropna(inplace=True, subset=["pitch_type", "release_speed"])

    result = result[result.pitch_type != "EP"]
    result = result[result.pitch_type != "PO"]

    result.to_csv("stats/data.csv")
