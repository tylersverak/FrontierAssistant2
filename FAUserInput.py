from thefuzz  import process
import FAStrings as strings
import json

import sys
import os

# Add folder of the running script/executable to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

FRONTIERBRAINS = {"LUCY", "BRANDON", "ANABEL", "TUCKER", "SPENSER", "GRETA"} # no noland because his team is random

# Functions for getting user input, to be used by Frontier Assistant 2


def getPokemonInput(trainer_name, slot_number, seen_species, possible_pokemon):
    '''
    Prompt the user for the name of the our opponent's first Pokemon's
    name as a string. Returns None if no valid mon can be found. Attempts
    to match invalid names to similar valid names.

    Args:
        trainer_name (str): name of the trainer
        slot_number (int): what slot we are getting input for
        seen_species (set): Pokemon we have already seen for this trainer
        possible_pokemon (set): all Pokemon in this trainer's pool

    Returns:
        The name of the Pokemon the user is seeing as a string. Can also return None
        if nothing was selected, or LAST to indicate that the user wants to re-analyze
        the last Pokemon.
    '''
    Pokemon = None
    slot_name = ["1ST", "2ND", "3RD"]
    while not Pokemon:
    
        response = None
        while not response:
            print("What Pokemon are you seeing? This is their " + slot_name[slot_number] + " Pokemon.")
            response = input().strip()

        if response.upper() == "HELP" or response.upper() == "H":
            print()
            print(strings.pokemon_input_message)
            continue

        # skip to next trainer if we don't care about analysis
        if response.upper() == "SKIP":
            return None
        
        # check the most recently updated slot and look at those sets again
        if response.upper() == "LAST":
            if slot_number == 0:
                print("Can't go to previous Pokemon, this is already the first Pokemon for this Trainer.")
                continue
            return strings.lastpokemonplaceholder

        # What's the mon's name? (edge case logic included)
        if response.upper() == "FARFETCH'D" or response.upper() == "FARFETCHD":
            response = "Farfetch'd" 
        elif response[:7].upper() == "NIDORAN":
            gender = None
            while gender == None:
                  genderinput = input("What gender is the Nidoran?\n(m) for Male, (f) for Female\n").upper().strip()
                  if genderinput == "F" or genderinput == "M":
                        gender = genderinput
            response = "Nidoran♂" if gender == "M" else "Nidoran♀"
        else:
            response = response.title()

        # Check we haven't already seen this
        if response in seen_species:
            print(trainer_name + " already has a " + response + ".")
            continue

        # Search for mon with that name
        if response in possible_pokemon:
            Pokemon = response # If we find an exact match, we are done
            continue
        best_match, score = process.extractOne(response, possible_pokemon)

        # Resolve invalid mon name
        if score >= 80: # If the response was close to a valid name
            yn_response = None
            while yn_response == None:
                print()
                yn_response = input("A Pokemon wasn't found with that name in " + trainer_name.capitalize() + "'s remaining sets, did you mean " + best_match + "?\nleave blank or y => yes   \tn or other => no\n")
                if yn_response.lower() == "y" or yn_response == "":
                    Pokemon = best_match # Match
                    continue
                else:
                    print()
        else:
            print()
            print("A Pokemon wasn't found with that name in " + trainer_name.capitalize() + "'s remaining sets.")
    return Pokemon
            

def getTrainerInput(TrainerData):
    '''
    Prompt the user for the name of the opposing trainer. Attempts to match invalid names to similar valid names.
    
    Args:
        TrainerData (df): dataframe of all Trainers in the battle frontier and each set in their pool
        
    Returns:
        The trainer's name as a string. Returns None if no valid trainer can be found. 
    '''
    Trainer = None
    
    while Trainer == None:
        # What's the trainer's name?
        print("What trainer are you battling?")
        response = input().upper().strip()

        if response == "":
            return None

        # Frontier Brains
        if response.upper() in FRONTIERBRAINS:
            sg = ""
            while sg != "S" and sg != "G":
                print("Is this for (S)ilver or (G)old?")
                sg = input().strip().upper()[0]
            if sg == "S":
                response += " SILVER"
            else:
                response += " GOLD"
            return response

        # Search for trainer with that name
        if response in TrainerData.index:
            return response # If we find an exact match, return
        possible_trainers = TrainerData.index
        best_match, score = process.extractOne(response, possible_trainers)

        # Resolve invalid trainer name
        if score >= 90: # If the response was close to a valid name
            yn_response = None
            while yn_response == None:
                print()
                yn_response = input("A trainer wasn't found with that name, did you mean " + best_match + "?\nleave blank or y => yes   \tn or other => no\n")
                if yn_response.lower() == "y" or yn_response == "":
                    return best_match # Match
                else:
                    print()
        else:
            print()
            print("A trainer wasn't found with that name.")
            
    return Trainer

