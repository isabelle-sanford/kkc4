


class ProcessLog:
    # for output of what's happening at each step during turn processing

    def __init__(self, month) -> None:
        # could optionally have "out" arg for where to print to
        self.log_string = f"Turn processing for month {month} initialized."
        self.month = month
        pass

    def log(self, logstring: str) -> None:
        self.log_string += "\n" + logstring
    
    # maybe log_section() or something

class Result:
    #

    def __init__(self, month):
        self.final = False
        self.month = month

        self.public_results = [] 
        self.player_messages = [] #?
        self.all_actions = []
        self.non_action_results = []




