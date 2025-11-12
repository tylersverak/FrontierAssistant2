import numpy as np
import pandas as pd
import sys
import os
import FAUserInput as fainput
import FA2GenerateTeam as fagenerate
import FAStrings as strings
import time

'''
Build command with pyinstaller

pyinstaller --onefile ^
    --paths=. ^
  --add-data "trainers.txt;." ^
  --add-data "BFpokemon.txt;." ^
  --add-data "combatchart.txt;." ^
  --add-data "pokemondata.txt;." ^
  --hidden-import FAStrings ^
  --hidden-import FA2GenerateTeam ^
  --icon "logo.ico" ^
FrontierAssistant2.py

'''

# Add folder of the running script/executable to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and PyInstaller exe """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



TrainerData = pd.read_csv(resource_path("trainers.txt"), index_col = "Name")
MovesetData = pd.read_csv(resource_path("BFpokemon.txt")).fillna(0)
SpeciesData = pd.read_csv(
    resource_path("pokemondata.txt"),
    na_values=["Null"],
    dtype={
        "#": int, # dex number
        "Total": int,
        "HP": int,
        "Atk": int,
        "Def": int,
        "SpA": int,
        "SpD": int,
        "Spe": int,
        "Generation": int,
        "Legendary": bool
    }
)
SpeciesData = SpeciesData.set_index("Species")
TypeChartData = pd.read_csv(resource_path("combatchart.txt"))
TypeChartData = TypeChartData.set_index("Types")

#======================================================================================================================#
#================================================== BUSINESS CODE =====================================================#
#======================================================================================================================#

def find_seen_items(seen_sets):
    """
    Uses seen Pokemon to determine what items future Pokemon cannot have.

    Args:
        seen_sets (list of list of Pokemon obj): A list of all slots, each containing lists of possible sets,
                                        each containing a Pokemon object

    Returns:
        A set of items that future Pokemon cannot have. Can return an empty set.
    """
    if not seen_sets or len(seen_sets) == 0:
        return set()
    
    # keep track of all items we have confirmed seen, and all
    # items that could have been seen.
    guaranteed_seen_items = set()
    unique_items = set()

    for slot in seen_sets:
        item_to_remove = slot[0].Item
        unique_items.add(item_to_remove)
        for moveset in slot:
            # if the Pokemon can have more than one item,
            if item_to_remove != moveset.Item:
                item_to_remove = None
            unique_items.add(moveset.Item)

        # if all sets from a slot have the same item,
        # remove it.
        # e.g. seen Marowak => remove Thick Club
        if item_to_remove:
            guaranteed_seen_items.add(item_to_remove)

    # If the number of possible
    # items seen is the same as the number of sets, then those
    # items can be considered seen (if p1 can have a or b, and 
    # p2 can have a or b, item a and b can be considered seen)
    # otherwise just return the ones we can guarantee
    if len(seen_sets) == len(unique_items):
        return unique_items
    return guaranteed_seen_items

def filterTeams(initial_teams, current_seen_team, seen_items):
    '''
    Based on what we know about their team and their items,
    filter out team combinations that are no longer possible.

    Args:
        initial_teams (df): large table of all teams
        current_seen_team (list): contains several lists, with each possible set for each slot
        seen_items (set): set of items that guaranteed cannot show up on a future Pokemon

    Returns:
        A dataframe with only teams that could still be possible.
    '''
    # creates dataframe with a boolean value where True means that team (represented by a row) contains
    # one of the potential sets we are looking for. the last index of current teams will be the most recently
    # created, which is the mon we are filtering on.
    name_mask = initial_teams[["p1_name", "p2_name", "p3_name"]].isin([mon.Name for mon in current_seen_team[-1]])
    # if any of the names matched, consider it a still valid team
    name_mask = name_mask.any(axis=1)
    # filter possible teams with this mask (only keep rows that are True)
    possible_teams = initial_teams[name_mask]

    # tynote this part could still use some optimization. lots of weird edge cases/optimization
    def item_filter(row):
        for i in range(1, 4):
            name = row[f'p{i}_name']
            item = row[f'p{i}_item']
            # if this set does not match any that could possibly have been seen, and it has
            # a seen item, delete the team (represented by deleting the row)
            if item in seen_items and name not in [mon.Name for slot in current_seen_team for mon in slot]:
                return False  # Invalid — confirmed item held by wrong mon
        return True

    possible_teams = possible_teams[possible_teams.apply(item_filter, axis=1)]
    return possible_teams

def filterAlarms(alarms):
    '''
    Remove alarms that are toggled off from the settings used for this run

    Args:
        alarms (dict): the current alarms

    Returns:
        a dict filtering out alarms that are inactive
    '''
    # if an alarm is not active, delete it from memory. it will remain in the file.
    alarms = {alarm: alarm_data for alarm, alarm_data in alarms.items() if alarms[alarm]["active"]}
    return alarms

    
def print_team(team):
    '''
    Neatly prints out a team.

    Args:
        team (list): contains lists of potential sets for each slot
    '''
    for index in range(len(team)):
        possible_sets = team[index]
        print("SLOT " + str(index + 1))
        for moveset in possible_sets:
            print(moveset)


#======================================================================================================================#
#===============================================   IMPORTANT FUNCTIONS   ==============================================#
#======================================================================================================================#

