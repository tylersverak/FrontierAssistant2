# all strings and variables related to strings

MAX_INPUT_LENGTH = 25

FA2ascii = """       _______________________________ 
      /     _________________________/ __   __                   
      \\_   |__   ______  _____   _____/  |_|__| ____________      
       |    __) \\_  __ \\/  _  \\ /    \\   __\\  |/ __ \\_  ___ \\
       |   |     |  | \\(  |_|  )   |  \\  | |  \\  ___/|  |  \\/
       \\___/     |__|   \\_____/|___|  /__| |__|\\_____>__|        
                                    \\/                         
      _____                .__          __                 __   
     /  _  \\   ______ _____|__| _______/  |______    _____/  |_ 
    /  /_\\  \\ /  ___//  ___/  |/  ___/\\   __\\__  \\  /    \\   __\\
   /    _    \\\\ ___ \\\\___ \\|  |\\___ \\  |  |  / __ \\|   |  \\  |
   \\___| |___/______>______>__/______> |__| (______/___|  /__|  
                                                        \\/     
                               .-''-.     
                             .' .-.  )    
                            / .'  / /     
                           (_/   / /      
                                / /       
                               / /        
                              . '         
                             / /    _.-') 
                           .' '  _.'.-''  
                          /  /.-'_.'      
                         /    _.'         
                        ( _.-'            
"""

printline = ("-------------------------------------------------------------------------------------------------------------------")

printthickline =("===================================================================================================================")

printusersettingsline =("========================================== USER SETTINGS ==========================================================")

printusersettingssaved =("========================================== SETTINGS SAVED =========================================================")

lastpokemonplaceholder = "LAST"

# redo spacing/formatting on this
set_identify_help_message = ("-Put an item, EV investment or move you have seen. It doesn't have to match case (Cut is the same as CUT) but" +
              "\nit does need to be spelled correctly, with spaces when appropriate. you can also put 'not ' in\n" +
              "front of an item name (doesn't work for moves) if you know it can't be a particular item, for example:\n'not lum" +
              " berry' will remove any Lum Berry sets.\n-Additionally, you can put 'max [stat]' or 'mid [stat]' if you know the EV" +
              " investment of a particular\nPokemon. A few examples might be 'max hp' or 'mid attack'. A full list of stats:\n" +
              "    HP=hp, Attack=atk, Defense=def, Special Attack=spa, Special Defense=spd, Speed=spe\n" +
              "Max indicates the max 255 EV investment in a stat, and mid indicates" +
              " the alternative 170 EV investment.\nAll EV investment is one of these two categories.\n" +
              "-If you messed up some of the set info, type 'r' to remove all info for the set and start over.\n" +
              "-Enter 's' to (S)how what sets still remain.\n")

set_identify_message = ("List what item or moves the Pokemon has in order to identify the set. " +
          "Leave the input empty and hit enter\nif no details are obtained. " +
          "For help or a full list of details to give, type 'help'.")

team_anal_message = ("Team analysis: enter what command you want to run to see information about the opponent's team.\n" +        
          "Type 'help' for a full list of commands. Read the guide for more info on each command.\n"+
          "Hit enter (no command) when you are ready to enter the next Pokemon.") 

team_anal_help_message = ("S > display (S)een Pokemon and what possible sets they could be.\n"+
                          "R > display (R)emaining movesets that could show up this battle.\n" +
                          "T > display (T)ype breakdown by percent for remaining movesets (not by species).\n"+
                          "A > display remaining moveset with an (A)larm on them.\n"+
                          "B > display (B)reakdown of type effectiveness against remaining sets.\n"+
                          "V > display (V)erbose output, similar to Frontier Assistant 1.")

usersettingsoptions = ("What would you like to change?\n" +
                       "A > create an (A)larm\n" +
                       "T > (T)oggle an alarm\n" +
                       "D > (D)elete an alarm\n" +
                       "L > change (L)evel\n" +
                       "V > (V)iew all current settings\n" +
                       "Leave blank to save and quit changes.")

pokemon_input_message = ("Put the name of the species of the Pokemon you are seeing. You don't need to enter special characters.\n" +
                         "Type 'skip' to ignore all remaining Pokemon and go to the next Trainer.\n"+
                         "Type 'last' to go back to the previous slot and add more info about that Pokemon.")