def identifySet(initial_sets, Pokemon):
    '''
    Once we know the species and the trainer's pool of sets, use more details from the battle to identify the set.

    Args:
        initial_sets: the sets from the filtered pool this trainer can have. can be any iterable data structure
        Pokemon (str): the species of the current Pokemon

    Returns:
        List of all movesets that could still be possible for this slot after filtering
    '''
    possible_sets = [first for first in initial_sets if first.Species == Pokemon]
    if len(possible_sets) == 0:
        raise ValueError("No possible sets.")
    elif len(possible_sets) == 1:
        return possible_sets
    
    print()
    print("Possible movesets:")
    for moveset in possible_sets:
        print(moveset)
    print(strings.set_identify_message)

    count = len(possible_sets)
    starting_sets = possible_sets
    while count > 1:
        print(str(count) + " possible sets.")
        detail = input("Seen move/item: ")
        current_sets = possible_sets

        if detail == "":
            return possible_sets
        elif detail.upper().strip() == "R":
            print("Restarting set analysis...")
            possible_sets = starting_sets
            count = len(starting_sets)
            continue
        elif detail.upper().strip() == "HELP":
            print()
            print(strings.set_identify_help_message)
            continue
        elif detail.upper().strip() == "S":
            for moveset in possible_sets:
                print(moveset)
            continue
        elif detail.upper().startswith("NOT "):
            # if we know it's not a certain item, we can remove sets with that item
            current_sets = [x for x in possible_sets if x.Item.upper() != detail.upper()[4:].strip()]
        elif detail.upper().startswith("MAX ") or detail.upper().startswith("MID "):
            stats = {"hp":"HPEV", "atk":"AttackEV", "def":"DefenseEV", "spa":"SpecialAttackEV", "spd":"SpecialDefenseEV", "spe":"SpeedEV"}
            stat_name = stats.get(detail[4:].strip().lower(), None)
            if stat_name:
            # index represents what stat has investment, remove all sets without that investment
                ev_amount = 255 if detail.upper().startswith("MAX ") else 170
                current_sets = [x for x in possible_sets if getattr(x, stat_name) == ev_amount]
        elif detail.upper().startswith("MID "):
            stats = ["hp", "atk", "def", "spa", "spd", "spe"]
            index = stats.index(detail[4:].strip().lower())
            if index >= 0:
            # index represents what stat has investment, remove all sets without that investment
                current_sets = [x for x in possible_sets if int(x.EVSpread.split("/")[index].strip().split()[0]) == 170]
        else:
            # remove sets that don't have the item we have seen
            current_sets = [x for x in possible_sets if x.Item.upper() == detail.upper().strip()]
            # remove sets that don't have a move we have seen, if the detail was not an item
            # if the detail didn't match any items in any sets, try to see if it's a move in any set
            if len(current_sets) == 0:
                current_sets = [x for x in possible_sets if detail.upper().strip() in (move.upper() for move in x.MoveList)]
            else:
                possible_sets = current_sets
        
        if len(current_sets) == count:
            # no need to update counts or possible set, information was useless
            print("Couldn't narrow down sets with that information.\nIf you think that information should eliminate some set possibilities, check your spelling.")
        elif len(current_sets) < 1:
            # if somehow we don't have any sets left, try again to find possible sets
            print("Impossible set combination, last input of '" + detail + "' was ignored. Check your spelling or input 'r' to restart set analysis on this Pokemon.")
        else:
            # we have successfully narrowed our search, update possible sets and count
            possible_sets = current_sets
            count = len(possible_sets)
            for moveset in possible_sets:
                print(moveset)
    print("MOVESET IDENTIFIED!")
    # return full list of possible sets
    return possible_sets

