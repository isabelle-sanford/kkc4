from enum import Enum

class LogOutcome(Enum):
    Failure = 0
    Success = 1
    Blocked = 2
    Redirected = 3


class Log:
    print_log = True
    
    def __init__(self) -> None:
        pass
    
    def Action(action, outcome: LogOutcome = LogOutcome.Success, notify_gm = False):
        flag_GM = ""
        if notify_gm:
            flag_GM = "GM Intervention Needed: "
        if outcome == LogOutcome.Blocked:
            outcome_string = f" but was blocked by {action.blocked_by}'s {action.blocked_by_action}."
        elif outcome == LogOutcome.Success:
            outcome_string = f" and succeeded."
        elif outcome == LogOutcome.Redirected:
            outcome_string = f" but was redirected to {action.redirect_target}."
        
        message = f"{action.player.info.name} tries to use {action.name}"
        print(flag_GM +message + outcome)

    def NotifyGM(action: Action, outcome):
        Log.Action(action, outcome, notify_gm=True)

    def Message(str):
        pass
    def Warning(str):
        pass
    def Error(str):
        pass