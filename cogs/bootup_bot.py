import discord
from discord.ext import commands
from discord import app_commands
import boto3
from dotenv import load_dotenv
import os
import math

# Channels in category
# format - [category-name, text-channel, text-channel, text-channel, text-channel, voice-channel]
# put a t in front of a text channel to indicate it is a text channel. i.e. tchannel1
# put a v in found of a voice channel to indicate it is a voice channel. i.e. vchannel1

PATH = os.getcwd() + "/cogs/bootup/"
rPATH = os.getcwd() + "/cogs/"

verify_channel = ['tinfo', 'tverify']

moderator_channel = ['tcommands',
                     'vmoderator', 'vbroadcast-voice']
help_channel = ['thelp-info', 'ttechnical', 'tforensics',
                'tunity', 'tec2-instance', "tstory", "tother", "twaiting-for-claim", "thelp-log"]
welcome_channel = ['tannouncements', 'tfaq', 'thelp-desk']
cci_channel = ['tcci-info-booth', 'tconnect-booth', 'ttwitter']
sponsor_channel = ['tsponsor-universe']
lounges_channel = ['tcoaches-and-parents', 'vcoaches-and-parents']

all_channels = {
    "VERIFY": verify_channel,
    "MODERATOR": moderator_channel,
    "HELP REQUESTS": help_channel,
    "WELCOME BOOTH": welcome_channel,
    "CCI HEADQUARTERS": cci_channel,
    "LOUNGES": lounges_channel,
    "SPONSOR BOOTH": sponsor_channel
}


class BootCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # internal create channel func
    async def create_channel(self, guild, category_name, channels):
        # creates category with correct perms
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            category = await guild.create_category(category_name)
        await category.set_permissions(guild.default_role, view_channel=False, send_messages=False)
        if category_name == "CCI HEADQUARTERS":
            await category.set_permissions(discord.utils.get(guild.roles, name="Participant"), view_channel=True, read_messages=True, send_messages=False, connect=True, speak=True)
            await category.set_permissions(discord.utils.get(guild.roles, name="Parent/Guardian"), view_channel=True, read_messages=True, send_messages=False, connect=True, speak=True)
            await category.set_permissions(discord.utils.get(guild.roles, name="Coach"), view_channel=True, read_messages=True, send_messages=False, connect=True, speak=True)
        if category_name == "LOUNGES":
            await category.set_permissions(discord.utils.get(guild.roles, name="Parent/Guardian"), view_channel=True, read_messages=True, send_messages=False, connect=True, speak=True)
            await category.set_permissions(discord.utils.get(guild.roles, name="Coach"), view_channel=True, read_messages=True, send_messages=False, connect=True, speak=True)
        if category_name == "SPONSOR BOOTH":
            print("In Progress")
        for channel in channels:
            temp_channel = discord.utils.get(
                category.channels, name=channel[1:])
            if not temp_channel:
                if (channel[0] == "t"):
                    temp_channel = await guild.create_text_channel(channel[1:], category=category)
                    # for initinal verification purposes
                    if temp_channel.name == "verify":
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = True
                        overwrite.read_messages = True
                        await temp_channel.set_permissions(guild.default_role, overwrite=overwrite)
                    elif temp_channel.name == "info":
                        overwrite = discord.PermissionOverwrite()
                        overwrite.send_messages = False
                        overwrite.read_messages = True
                        await temp_channel.set_permissions(guild.default_role, overwrite=overwrite)
                else:
                    await guild.create_voice_channel(channel[1:], category=category)
            else:
                print(f"{channel[1:]} already exists")

    # setup the server, does not include teams
    @app_commands.command(name="setup_server", description="Creates all channels except for teams")
    @app_commands.default_permissions(administrator=True)
    async def setup_server(self, itx: discord.Interaction):
        await itx.response.defer()
        guild = itx.guild

        for key in all_channels.keys():
            channel = all_channels.get(key)
            await self.create_channel(guild, key, channel)

        await itx.followup.send(f"Finished creating server :) {itx.user.mention}")

    # internal create_role function, used for checking if a role has already been made or not
    async def create_role(self, guild, name, hoist, permissions, color):
        name_lower = name.lower()
        if not discord.utils.get(guild.roles, name=name):
            print(f"creating role for {name}")

            return await guild.create_role(
                name=name,
                hoist=hoist,
                permissions=discord.Permissions(permissions),
                colour=discord.Colour(color)
            )
        else:
            print(f"already have a {name} role")

    # Creates server roles
    @ app_commands.command(name="setup_roles", description="Creates all the roles for the server (excludes team roles)")
    @ app_commands.default_permissions(administrator=True)
    async def setup_roles(self, itx: discord.Interaction):
        await itx.response.defer()
        guild = itx.guild

        roles = ["CCI Event Staff", "CCI Technical Staff", "CCI Volunteer",
                 "Parent/Guardian", "Coach", "Participants", ]

        # This is to be used for anyone that should have LIMITED access (can't edit server/channels/roles)
        await self.create_role(guild, "CCI Event Staff", True, 2213666624, 0xFE8C28)
        # Create moderator (tech support) role, if one doesn't already exist
        await self.create_role(guild, "CCI Technical Staff", True, 4294442835, 0xFE8C20)
        # Has same permission as event staff
        await self.create_role(guild, "CCI Volunteer", False, 2213666624, 0xE74C3C)
        # participant role
        await self.create_role(guild, "Participant", True, 36818432, 0xFE3008)
        # parent role
        await self.create_role(guild, "Parent/Guardian", True, 36818432, 0xFE8008)
        # Coach role that allows additional access to ONLY coaches channel, NOT to their teams' channels
        await self.create_role(guild, "Coach", True, 36818432, 0xAEBDFF)

        await itx.followup.send("Finished Creating Essential Roles!")

    # Delete all team text and voice channels
    @ app_commands.command(name="reset_teams", description="Deletes Every Team Channel")
    @ app_commands.default_permissions(administrator=True)
    async def reset_server(self, itx: discord.Interaction):
        guild = itx.guild
        for channel in guild.channels:
            if "team" in str(channel):
                print(channel, type(str(channel)))
                try:
                    await channel.delete()
                except:
                    print(f'Cannot delete server channel: {channel}')

    # Delete all team text and voice channels
    @ app_commands.command(name="reset_roles", description="Deletes Almost All Roles")
    @ app_commands.default_permissions(administrator=True)
    async def reset_roles(self, itx: discord.Interaction):
        await itx.response.defer()
        for role in itx.guild.roles:
            if "team" in str(role):
                print(role)
                try:
                    await role.delete()
                except:
                    print(f'Cannot delete this role {role}')

        await itx.followup.send(f"Finished resetting roles :) {itx.user.mention}")

    # Creates team channels
    @ app_commands.command(name="setup_teams", description="Create team channels and roles, may be used again to add new teams")
    @ app_commands.default_permissions(administrator=True)
    async def setup_teams(self, itx: discord.Interaction):
        # authenication
        load_dotenv()
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = os.getenv('REGION_NAME')
        session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key, region_name=region_name)

        # specify ddb and table type
        DB_TEAMS = os.getenv('DB_TEAMS')
        dynamodb = session.resource("dynamodb", region_name)
        table = dynamodb.Table(DB_TEAMS)

        # extract table data
        response = table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        # append all team names in list
        teamnames = []
        for i in data:
            teamnames.append(i['teamname'])

        # max 50, /2 for tc and vc
        category_amt = math.ceil(len(teamnames)/25)
        for i in range(0, category_amt):
            category = ''
            # does category exist?
            if discord.utils.get(itx.guild.categories, name=f"TEAM TEXT {i}"):
                category = discord.utils.get(
                    itx.guild.categories, name=f"TEAM TEXT {i}")
            else:
                category = await itx.guild.create_category(name=f"TEAM TEXT {i}")
                await category.set_permissions(itx.guild.default_role, view_channel=False)

            # should it go to the max or cut early because it has no more teams
            condition = 0
            if(i != category_amt-1):
                condition = (i+1)*25
            else:
                condition = len(teamnames)

            # loop through categories and put channels in them
            for j in range((i)*25, condition):
                # formatted team from DB
                print(teamnames[j])
                f_team = teamnames[j].lower().replace(" ", "-")
                # ensure each team has a tc and vc, have a team role that can access it
                temp_role = None
                if not discord.utils.get(category.text_channels, name=f'team-{j}-{f_team}'):
                    try:
                        # Role adding
                        temp_role = await self.create_role(itx.guild, f'team-{j}-{f_team}', True, 36818496, 0xA4D65E)
                        temp_tc = await category.create_text_channel(name=f'team-{j}-{f_team}')

                        await temp_tc.set_permissions(temp_role, view_channel=True, read_messages=True, send_messages=True, connect=True, speak=True, use_application_commands=True)

                    except:
                        print(f'team-{j}-{f_team} Role Exists')
                if not discord.utils.get(category.voice_channels, name=f'team-{j}-{f_team}'):
                    try:
                        temp_vc = await category.create_voice_channel(name=f'team-{j}-{f_team}')
                        await temp_vc.set_permissions(temp_role, view_channel=True, read_messages=True, send_messages=True, connect=True, speak=True)

                    except:
                        print(f'team-{j}-{f_team} Role Exists')

    # Sends messages to the various channels specified
    @ app_commands.command(name="setup_msg", description="Sends all the default messages for channels (i.e. rules in #rules)")
    @ app_commands.default_permissions(administrator=True)
    async def setup_msg(self, itx: discord.Interaction, channel_name: str):
        # takes a while, defer to respond at a later time
        await itx.response.defer(ephemeral=True)
        setup_channels = ["all", "rules", "info"]
        print(setup_channels)
        if channel_name not in setup_channels:
            await itx.followup.send(
                ephemeral=True, content=f"No channels with that name: {channel_name}, {itx.user.mention}")
            return
        elif channel_name == "rules" or channel_name == "all":
            rChan = discord.utils.get(
                itx.guild.text_channels, name="rules")  # rules channel
            f_rules = "**Space Grand Challenge 2022 Rules List**\n"
            f_rules += "*Ethics Statement*\n"
            f_rules += "```- The Space Grand Challenge (SGC) is committed to growing a workforce that values, demonstrates, and models ethical behaviors that are essential to a robust, healthy, and honest working and learning environment. The SGC is dedicated to promoting the Cal Poly vision of day-one ready professionals, and will work to tirelessly promote skills that foster an ethical workforce community.```\n"

            await rChan.send(f_rules)

            await rChan.send("*Rules*\n")  # Formatted rules
            f_rules = ""
            with open(rPATH + "rules.txt", "r") as fR:
                for line in fR:
                    f_rules += "- " + line

            f_rules = f_rules.split("\n")  # split rules

            for i in range(1, len(f_rules)+1, 5):
                sliced_rules = f_rules[i-1:i+4]  # temp slice of rules
                tMsg = ''
                for t in sliced_rules:
                    tMsg += t + "\n\n"
                await rChan.send("```" + tMsg + "```")
        if channel_name == "info" or channel_name == "all":
            chan = discord.utils.get(
                itx.guild.text_channels, name="info")
            await chan.send("To gain access to the see other channels please use ```/verify```\n• **Commands** in this server are predicated with the `/` key, for example use `/verify` to verify yourself to see other channels\n\n• Feel free to browse the other commands once verified by typing `/` and scrolling through!\n\n• **If at anytime you need help getting in message staff!**")

        await itx.followup.send(
            ephemeral=True, content=f"Finished Sending Messages {itx.user.mention}")


async def setup(bot):  # set async function
    await bot.add_cog(BootCog(bot))  # Use await`
