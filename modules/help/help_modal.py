import discord
from discord import ui
from discord.ui import View
from datetime import datetime
from modules.help.buttons import claim_button as claim
from modules.help.buttons import cancel_button as cancel
from modules.help import help_list as Team_List
from cogs import help

"""
    Holds the help_modal/help_embed:
    after user submits their modal 
        - it enqueues the user, 
        - sends an embed waiting to be claimed
        - a cancel button to the team text cancel
    
    NEED TO DO:
        - Possible tweak/rework on claim embed
            - where to send the claim embed
            - how to process the claims
            - The styling of claim embed

    Search using the message itself, make a function to do so
"""


class help_modal(ui.Modal, title="What do you need help with?"):
    name = discord.ui.TextInput(
        label="Name",
        style=discord.TextStyle.short,
        placeholder="Enter your name",
        required=True,
        max_length=20,
    )

    problem = discord.ui.TextInput(
        label='Problem',
        style=discord.TextStyle.paragraph,
        placeholder="Describe your problem",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        '''After submitting it will send it to the moderator channel.
           Moderator, have button that allow them to join the team voice channel, text channel and a resolve button if resolved.
           after resloved the team will be dequeued. '''
        
        team_name = Team_List.get_role(interaction.user)
        print("getting team num " + str(team_name))

        # If team is not already in the queue
        if Team_List.check_item(team_name) == False:
            await self.configure_embeds(interaction, team_name)

        # If team is already in the queue
        else:
            message = "Your team is already in the queue, please wait until a moderator gets to your request"
            await interaction.response.send_message(message, ephemeral=True)

    
    async def configure_embeds(self, interaction: discord.Interaction, team_name):
        help_embed = self.help_embed(interaction.user, team_name, interaction.user.avatar)
        cancel_embed = self.cancel_embed(interaction.user, team_name, interaction.user.avatar)

        """Currently team channel defaulted to other"""
        # Getting the correct channel to send to
        claim_channel = discord.utils.get(
            interaction.guild.text_channels, name='waiting-for-claim')
        cancel_channel = discord.utils.get(
            interaction.guild.text_channels, name=team_name)

        # Send to the waiting-for-claim channel
        view = claim.claim()
        claim_message = await claim_channel.send(content="<@&1100643277625114726>", embed=help_embed, view=view)

        # sending cancel button to team channel
        view = cancel.cancel()
        cancel_message = await cancel_channel.send(embed=cancel_embed, view=view)

        # Send to the users
        message = "your request is being processed, you are number " + \
            str(Team_List.get_list_position()) + " in the queue"
        await interaction.response.send_message(message, ephemeral=True)
        
        Team_List.enqueue(team_name, claim_message, cancel_message,
                    None, None, str(Team_List.get_label()), interaction.user)
        
        msg_id = Team_List.get_id()
        print("msg_id: " + str(msg_id))
        msg = await cancel_channel.fetch_message(msg_id)
        print("message channel: " + msg.channel.name)
        print("enqueued " + str(team_name))
        


    def cancel_embed(self, user, team_name, avatar_icon_url):
        """This function creates the embed for the cancel_request"""

        # title
        cancel_embed = discord.Embed(
            title="Cancel Request", color=0xff0000)

        # author field
        cancel_embed.set_author(
            name=user,
            icon_url=avatar_icon_url
        )

        # name_field
        cancel_embed.add_field(
            name=f"{self.name.label}",
            value=f"{self.name}",
            inline=True
        )

        # team_field
        cancel_embed.add_field(
            name=f"Team",
            value=f"{team_name}",
            inline=True
        )

        # problem_field
        cancel_embed.add_field(
            name="Problem Description",
            value=f"```{self.problem}```", inline=False
        )

        # cancel field
        cancel_embed.add_field(name="Cancel",
                               value="The button below is to cancel your current help_request and to remove yourself from the queue")

        return cancel_embed

    def help_embed(self, user, team_name, avatar_icon_url):
        """This function creates the embed for the help request"""
        problem_type = Team_List.get_label()
        a = "in embed " + problem_type
        # title
        embed = discord.Embed(
            title=f"{problem_type} Problem", timestamp=datetime.now(), color=0xFF0000)

        # author_field
        embed.set_author(
            name = user,
            icon_url=avatar_icon_url
        )

        # name_field
        embed.add_field(
            name=f"{self.name.label}",
            value=f"{self.name}",
            inline=True
        )

        # team_field
        embed.add_field(
            name=f"Team",
            value=f"{team_name}",
            inline=True
        )

        # problem_field
        embed.add_field(
            name="Problem Description",
            value=f"```{self.problem}```", inline=False
        )

        # claim_field
        embed.add_field(
            name="Claim Status",
            value="```Waiting to be claimed!```", inline=False
        )

        return embed
