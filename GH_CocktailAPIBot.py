import discord
import os
"""importing module to make http requets"""
import requests
"""Importing module to print qr code to command line"""
#import qrcodeT
#import json
import logging

listUrlBase =  "http://www.thecocktaildb.com/api/json/v1/1/search.php?f="
drinkUrlBase = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s="
idUrlBase = "http://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="

def start():
  intents = discord.Intents.default()
  intents.message_content = True

  client = discord.Client(intents=intents)

  @client.event
  async def on_read():
    print("Logged in and ready, sir")

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    #-----------------------------------------
    if message.content.startswith('BB'):
      await message.channel.send('At the ready sir! If you\'d like to interact enter: \"$menu\".')
   
    #-----------------------------------------  
    elif message.content.startswith('$menu'):
      await message.channel.send("Options:\nList of drinks by letter - $list (letter here)\nSee if I know how to make that drink - $drink (drink name here)\nHow to make a drink - $(name of drink here)")
    
    #-----------------------------------------
    elif message.content.startswith('$list'):
      print("Received message from - " + str(message.author) + " - \"" + str(message.content) + "\"")
      try:
        #get input of letter to list drink names
        inLetter = message.content.replace("$list ", "")
        inLetter.replace(" ", "")
        print("looking for - " + inLetter)

        #concatenate the letter to the listUrl base to complete the URL
        listUrl = listUrlBase + inLetter
        print(listUrl)

        #begin URL lookup
        response = requests.get(url=listUrl)
        print(response)

        #if successful print to console that we fetched data
        if response.status_code == 200:
            print("sucessfully fetched the data")

            #load the json response to a variableto iterate through
            drinks = response.json()

            #iterate through the array value and lists the names of the drinks
            dList = []
            for i in drinks.get("drinks"):
                dList.append(i.get("strDrink"))

            #return the list
            print(dList)
            await message.channel.send(str(dList))

      except requests.exceptions.RequestException as e:
          await message.channel.send("Sorry sir, I seemed to have misplaced the list.")
          print(e)

    #-----------------------------------------
    elif '$drink' in message.content:
      print("Received message from - " + str(message.author) + " - \"" + str(message.content) + "\"")
      try:
        #get input of name of drink
        inDrink = message.content.replace("$drink ", "")
        inDrink.replace(" ", "")
        print("looking for - " + inDrink)

        #concatenate the letter to the searchUrl to complete the URL
        drinkUrl = drinkUrlBase + inDrink

        #begin lookup
        response =requests.get(url=drinkUrl)

        #if succesful print to console that we fetched data
        if response.status_code == 200:
            drinks = response.json()
            
            if drinks.get("drinks") == None:
                await message.channel.send("Sorry, I don't have that on my list.")
                return
            else:
                #iterate through list and return an array with names and ids for drinks
                dList = []
                for i in drinks.get("drinks"):
                    newObj = {
                        "strDrink" : i.get("strDrink"),
                        "idDrink" : i.get("idDrink")
                    }

                    dList.append(newObj)

                #return names of drinks found
                await message.channel.send("Here's what I know how to make sir, (this may take a second)")
                for i in dList:
                    await message.channel.send(i.get("strDrink"))
                
                #ask if there is a drink they want
                await message.channel.send("If any of these suit your fancy, please enter that name as \"$(name here)\"")
        else:
            await message.channel.send("I'm afraid, sir, that is not one of the drinks listed here.")
      except requests.exceptions.RequestException as e:
          await message.channel.send("Sorry sir, I seemed to have misplaced my menu.")
          print(e)

    #---------------------------------------------
    elif message.content.startswith('$'):
      print("Received message from - " + str(message.author) + " - \"" + str(message.content) + "\"")
      
      try:
        #get input of name of drink
        inDrink = message.content.replace('$', '')
        print("looking for - " + inDrink)

        #concatenate the letter to the searchUrl to complete the URL
        drinkUrl = drinkUrlBase + inDrink

        #begin lookup
        response =requests.get(url=drinkUrl)

        #if succesful print to console that we fetched data
        if response.status_code == 200:
            drinks = response.json()
            
            #if the json response is empty that means that the drink is not included in our list
            if drinks.get("drinks") == None:
                await message.channel.send("Sorry, I don't have that on my list.")

            #with a response with actual drinks listed we can look through that list for the drink we want
            else:
                #iterate through list and add to an array with names and ids for drinks
                dList = []
                for i in drinks.get("drinks"):
                    newObj = {
                        "strDrink" : i.get("strDrink"),
                        "idDrink" : i.get("idDrink")
                    }
                    dList.append(newObj)

                #this will cause the next check to exit if we were not able to find the drink in our list
                foundId = -1
                
                for i in dList:
                    if (i.get("strDrink").lower() == str(inDrink)):
                        foundId = i.get("idDrink")
                
                #return with found information if Id is matched
                if foundId != -1:
                    await message.channel.send("Indeed sir, info coming right up! (this may take a second)")
                    idUrl = idUrlBase + str(foundId)

                    try:
                        response = requests.get(url=idUrl)
                        
                        if response.status_code == 200:
                            drinks = response.json().get("drinks")
                            drink = drinks[0]
                            
                            await message.channel.send("Ingredients are - ")
                            for i in range(15):
                                x = i+1
                                ing = drink.get("strIngredient" + str(x))
                                msr = drink.get("strMeasure" + str(x))

                                if (ing == None):
                                    break
                                if (msr == None):
                                    await message.channel.send(str(ing))
                                else:
                                    await message.channel.send(str(msr) + " " + str(ing))
                            
                            await message.channel.send("Here is how to make the drink -")
                            await message.channel.send(drink.get("strInstructions"))
                    except requests.exceptions.RequestException as e:
                      await message.channel.send("Sorry sir, I seemed to have misplaced my menu.")
                      print(e)  

                else:
                  await message.channel.send("Sorry can you be more specfic? Try using \"$drink " + inDrink + "\" to see if I know that drink.")
      except requests.exceptions.RequestException as e:
        await message.channel.send("Sorry sir, I seemed to have misplaced my menu.")
        print(e)  

  #To run this code, enter bot token below (may need to add '\n' to the end as well)
  client.run('#################################################')