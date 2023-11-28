from modules.help.buttons import problem_buttons
from modules.help import help_list as Team_List

import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="queue", description="Prints the Whole Queue")
    async def queue(self, ctx):
        whole_queue = Team_List.print_queue()
        print(whole_queue)
        if (whole_queue == None) or len(whole_queue) == 0:
            whole_queue = "Queue is currently empty"

        await ctx.response.send_message(whole_queue)
    

    @app_commands.command(name="help_message", description="Display Help Message")
    @app_commands.default_permissions(add_reactions=True)
    async def help_message(self, ctx):
        if Team_List.get_role(ctx.user) == None:
            await ctx.response.send_message(content="You must have a team role to make a request\n" + "Verfiy in the verfiy channel to get a team role", ephemeral=True)
        
        else:
            embed = select_request_embed()
            view = problem_buttons.problem_buttons()
            await ctx.response.send_message(embed=embed, view=view)

def select_request_embed():
    """Creates the embed for the selecting the request"""

    embed = discord.Embed(
        title="SGC Help Bot",
        color=0xbd8b13,
        description='Need Help? Send a help request to a moderator! \nPlease pick a avaliable catagory below.'
    )

    embed.add_field(
        name="__Technical:__",
        value="> Any requests related to technical issues. i.e. Account, Discord, Pre-Qualifications, Website, etc.",
        inline=False
    )

    embed.add_field(
        name="__Forensics:__",
        value="> Any requests related to the forensics challenge.",
        inline=False
    )

    embed.add_field(
        name="__Unity:__",
        value="> Any requests related to the unity rooms challenges.",
        inline=False
    )

    embed.add_field(
        name="__ec2-instance:__",
        value="> Any requests related to your ec2 instance.",
        inline=False
    )

    embed.add_field(
        name="__Story:__",
        value="> Any requests related to the story of the challenge.",
        inline=False
    )

    embed.add_field(
        name="__Other:__",
        value="> Other General Requests.",
        inline=False
    )

    embed.add_field(
        name="__Additional features__",
        value="cancel request: Found in your teams text channel at the time of the request.\nplace in queue: **/queue** command",
        inline=False
    )

    return embed


async def setup(bot):  # set async function
    await bot.add_cog(HelpCog(bot))  # Use await
