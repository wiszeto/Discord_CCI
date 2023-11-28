import asyncio
import discord
from discord.ui import Button, View
from datetime import datetime
from modules.help import reject_modal as Reject
from modules.help import old_help_modal as help
from modules.help import help_list as Team_List

"""
    Holds the button class: Main functionality (callback){What happens if button is clicked}
        -if they clicked a button in the support_categories:
            - sends help_modal (look into help_modal.py for more info)
        
        -if they clicked Claim:
            - edit help_emed to claim embed
            - send claim_embed to help-log
            - sends to the embed to access team voice and text channel into the apporiate help-channel
        -if they clicked Reslove:
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
        
        -if they clicked Cancel:
            - removes the cancel button from the team text channel
            - dequeues the team from the queue
            - edit help_embed to canceled
"""

class MyButton(Button):
    def __init__(self, label, style, emoji=None, url=None):
        super().__init__(label=label, style=style, emoji=emoji, url=url)

    async def callback(self, interaction):
        ''' After User chooses their category and the button is clicked, it will create a help modal
            allowing users to fill out the help_request. After they submit, they are added to the queue
            and it sends it to the moderator channel.'''

        # all the support categories
        support_cat = ["Technical", "Forensics",
                       "Unity", "ec2-instance", "Story", "Other"]

        # Sending the appropriate field to the help_modal
        if self.label in support_cat:
            team_name = Team_List.get_role(interaction.user)
            if Team_List.check_item(team_name) == False:
                print(self.label + " clicked")
                print("Button Processed in support_cat")
                Team_List.set_label(self.label)
                await interaction.response.send_modal(help.help_modal())

            else:
                print("already in queue")
                message = "Your team is already in the queue, please wait until a moderator gets to your request"
                await interaction.response.send_message(message, ephemeral=True)

        # Edit message to resloved
        elif self.label == "Resolve":
            if interaction.message.content == interaction.user.mention:
                #Creating Resolve embed
                fields = get_fields(interaction.message.embeds, "Resolve")
                resolve_embed = resolved_embed(fields, interaction.user)

                # Clear the old embed
                view = View(timeout=999999999)
                view.clear_items()

                # get log message
                team_name = Team_List.get_role(interaction.user)
                item = Team_List.get_item(None, None, interaction.message)

                help_log_message = item.help_log_message

                # edit the help_log message to resolved
                await help_log_message.edit(embed=resolve_embed, view=view)

                # edit the help message to be resolved
                await interaction.message.edit(embed=resolve_embed, view=view)

                cancel_message = item.cancel_message
                new_view = View(timeout=180)
                await cancel_message.edit(content="Your Request has been resolved, please use /help_message to request for more assistance.", embed=None, view=new_view)
                
                # Remove that team from the queue
                Team_List.remove(team_name)
            
            else:
                await interaction.response.send_message(content=f"Only {interaction.message.content} can resolve this request.", ephemeral=True)


        elif self.label == "Reject":
            print("Button Processed in reject")

            if interaction.message.content == str(interaction.user.mention):
                await reject_button(interaction)

            else:
                await interaction.response.send_message(
                    content=f"Only {interaction.message.content} can reject this request.", ephemeral=True)

        elif self.label == "Claim":
            print("Button Processed in claim")


            #getting team number
            item = Team_List.get_item(None, interaction.message, None)
            team_name = item.team_num

            # Creating invite for team voice channel
            vc_channel = discord.utils.get(
                interaction.guild.voice_channels, name=team_name)
            voice_invite = await vc_channel.create_invite(max_uses=99)

            # Creating invite for team text channel
            tc_channel = discord.utils.get(
                interaction.guild.text_channels, name=team_name)
            text_invite = await tc_channel.create_invite(max_uses=99)

            # Buttons
            reject = MyButton("Reject", discord.ButtonStyle.red)
            close = MyButton("Resolve", discord.ButtonStyle.green)

            # Url Buttons
            voice = MyButton("Join VC", discord.ButtonStyle.url,
                             url=str(voice_invite))
            text = MyButton("Join Text", discord.ButtonStyle.url,
                            url=str(text_invite))

            # add the buttons to the message
            view = View(timeout=None)
            claimed_view = set_view(close, reject, voice, text)

            #creating the claim embed
            fields = get_fields(interaction.message.embeds, "Claim")
            claim_embed = claimed_embed(fields, interaction.user)

            # Getting the correct channel to send to
            type_channel = discord.utils.get(
                interaction.guild.text_channels, name=fields[3].lower())

            lock = asyncio.Lock()
            is_done = False

            # get log channel
            log_channel = discord.utils.get(
                interaction.guild.text_channels, name="help-log")

            # send to log channel
            help_log_message = await log_channel.send(embed=claim_embed)

            # Add bot message to the linked list
            team_name = Team_List.get_role(interaction.user)
            Team_List.add_claimed_message(team_name, claimed_message)
            Team_List.add_help_log_message(team_name, help_log_message)
            await await_callbacks(reject, close, voice, text)

        elif self.label == "Cancel":
            print("Button Processed in cancel")
            self.claim.disabled =  True
            # Get that team from the queue
            team_name = Team_List.get_role(interaction.user)
            item = Team_List.get_item(team_name, None, None)
            claim_message = item.claim_message
            claimed_message = item.claimed_message
            help_log_message = item.help_log_message

            # Create the cancel embed
            view = View(timeout=None)
            fields = get_fields(claim_message.embeds, "Claim")
            cancel_embed = canceled_embed(fields, interaction.user)

            if claimed_message != None:
                await claimed_message.edit(embed=cancel_embed, view=view)
                await help_log_message.edit(embed=cancel_embed, view=view)

            # Edit the message in the waiting-for-channel channel
            await claim_message.edit(embed=cancel_embed, view=view)

            # Delete the cancel button
            await interaction.message.delete()
            await interaction.response.send_message(content=f"Your Request Has Been Canceled", ephemeral=True)

            # Remove that team from the queue
            Team_List.remove(team_name)
            Team_List.print_queue()

