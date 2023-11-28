import discord
from discord.ui import View
from modules.help import help_list as Team_List
from datetime import datetime
from modules.help.buttons import problem_buttons as button
from modules.help.buttons import claimed_buttons as claimed

""" (Overview in problem_buttons.py)
Claim Button in waiting for claim

Claim (message in waiting-for-claim channel)
  if they clicked Claim:
    - sends a claimed embed which has access team voice and text channel into the apporiate help-channel
        -Has resolve and reject button
           -resolve: resolves the users request
           -reject: rejects the users request

    - edit help_emed to claim embed
    - send claim_embed to help-log
"""

#message waiting to be claimed in waiting-for-claim channel
class claim(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    
    @discord.ui.button(label='Claim', style=discord.ButtonStyle.green)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.claim.disabled = True
        await interaction.message.edit(view=self)
        await claim_button(interaction)
        self.stop()

async def claim_button(interaction):
    #getting team number
    item = Team_List.get_item("Placeholder", interaction.message, "Placeholder")
    team_name = item.team_num

    #creating the claim embed
    fields = button.get_fields(interaction.message.embeds, "Claim")
    claim_embed = claimed_embed(fields, interaction.user, item.problem)
    

    invite = await get_vc_tc(interaction, team_name)
    
    # Getting the correct channel to send to
    type_channel = discord.utils.get(
        interaction.guild.text_channels, name=item.problem.lower())
    
    # Set the View to the new Embed
    view = claimed.claimed()
    text = discord.ui.Button(label = "Join Text", style = discord.ButtonStyle.url,
                            url=str(invite[0]))
    voice = discord.ui.Button(label = "Join VC", style = discord.ButtonStyle.url,
                             url=str(invite[1]))
    view.add_item(voice)
    view.add_item(text)
    claimed_message = await type_channel.send(content=interaction.user.mention, embed=claim_embed, view=view)

    #change message to claimed
    view = View(timeout=None)
    await interaction.message.edit(content=interaction.user.mention, embed=claim_embed, view=view)

    # get log channel
    log_channel = discord.utils.get(
        interaction.guild.text_channels, name="help-log")

    # send to log channel
    help_log_message = await log_channel.send(embed=claim_embed)

    # Add bot message to the linked list
    #team_name = Team_List.get_role(interaction.user)
    Team_List.add_claimed_message(team_name, claimed_message)
    Team_List.add_help_log_message(team_name, help_log_message)


async def get_vc_tc(interaction, team_name):
    #getting team number
    item = Team_List.get_item(None, interaction.message, None)
    team_name = item.team_num
    print("in vs tc vc " + str(team_name))

    #creating invite for voice channel

    vc_channel = discord.utils.get(
                interaction.guild.voice_channels, name=team_name)
    voice_invite = await vc_channel.create_invite(max_uses=99)

    # Creating invite for team text channel
    tc_channel = discord.utils.get(
        interaction.guild.text_channels, name=team_name)
    text_invite = await tc_channel.create_invite(max_uses=99)

    return (text_invite, voice_invite)


def claimed_embed(fields, interaction_user, problem):
    embed = discord.Embed(
        title=f"{problem} Problem",
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


