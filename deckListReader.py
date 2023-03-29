# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 01:03:29 2023

@author: Mason Muniz
"""

import requests

def retrieveBanList(banlistFile,limitedlistFile,semilimitedlistFile):
    
    #make the request
    request = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php?banlist=tcg")
    
    #check the status code
    if (not request.status_code == 200):
        print("Error in request status=> " + request.status_code)

    banlist = request.json()
    banlistNames = list()
    limitedlistNames = list()
    semilimitedlistNames = list()
    
    #iterate through the json file, pulling out banned, limited, and semi'd cards
    #while setting the strings into a standard format
    for j in range(0,len(banlist['data'])):
        if(banlist['data'][j]['banlist_info']["ban_tcg"] == "Banned"):
            banlistNames.append("".join(banlist['data'][j]['name'].lower().split()))
        elif(banlist['data'][j]['banlist_info']["ban_tcg"] == "Limited"):
            limitedlistNames.append("".join(banlist['data'][j]['name'].lower().split()))
        elif(banlist['data'][j]['banlist_info']["ban_tcg"] == "Semi-Limited"):
            semilimitedlistNames.append("".join(banlist['data'][j]['name'].lower().split()))
    
    #put the card into the file
    for i in banlistNames:
        banlistFile.write(i)
        banlistFile.write("\n")
    
    for i in limitedlistNames:
        limitedlistFile.write(i)
        limitedlistFile.write("\n")
        
    for i in semilimitedlistNames:
        semilimitedlistFile.write(i)
        semilimitedlistFile.write("\n")
        
    return [banlistNames,limitedlistNames,semilimitedlistNames]

def count(deckList):
    count = 0

    for i in deckList.values():
        count += int(i)
        
    return count

def isCountLegal(main, extra, side):
    #get the count of each deck
    mainCount = count(main)
    extraCount = count(extra)
    sideCount = count(side)
    
    #messages we'll append to depending on legality
    mainMessage = "Main deck too "
    extraMessage = "Extra deck too "
    sideMessage = "Side deck too "
    
    #boolean we'll change if anything becomes illegal
    isCountCompliant = True
    
    #test main count
    if mainCount < 40:
        mainMessage += "small => {}".format(mainCount)
        isCountCompliant = False
    elif mainCount > 60:
        mainMessage += "large => {}".format(mainCount)
        isCountCompliant = False
    else:
        mainMessage = "Main deck count legal => {}".format(mainCount);
        
    print(mainMessage)
    
    #test extra count
    if extraCount < 0:
        extraMessage += "small => {}".format(extraCount)
        isCountCompliant = False
    elif extraCount > 15:
        extraMessage += "large => {}".format(extraCount)
        isCountCompliant = False
    else:
        extraMessage = "Extra deck count legal => {}".format(extraCount);
        
    print(extraMessage)
    
    #test side count
    if sideCount < 0:
        sideMessage += "small => {}".format(sideCount)
        isCountCompliant = False
    elif sideCount > 15:
        sideMessage += "large => {}".format(sideCount)
        isCountCompliant = False
    else:
        sideMessage = "Side deck count legal => {}".format(sideCount);
        
    print(sideMessage)
    
    print("\n")
    
    return isCountCompliant
    
def isBanLegal(main,extra,side):
    
    banlistFile = open("banList.txt","w")
    limitedlistFile = open("limitedlist.txt","w")
    semilimitedlistFile = open("semilimitedlist.txt","w")
    
    #retrieve the ban list
    banList = retrieveBanList(banlistFile,limitedlistFile,semilimitedlistFile)
    limitedList = banList[1]
    semiList = banList[2]
    banList = banList[0]
    
    #boolean that we change if we find anything illegal
    isBanCompliant = True
    
    #for each card
    for i,card in enumerate(main.keys()):
        
        #if it's in the ban list
        if card in banList:
            print("Not legal!" + "Banned card detected=> " + card + "\n")
            isBanCompliant = False
        
        #if it's in the limited list
        elif card in limitedList:
            
            #and the subsequent count is illegal
            if main[card] > 1:
                print("Not legal!" + str(main[card]) + 
                      " copies of a limited card detected=> " + card + "\n")
                isBanCompliant = False
        
        #if it's in the semi limited list
        elif card in semiList:
            
            #and the subseqeunt count is illegal
            if main[card] > 2:
                print("Not legal!" + str(main[card]) + 
                      " copies of a semi-limited card detected=> " + card + "\n")
                isBanCompliant = False
    
    #finally, check the boolean to see if we're legal
    if isBanCompliant:
        print("Deck is ban compliant!")
    else:
        print("Deck is NOT ban compliant!")
        
    banlistFile.close()
    limitedlistFile.close()
    semilimitedlistFile.close()
        
    return isBanCompliant
    
    
    
def isLegal(main,extra,side):
    
    isbanLegal = isBanLegal(main,extra,side)
    iscountLegal = isCountLegal(main,extra,side)
    isFullLegal = isbanLegal and iscountLegal
    
    return isFullLegal

if __name__ == "__main__":
    f = open(input("Input file name=> "),"r")
    nextLine = f.readline()
    
    main = dict()
    extra = dict()
    side = dict()
    counter = 0
    
    #boolean we change if something becomes illegal
    isDeckLegal = True
    
    #read the deck list
    while(nextLine != ""):
        
        #assumes a blank line separates each section
        if nextLine == "\n":
            counter += 1
            nextLine = f.readline()
            continue
        
        #assuming our order is main=>side=>extra
        nextLine.strip()
        card = nextLine.split()
        
        #correcting for "3x" or "1x" type format
        if "x" in card[0]:
            card[0] = card[0][0:1]

        #putting the name in a standard format
        name = "".join(card[1:])
        name = name.lower()
        
        #checking if the inidvidual card count is legal
        if int(card[0]) > 3 or int(card[0]) < 1:
            isDeckLegal = False
            print(card[0] + " copies of a card=> " + name + "\n")
        
        #determines which map to add the card to
        if counter == 0:
            main[name] = int(card[0])
        elif counter == 1:
            extra[name] = int(card[0])
        elif counter == 2:
            side[name] = int(card[0])
        
        #set up for next iteration
        nextLine = f.readline()
        
    #check if list is legal
    isDeckLegal = isDeckLegal and isLegal(main,extra,side)
    
    #check the boolean for legality
    if isDeckLegal:
        print("Deck list is legal!")
    else:
        print("Deck list is NOT legal!")
    
    f.close()