import discord
from discord.ui import View
from modules.help import help_list as Team_List
from modules.help import reject_modal as Reject
from modules.help.buttons import problem_buttons as button
from datetime import datetime

"""(Overview in problem_buttons.py)
Buttons you can use after you claimed teh request

Claimed (message in {problem type} channel)
    What happens if users clicks resolve or reject

      -if clicked Reslove:
            - checks if the support of clicked that request claimed it first
                - if they did:
                    - dequeues the team from the queue
                    - edits the help_embed to resloved embed

                - if not, don't do anything:
                    - sends a message to that user that only this user can reslove it

      -if they clicked Reject:
            - sends reject modal (look into reject_modal.py for more info)
            - edits the help_embed to reject embed
            - removes team from queue
"""

#after message claimed, if will be in one of the help channels
class claimed(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    
    @discord.ui.button(label='Reslove', style=discord.ButtonStyle.green)
    async def vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.message.content == interaction.user.mention:
            item = Team_List.get_item(None, None, interaction.message)
            print(item)
            await resolve_button(interaction, item)
        else:
            await interaction.response.send_message(content=f"Only {interaction.message.content} can resolve this request.", ephemeral=True)
                   
                                                                                #add it as a node value
    @discord.ui.button(label='Reject', style=discord.ButtonStyle.red)
    async def tc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.message.content == str(interaction.user.mention):
            await reject_button(interaction)
        else:
            await interaction.response.send_message(content=f"Only {interaction.message.content} can resolve this request.", ephemeral=True)


async def resolve_button(interaction, item):
    #Creating Resolve embed
    fields = button.get_fields(interaction.message.embeds, "Resolve")
    resolve_embed = resolved_embed(fields, interaction.user)

    # Clear the old embed
    view = View(timeout=999999999)
    view.clear_items()

    #get log message
    help_log_message = item.help_log_message

    # edit the help_log message to resolved
    await help_log_message.edit(embed=resolve_embed, view=view)

    # edit the help message to be resolved
    await interaction.message.edit(embed=resolve_embed, view=view)

    #edit the cancel button from the team's channel
    cancel_message = item.cancel_message
    new_view = View(timeout=180)
    await cancel_message.edit(content="Your Request has been resolved, please use /help_message to request for more assistance.", embed=None, view=new_view)
    
    # Remove that team from the queue
    Team_List.remove(item.team_num)


async def reject_button(interaction):
    # Send the Reject Modal, on why the support user rejected the request
    await interaction.response.send_modal(Reject.reject_modal())

    fields = button.get_fields(interaction.message.embeds, "Reject")
    reject_embed = rejected_embed(fields, interaction.user)

    # Clear the old embed
    view = View(timeout=None)
    view.clear_items()

    item = Team_List.get_item(None, None, interaction.message)
    # team_name = item.team_num

    help_log_message = item.help_log_message
    await help_log_message.edit(embed=reject_embed, view=view)

    # Set the View to the new Embed
    await interaction.message.edit(embed=reject_embed, view=view)


def resolved_embed(fields, interaction_user):
    embed = discord.Embed(
        title=f"Resolved! by {interaction_user}",
        color=0x00FF00,
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


def rejected_embed(fields, interaction_user):
    embed = discord.Embed(
        title=f"Rejected by {interaction_user}",
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