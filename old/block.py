from player import Player, Action

### ==== Functions ==== ###
def generate_action_list(player_list: list[Player]) -> list[Action]:
    action_list: list[Action] = []
    for p in player_list:
        for a in p.choices.actions:
            action_list.append(a)
    return action_list

def generate_block_list(action_list: list[Action]):
    block_list = []
    for a in action_list:
        if a.type.find("Block") > -1:
            block_list.append(a)
    return block_list

# Recursive function
def process_unblocked(block_list: list[Action], count = 0):
    print(f"\nInteration {count} starting...")
    game_state_changed = False
    
    for action in block_list:
        action.clear_blocked_by()

    for action in block_list:
        action.set_blocked_by()

    for action in block_list:
        # Ignoring players who have been blocked, if the player isn't being blocked, apply their blocks.
        if not(action.blocked) and len(action.blocked_by) == 0:
            if action.type == "Block All":
                print(f"Blocking all {action.target.info.name}'s actions.")
                for a in action.target.choice.actions:
                    if a.blocked == False:
                        a.blocked = True
                        game_state_changed = True
            elif action.type == "Block One":
                a = action.target.find_action("Block") # Technically different to how the BlockedBy flag is set by with SetBlockedBy()
                if a is not None:
                    print(f"Blocking {action.target.info.name}'s Block action.")
                    if a.blocked == False:
                        a.blocked = True
                        a.blocked_by = action.player # Don't know if this will have been already set...
                        game_state_changed = True

    if game_state_changed:
        process_unblocked(block_list, count + 1)
    print(f"... Iteration {count} finished!\n")

def process_cyclical_blocks(action: Action, sequence: list[Action]):
    sequence.append(action)

    if len(action.blocked_by) == 0:
        print("[End of Chain]")
        str = "["
        for n in sequence:
            str += f"{n.player.info.name} -> "
        print(f"{str} end]")
    else:
        for attack in action.blocked_by_action:
            # Dunno if this makes sense going backwards?
            if attack.blocked:
                continue
            if attack not in sequence:
                process_cyclical_blocks(attack, sequence.copy())
            else:
                # From the first occurence of the duplicate to the end of the list, including self, set the "is_blocked" flag on each participant.
                str = "["
                for i in range(sequence.index(attack),len(sequence)):
                    sequence[i].in_block_cycle = True
                    str += f"{sequence[i].player.info.name} -> "
                print("Iteration terminated (Cycle identified and blocked).")
                print(f"{str} {attack}]")

def processRedirectBlocks(action_list: list[Action]):
    for a in action_list:
        if a.type.find("Redirect") > -1:
            # Do we need to specify Redirect Block specifically?
            for b in a.target.choice.actions:
                if (b.type.find("Block") > -1) and (b.target == a.player):
                        # Redirect the block now.
                        b.redirected = True
                        b.redirect_target = a.target_two
                        # Do we need a "action processed flag"?
            


### ==== Runtime Code ==== ###
# 1. Check for redirects & blocks that target each other and redirect the block.
# 2. Check for redirect/block chains and process from the start of the chain forwards.
# --> Actually, this is still just the recursive unblocked/redirected things triggering in turn. 
# --> Need a check to see if it has a redirect targetting it?
# ----> Needs to both see if the action itself is being redirected, and whether a block/redirect is being move to target it.
# ----> Unless it's redirecting a block that is targetting itself, block 
# 3. Process unblocked/redirected blocks and unblocked/redirected redirects (order should not matter)
# 4. Process block/redirect loops
# 5. Process remaining redirects/blocks (order should not matter)

class Block:
    def __init__(self) -> None:
        pass

    def run_blocks(self, player_list: list[Player] = None):
        print("run_blocks()...")
        all_players: list[Player] = [] # Test().StartTest(7)
        if player_list is not None:
            all_players = player_list
            
        all_actions: list[Action] = generate_action_list(all_players)
        all_blocks: list[Action] = generate_block_list(all_actions)

        print(''.join(map(str,all_blocks)))


        # 1. Check for redirects & blocks targetting each other.

        # processRedirectBlocks(all_actions)

        # 2. Check for redirect/block chains



        # 3. Process unblocked/redireted blocks and unblocked/redirected redirects


        process_unblocked(all_blocks)


        # 4. Process block/redirect loops

        for a in all_blocks:
            process_cyclical_blocks(a,[])

        for a in all_actions:
            if a.in_block_cycle:
                a.blocked = True

        # 5. Process remaining redirects/blocks

        process_unblocked(all_blocks)


        for p in all_players:
            print(f"{p.info.name}: is_blocked = {p.status.is_blocked}")
            for a in p.choices.actions:
                    print(f" - {a.name}: is_blocked = {a.blocked}")

        print("run_blocks()... Done!")