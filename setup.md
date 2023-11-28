# Space Grand Challenge - Discord Setup
This readme outlines a very rough draft on how to setup the SGC discord server. A lot of the configurations are done through the bots and other configurations must be done manually. I hope with this guide you should be able to create a server that fits the SGC's needs.

## Categories
Within the server, we separated our channels into specific categories. This was done to help segment each of our channels to help participants understand the general purpose of a specific channel.
- `Moderator`: Holds all the channels that **only** moderators can access. Typically this will be channels geared towards moderator communication and commands for bots.
- `Help Reqests`: Holds all channels relating to catagory of reqeusts.
- `Welcome Booth`: Holds all the competition-related channels for informational purposes. Here we have things such as rules, announcements, FAQs, and resources for competitors to use.
- `CCI Headquarters`: Holds CCI-related channels that promote and inform competitors about our organization as a whole.
- `Sponsor Booth`: Holds any sponsor-related channels for sponsors to use and inform competitors about the company/organization they're representing.
- `Lounges`: Holds channels that coaches and parents may use for communication purposes. Since coaches and parents **cannot** communicate with participants during the competition, we want to still provide them an outlet of communication through our server for any questions.
- `Teams`: Holds the team channels that provide competitors with the abilities to communicate either through voice or text.

## Channels
In the server we have specific types of channels holding a special purpose in the competition, below are each of the unique channels with a description.
- Moderator
  - `commands`: Used for running bot commands.
  - `moderator`: Used for moderator communication.
- Help Requests
  - `waiting-for-claim`: Used for unclaimed help requests to be claimed.
  - `forensics`: Used for any forensics-related HelpBot requests.
  - `technical`: Used for any technical-related HelpBot requests.
  - `unity`: Used for any unity-related HelpBot requests.
  - `ec2-instance`: Used for any ec2-instance-related HelpBot requests.
  - `story`: Used for any story-related HelpBot requests.
  - `other`: Used for any other requests not mention above.
  - `help-log`: logs all help requests
- Welcome Booth
  - `welcome-and-rules`: Rule announcements related to the competition.
  - `announcements`: Any announcements needed to be made to the competition.
  - `how-to-use-bots`: Tutorials for using the Help and Welcome Bots.
  - `faq`: Answers to frequently asked questions by competitors/coaches/etc.
  - `help-desk`: A place for competitors/coaches to ask general questions not specifically related to thier competition involvement.
  - `cool`: Channel for cool links, videos, etc.
  - `resources`: Any resources that may be useful for competitors as they participate in the competition.
- CCI Headquarters
  - `cci-info-booth`: Contains information pertaining to the CCI as an organization and defines what they do as a whole.
  - `connect-booth`: Used as a networking channel for connecting/partnering with the CCI and their mission.
  - `twitter`: Contains all twitter posts made on the original CCI account for competitors to stay updated.
- Sponsor Booth
  - `sponsor-universe`: A channel dedicated towards highlighting the SGC sponsors and so that competitors can connect, or ask any questions to our sponsors.
- Lounges
  - `coaches-and-parents`: A channel for coaches and parents to communicate outside of the competition. Since coaches and parents cannot assist during the competition, we still wanted them to have a platform to communicate amongst themselves.
- Teams - Text and Voice
  - `team-1`: Channel for team 1 competitors so that they are able to communicate and share information during the competition.
  - `team-2`: Channel for team 2 competitors ...
  - ...

## Roles
There are a couple of different roles within the server. Mostly roles pertaining to administrators, participants, and coaches/parents. Below are the different roles and descriptions.
- `Admin`: The highest level moderator in the server. Can run commands on the bots for configuration and modify the server as needed.
- `CCI Technical Staff`: Moderator role with limited permissions, cannot run commands on the bots for configuration. Role is mainly used for more technical support on discord.
- `CCI Event Staff`: Moderator role with limited permissions, cannot run commands on the bots for configuration. This role is mainly used for discord support.
- `CCI Volunteer`: Moderator role for any competition volunteers. Has similar permissions to CCI Event Staff.
- `Coach`: User role for coaches, limits them to specific channels since they cannot participate in the competition. Role cannot access any team channels.
- `Parent`: User role for parents, very similar permissions to coach.
- `Team #N`: User role for competitors in team N. N being an integer ranging from 1 to the number of teams in the competition. This role gives access to team-specific channels for communication purposes.

## Recommended Flow
Now that we have most of the general descriptions out of the way. I will now describe the setup flow that I recommend. That way you don't get stuck and don't do double the work since some of the bots will facilitate the creation of the server.

### 1. Run the Bots
Before you do anything, RUN THE BOTS. Configure the bots by changing the variables in the cogs.  You'll have to run commands so also be sure to have the highest admin role in the server.

AGAIN, RUN THE BOTS before you do anything. 

### 2. Roles
Now that the bots have configured their channels/categories/etc. there should be a couple of roles left to create. Be sure to go through the roles and verify which are missing.

Once the roles are created you can begin configuring the channels.

### 3. Welcome Booth
The Welcome Booth category is one of the more important channels that competitors will rely on throughout the competition. These channels have very specific permissions so be sure to verify on the old server what roles should and should not have access.

Reason being is all competitors are not allowed to write messages in some of the servers. Channels like `announcements` need to be read-only so that important information is only sent and no other messages are present.

### 4. CCI Headquarters
This would be a good next category to setup. Most of these channels are informational so there won't be a lot of communication needed (except for connect-booth if needed) so make sure to set the correct permissions.

Within this category, the `twitter` channel will need an interesting set of configurations. Reason why is because it uses the IFTTT bot.
1. Go to IFTTT and log in/sign up (https://ifttt.com)
2. Go to My Applets
3. Click "New Applet"
4. Click "+ this"
5. Search for and click Twitter
6. Click the "New tweet by a specific user" trigger
7. Enter the Twitter username to watch
8. Click "Create trigger"
9. Click "+ that"
10. Search for "maker" and click "Maker Webhooks"
11. Select the "Make a web request" action (should be the only one)
12. Go to the Discord server and open the Server Settings
13. Go to Webhooks and create a webhook
14. Give it a name, select the channel to post in, and upload an avatar for the bot
15. Copy the webhook URL
16. Go back to IFTTT and paste it into the URL field
17. Select Method: Post
18. Content type: application/json
19. Copy the code below and modify the parts that have "replace_" in them to your liking:
```
{
    "username":"replace_with_bot_displayname", 
    "icon_url":"replace_with_userimage_url", 
    "content":"@{{UserName}} tweeted this at {{CreatedAt}}: {{LinkToTweet}}"
}
```
20. Paste it into the Body field on IFTTT 21. Click Create Action.

### 5. Teams and Coaches
These categories should be configured with the bots. But in case that is not the case, be sure to configure the channels correctly. The bots will rely on the AWS DynamoDB tables for configuration so also make sure those connections are being made to ensure teams and coaches are configured correctly.

### 6. Permissions
Each of the channels have specific permissions in terms of who is allowed to read, or send messages. So make sure to verify that all channels contain the correct permissions per the old server configurations. 
