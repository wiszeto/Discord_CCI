import pickle

class TeamData:
    def __init__(self, team_num, claim_message, cancel_message, help_log_message, claimed_message, problem, user_id):
        self.team_num = team_num
        self.claim_message = claim_message
        self.cancel_message = cancel_message
        self.help_log_message = help_log_message
        self.claimed_message = claimed_message
        self.problem = problem
        self.user_id = user_id
    
"""
To pickle this, I need to add the channel of all the messages and the id of that message
"""

global help_queue
help_queue = []

global type_label
type_label = None

def enqueue(team_num, claim_message, cancel_message, help_log_message, claimed_message, problem, user):
    """Only adds team onto the queue if they are not in the list"""
    global help_queue
    if not check_item(team_num) or not check_user(user):
        Team = TeamData(team_num, claim_message, cancel_message, help_log_message, claimed_message, problem, user)
        help_queue.append(Team)
        print("Content: " + help_queue[0].cancel_message.channel.name)
        return True
    else:
        return False

def get_item(team_num, claim_message, claimed_message):
    """Get the item in the queue"""
    global help_queue
    if len(help_queue) == 0:
        return False

    # team.claim_message == claim_message or team.claimed_message == claimed_message:
    for team in help_queue:
        if team_num != None:
            if team.team_num == team_num:
                return team

        if claim_message != None:
            if team.claim_message == claim_message:
                return team
        
        if claimed_message != None:
            if team.claimed_message == claimed_message:
                return team

    return None

def add_help_log_message(team_num, help_log_message):
    """Adds the help_log_message to the TeamData item"""
    global help_queue
    if len(help_queue) == 0:
        return False

    for team in help_queue:
        if team.team_num.strip() == team_num.strip():
            team.help_log_message = help_log_message
            return team
    return None


def add_claimed_message(team_num, claimed_message):
    """Adds the claimed_message to the TeamData item"""
    global help_queue
    if len(help_queue) == 0:
        return False
    
    for team in help_queue:
        if team.team_num.strip() == team_num.strip():
            team.claimed_message = claimed_message
            return team
    return None


def add_cancel_message(team_num, cancel_message):
    """Adds the cancel_message to the TeamData item"""
    global help_queue
    if len(help_queue) == 0:
        return False
    
    for team in help_queue:
        if team.team_num.strip() == team_num.strip():
            team.cancel_message = cancel_message
            return team
    return None


def check_item(team_num):
    """ Check if team is in the queue """
    global help_queue
    if len(help_queue) == 0:
        return False
    
    for team in help_queue:
        if team.team_num == team_num:
            return True
    return False

def check_user(user_id):
    """ Checks if user is in the queue """
    global help_queue
    if len(help_queue) == 0:
        return False
    
    for team in help_queue:
        if team.user_id == user_id:
            return True
    return False

def remove(team_num):
    """Removes team from the queue"""
    global help_queue
    if len(help_queue) == 0:
        return False

    for i in range(len(help_queue)):
        if help_queue[i].team_num == team_num:
            help_queue.pop(i)
            return True
    return False 

def get_id():
    global help_queue
    return help_queue[0].cancel_message.id


def print_queue():
    '''Prints the queue'''
    global help_queue
    queue = ""
    i = 1
    for team in help_queue:
        queue += str(i) + ". " + team.team_num + "  \n"
        i+=1
    return queue


def set_label(label):
    global type_label
    type_label = label


def get_label():
    global type_label
    return type_label

def get_role(user):
    roles = user.roles
    for role in roles:
        if "team-" in role.name:
            return str(role.name)
    

def get_list_position():
    global help_queue
    return len(help_queue) + 1