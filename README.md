# CCI Discord bot 2022

The new SGC discord bots have changed a lot based on its previous versions. The main changes include use of discord COGS, which helped centralize all bots into one bot, the use of discord.py 2.0, which added a lot of ui changes and new interactions like discord modals and buttons, and finally, the use of slash commands.

Here are a general description of what each COG does:

- Welcome COG: Welcomes participants, coaches, and parents into their corresponding roles given a email.
- Help COG: Allows participants to submit a help request to the moderators on Discord.
- Bootup COG: This cog contains all the neccesary commands to start up the server.
- Misc COG: Handles miscallaneous commands, such as !ping.

## Welcome COG
The welcome cog has one command that deploys a embed. It is what participants see when they first enter the server. Participants will enter a email, and the bot will  automatically assign their role (parent, coach, student, event staff) and team from the AWS backend. 

Note: In the competition, it is a prequalification to be registered in the discord server to participate, so this bot MUST work efficiently.

### Commands
- /welcome_message - Creates a embed that allows users to enter in a email.
  - Buttons: Start 

## Help COG
The purpose of this bot is to allow competitors to ask for support during any period of the competition. Upon running the command /help_message, participants will select the type of help they need by clicking on a discord button. Before the competition, participants are only allowed technical help and other help. During the competition, participants are allowed all types of help catagories. Participants will fill out a discord modal with their name, team number, and a description of their problem. 
##Bootup COG

### Configuring the Bot
Here are the different type of help catagories:
- technical: Any technical issues in relation to the registration, setup, or competition resources.
    - Competitor cannot register on the web application.
    - Competitor cannot view their status.
    - Competitor's score is not being updated.
- forensics: Help requests regarding the forensics or analysis side of the competition. Some examples may include:
    - Competitor is having issues with the STK Viewer application.
    - Competitor is stuck in the Autopsy challenge.
    - Competitor can't get Cellebrite Reader to run.
- unity: Any questions or issues regarding the unity side of the competition. Some examples:
    - Competitor is stuck trying to solve a challenge.
    - Competitor finds a game breaking bug in a room.
    - Competitor is having issues accessing a unity room.
- ec2-instance: Any issues or questions regarding the intiation, connection, or use of the ec2 instance. Some examples:
    - Competitor does not know how to connect to their EC2 instance.
    - Competitor is having trouble connecting to the EC2 instance.
    - Competitor's EC2 instance does not appear on the web application.
- story: Any questions or concerns regarding the story of the competition. NOTE: Be careful of giving too much detail away. Direct them in the right direction, do not just give answers.
- other: Any other help requests that are not within the catagories above.

### Commands
- /help_message - Creates a embed that allows users to submit a help request.
- /enable - Unlocks all of the help catagories. (forensics, unity, ec2, story)
- /disable - Disables competition catagories. (forensics, unity, ec2, story)
- /queue - Returns their position in the queue.

### Moderator Side
Upon submiting a help request, the request will show up in the waiting for claim channel. Moderators then click the claim button to claim the request. This will lock the request only to the moderator who clicked the claim button. We only want one moderator working on one request at the same time to avoid multiple moderators working on the same request. Upon clicking the claim button, a embed will appear in the corresponing catagory of help, and you will be given the option to resolve the embed, reject the embed, join voice channel, or join text channel.

## Bootup COG
This cog deals with the technical side of discord, such as creating the neccesary roles, channels, catagories. It is crucial for the setup of the discor server and provides the framework for competitors to request their team roles so that they can communicate with their teammates. 

### Commands
- /server - a pannel that displays information about the server, such as information about the server, created on date, owner of the server, member count, channel count, etc.
- /setup_server - Will create all static channel for the server. This does not include the team channels.
- /create_roles - Will create all roles for the server. These roles include: CCI Event Staff, CCI Technical Staff, CCI Volunteer, Parent/Guardian, Coach, Participant.
- /reset_server - Will delete all channels, and catagories except #general.
- /setup_teams - Will create text and voice channels for each team in the DDB table, will also add new teams.
- /setup_msg - Sends all the default messages for channels (i.e. rules in #rules)


## Bot Setup

1. Install discord modules
    1. boto3 (for aws backend intergration)
    2. dotenv (for hiding sensitive data)
    3. os (for getting sensitive data and cogs)
    4. re (for finding regular expressions)
    5. math (for calculating channels)
1. Install Rapptz discord.py 2.0
    1. ```pip install -U git+https://github.com/Rapptz/discord.py```
1. Obtain .env file for sensitive data (ask contributors)
    1. NEVER SHARE OUTSIDE OF CCI
    1. DO NOT UPLOAD TO GIT
1. Run main bot.py to start bot


## Contributors