# Cross-platform single keypress
def wait_for_keypress():
    '''
    Waits for a keypress from the user to wipe the screen, accounting for OS
    '''
    press_key_message = "\n\t\t\tPress any key to continue..."
    try:
        # Windows
        import msvcrt
        print(press_key_message)
        msvcrt.getch()
        os.system('cls')
        os.system('mode con: cols=115 lines=40')
    except ImportError:
        # Unix
        import tty
        import termios
        print(press_key_message)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        os.system('clear')
    
def main():
    os.system("mode con: cols=68 lines=29")
    print(strings.FA2ascii)
    wait_for_keypress()

    # load settings from the settings file. if the file is missing, recreate it with default settings.
    team_size = 3
    settings_file = "FA2settings.json"
    if not os.path.isfile(settings_file):
        print("WARNING: Settings file not found. If this is your first time running the program, you may ignore this warning.\n" +
              "If you have used Frontier Assistant 2 previously, your settings were corrupted and the default settings\nhave been restored.\n")
        fainput.create_settings_file(settings_file)
    try:
        user_settings = fainput.load_settings(settings_file)
    except:
        print("Your settings file is corrupted. Please fix or delete it and run the program again.")
        return
    fainput.edit_user_settings(MovesetData, user_settings, settings_file)
    user_settings["Alarms"] = filterAlarms(user_settings["Alarms"])

    while True:
        print(strings.printthickline)
        # Get trainer name
        Trainer = fainput.getTrainerInput(TrainerData)
        if not Trainer:
            break
        trainer_team = []
        seen_items = set()
        
        # Find possible pokemon sets the trainer can have
        possible_sets = fagenerate.generateValidSets(Trainer, TrainerData, MovesetData, user_settings, SpeciesData)
        possible_teams = pd.DataFrame(fagenerate.generateValidTeams(possible_sets))

        # Frontier Brain
        if len(possible_teams) == 1:
            print()
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ VS FRONTIER BRAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            for brain_mon in possible_sets:
                print(brain_mon)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print()
            continue

        slot_number = 0
        while slot_number < team_size:
            print()

            # Get Pokemon's name from user
            possible_species_from_pool = {moveset.Species for moveset in possible_sets}
            species_on_team = {slot[0].Species for slot in trainer_team}
            species_name_string = fainput.getPokemonInput(Trainer, slot_number, species_on_team, possible_species_from_pool)
            if not species_name_string:
                # if they don't tell us the name, reprompt the user
                break
            
            # Find all possible sets for that Pokemon/Trainer combination, or edit last slot
            if species_name_string == strings.lastpokemonplaceholder:
                # this is the case we are editing the previous slot
                possible_sets_for_this_slot = fainput.identifySet(trainer_team[-1], trainer_team[-1][0].Species)
                trainer_team[-1] = possible_sets_for_this_slot
                slot_number -= 1
            else:
                possible_sets_for_this_slot = fainput.identifySet(possible_sets, species_name_string)
                trainer_team.append(possible_sets_for_this_slot)

            print()
            item_if_guaranteed = possible_sets_for_this_slot[0].Item
            # have a different message if we know for certain the moveset
            if len(possible_sets_for_this_slot) == 1:
                print("Current slot's confirmed moveset:")
            else:
                print("Possible movesets for this slot:")
            for moveset in possible_sets_for_this_slot:
                print(moveset)
                # this should store None if this slot has no guaranteed item, otherwise store the item
                if moveset.Item != item_if_guaranteed:
                    item_if_guaranteed = None
            print()
            # this should remove any sets from previous slots that have an item that we 100% know must be in the
            # current slot
            if item_if_guaranteed:
                for x in range(slot_number):
                    trainer_team[x] = [moveset for moveset in trainer_team[x] if moveset.Item != item_if_guaranteed]


            # Find what items can be ruled out for future slots
            # keep items we already guaranteed
            seen_items = seen_items | find_seen_items(trainer_team)
            if len(seen_items) == 0:
                print("No confirmed items.")
            else:
                print("Confirmed items: " + str(seen_items))
            print("Number of possible remaining team compositions: " + str(len(possible_teams)))
            print(strings.printline)

            # filter teams, then from the remaining teams, redetermine the possible sets
            possible_teams = filterTeams(possible_teams, trainer_team, seen_items)
            # iterate to next slot! very important!
            slot_number += 1
            if slot_number >= team_size:
                # by this point, the possible number of teams should be fairly small, 512 worst case scenario
                print("Possible team compositions:")
                final_team_comps = possible_teams[['p1_name', 'p2_name', 'p3_name']].to_string(index=False, header=False).split("\n")
                for x in range(min(10, len(final_team_comps))):
                    print(final_team_comps[x])
                if len(final_team_comps) > 10:
                    print("And " + str(len(final_team_comps) - 10) + " more...")
                continue

            # recalc remaining possible movesets exist from filtered team data
            remaining_set_names =  set(pd.concat([possible_teams['p1_name'], possible_teams['p2_name'], possible_teams['p3_name']]))
            species_on_team.add(species_name_string)
            # remove from the remaining sets any with the current species (we've already seen it), and any sets that can't be possible
            possible_sets = [moveset for moveset in possible_sets if (moveset.Name in remaining_set_names and moveset.Species not in species_on_team)]
            # allow the user to prompt and see more data about the team
            fainput.team_analysis(possible_sets, trainer_team, TypeChartData, possible_teams)
            
    # :3
    print("Thanks for playing! Keep enjoying the Emerald BATTLE FRONTIER!!!")
    time.sleep(1)

main()