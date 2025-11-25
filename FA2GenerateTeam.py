import itertools
import sys
import os
import PokemonClass

# Add folder of the running script/executable to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



def _combo_to_flat_dict(combo):
    '''
    Helper function for translating Pokemon data to dataframe.

    Args:
        combo (list): the movesets that make up this team

    Returns:
        dict of all data for the Pokemon in the given list
    '''
    flat_data = {}
    for i, p in enumerate(combo, start=1):
        flat_data[f'p{i}_name'] = p.Name
        flat_data[f'p{i}_species'] = p.Species
        flat_data[f'p{i}_item'] = p.Item
        flat_data[f'p{i}_move1'] = p.Move1
        flat_data[f'p{i}_move2'] = p.Move2
        flat_data[f'p{i}_move3'] = p.Move3
        flat_data[f'p{i}_move4'] = p.Move4
        flat_data[f'p{i}_speed'] = p.Speed
        # could add 3 fields, each for the Pokemon object of each
    return flat_data

def generateValidTeams(pokemon_sets):
    '''
    Generate all possible teams of 3 based off the sets in the pool

    Args:
        pokemon_sets (list): list of all movesets in the pool

    Returns:
        a list of dictionaries, each dictionary representing the data for a team and its members
    '''
    valid_teams = []

    # from the valid sets, make every combination that doesn't violate Species or Item Clause
    for combo in itertools.combinations(pokemon_sets, 3): # already makes the groups unordered
        species = {p.Species for p in combo}
        items = {p.Item for p in combo}

        # if valid, add the team to the dataframe
        if len(species) == 3 and len(items) == 3:
            row = _combo_to_flat_dict(combo)
            valid_teams.append(row)

    return valid_teams

def _check_set_for_alarms(mon, alarms):
    '''
    For a given moveset, checks if anything about that moveset should trigger an alarm, and saves
    that data to the PokemonSet object to use when printed.

    Args:
        mon (PokemonSet): the Pokemon in question
        alarms (dict): the current alarms

    Future:
        it makes sense to have the alarm be the key in the settings file, used to grab all alarms associated with it.
        but it would speed this up if we could load them "in reverse" so we just get multiple lists of triggers, one
        for each type like item, move, etc and we could use the Pokemon data to look up the alarm name. so for example,
        for each moveset, grab the item and see if it's in the item alarm dictionary. if so, it should map to an alarm
        name. so like in the move alarm dictionary, sheer cold/fissure/etc would map to OHKO.
    '''
    for alarm_name in alarms.keys():
            alarm = alarms[alarm_name]
            # Species alarm
            if alarm["type"] == "P":
                  if mon.Name.upper().split()[0] in alarm["triggers"]:
                        mon.add_alarm(alarm_name, alarm["type"], alarm["triggers"])
            # Check if the set has at least one alarm move
            elif alarm["type"] == "M":
                  for move in [mon.Move1, mon.Move2, mon.Move3, mon.Move4]:
                    if move.upper() in alarm["triggers"]:
                            mon.add_alarm(alarm_name, alarm["type"], alarm["triggers"])
                            break
            elif alarm["type"] == "I":
                  if mon.Item.upper() in alarm["triggers"]:
                        mon.add_alarm(alarm_name, alarm["type"], alarm["triggers"])
            else:
                  raise ValueError("Alarm " + alarm_name + " has an invalid type of " + alarm["type"] + ".")

                  


def generateValidSets(trainer_name, TrainerData, MovesetData, user_settings, species_data):
    """
    Uses a Trainer's name to return all their valid sets.

    Args:
        trainer_name (str): Name of Trainer
        TrainderData (df): DataFrame of Trainer's possible movesets
        MovesetData (df): DataFrame of information for each moveset 
        Level (int): The level of the Pokemon faced
        species_data (df): info about the Pokemon's species, like base stats and type

    Returns:
        List of Pokemon objects that could be on the Trainer's team.

    Future:
        Could expand what species data is added to each Pokemon, like Legendary
        status or base stats.
    """
    if trainer_name.upper() == "GILLIAN":
        gillians = TrainerData.loc[["GILLIAN"]]

        print("Which GILLIAN do you mean? Enter 'c' for Cooltrainer (F), and 'l' for Lady.")

        while True:
            chosen = input().strip().lower()

            if chosen == 'c':
                trainer_row = gillians[gillians['Class'] == "Cooltrainer (F)"].iloc[0]
                break

            elif chosen == 'l':
                trainer_row = gillians[gillians['Class'] == "Lady"].iloc[0]
                break

            print("Invalid class, try again.")
    else:
        trainer_row = TrainerData.loc[trainer_name]

    trainerSets = list(trainer_row.values)
    del trainerSets[0]
    trainerSets = [x for x in trainerSets if x == x] # Removes NaN sets
    PokemonList = []
    Level = user_settings["Level"]

    for identifier in trainerSets:
        # find the row in the moveset data for the set, e.g. Ursaring2
        # then pass that to the Pokemon creation
        row = MovesetData[MovesetData["Name"] == identifier].iloc[0]
        species = species_data.loc[row["Species"]]
        Pokemon = PokemonClass.PokemonSet(row, Level, species["Type1"], species["Type2"])
        # Filter out Open Level only sets (if necessary)
        if int(Level) != 50 or Pokemon.Entry <= 850: # removes legend trio bonus sets too
            _check_set_for_alarms(Pokemon, user_settings["Alarms"])
            PokemonList.append(Pokemon)
    return PokemonList



