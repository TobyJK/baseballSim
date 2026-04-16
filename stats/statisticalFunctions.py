import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import seaborn as sns
import pybaseball as pb
import scipy.stats as scistats

def getPitcherIDs(
        pitchers: list[str]
) -> list[int]:
    
    """
    Return the mlbam ids of given pitchers from names.

    pitchers : List(str) : the names of pitchers in 'Firstname Surname'
    """

    correctNames = [x.lower().split(" ")[::-1] for x in pitchers]
    pitcherIDs = [pb.playerid_lookup(x[0], x[1]).key_mlbam.iloc[0] for x in correctNames]

    return pitcherIDs

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
    pitchers : List(STR) : the names of pitchers in 'Firstname Surname'
    """

    pitcherIDs = getPitcherIDs(pitchers)

    result = pd.concat([pb.statcast_pitcher(startDate, endDate, x) for x in pitcherIDs])

    result.drop(inplace=True, columns=["game_date", "spin_dir", "spin_rate_deprecated", "break_angle_deprecated", "break_length_deprecated", 
                "game_type", "home_team", "away_team", "tfs_deprecated", "tfs_zulu_deprecated", "umpire", "sv_id", "if_fielding_alignment", "of_fielding_alignment",
                "game_pk", "fielder_2", "fielder_3", "fielder_4", "fielder_6", "fielder_7", "fielder_8", "fielder_9", "des", "game_year",
                "pitcher_days_since_prev_game", "batter_days_since_prev_game", "pitcher_days_until_next_game", "batter_days_until_next_game"])
    
    result.dropna(inplace=True, subset=["pitch_type", "release_speed"])

    result = result.loc[result.pitch_type != "EP"]
    result = result.loc[result.pitch_type != "PO"]

    result.to_csv("stats/data.csv")

def adjustPitchHeight():
    pass

def plotPitches(
        pitcherIDs: list[int],
        pitchTypes: list[str]
) -> None:
    
    data = pd.read_csv("stats/data.csv")
    correctData = data.loc[data["pitch_type"].isin(pitchTypes) & data["pitcher"].isin(pitcherIDs)]
    # correctData = correctData.loc[correctData["description"].isin(["called_strike", "ball"])]

    print(correctData.loc[:, "plate_x"].mean(), correctData.loc[:, "plate_z"].mean())

    _, axis = plt.subplots()
    sns.scatterplot(data=correctData, x="plate_x", y="plate_z", hue="description", style="description", ax=axis)

    axis.add_patch(patches.Rectangle((-0.831, 1.524), 2*0.831, 2.149,
                 edgecolor = 'lightgray',
                 fill=False,
                 lw=3,
                 zorder = 0.1))

    plt.show()

    sns.kdeplot(data=correctData, x="plate_x")
    plt.show()

    sns.kdeplot(data=correctData, y="plate_z")
    plt.show()

    sns.displot(correctData, x="plate_x", kind="ecdf")
    plt.show()

    sns.displot(correctData, x="plate_z", kind="ecdf")
    plt.show()

    print(scistats.normaltest(correctData["plate_x"]))
    print(scistats.normaltest(correctData["plate_z"]))

    scistats.probplot(correctData["plate_x"], dist="norm", plot=plt)
    plt.show()

    scistats.probplot(correctData["plate_z"], dist="norm", plot=plt)
    plt.show()
