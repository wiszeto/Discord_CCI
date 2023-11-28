import discord
from discord.ui import View
from datetime import datetime
from modules.help import reject_modal as Reject
from modules.help import help_modal as help
from modules.help import help_list as Team_List

"""
    Overview of the support ticket system
    
    Using the Slash Command
    1.users make a request using /help_message
    2.Once the choose the problem type they get a modal to fill out

    Event staff side
    3. Staff will be waiting in the waiting-for-claim channel
    4. If staff sees a new message, they have to claim it (So multiple staff don't work on the same request)
    5. After claiming, the ticket will go to the corresponding help type requested by the user
    6. In that ticket it will have Resolve button, Reject Button, VC button and TC button
    7. TC and VC button allow staff to join team's VC or TC in a click of a button
    8. After resolving the request, staff will remove it from the queue by click resolve button
    9. If staff deems request unworthy, they can reject the request. Fill out modal of why they rejected and remove request from queue

    User Side
    10. After making a request users have the option to cancel a request
    11. After using the slash commands a message with a cancel button will appear in their team text channel
    12. User's can cancel their request by simply pressing the button


    Overview of all the Buttons:
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



"""
Problem Button (initalized by /help_message in help.py)
    Contains all the help category buttons
    All the button save the type of help and send the modal to the user
"""
class problem_buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    
    @discord.ui.button(label='Technical', style=discord.ButtonStyle.blurple)
    async def technical(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("HELLO")
        if Team_List.get_role(interaction.user) == None:
            await interaction.response.send_message(content="You must have a team role to make a request. if you are looking for general help, please consult #help-desk", ephemeral=True)
        else:
            Team_List.set_label(button.label)
            await interaction.response.send_modal(help.help_modal())

    @discord.ui.button(label='Forensics', style=discord.ButtonStyle.blurple)
    async def forensics(self, interaction: discord.Interaction, button: discord.ui.Button):
        if Team_List.get_role(interaction.user) == None:
            await interaction.response.send_message(content="You must have a team role to make a request. if you are looking for general help, please consult #help-desk", ephemeral=True)
        else:
            Team_List.set_label(button.label)
            await interaction.response.send_modal(help.help_modal())
     
    @discord.ui.button(label='ec2-instance', style=discord.ButtonStyle.green)
    async def ec2_instance(self, interaction: discord.Interaction, button: discord.ui.Button):
        if Team_List.get_role(interaction.user) == None:
            await interaction.response.send_message(content="You must have a team role to make a request. if you are looking for general help, please consult #help-desk", ephemeral=True)
        else:
            Team_List.set_label(button.label)
            await interaction.response.send_modal(help.help_modal())

    @discord.ui.button(label='Unity', style=discord.ButtonStyle.green)
    async def unity(self, interaction: discord.Interaction, button: discord.ui.Button):
        if Team_List.get_role(interaction.user) == None:
            await interaction.response.send_message(content="You must have a team role to make a request. if you are looking for general help, please consult #help-desk", ephemeral=True)
        else:
            Team_List.set_label(button.label)
            await interaction.response.send_modal(help.help_modal())

    @discord.ui.button(label='Story', style=discord.ButtonStyle.green)
    async def story(self, interaction: discord.Interaction, button: discord.ui.Button):
        if Team_List.get_role(interaction.user) == None:
            await interaction.response.send_message(content="You must have a team role to make a request. if you are looking for general help, please consult #help-desk", ephemeral=True)
        else:
            Team_List.set_label(button.label)
            await interaction.response.send_modal(help.help_modal())
    
    @discord.ui.button(label='Other', style=discord.ButtonStyle.grey)
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        if Team_List.get_role(interaction.user) == None:
            await interaction.response.send_message(content="You must have a team role to make a request. if you are looking for general help, please consult #help-desk", ephemeral=True)
        else:
            Team_List.set_label(button.label)
            await interaction.response.send_modal(help.help_modal())

def get_fields(interactions_embeds, label):
    """This functions gets the apporiate fields from the embeds"""
    fields = []
    for i in interactions_embeds:
        field = i.to_dict()
        fields = field.get('fields')
        print(fields)
    if (label == "Claim" or label == "Reject" or "Cancel"):
        name = fields[0].get("value")
        team_num = fields[1].get("value")
        problem = fields[2].get("value")
        type = field.get('title').replace(' Problem', '')
        fields = [name, team_num, problem, type]

    elif label == "Resolve":
        name = fields[0].get("value")
        team_num = fields[1].get("value")
        problem = fields[2].get("value")
        type = field.get('title')
        fields = [name, team_num, problem, type]

    return fields


def select_request_embed():
    """Creates the embed for the selecting the request, embed differs depending on mode of full_request"""

    # embed part of help message

    embed = discord.Embed(
        title="SGC Help Bot",
        color=0xbd8b13,
        description='Need Help? Send a help request to a moderator! \nPlease pick a avaliable catagory below.'
    )

    """This function creates the embed for the help request"""

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

