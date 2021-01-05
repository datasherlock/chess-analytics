#!/usr/bin/env python
# coding: utf-8

#Import libraries

import re
import pandas as pd
import os
import requests
import json
import urllib.request
from pathlib import Path


#Declare Globals
pgnMeta = ["Event","Site","Date","Round","White","Black","Result", \
            "CurrentPosition","Timezone", "ECO","ECOURL","UTDate","UTCTime","WhiteELO", \
            "BlackELO","Timecontrol","Termination","StartTime","EndDate","EndTime","Link","Moves"]
tgtFilePath="./Documents/mygames.csv" #This is the path where the final CSV gets created
moveStartLine = 22 #Moves in chess.com PGNs typically start from the 22nd line for each game
PGNDirectory="./Documents/PGN" #This is the location where the API downloads the PGNs from the archives
user='datasherlock' #The user for whom the script is intended to run


def getPGN(user):
    """This function accesses the chess.com public API and downloads all the PGNs to a folder"""
    pgn_archive_links = requests.get("https://api.chess.com/pub/player/"+user+"/games/archives", verify=False)
    if not os.path.exists(PGNDirectory):
        os.makedirs(PGNDirectory)

    for url in json.loads(pgn_archive_links.content)["archives"]:
        filepath = PGNDirectory + "/"+ url.split("/")[7]+url.split("/")[8]+'.pgn'
        my_file = Path(filepath)
        if not my_file.is_file():
            urllib.request.urlretrieve(url+'/pgn',filepath)

def importPGNData(filepath):
    """This function returns the data read as a string"""
    with open(filepath) as f:
        return f.readlines()

def getEdgePoints(data):
    """This function returns the start and end indices for each game in the PGN"""
    ends=[]
    starts=[]
    for n,l in enumerate(data):
        if l.startswith("[Event"):
            if n!=0:
                ends.append(n - 1)
            starts.append(n)
        elif (n==len(data)-1):
            ends.append(n)

    return (starts,ends)


def grpGames(data, starts, ends):
    """This function groups games into individual lists based on the start and end index"""
    blocks=[]
    for i in range(len(ends)):
        try:
            element = data[starts[i]: ends[i]+1]
        except:
            print(i)
        if element not in blocks: blocks.append(element)
    return blocks

def mergeMoves(game):
    """This function cleans out the moves and other attributes, removes newlines and formats the list to be converted into a dictionary"""
    firstmove=lastmove=-1
    for n,eachrow in enumerate(game):
                game[n]=game[n].replace('\n','')
                try:
                    if n <= moveStartLine-2: game[n] = stripwhitespace(game[n]).split('~')[1].strip(']["')
                except:
                    if n <= moveStartLine-4: game[n] = stripwhitespace(game[n]).split('~')[1].strip(']["')
                    pass
    return list(filter(None,game))


def stripwhitespace(text):
    lst = text.split('"')
    for i, item in enumerate(lst):
        if not i % 2:
            lst[i] = re.sub("\s+", "~", item)
    return '"'.join(lst)

def createGameDictLetsPlay(game_dict):
    """This is a helper function to address games under Lets Play events on chess.com. These events have a slightly different way of representation than the Live Chess events"""
    for n, move in enumerate(game_dict["Moves"].split(" ")):

        if n%3==0: #every 3rd element is the move number
            if move == '1-0' or move=='0-1' or move=='1/2-1/2':
                None
            else: movenum = n
        elif n==movenum+2:
            if move == '1-0' or move=='0-1' or move=='1/2-1/2':
                None
            else: game_dict["whitemoves"].append(move)
        else:
            if move == '1-0' or move=='0-1' or move=='1/2-1/2':
                None
            else: game_dict["blackmoves"].append(move)

    if len(game_dict["blackmoves"])>len(game_dict["whitemoves"]): game_dict["whitemoves"].append("over")
    if len(game_dict["blackmoves"])<len(game_dict["whitemoves"]): game_dict["blackmoves"].append("over")
    del game_dict["Moves"]
    return game_dict


def createGameDictLiveChess(game_dict):
    """This is a helper function to address games under Live Chess events on chess.com."""
    try:
        for n, move in enumerate(game_dict["Moves"].split(" ")):

            if '{' in move or '}' in move:
                None
            elif '.' in move:
                movenum = int(move.split(".")[0])
                if "..." in move:
                    color = 'black'
                else: color="white"
            else:
                if color=="white":
                    if move == '1-0' or move=='0-1' or move=='1/2-1/2': None
                    else: game_dict["whitemoves"].append(move)
                else:
                    if move == '1-0' or move=='0-1' or move=='1/2-1/2': None
                    else: game_dict["blackmoves"].append(move)

        if len(game_dict["blackmoves"])>len(game_dict["whitemoves"]): game_dict["whitemoves"].append("over")
        if len(game_dict["blackmoves"])<len(game_dict["whitemoves"]): game_dict["blackmoves"].append("over")
        del game_dict["Moves"]
    except: pass

    return game_dict


def createGameDict(games):
    allgames=[]
    for gamenum, eachgame in enumerate(games):
        game_dict = dict(zip(pgnMeta, eachgame))
        movenum = 0
        game_dict["whitemoves"] = []
        game_dict["blackmoves"] = []
        color="white"
        if game_dict["Event"]=="Let's Play!": allgames.append(createGameDictLetsPlay(game_dict))
        else: allgames.append(createGameDictLiveChess(game_dict))

    return allgames



def main():
    getPGN(user)
    tgtFilePathObj = Path(tgtFilePath)
    tgtFilePathObj.unlink(missing_ok=True)

    with os.scandir(PGNDirectory) as pgndir:
        for file in pgndir:
            print('*', end =" ")
            data = importPGNData(file)

            starts, ends = getEdgePoints(data)
            games = grpGames(data, starts, ends)
            games = list(map(mergeMoves, games))
            allgames= createGameDict(games)

            for gamenum, game in enumerate(allgames):
                df = pd.DataFrame(allgames[gamenum])

                with open(tgtFilePath, 'a') as f:
                    df.to_csv(f, mode='a', header=f.tell()==0)
    print("Export Complete!")

#Run Program
main()
