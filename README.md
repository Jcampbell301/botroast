# GroupMe-Bot
GroupMe Bot that does different things when pinged with different commands.

## Registration
A GroupMe Bot can be created [here](https://dev.groupme.com/docs/v3). Creation of a bot gives the option of a callback URL. In order to bestow your bot with the functionality found within this repo, the callback URL should be the following:
```
http://groupmebot-stage.herokuapp.com/callback/<BOT_ID>
```
Once created, the bot can be registered [here](http://groupmebot-stage.herokuapp.com/register). Once registered, the bot will be functional within your group.

You are able to register more than one bot, which all must created through the GroupMe service and consequently have unique Bot IDs. In addition, you are able to change the Group ID of an existing bot by simply entering in the same information with the new Group ID at the registration page. The Bot's information will be updated. Be sure to update the Bot's information within the GroupMe service, otherwise there will be unknown and unintended consequences.

## Functionality/Commands
This Bot does some things. Functionality is still quite limited but the developer's ambitions are quite large.

+ `!help` - List available commands.
+ `!burn` - Posts a link to a list of burn centers. Especially useful after roasting another user.
+ `!since <String>` - Returns the amount of time since the last instance of the given String. Good tool for Pavlovian endeavors.
+ `!history` - Computes statistics and renders graphs regarding the history of this group.
+ `!spell <User>` - Not yet implemented. Checks the spelling of the given user's last message.
+ `!roast <User>` - Not yet implemented. Roasts the given user.
+ `!add_roast <String>` - Not yet implemented. Adds given roast to database of roasts.
+ `!impersonate <User>` - Not yet implemented. Impersonates the given user by quoting one of their past messages.
+ `!mood <User>` - Not yet implemented. Runs a sentiment analysis on the user's last message.

# Analytics
The Bot's `!history` command has been isolated as a standalone service found [here](http://groupmebot-stage.herokuapp.com/analyze). Only your Access Token and Group ID are needed: no bot registration is needed. After analysis, you will be redirected to a page with analytics displayed, and this webpage can be accessed by anyone with the url. Any conclusions regarding the dynamic within the group are NOT MINE. These are just stats, not Freudian diagnoses. 

Here is an example of one of my own group chats: [http://groupmebot-stage.herokuapp.com/analytics/19428404](http://groupmebot-stage.herokuapp.com/analytics/19428404)
