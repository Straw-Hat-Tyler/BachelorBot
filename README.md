# BachelorBot
Discord Bot that returns Cocktail ingredients and recipes

This code, while running, will have the Bot user make calls to the CocktailAPI and return messages to the Discord channel with ingredients and a recipe. The calls make take up to a few seconds to process while returngin long lists of ingredients or drink names. Please note that you will need to fill in the Bot token at the bottom of the file.

The bot responds to the commands below (entering a message that starts with "$menu" will cause the bot to return a similar message),

  Pulsecheck - if message starts with "BB" -> returns a message to confirm if Bot is active
  List of drinks by letter - if message starts with "$list (letter here)" -> returns a list of drinks using the (letter) provided
  See if I know how to make that drink - if message starts with "$drink (drink name here)" -> returns a list of drinks using the (drink name) provided
  How to make a drink - if message contains "$(name of drink here)" -> returns ingredients and recipe*

*be aware that this will catch ALL messages sent that start with '$'. Though the Bot will not crash it may interject to tell you it doesn't know how to make that drink (and let me know if does, the command line should give some insight)