async def reject_button(interaction):
    # Send the Reject Modal, on why the support user rejected the request
    await interaction.response.send_modal(Reject.reject_modal())

    fields = get_fields(interaction.message.embeds, "Reject")
    reject_embed = rejected_embed(fields, interaction.user)

    # Clear the old embed
    view = View(timeout=None)
    view.clear_items()

    item = Team_List.get_item(None, None, interaction.message)
    team_name = item.team_num

    help_log_message = item.help_log_message
    await help_log_message.edit(embed=reject_embed, view=view)

    # Set the View to the new Embed
    await interaction.message.edit(embed=reject_embed, view=view)


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


def resolved_embed(fields, interaction_user):
    embed = discord.Embed(
        title=f"Resolved! by {interaction_user}",
        color=0x00FF00,
        timestamp=datetime.now()
    )

    embed.add_field(
        name="Name",
        value=fields[0]['value'],
        inline=True
    )

    embed.add_field(
        name="Team Number",
        value=fields[1]['value'],
        inline=True
    )

    embed.add_field(
        name="Problem Description",
        value=fields[2]['value'],
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


def claimed_embed(fields, interaction_user):
    embed = discord.Embed(
        title=f"{fields[3]} Problem",
        color=0xFFFF00,
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

    embed.add_field(
        name="Claim Status",
        value=f"```{interaction_user} has claimed this request!```",
        inline=False
    )

    return embed


def get_fields(interactions_embeds, label):
    """This functions gets the apporiate fields from the embeds"""
    fields = []
    for i in interactions_embeds:
        field = i.to_dict()
        fields = field.get('fields')
        # print(fields)

    if (label == "Claim" or label == "Reject"):
        name = fields[0].get("value")
        team_num = fields[1].get("value")
        problem = fields[2].get("value")
        type = field.get('title').replace(' Problem', '')
        fields = [name, team_num, problem, type]

    elif label == "Reslove":
        name = fields[0].get("value")
        team_num = fields[1].get("value")
        problem = fields[2].get("value")
        type = field.get('title')
        print(fields)
        fields = [name, team_num, problem, type]

    return fields


async def await_callbacks(*buttons):
    for button in buttons:
        await button.callback(button)


def set_view(*args):
    # timeout needs to be high if you don't want the interaction to expire
    view = View(timeout=None)
    for items in args:
        view.add_item(items)
    return view