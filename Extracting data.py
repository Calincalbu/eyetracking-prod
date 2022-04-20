# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:57:26 2022

@author: CalinCalbureanu
"""

from matplotlib.font_manager import json_load
import pandas as pd
import os
import matplotlib.pyplot as plt
from functions import *
from Bio.Align import *
from scipy.stats import ttest_rel as ttest
import scipy.stats as stats
from numpy import mean
import json

def getData (f): # Extracting data from csv file with Headers
    os.getcwd()
    headers = ["Sceneid", "Deviceid", "Starttime", "Timestamp", "Status", "GazedObjectName", "Duration", "RightStatus", "RightPupilSize", "LeftStatus", "LeftPupilSize","a"]
    data = pd.read_csv(f, sep=";",names = headers, index_col = "Sceneid")
    del data["a"] # We delete the extra column generated bc of the ; separator
    # Timestamp ; RightPupilSize ; LeftPupilSize - are string variables -- they need to be converted
    # First Timestamp - convertion 
    # NOTE - Timestamp is measured in seconds for that we remove the comma since they might be many seconds
    data["Timestamp"] = [float(x.replace(",",".")) for x in data["Timestamp"]]
    data["RightPupilSize"] = [float(x.replace(',','.')) for x in data ["RightPupilSize"]]
    data["LeftPupilSize"] = [float(x.replace(',','.')) for x in data ["LeftPupilSize"]]

    # Create dictionary with subjects and their specific scenes (3 and 4)
    data3 = data.loc[3]
    data4 = data.loc[4]
    
    return dict({"easy": data3 , "hard" : data4})

def getData2 (f):   # Extracting data from csv files__Date stamp --> 15.03.2022 // 22.03.2022
    os.getcwd()
    headers = ["Sceneid", "Runid", "Deviceid", "Starttime", "Timestamp", "Status", "GazedObjectName", "Duration", "RightStatus", "RightPupilSize", "LeftStatus", "LeftPupilSize"]
    data = pd.read_csv(f, sep=";", names = headers, low_memory = False)
    del data["Runid"]   # We delete the extra column for this new set of data 
    data = data.iloc[1:]    # Header row in data is somehow malformed and not separated by pandas, thus manual review
    
    
    data["Timestamp"] = [float(x.replace(',','.')) for x in data["Timestamp"]] # float() argument must be a string or a number, not generator
    data["RightPupilSize"] = [float(x.replace(',','.')) for x in data ["RightPupilSize"]]
    data["LeftPupilSize"] = [float(x.replace(',','.')) for x in data ["LeftPupilSize"]]
    
    
    # Create dictionary with subjects and their specific scenes (2 and 3)
    data3 = data.loc[data["Sceneid"] == "3"]
    data2 = data.loc[data["Sceneid"] == "2"]
    
    return dict({"easy": data3 , "hard" : data2})

def geteyedata (f): # Create new dataframe for "RightStatus" "RightPupilSize" "LeftStatus" "LeftPupilSize"
    eyedata = f[["Timestamp","RightStatus","RightPupilSize","LeftStatus","LeftPupilSize"]]
    return eyedata




def getdict(f, f2):
    # f is the folder path for the folder that contains all the csv files of the participants
    
    # We iterate through the folder assigning each subject as follows:
        # subj [0] --> Easy scenario ["easy"] --> Alldata ["all"] ; Pupildata ["pupil"](from the easy scenario)
        #        --> Hard scenario ["hard"] --> Alldata ["all"] ; Pupildata ["pupil"](from the hard scenario)
        # subj [1] --> same as above
    
    Datadict = {}
    i = 0
    for j in os.listdir(f):
        #extra
        file = os.path.join(f, j)
        #extra
        Datadict[i] = {}
        Datadict[i]["easy"] = {}
        Datadict[i]["easy"]["all"] = getData(file)["easy"]
        Datadict[i]["easy"]["pupil"] = geteyedata(Datadict[i]["easy"]["all"])
        Datadict[i]["hard"] = {}
        Datadict[i]["hard"]["all"] = getData(file)["hard"]
        Datadict[i]["hard"]["pupil"] = geteyedata(Datadict[i]["hard"]["all"])
        i += 1

    for j in os.listdir(f2):
        file2 = os.path.join(f2, j)
        Datadict[i] = {}
        Datadict[i]["easy"] = {}
        Datadict[i]["easy"]["all"] = getData2(file2)["easy"]
        Datadict[i]["easy"]["pupil"] = geteyedata(Datadict[i]["easy"]["all"])
        Datadict[i]["hard"] = {}
        Datadict[i]["hard"]["all"] = getData2(file2)["hard"]
        Datadict[i]["hard"]["pupil"] = geteyedata(Datadict[i]["hard"]["all"])
        i += 1

    return Datadict

# NOTE --> IPA index function
def regIPA(data): # Registers the IPA index for each participant per scenario
    for i in data:
        data[i]["easy"]["Ripa"] = ipa(list(data[i]["easy"]["pupil"]["RightPupilSize"]),list(data[i]["easy"]["pupil"]["Timestamp"]))
        data[i]["easy"]["Lipa"] = ipa(list(data[i]["easy"]["pupil"]["LeftPupilSize"]),list(data[i]["easy"]["pupil"]["Timestamp"]))
        data[i]["hard"]["Ripa"] = ipa(list(data[i]["hard"]["pupil"]["RightPupilSize"]),list(data[i]["hard"]["pupil"]["Timestamp"]))
        data[i]["hard"]["Lipa"] = ipa(list(data[i]["hard"]["pupil"]["LeftPupilSize"]),list(data[i]["hard"]["pupil"]["Timestamp"]))


def printIPAsubjects(data):
    for i in data:   
        print("Subject", i, ":")
        print("Easy scenario")
        print("IPA RightEye",datar[i]["easy"]["Ripa"],"LeftEye", datar[i]["easy"]["Lipa"],"\n")
        print("Hard scenario")
        print("IPA RightEye",datar[i]["hard"]["Ripa"],"LeftEye", datar[i]["hard"]["Lipa"],"\n")


def statIPA(datar):
    GroupEasyLeft = []
    GroupEasyRight = []
    GroupHardLeft = []
    GroupHardRight = []

    for i in range(11):
        GroupEasyLeft.append(datar[i]["easy"]["Lipa"])
        GroupEasyRight.append(datar[i]["easy"]["Ripa"])
        GroupHardLeft.append(datar[i]["hard"]["Lipa"])
        GroupHardRight.append(datar[i]["hard"]["Ripa"])
    
    # printIPAlists() # -- prints the lists of easy IPA and Hard IPA
    a = [0,1,2,3,4,5,6,7,8,9,10]

    plt.boxplot([GroupEasyLeft,GroupEasyRight,GroupHardLeft,GroupHardRight], labels =["Easy Left","Easy Right","Hard Left","Hard Right"] )
    plt.title("IPA scores")
    plt.show()
    plt.close()

    greasy = GroupEasyLeft + GroupEasyRight
    grhard = GroupHardLeft + GroupHardRight
    plt.boxplot([greasy,grhard], labels=["Easy scenario","Hard scenario"])
    plt.title("IPA scores")
    
    plt.show()

    stat, p = ttest(GroupEasyLeft,GroupHardLeft)
    print('\nLeftPupil:\nStatistics=%.3f, p=%.3f' % (stat, p))
    stats, p2 = ttest(GroupEasyRight,GroupHardRight)
    
    print('\nRightPupil:\nStatistics=%.3f, p=%.3f' % (stats, p2))

    statss, p3 = ttest(GroupEasyLeft+GroupEasyRight,GroupHardLeft+GroupHardRight)
    print('\nRightPupil:\nStatistics=%.3f, p=%.3f' % (statss, p3))
    
    print("mean of GroupEasyLeft is: ", mean(GroupEasyLeft))
    print("mean of GroupEasyRight is: ", mean(GroupEasyRight))
    print("mean of GroupHardLeft is: ", mean(GroupHardLeft))
    print("mean of GroupHardRight is: ", mean(GroupHardRight))
    print("mean of EasyGroup is: ", mean(GroupEasyRight+GroupEasyLeft))
    print("mean of HardGroup is: ", mean(GroupHardRight+GroupHardLeft))

        
# NOTE --> Scan-path functions
def collidercodedict(data): # Gather all existent colliders and assign key letter to each
    colliders = []
    letters = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R' ]
    codedict = {}
    tempdata = data[0]["easy"]["all"]["GazedObjectName"].dropna()

    for i in tempdata:   
        if i in colliders:
            continue
        else:
            codedict[i] = letters[0]
            letters.remove(letters[0])
            colliders.append(i)
        if len(letters) == 0:
            break
    return codedict

def getscanpath(data): # Add the coded scanpath for each recorded scenario per participant
    codedict = collidercodedict(data)
    # NOTE: The below defines collider grouping per letter
    # A = ["TeleportableFloorCollider","TeleportButton"] # -> Movement colliders
    # B = ["Collider","Collider (1)","Collider (2)","Collider (3)","Collider (4)"] # -> Irrelevant colliders
    # C = ["RadarSlider","b_target1","b_target2","TiledMapSlider","TrackedIcon(Clone)","ButtonLogic"] # -> Search colliders
    # D = ["LeverLogic", "TillerLogic", "SteeringWheelLogic","KnobLogic","KnobSwitchLogic"] # -> Steering colliders

    A = ["A","P"]
    B = ["B","D","F","G","Q"]
    C = ["C","J","H","K","L","E"]
    D = ["I","M","N","O","R"]
    for i in data:
        df1 = data[i]["easy"]["all"].replace({"GazedObjectName" : codedict})
        df2 = data[i]["hard"]["all"].replace({"GazedObjectName" : codedict})
        a = df1["GazedObjectName"].dropna()
        astr = ""
        for j in a:
            if j in A:
                astr = astr + "A"
            elif j in B:
                astr = astr + "B"
            elif j in C:
                astr = astr + "C"
            elif j in D:
                astr = astr + "D"
        data[i]["easy"]["Scanpath"] = astr
        b = df2["GazedObjectName"].dropna()
        bstr = ""
        for k in b:
            if k in A:
                bstr = bstr + "A"
            elif k in B:
                bstr = bstr + "B"
            elif k in C:
                bstr = bstr + "C"
            elif k in D:
                bstr = bstr + "D"

        data[i]["hard"]["Scanpath"] = bstr
        
def getsimscore(data): # Adds mean similarity score for each participant per task category (Easy/Hard)
    # NOTE: CAUTION VERY LONG PROCESS --> first participant ~15 min then ~2-3 mins per participant // Per category
    # Approx time ~ 30 mins per category --> approx 1 hour or so in total
    aligner = PairwiseAligner()

    aligner.substitution_matrix = substitution_matrices.load("CALIN")
    score = 0
    for i in data:
        print("Starting align...Subject", i, "Easy scenario")
        simscorelist = []
        for j in data:
            if i == j:
                continue
            print(".")
            alignments = aligner.align(data[i]["easy"]["Scanpath"], data[j]["easy"]["Scanpath"])
            score = aligner.score(data[i]["easy"]["Scanpath"], data[j]["easy"]["Scanpath"])
            simscorelist.append(score)
        data[i]["easy"]["Simscore"] = mean(simscorelist)
    for i in data:
        print("Starting align...Subject", i, "Hard scenario")
        simscorelist = []
        for j in data:
            if i == j:
                continue
            print(".")
            alignments = aligner.align(data[i]["hard"]["Scanpath"], data[j]["hard"]["Scanpath"])
            score = aligner.score(data[i]["hard"]["Scanpath"], data[j]["hard"]["Scanpath"])
            simscorelist.append(score)
        data[i]["hard"]["Simscore"] = mean(simscorelist)
    print("Align Done!")

def scanpathstat(datar):
    scaneasy = []
    scanhard = []
    for i in datar:
        scaneasy.append(datar[i]["easy"]["Simscore"])
        scanhard.append(datar[i]["hard"]["Simscore"])
    print("Mean similarity scores for Easy task:\n")
    print(scaneasy)
    print("Mean similarity scores for Hard task:\n")
    print(scanhard)
    plt.boxplot([scaneasy,scanhard], labels = ["Similarity score easy","Similarity score hard"])
    plt.show()
    stat, p = ttest(scaneasy,scanhard)
    print('\nScanpath:\nStatistics=%.3f, p=%.3f' % (stat, p))
    return scaneasy, scanhard


if __name__ == "__main__":
    # NOTE --> Uncomment for extraction
    # Insert here the folders:
    folder = "Data"
    folder2 = "Data2"

    data = getdict(folder,folder2)

    # NOTE BELOW YOU HAVE THE CODE FOR GETTING THE SIMSCORE
    getscanpath(data)
    getsimscore(data)


    # NOTE ----> Tasks for scanpath stat analysis :
    # 1. Sim score for each participant acrosss all the rest
    # 2. Assign mean sim score for each participant 
    # 3. Seperate easy from hard mean sim score
    # getsimscore(data) function does these tasks and records them into the data dictionary
    # 4. get simscores per easy task vs. hard task
    # 5. create substitution matrix so that more matches for significant colliders mean higher score --> more time spent on important stuff
    # ------> therefore higher cognitive load in hard task vs. easy task
     
    # getsimscore(data) # --> LONG TIME ~1 hour to record meansimscore per participant
    
    
    # NOTE --> IPA Section
    regIPA(data)
    printIPAsubjects(data) # --> prints IPA for each subject Easy vs. Hard

    # Saving Results of analyses to data
    dataresults = {}
    for i in range(len(data)):
        dataresults[i]={}
        dataresults[i]["easy"]={}
        dataresults[i]["hard"]={}
    a = 0
    print(data[0]["easy"]["Ripa"])
    for i in data:
        dataresults[i]["easy"]["Lipa"] = data[i]["easy"]["Lipa"]
        dataresults[i]["easy"]["Ripa"] = data[i]["easy"]["Ripa"]
        dataresults[i]["hard"]["Ripa"] = data[i]["hard"]["Ripa"]
        dataresults[i]["hard"]["Lipa"] = data[i]["hard"]["Lipa"]
        dataresults[i]["easy"]["Simscore"] = data[i]["easy"]["Simscore"]
        dataresults[i]["hard"]["Simscore"] = data[i]["hard"]["Simscore"]
        a += 1
    # Save the results of analysis in a separate file for faster access to statistical analysis
    print('JSON dump \'Results.json\' surpressed for protection.')
    # json.dump(dataresults, open("Results2.json", 'w'))

    datar = json_load("Results2.json") # replace 0,1,2 from string to int
    for i in range(11):
        datar[i] = datar.pop(str(i))
    
    scaneasy, scanhard = scanpathstat(datar) # --> TTest between Easy task similarity scores and Hard task similarity scores
    plt.boxplot([scaneasy, scanhard], labels = ["Easy scenario", "Hard scenario"] )
    plt.title("Scanpath Similarity Scores")
    plt.ylabel("Similarity Score")
    plt.legend()
    plt.show()
    plt.close()

    fvalue, pvalue = stats.f_oneway(scaneasy, scanhard)
    print("Scan-path One-way ANOVA:\nStatistics =%.3f ; p =%.3f" % (fvalue, pvalue))

    statIPA(datar)




    

    
    