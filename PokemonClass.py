

class PokemonAlarm:
	def __init__(self, name, type, triggers):
		self.Name = name
		self.Type = type
		self.Triggers = triggers

class PokemonSet:
	def __init__(self, data, level, type1, type2):
		self.Name = data["Name"]
		self.Entry = int(data["Entry"]) if data["Entry"].isdigit() else 0
		self.Nature = data["Nature"]
		self.Species = data["Species"]
		self.Type1 = type1
		self.Type2 = type2 if isinstance(type2, str) else None
		self.Instance = int(data["Instance"]) if data["Instance"].isdigit() else 0
		self.Item = data["Item"]
		self.Nature = data["Nature"]
		self.Move1 = data["Move 1"]	
		self.Move2 = data["Move 2"]
		self.Move3 = data["Move 3"]
		self.Move4 = data["Move 4"]
		self.HPEV = int(data["HP EV"])
		self.AttackEV = int(data["Atk EV"])
		self.DefenseEV = int(data["Def EV"])
		self.SpecialAttackEV = int(data["SpA EV"])
		self.SpecialDefenseEV = int(data["SpD EV"])
		self.SpeedEV = int(data["Speed EV"])
		self.EVSpread = data["EVs (HP/Atk/Def/SpA/SpD/Spe)"]
		self.Speed = 0 # int(data[f"Lv {level} Speed"]) # doesn't work with levels not 100 or 50
		self.MoveList = [self.Move1, self.Move2, self.Move3, self.Move4]
		self.Abilities = data["Possible Ability"]
		self.LocalOdds = 1
		self.GlobalOdds = 1
		self.Alarms = []
		self.Level = level

	def __str__(self):
		warning = "     "
		mon_name = self.Name
		mon_item = self.Item
		moves = [self.Move1, self.Move2, self.Move3, self.Move4]
		move_spacing = 16

		# only Brain Pokemon should have entry of 0
		if self.Entry == 0:
			mon_name = mon_name.split()[0]

		if self.Alarms:
			# capitalize whatever set off the alarm
			warning = "     WARNING: "
			for alarm in self.Alarms:
				warning += alarm.Name +"   "
				if alarm.Type == "P":
					mon_name = mon_name.upper()
				elif alarm.Type == "M":
					moves = [move.upper() if move.upper() in alarm.Triggers else move for move in moves]
				elif alarm.Type == "I":
					mon_item = mon_item.upper()
			warning += "\n"
			warning += "!!!".ljust(5)
		return (warning + f"{mon_name} holding {mon_item}, abilities: {self.Abilities}, EVs: {self.EVSpread.replace(" ","")}, {self.Nature}\n\t{moves[0].ljust(move_spacing)}{moves[1].ljust(move_spacing)}{moves[2].ljust(move_spacing)}{moves[3].ljust(move_spacing)}")
	
	__repr__ = __str__ # super weird looking, but ensures whether the object is printed in a user friendly or not way, it looks the same (uses __str__)

	def getInstance(self):
		return self.Instance
	
	def add_alarm(self, name, type, triggers):
		new_alarm = PokemonAlarm(name, type, triggers)
		self.Alarms.append(new_alarm)