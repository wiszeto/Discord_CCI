import discord
from discord.ui import View
from modules.help import help_list as Team_List
from modules.help.buttons import problem_buttons as button
from datetime import datetime

""" (Overview in problem_buttons.py)
Cancel (message in requested user's team text channel)

    -if they clicked Cancel:
            - removes the cancel button from the team text channel
            - dequeues the team from the queue
            - edit help_embed to canceled
"""
class cancel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def tc(self, interaction: discord.Interaction, button: discord.ui.Button):
        team_num = Team_List.get_role(interaction.user)
        item = Team_List.get_item(team_num, None, None)
        await cancel_button(interaction, item)
    
async def cancel_button(interaction, item):
    # Get tall messages
    team_name = item.team_num
    claim_message = item.claim_message
    claimed_message = item.claimed_message
    help_log_message = item.help_log_message

    # Create the cancel embed
    view = View(timeout=None)
    fields = button.get_fields(claim_message.embeds, "Cancel")
    cancel_embed = canceled_embed(fields, interaction.user)

    #if user decides to cancel request after it has been claimed
    if claimed_message != None:
        await claimed_message.edit(embed=cancel_embed, view=view)
        await help_log_message.edit(embed=cancel_embed, view=view)

    #otherwise request is still waiting to be claimed
    #Edit the message in the waiting-for-channel channel to be canceled
    await claim_message.edit(embed=cancel_embed, view=view)

    # Delete the cancel button
    await interaction.message.delete()
    await interaction.response.send_message(content=f"Your Request Has Been Canceled", ephemeral=True)

    # Remove that team from the queue
    Team_List.remove(team_name)


def canceled_embed(fields, interaction_user):
    embed = discord.Embed(
        title=f"Canceled by {interaction_user}",
        color=0xFF0000,
        timestamp=datetime.now()
    )

    embed.add_field(
        name="Name",
        value=fields[0],
        inline=True
    )

    embed.add_field(
        name="Team Number",
        value=fields[1],
        inline=True
    )

    embed.add_field(
        name="Problem Description",
        value=fields[2],
        inline=False
    )

    return embed
