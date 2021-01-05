#!/usr/bin/env python
# coding: utf-8

# In[115]:


import re
import pandas as pd
import os
import requests
import json
import urllib.request
from pathlib import Path


# In[69]:


#Globals

#filepath = "./Documents/apichess.pgn"
pgnMeta = ["Event","Site","Date","Round","White","Black","Result","CurrentPosition","Timezone",            "ECO","ECOURL","UTDate","UTCTime","WhiteELO","BlackELO","Timecontrol","Termination","StartTime","EndDate","EndTime","Link","Moves"]
tgtFilePath="./Documents/mygames.csv"
moveStartLine = 22
PGNDirectory="./Documents/PGN"
user='datasherlock'


# In[112]:


def getPGN(user):
    pgn_archive_links = requests.get("https://api.chess.com/pub/player/"+user+"/games/archives", verify=False)
    
   
    
    if not os.path.exists(PGNDirectory):
        os.makedirs(PGNDirectory)

    for url in json.loads(pgn_archive_links.content)["archives"]:
        filepath = PGNDirectory + "/"+ url.split("/")[7]+url.split("/")[8]+'.pgn'
        my_file = Path(filepath)
        if not my_file.is_file():
            urllib.request.urlretrieve(url+'/pgn',filepath)


# In[71]:


def importPGNData(filepath):
    with open(filepath) as f:
        return f.readlines()


# In[72]:


def getEdgePoints(data):
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


# In[73]:


def grpGames(data, starts, ends):
    blocks=[]
    for i in range(len(ends)):
        try:
            element = data[starts[i]: ends[i]+1]
        except:
            print(i)
        if element not in blocks: blocks.append(element)        
    return blocks


# In[107]:


def mergeMoves(game):
    firstmove=lastmove=-1
    for n,eachrow in enumerate(game):
                game[n]=game[n].replace('\n','')
                try:
                    if n <= moveStartLine-2: game[n] = stripwhitespace(game[n]).split('~')[1].strip(']["')
                except:
                    if n <= moveStartLine-4: game[n] = stripwhitespace(game[n]).split('~')[1].strip(']["')
                    pass
            
   # moves = ' '.join(game[firstmove:lastmove+2])
   # del game[firstmove:lastmove+2]
   # game.append(moves)
    return list(filter(None,game))


# In[101]:


def stripwhitespace(text):
    lst = text.split('"')
    for i, item in enumerate(lst):
        if not i % 2:
            lst[i] = re.sub("\s+", "~", item)
    return '"'.join(lst)


# In[102]:


def createGameDictLetsPlay(game_dict):
        for n, move in enumerate(game_dict["Moves"].split(" ")):
            
            if n%3==0:
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

        


# In[109]:


def createGameDictLiveChess(game_dict):
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
        


# In[104]:


def createGameDict(games):
    allgames=[]
    for gamenum, eachgame in enumerate(games):
        game_dict = dict(zip(pgnMeta, eachgame))
        movenum = 0
        game_dict["whitemoves"] = []
        game_dict["blackmoves"] = []
        game_dict["Result"]=""
        color="white"
        if game_dict["Event"]=="Let's Play!": allgames.append(createGameDictLetsPlay(game_dict))
        else: allgames.append(createGameDictLiveChess(game_dict))
    
    return allgames
        


# In[122]:


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


# In[124]:


main()


# In[ ]:




