# Space Grand Challenge - Discord Support
The main purpose of the SGC Discord Server is to provide competitors with support during the competition. Whether its handling registration issues or accessing specific resources. Our goal as moderators of the discord server is to help with any issues experienced pre, during, and post competition.

## Pre-Competition
During this phase, most of the support will involve helping students and coaches register both on the application and the discord server. Since the competition hasn't started, you will and should not expect competitors to be asking for help regarding the competition logistics.

Before the competition begins, ensure that all the correct permissions are set for each of the channels. The main goal should be to moderate the participants so that they are not able to spam any of the channels. In CCIC 2020, we had an instance were all participants began spamming the #helpdesk channel and it became an absolute mess to moderate. So try to avoid something like that from occurring.

Here are some of the requests to expect:
- Competitor/Coach is having trouble creating an account on the SGC web application.
    - Solution: Check if their email is correctly registered on the DynamoDB table representing the users of the application.
- Competitor/Coach did not receive the verification email after creating an account on the SGC web application.
    - Solution: Check if the lambda function in the AWS backend handling account creations is working correctly. Logs are your friend on this one. 
- Competitor cannot access the prequalifications page.
    - Solution: If the prequalification page is locked, then there must be some set time on the DynamoDB table with the name challengeDetails containing an incorrect timeframe.
- Competitor cannot access the prequalification unity room.
    - Solution: This could either be on the user's end or our end. If the user has a system with lower hardware specs than necessary, then there's not a lot we can do on our end besides giving them the flag. If its our end having the issue, then contact the Unity team to troubleshoot the issue.
- Competitor wants to replace a teammate.
    - Solution: Based on our current rules, we cannot replace teammates after registration. But make sure to double-check in case those rules have changed.
- Competitor wants their name changed on the Discord server:
    - Solution: You can change the competitor's nickname on discord, whenever they register through the WelcomeBot, the bot will modify their nickname on the server. If competitors want this change for privacy reasons, then I would contact a higher up to identify if this request should be given or not.
- Competitor is having issues with the discord WelcomeBot.
    - Solution: Typically this occurs when the competitor is attempting to register into their team channel, verify if the email is correct or not.

## During Competition
The infamous competition! This is where the support can get a little hectic as teams begin their investigations of the evidence! You will receive a lot of different types of requests that will either be easy to answer or hard to troubleshoot, so be absolutely perpared for anything technical or story related.

Here are some of the many requests to expect:
- Competitor cannot access EC2 instance.
    - Solution: If competitor does not know how to connect, refer them to a how-to-guide on remote desktop and connecting to ec2 instances. If the instance is faulty, contact the AWS team for troubleshooting.
- Competitor cannot access Unity rooms.
    - Solution: This could either be on the user's end or our end. If the user has a system with lower hardware specs than necessary, then there's not a lot we can do on our end besides having another one of their teammates with higher specs to take on the rooms. If its our end having the issue, then contact the Unity team to troubleshoot the issue.
- Competitor cannot access either analysis or locations page.
    - Solution: If competitors are locked out from these pages then the time set for the challenge in the DynamoDB `challengeDetails` table must be incorrect. You can fix this through the Admin page on the web application.
- Competitor is stuck on a challenge.
    - Solution: While there are chances for receiving hints for point reductions, if the team is extremely stuck and cannot figure it out, then you may help them by giving them a hint. But in a typical case, let them know they can request a hint.
- Competitor believes score is incorrect.
    - Solution: Double-check that our scoring system is working, if not then make sure to check the lambdas responsible for score changes. In the past, we've had issues where scores aren't accounted for one section of the challenge, so please double check all is working correctly.

## Post Competition 
Once the competition ends, there will be a lot requests asking about the scoring of the competition. Typically we do not send around scores to keep competitors from fighting for their score. But if things change, then follow the new protocols the higher ups set. 

Besides that, there won't be a lot of requests going through since the competition will be over. So you can start turning off the HelpBot and locking all the channels down so that no one but the moderators can comment/send messages. 
