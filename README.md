# FrontierAssistant2
Ever been playing through the Pokemon Emerald Battle Frontier and thought "gosh, this is really hard, I wish I had some sort of software to support my decision making and help me know what I'm up against"?

Then do I have the solution for you! Based off of the Frontier Assistant, this robust upgrade will provide you with key information about every Battle Frontier opponent and what Pokemon they are using so you can gain an edge against the CPU! Simply tell the program what the opposing trainer's name is and what their first Pokemon is, and it will show you all possible movesets it could be. By using information you gain during the battle (what moves or item they have) you can start to rule out what movesets you are up against. From there, that data is used to determine what other sets are possible on their team (remember, they can only have one Pokemon of each species, and one copy of each item). You can also see all kinds of data about their team, including what possible movesets are left, what percent of each remaining Pokemon is of each type, and more!

The program will create a settings file in whatever folder it is in, so it is recommended to put it in its own folder. The settings file will store what level you are playing at (50, Open Level) and any alarms you may want to add. Alarms can be made for moves, items, or species that you think would be a threat to your team, so when they come up, the moveset is displayed in a way to grab your attention so you can play more carefully around the risky moveset. You can also see how many remaining alarming moveset exists for a trainer you are up against, and what exactly set off the alarm. Alarms can be added, deleted, or toggled on or off if you are playing with a team with different weaknesses.

DOWNLOAD: https://github.com/tylersverak/FrontierAssistant2/releases/latest
Use the link above to download the latest release (currently Windows only) or you can download and run the Python program!

Message me on Smogon forums @meleeisbetter if you have any thoughts/questions/feedback! Keep enjoying the Emerald Battle Frontier!

**DIRECTIONS**

SETTINGS
When the program first opens, it will display the settings menu. If you just want to hop in or already set up your settings, just press enter to continue.

ALARMS
- use 'a' in the settings menu to create an alarm **(NOTE: all menus are case insensitive)** and it will ask you to create a name. From there, an alarm can be made for Items, Moves, or Pokemon. Enter the first letter of what type you want. From there, enter the name of whatever item/move/species should "trigger" the alarm (like an alarm named OHKO Moves could be Sheer Cold, Horn Drill, etc).
- use 't' to toggle alarms. when an alarm is off, it won't show up at all in the program, but you can easily turn it on later without recreating the alarm. If you use a team with a Sturdy user, you could turn off the OHKO alarm.
-  use 'd' to delete alarms you don't want to use again
-  use 'L' to change the level (50, anything 60-100, or Open Level, which assumes level 100)
-  use 'v' to view the current settings

TRAINERS

When you start, it first asks what trainer you are up against. If you leave it blank, it closes the program.

POKEMON

From there, the core loop starts. First enter the Pokemon you are looking at. There is special logic for handling names with odd characters like Mr. Mime and the Nidorans. You can also enter 'skip' to just skip to the next trainer, if you don't need any more info about the current battle. From there, it will show all movesets in the pool of that species. If more than one set is possible, it will ask you to enter info to narrow down what set it is. Give no input (just hit enter) when you are done (usually when you KO the opponent). You can type 'help' and it will give information on all the different kinds of info it can use to filter sets, which is also listed here:
- [item name]
- [move name]
- not [item you know it cannot be, i.e. no leftovers since no healing]
- mid [stat abbreviation] if you know there are 170 EVs in that stat
- max [stat] if you know they have 255 EVs in that stat
Once the set has been identified or you can't find anything else about the set, the program will use what data it has to eliminate movesets from the pool that would be impossible. From there, you can see a menu used for breakdowns of the opponent's team, and when you're done, just hit enter to go to the next Pokemon. You can also enter 'last' to go back to the previous Pokemon and analyze their moveset again. Otherwise, use one of the following:
- use 's' to display what Pokemon and what possible sets we know are on the team so far
- use 'r' to display all remaining possible sets in the opponent's pool
- use 't' to show a breakdown of what percent of the remaining sets are of each type (very cool IMO even if it has less use cases)
- use 'a' to show all remaining sets that have an alarm associated with them
- use 'b' to show a breakdown of how effective each attacking type would be against the remaining Pokemon, taking immunity abilities into account (Levitate, Volt Absorb, etc) with the exception of Wonder Guard.
- use 'v' for a verbose output like the original Frontier Assistant, with tons of detail on every set
From there, just keep going until you win the match!

There's special logic for the Frontier Brains, and some easter egg trainer sets in the data.

Happy battling!
  
