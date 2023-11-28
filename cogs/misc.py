import discord
from discord import app_commands
from discord.ext import commands


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Pong, sends the bots latency")
    @app_commands.default_permissions(administrator=False)
    async def ping(self, itx: discord.Interaction):  # ping for latency, !ping
        await itx.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')

    @app_commands.command(name="purge", description="Purge the amount of messages you would like")
    @app_commands.default_permissions(administrator=True)
    async def purge(self, itx: discord.Interaction, amount: int):
        await itx.channel.purge(limit=amount)
        await itx.response.send_message(f"{itx.user.mention} Purged {amount} messages")

        # display server stats in a cool way
    @app_commands.command(name="server", description="Server stats")
    async def server(self, itx: discord.Interaction):
        embed = discord.Embed(
            title=f"{itx.guild.name} Info", description="Information of this Server", color=discord.Colour.blue())
        embed.add_field(name='🆔Server ID',
                        value=f"{itx.guild.id}", inline=True)
        embed.add_field(name='📆Created On', value=itx.guild.created_at.strftime(
            "%b %d %Y"), inline=True)
        embed.add_field(name='👑Owner', value=f"{itx.guild.owner}", inline=True)
        embed.add_field(name='👥Members',
                        value=f'{itx.guild.member_count} Members', inline=True)
        embed.add_field(
            name='💬Channels', value=f'{len(itx.guild.text_channels)} Text | {len(itx.guild.voice_channels)} Voice', inline=True)
        embed.add_field(
            name='🌎Region', value=f'{"United States :flag_us:"}', inline=True)
        embed.set_thumbnail(url=itx.guild.icon)
        embed.set_footer(text="⭐ • Have a nice Day • ⭐")
        embed.set_author(name=f'{itx.user.name}',
                         icon_url=itx.user.display_avatar.url)
        await itx.response.send_message(embed=embed)
        
    @app_commands.command(name="commands", description="Returns a description for each command.")
    @app_commands.default_permissions(administrator=False)
    async def ping(self, itx: discord.Interaction):  # ping for latency, !ping
        embed = discord.Embed(
            title=f"Command Information", description="Information about each command.", color=discord.Colour.blue())
        embed.add_field(name='Welcome Commands',
                        value="• /verify - Creates a embed that allows users to enter in a email.", inline=False)
        embed.add_field(name='Help Commands',
                        value="• /help_message - Creates a embed that allows users to submit a help request.\n• /queue - Returns their position in the queue.", inline=False)
        #embed.add_field(name='Setup Commands',
        #                value="• /setup_server - Will create all static channel for the server. This does not include the team channels.\n• /create_roles - Will create all roles for the server. These roles include: CCI Event Staff, CCI Technical Staff, CCI Volunteer, Parent/Guardian, Coach, Participant.\n• /reset_server - Will delete all channels, and catagories except #general.\n• /setup_teams - Will create text and voice channels for each team in the DDB table, will also add new teams.\n• /setup_msg - Sends all the default messages for channels (i.e. rules in #rules)", inline=False)
        embed.add_field(name='Misc Commands',
                        value="• /ping - Get latency of bot.\n• /commands - Displays all commands.", inline=False)
        activeservers = itx.guild.text_channels
        for i in activeservers:
            print(i)
        await itx.response.send_message(embed=embed)
        
async def setup(bot):  # set async function
    await bot.add_cog(MiscCog(bot))  # Use await