def team_analysis(possible_sets_remaining, team_revealed, type_chart, remaining_teams):
    '''
    Analyzes the team up to this point and lets the user see
    known data about the opponent

    Args:
        possible_sets_remaining (list): possible movesets still in the trainer's pool
        team_revealed (list): contains lists for each possible slot's possible movesets
        type_chart (df): dataframe of type effectiveness multipliers, indexed by attacking type
        remaining_teams (df): dataframe of remaining possible teams
    '''
    print(strings.team_anal_message)
    list_of_remaining_sets = list(possible_sets_remaining)
    list_of_remaining_sets.sort(key = lambda p: p.Name)

    response = input().strip().upper()
    while response != "":
        print()
        if response == "HELP" or response == "H":
            print(strings.team_anal_help_message)

        elif response == "S":
            # seen team slots
            scrolling_wait = sum(len(sublist) for sublist in team_revealed) > 10
            for slot_index, slot in enumerate(team_revealed, start=1):
                print("SLOT " + str(slot_index))
                for moveset in slot:
                    print(moveset)
                if scrolling_wait and slot_index < len(team_revealed):
                    input("Hit enter to see the next slot's sets...")
                print(strings.printline)

        elif response == "R":
            # remaining mons

            sorted_remaining_name = sorted([moveset.Name + " <!>" if len(moveset.Alarms) >= 1 else moveset.Name
                                            for moveset in possible_sets_remaining])
            summary_string = ""
            for i, moveset in enumerate(sorted_remaining_name):
                summary_string += moveset.ljust(18)
                if (i + 1)  % 4 == 0:
                    summary_string += "\n"
            
            print("REMAINING SETS: (by alphabetical order, <!> indicates an Alarm)")
            print(summary_string)

        elif response == "T":
            # show distribution of remaining types

            types = {}
            total_movesets = len(possible_sets_remaining)
            for moveset in list_of_remaining_sets:
                first_type = moveset.Type1
                second_type = moveset.Type2

                first_type_count = types.get(first_type, 0)
                types[first_type] = first_type_count + 1
                # there might not be a second type
                if second_type:
                    second_type_count = types.get(second_type, 0)
                    types[second_type] = second_type_count + 1
            width = 30
            for type, count in sorted(types.items(), key=lambda item: item[1], reverse=True):
                percent_of_type_as_str = f"{count * 100 / total_movesets:.2f}%"
                print(f"{type.upper():<{width - len(percent_of_type_as_str)}}{percent_of_type_as_str}")

        elif response == "B":
            effectiveness = {}
            immunities = {}
            total = 0
            ability_immunities = {"Levitate":"Ground", "Water Absorb":"Water", "Volt Absorb":"Electric", "Flash Fire":"Fire"}
            for moveset in list_of_remaining_sets:
                # factor in abilities as well
                immune_ability_type = None
                for ability in moveset.Abilities.split("/"):
                    ability_type_blocked = ability_immunities.get(ability.strip())
                    if ability_type_blocked:
                        count_immune = immunities.get(ability_type_blocked, 0)
                        immunities[ability_type_blocked] = count_immune + 1
                        immune_ability_type = ability_type_blocked
                
                # calculate effectiveness of each type against this Pokemon
                for type_index in type_chart.index:
                    # if ability creates immunity, this type has already been considered
                    if type_index == immune_ability_type:
                        continue
                    current_effectiveness = 1
                    current_effectiveness *= type_chart.loc[type_index, moveset.Type1]
                    if moveset.Type2:
                        current_effectiveness *= type_chart.loc[type_index, moveset.Type2]
                    # if the Pokemon is immune, just make sure it is in the chart
                    if current_effectiveness == 0:
                        count_immune = immunities.get(type_index, 0)
                        immunities[type_index] = count_immune + 1
                        if type_index not in effectiveness.keys():
                            effectiveness[type_index] = 0
                    # Pokemon is not immune, update the chart
                    else:
                        previous_effectiveness = effectiveness.get(type_index, 0)
                        effectiveness[type_index] = previous_effectiveness + current_effectiveness

                total += 1

            print("Effectiveness of each type against remaining team (on average) and # of immune Pokemon (counting abilities)")
            print("TYPE:          MULT: IMM:")
            for pokemon_type in effectiveness.keys():
                # there's a Null type in Pokemon, skip it
                if pokemon_type == "Null":
                    continue
                print(pokemon_type.ljust(10) + f"{effectiveness[pokemon_type] / total:.2f}x".rjust(10) +
                      str(immunities.get(pokemon_type, 0)).rjust(5))
            print()

        elif response == "A":
            # show sets with Alarms
            total_alarms = 0
            types_of_alarms = set()
            for moveset in list_of_remaining_sets:
                if moveset.Alarms:
                    if total_alarms == 0:
                        print("REMAINING ALARMING SETS:")
                    print(moveset)
                    total_alarms += 1
                    # can only show so many before it scrolls off the page
                    if total_alarms % 10 == 0:
                        input("Hit enter to show more results...")
                        print(strings.printline)
                    for alarm in moveset.Alarms:
                        types_of_alarms.add(alarm.Name)
            if total_alarms == 0:
                print("No alarming movesets in remaining sets.")
            else:
                print(str(total_alarms) + " of " + str(len(list_of_remaining_sets)) + " sets have alarms (" + 
                      f"{total_alarms * 100 / len(list_of_remaining_sets):.2f})%")
                print("Types of alarms left: " + str(types_of_alarms))

        elif response == "V":
            # prints out every possible sets left and how likely it is
            number_of_teams_remaining = len(remaining_teams)
            sets_shown = 0
            for moveset in list_of_remaining_sets:
                appearances = (remaining_teams[["p1_name", "p2_name", "p3_name"]] == moveset.Name).sum().sum()
                percent_message = ("Percent chance of " + moveset.Name + " appearing: " + f"{appearances * 100 / number_of_teams_remaining:.2f}%")
                # have warning message appear on same line if it exists
                if moveset.Alarms:
                    print(percent_message + str(moveset))
                else:
                    print(percent_message)
                    print(moveset)

                sets_shown += 1
                if sets_shown % 10 == 0:
                    input("Hit enter to show more results...")
                    print(strings.printline)

        else:
            print("Not a valid command.")

        print()
        print("What else would you like to know? (Leave blank to input next Pokemon)")
        response = input().strip().upper()

