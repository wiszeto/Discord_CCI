import discord
from datetime import datetime
from discord.ui import View
from discord import ui
from modules.help import help_list as Team_List

"""
    Holds the reject modal

    If support clicks reject button
        - sends modal on why they reject that claim
        - dequeues that team request from the queue (Have not done yet)

"""

class reject_modal(ui.Modal, title="Request Rejection"):

    reject = discord.ui.TextInput(
        label='Reason For Rejection',
        style=discord.TextStyle.paragraph,
        placeholder="Why did you reject?",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        ''' Modal to allow moderator, to inform the user of why their request was rejected '''

        item = Team_List.get_item(None, None, interaction.message)
        team_name = item.team_num

        #creating the reject embed
        embed = discord.Embed(
            title=f"Team {team_name} Help Request Rejected", timestamp=datetime.now(), color=0xFF0000)

        embed.add_field(name=f"{self.reject.label}",
                        value=f"{self.reject.value}", inline=True)

        view = View(timeout=None)

        # Since support person rejected the request
        # change the cancel message from the team text channel to the reason they got rejected
        team_message = item.cancel_message
        await team_message.edit(embed=embed, view=view)

        #edit help-log-message to rejected
        help_log_message = item.help_log_message
        help_log_message.edit(embed=embed, view=view)

        # Send to the person who rejected it
        await interaction.response.send_message("Succesfully rejected!", ephemeral=True)

        #remove them from the queue
        Team_List.remove(team_name)
