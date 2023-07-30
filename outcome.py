


from actions import Action


class ProcessLog:
    # for output of what's happening at each step during turn processing

    def __init__(self, month) -> None:
        # could optionally have "out" arg for where to print to
        self.log_string = f"Turn processing for month {month} initialized."
        self.month = month
        self.section_list = ["init"]
        self.sections = {"init": ["starting log..."]}
        self.curr_section = "init"

        self.results = Result(month)

    def add_section(self, name: str, starter: str):
        self.sections[name] = [starter]
        self.curr_section = name
        self.section_list.append(name)

    def log(self, logstring: str, section: str = None) -> None:
        if section is None:
            section = self.curr_section
        
        self.sections[section].append(logstring)
    
    def get_log(self, section = None):
        if section is not None: # printing specific section 
            return "\n".join(self.sections[section])
        
        ret = ""

        for sect in self.section_list:
            ret += f"\n----{sect}----\n"
            ret += "\n\t".join(self.sections[sect])
        
        return ret

    
    # maybe log_section() or something

class Result:
    #

    def __init__(self, month):
        self.final = False
        self.month = month

        self.public_results = [] 
        self.player_messages = [] #?
        self.all_actions: list[Action] = []
        self.non_action_results = []

        self.gm_todo = []

        self.warnings = []
        self.errors = []