def print_alarms(current_alarms):
    '''
    Print out the current alarms that exist

    Args:
        current_alarms (list): list of alarms
    '''
    if current_alarms == None or len(current_alarms) == 0:
        print("No alarms created.")
    else:
        lines_since_break = 1
        vertical_max = 30
        print("Current state of alarms:")
        for alarm in current_alarms:
            alarm_data = current_alarms[alarm]
            name = alarm
            if len(name) > 15:
                name = name[:12] + "..."
            status = "On" if alarm_data["active"] else "Off"
            name_type_of_alarm = "Move"
            if alarm_data["type"] == "P":
                name_type_of_alarm = "Species"
            elif alarm_data["type"] == "I":
                name_type_of_alarm = "Item"
            print(name.ljust(15) + "Type of Alarm: " + name_type_of_alarm.ljust(8) + str(status).rjust(4))
            lines_since_break += 1
            # print out the triggers for each alarm
            for trigger in alarm_data["triggers"]:
                print("\t" + trigger)
                lines_since_break += 1
                if lines_since_break > vertical_max:
                    input("Hit enter to show more alarm data...")
                    print(strings.printline)
                    lines_since_break = 0


def edit_user_settings(moveset_df, user_settings, settings_file):
    '''
    Pull up the settings and allow the user to change alarms and the level to play at

    Args:
        moveset_df (df): dataframe of all Pokemon movesets
        user_settings (dict): current user settings
        settings_file (str): name of the file to pull and save data
    '''
    item_list = list(moveset_df[moveset_df['Item'] != 0]['Item'])
    species_list = list(moveset_df[moveset_df['Species'] != 0]['Species'])
    move_list = list(moveset_df['Move 1']) + list(moveset_df['Move 2']) + list(moveset_df['Move 3']) + list(moveset_df['Move 4'])
    move_list = list(filter(lambda x: isinstance(x, str), move_list))

    all_items = set([item.upper() for item in item_list])
    all_species = set([species.upper() for species in species_list])
    all_moves = set([move.upper() for move in move_list])
    # remove bogus values from all move columns
    all_moves.discard("---")
    
    print(strings.printusersettingsline)
    response = None
    while response != "":
        print(strings.usersettingsoptions)
        response = input().strip().upper()
        if response == "":
            continue
        response = response[0]

        if response == "A":
            # create alarm
            print("What should the alarm be called?")
            name = input().strip().upper()[:strings.MAX_INPUT_LENGTH]
            if name == "":
                continue
            if user_settings["Alarms"].get(name):
                print("WARNING: There exists an alarm with this name. By proceeding, you will overwrite this alarm. Continue?")
                print("leave blank or y => yes   \tn or other => no")
                yn = input().strip().upper()
                if yn != "Y" and yn != "":
                    continue
            alarm_type = ""
            while (alarm_type == ""):
                print("What is this alarm for? Valid types are (I)tem, (M)ove, (P)okemon")
                alarm_type = input().strip().upper()
                if alarm_type == "":
                    continue
                alarm_type = alarm_type[0]
                if (alarm_type != "I" and alarm_type != "M" and alarm_type != "P"):
                    print("Invalid type.")
                    alarm_type = ""
            current_pool = None
            if alarm_type == "I":
                current_pool = all_items
                print("Which items trigger this alarm?")
            elif alarm_type == "M":
                current_pool = all_moves
                print("Which moves trigger this alarm?")
            elif alarm_type == "P":
                current_pool = all_species
                print("Which Pokemon species trigger this alarm?")
            print("NOTE: any name of a move/Pokemon/item must use the official spelling, but it does not have to be case sensitive.")
            to_add = None
            triggers = []
            while to_add != "":
                to_add = input().strip().upper()
                if to_add in current_pool:
                    triggers.append(to_add)
                    print("Added " + to_add)
                elif to_add != "":
                    print("Invalid alarm for this type for alarm type " + alarm_type)
            # actually adds alarm
            temp_dict = {"triggers":triggers, "type":alarm_type, "active":True}
            user_settings["Alarms"][name] = temp_dict
            print("Successfully created alarm of type " + alarm_type + " called " + name + ".")
            print()

        elif response == "T":
            # toggle alarms on/off
            current_alarms = user_settings.get("Alarms")
            print_alarms(current_alarms)

            print()
            alarm_to_toggle_name = None
            while (alarm_to_toggle_name != ""):
                print("What alarm would you like to toggle? Leave blank to quit and save.")
                alarm_to_toggle_name = input().strip().upper()
                alarm_to_toggle_data = current_alarms.get(alarm_to_toggle_name)
                if alarm_to_toggle_data:
                    # if it exists, toggle it to the other state
                    alarm_to_toggle_data["active"] = not alarm_to_toggle_data["active"]
                    if alarm_to_toggle_data["active"]:
                        print("Turned alarm " + alarm_to_toggle_name + " to ON")
                    else:
                        print("Turned alarm " + alarm_to_toggle_name + " to OFF")
                    print()
                else:
                    if alarm_to_toggle_name != "":
                        print("Couldn't find that alarm. Check your spelling and try again.")

        elif response == "D":
            # delete alarm
            current_alarms = user_settings.get("Alarms")
            print_alarms(current_alarms)
            delete_target = None
            # loop until user gives blank input, or no alarms are left
            while delete_target != "" and len(current_alarms) > 0:
                print("Which alarm would you like to delete? Leave blank to quit and save.")
                delete_target = input().strip().upper()
                if delete_target in current_alarms.keys():
                    print("Are you sure you want to delete alarm " + delete_target + "?")
                    print("leave blank or y => yes   \tn or other => no")
                    yn = input().strip().upper()
                    if yn == "Y" or yn == "":
                        del current_alarms[delete_target]
                        print("Deleted alarm " + delete_target + ".")
                else:
                    if delete_target != "":
                        print("Couldn't find that alarm. Check your spelling and try again.")
            print()

        elif response == "L":
            # change level
            current_level = user_settings.get("Level")
            print("The current level is " + current_level + ".")
            resolved = False
            while not resolved:
                print("What level do you want to play at? Leave blank to keep the current level.")
                new_level = input().strip().upper()
                if new_level != "":
                    # if the user gives a number, make sure it's 50 or in the Open Level range
                    if new_level.isdigit():
                        level_num = int(new_level)
                        if level_num == 50 or (level_num >= 60 and level_num <= 100):
                            resolved = True
                            print("Set level to " + new_level + ".")
                            user_settings["Level"] = new_level
                        else:
                            print("You can't play the Battle Frontier at that level.")
                    else:
                        if new_level == "OPEN":
                            resolved = True
                            print("Set level to 100.")
                            user_settings["Level"] = "100"
                        else:
                            print("Invalid input for level. Try OPEN or enter the number.")
                else:
                    resolved = True
            print()

        elif response == "V":
            # print out all info
            print("Level: " + user_settings["Level"])
            print_alarms(user_settings["Alarms"])
            print()

        else:
            print("Invalid choice.")
            print()


    # save the editing settings back to the file. need to manually load them back into program later!
    print(strings.printusersettingssaved)
    print()
    create_settings_file(settings_file, user_settings)


def create_settings_file(settings_file, new_settings=None):
    '''
    Creates a settings file

    Args:
        settings_file (str): name of the file created
        new_settings (dict): settings to use instead of the default
    '''
    settings = None
    if new_settings:
        settings = new_settings
    else:
        settings = {
            "Level": "50",
            "Alarms": {}
        }
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4)

def load_settings(settings_file):
    '''
    Load settings from the file

    Args:
        settings_file (str): name of settings file
    '''
    with open(settings_file, "r") as file:
        settings = json.load(file)
    return settings

