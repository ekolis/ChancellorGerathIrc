###
# Copyright (c) 2014, Ed Kolis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.ircmsgs as ircmsgs
import supybot.callbacks as callbacks
import random
import string
import re


class Verbs(callbacks.Plugin):
	"""This plugin provides various commands to do "fun things" (using the Dwarf Fortress meaning of "fun") to users in the form of silly action commands, as well as to provide useful (and not-so-useful) information."""
	pass
	
	def __init__(self, irc):
		self.__parent = super(Verbs, self)
		self.__parent.__init__(irc)
		self.rng = random.Random()   # create our rng
		self.rng.seed()   # automatically seeds with current time
		self.attacks = [
				"stabs",
				"bludgeons",
				"zaps",
				"eviscerates",
				"decapitates",
				"blows up",
				"disintegrates",
				"flattens",
				"annihilates",
				"vaporizes",
				"poisons",
				]
		self.weapons = [
			"a knife",
		    "a katana",
		    "a bazooka",
		    "an ICBM",
		    "a depleted uranium cannon",
		    "a phased polaron beam",
		    "a wave motion gun",
		    "a copy of MOO3",
		    "a range check error in se5.exe",
			"a magma beam that fires magma from the core of a star",
			"a +1 enchanted shard cannon of armor piercing",
			"a futon torpedo",
			"a cloud of Von Neumman nano-disassemblers",
			"a trained vorpal bunny",
			"a 9001kT weight",
			"a Nerf disruptor",
			"the Charge Kick from Megaman 5",
			"a cross-shaped boomerang",
			"a boomerang-shaped cross",
			"the handyman's secret weapon: duct tape",
			"Lattice's glitchy charge shot from Megaman 21XX",
			"a lead pipe with Colonel Mustard's fingerprints on it",
			"a plague bomb",
			"a stellar nucleonic torpedo",
			"a dead-cow-firing catapult",
			"the Unholy Grail",
			"a +6 --==*masterwork*==-- unobtanium sword of murderousness",
			"his entire Minecraft inventory",
			"a proton pack",
			"a thermal detonator",
			"a cobalt warhead",
			"a corbomite warhead that doesn't actually exist",
			"a fistful of neutronium ingots",
			]
		self.immortals = {
			"obama": "You're on a list now, buddy.",
			"president": "You're on a list now, buddy.",
			"jesus": "Why? He'll only respawn on Sunday.",
			"god": "Wish me luck...",
			"holy spirit": "Exactly how do you expect me to do that?",
			"hitler": "But think of the consequences to the timeline!",
			"yourself": "Kay, I'm splodin.",
			"chancellorgerath": "Kay, I'm splodin.",
			"me": "You should probably talk to a psychiatrist.",
			"doctor": "OK, now he looks different and has trouble remembering things.",
			"master": "She says you should call her 'Missy' now. Yes, 'she'.",
			"death": "Now Dracula's pissed...",
			"archduke": "Dude, that already happened like 100 years ago. Get with the times!",
		}
		self.phongs = ["does horrible, unspeakable things to", "does kind, pleasant things for", "offers a trade and research treaty to", "colony-spams the systems belonging to"]
		self.definitions = {
				# space empires games
				"se": "Aaron Hall's Space Empires series, comprising SE1 through SE5, as well as the spinoff action RPG Starfury and the never-spoken-of Facebook game SE: Battle for Supremacy.",
				"se1": "The original Space Empires game. Never actually released apart from an SE1/2/3 bundle. The black sheep of the Space Empires family, it didn't even have designable ships or warp points!",
				"sei": "The original Space Empires game. Never actually released apart from an SE1/2/3 bundle. The black sheep of the Space Empires family, it didn't even have designable ships or warp points!",
				"se2": "Space Empires II. The second game in the Space Empires series, released in the mid-1990s. Only supported up to four players, and didn't have online multiplayer or moddability. Still quite a bit of fun back in the day!",
				"seii": "Space Empires II. The second game in the Space Empires series, released in the mid-1990s. Only supported up to four players, and didn't have online multiplayer or moddability. Still quite a bit of fun back in the day!",
				"se3": "Space Empires III. The third game in the Space Empires series, released in 1997. Arguably the most balanced Space Empires game, but held back by limited moddability.",
				"seiii": "Space Empires III. The third game in the Space Empires series, released in 1997. Arguably the most balanced Space Empires game, but held back by limited moddability.",
				"se4": "Space Empires IV. The fourth game in the Space Empires series, released in 2000. Considered to be the high point of the series by many (hipsters?), much like Super Smash Bros Melee, which was coincidentally released around the same time.",
				"seiv": "Space Empires IV. The fourth game in the Space Empires series, released in 2000. Considered to be the high point of the series by many (hipsters?), much like Super Smash Bros Melee, which was coincidentally released around the same time.",
				"se5": "Space Empires V. The fifth game in the Space Empires series, released in 2006. Considered to be the low point of the series by many (hipsters?), much like Super Smash Bros Brawl, which was coincidentally released around the same time.",
				"sev": "Space Empires V. The fifth game in the Space Empires series, released in 2006. Considered to be the low point of the series by many (hipsters?), much like Super Smash Bros Brawl, which was coincidentally released around the same time.",
				"se10": "Space Empires X. The tenth game in the Space Empires series, released to commemmorate the 100th anniversary of the moon landing in 2069. This game introduces a large number of innovations to the series, such as first person perspective and haptic feedback. It was the most popular game in the series by far, being played by billions of people around the world.",
				"sex": "Space Empires X. The tenth game in the Space Empires series, released to commemmorate the 100th anniversary of the moon landing in 2069. This game introduces a large number of innovations to the series, such as first person perspective and haptic feedback. It was the most popular game in the series by far, being played by billions of people around the world.",
				"starfury": "a spinoff of the Space Empires series in the action-RPG genre, released in 2003. Now you too can be a starship captain, and crash your ship into asteroids the size of planets!",
				"bfs": "Battle for Supremacy. Go on, ask me more. On second thought, don't bother. You probably don't even want to know.",
				"battle for supremacy": "essentially Farmville with a Space Empires skin on it. Don't even bother.",

				# other aaron hall games
				"do": "Dungeon Odyssey. Go on, ask me more!",
				"dungeon odyssey": "a roguelike in the style of Diablo created by Aaron Hall and released in 2002.",
				"ws": "World Supremacy. Go on, ask me more!",
				"world supremacy": "an Aaron Hall game, released in 2010, similar to Risk or Empire, but with (really really bad) tactical combat in addition to the main strategic game.",
				"sc": "Space Captain. Go on, ask me more!",
				"space captain": "an Aaron Hall action RPG designed for Android tablets, released in 2014. Similar to Starfury, but with brand-new alien races..",

				# other 4X games
				"moo": "the Master of Orion series, comprising MOO1, MOO2, and MOO3.",
				"moo1": "Master of Orion. A game that 4X hipsters say is somehow even better than MOO2. Maybe they're right; who knows?",
				"moo2": "Master of Orion ][. The gold standard of 4X games. Highly revered by fans of the genre, and every new 4X game the past few years has tried to be the 'next MOO2'...",
				"moo3": "Master of Orion ]|[. A game that has an even worse GUI than SE5. What, you didn't think that was possible?",
				"sots": "the Sword of the Stars series, comprising SotS1 and SotS2.",
				"sots1": "Sword of the Stars. A classic 4X that features six races, each with its own unique method of interstellar travel, as well as detailed ship design and realtime 3D tactical combat.",
				"sots2": "Sword of the Stars II. The sequel to Sword of the Stars. Tried to be bigger and grander than the original, and while it succeeded, it also succeeded in crashing everyone's computers... Yes, this is the Crysis of the 4X genre!",
				"galciv": "the Galactic Civilizations series, comprising Galciv1 through Galciv3.",
				"galciv1": "Galactic Civilizations. A 'beer and pretzels' 4X with simplified game mechanics, but those simple mechanics led to the creation of an extremely polished AI.",
				"galciv2": "Galactic Civilizations II. Sequel to Galactic Civilizations, known for its unique 3D ship designer which allows you to create ships in any shape imaginable, similar to THANCS, but in 3D. Sadly, all these customizations are completely cosmetic...",
				"galciv3": "Galactic Civilizations III. The third Galactic Civilizations game. In a first for the series, this game features actual combat mechanics, as opposed to Civ-style 'throw a stack of numbers at the opponent'! Combat is still AI-controlled, but now you have to put some thought into your custom ship designs...",

				# websites
				"pbw": "a website where you can play Space Empires (as well as several other turn-based strategy games) online, using an automated PBEM-style simultaneous turns system: http://pbw.spaceempires.net",
				"senet": "the most prominent fan site for the Space Empires series: http://www.spaceempires.net",

				# mods
				"stock": "the game without any mods. As the series progressed, this got less and less balanced... fortunately the game also got more and more moddable!",
				"cb": "Carrier Battles. Go on, ask me more!",
				"carrier battles": "Suicide Junkie's total conversion of SE4 to give it a sort of \"World War II in space\" feel. It plays nothing at all like stock. Go on, give it a try! http://imagemodserver.duckdns.org/other/MM/SE4/Mods/CarrierBattles/",
				"stellar warfare": "not a Star Wars mod, despite what it sounds like. It's a total conversion for SE5 (inspired somewhat by DJAS) to make it more tactical, created by ekolis. http://edkolis.exofire.net/swmod.php",
				"invasion": "an SE4 mod by Combat Wombat which features MORE OF EVERYTHING, because more stuff is good! But different stuff from all the other kitchen sink mods...",
				"bm": "Balance Mod. Go on, ask me more!",
				"balance mod": "a mod for SE5 created by Captain Kwok, which may have singlehandedly saved SE5, since the stock game was so horribly imbalanced.",
				"djas": "arthurtuxedo's SE5 mod which introduces the concept of \"tiered\" techs, linked via an extremely expensive theoretical prerequisite, leading to the dilemma of going for uber tech (leaving you vulnerable in the mean time) or buffing your current techs.",
				"warp 10 mod": "a Star Trek themed mod for SE5 originally designed by ekolis but massively reworked by marhawkman to feature an enormous collection of unique races and techs from the Star Trek universe. Seriously, who the heck are the \"Baku\" anyway, and what's a \"chronophasic shield generator\"?!",
				"dark nova": "an SE4 mod by bearclaw which features MORE OF EVERYTHING, because more stuff is good! But different stuff from all the other kitchen sink mods...",
				"dn4": "Dark Nova. Go on, ask me more!",
				"fusion mod": "an SE4 mod by BlackKnyght which features MORE OF EVERYTHING, because more stuff is good! But different stuff from all the other kitchen sink mods...",
				"devnull": "an SE4 mod by devnullicus and Rollo which features MORE OF EVERYTHING, because more stuff is good! But different stuff from all the other kitchen sink mods...",
				"eclipse mod": "an SE4 mod by KevinArisa which features MORE OF EVERYTHING, because more stuff is good! But different stuff from all the other kitchen sink mods...",
				"adamant": "an SE4 mod by Fyron whose main attraction is the five different 'racial paradigms'. You can even play as a magic race! Unfortunately most of the paradigms are pretty much identical gameplay-wise...",

				# people
				"aaron": "Aaron Hall. Go on, ask me more!",
				"aaron hall": "the mad genius behind the Space Empires series. Also created Dungeon Odyssey, World Supremacy, and Space Captain.",
				"sj": "Suicide Junkie. Go on, ask me more!",
				"suicide junkie": "Creator of Carrier Battles, Event Horizon, Vector Tactics, and much, much more.",
				"gerath": "Its-a me! Gerath! ...Or is it that other guy on IRC who took my name before I could get to it?!",
				"eorg": "the guy who eorging was named after. (Go ahead, ask me what eorging is. I dare you.) He's my favorite SE4 player because he always played as the Phong.",
				"gutb": "the guy who thought he could win in SE4 using only escorts, due to a misunderstanding of how evasion bonuses work. Sadly, this strategy actually works in stock SE5, due to the horrible balance of the game...",
				"ekolis": "the guy who got me into IRCing, and also worked on FrEee and Stellar Warfare.",
				"cw": "Combat Wombat. Go on, ask me more!",
				"combat wombat": "a giant wombat who worked on FrEee and Invasion.",
				"kwok": "Captain Kwok. Go on, ask me more!",
				"captain kwok": "the creator of the Balance Mod, and eternal procrastinator",
				"fyron": "the totally radical dude who created http://www.spaceempires.net",

				# bots
				"chancellorgerath": "Its-a me! Chancellor Gerath of the Phong Confederation!",
				"xintis": "Who's that? Does he rule some empire I should be eorging?",

				# races
				"phong": "the most industrious race of sentient beings in the entire galaxy. We're friendly. Also we have crystalline tech. Did I mention we're friendly? Can I colonize those rock planets you're not using?",
				"zynarran": "the mortal enemy of the Phong.",
				"eee": "a pretty friendly race. But don't get on their bad side. Their anti-proton beams will make you scream EEEEEEEEEEEEEEEEEE!!!",
				"dancing phong": "the most beautiful dancers in the galaxy - go on, take a look! http://imagemodserver.duckdns.org/other/MM/SE4/otherimages/DancingPhong.gif",

				# fan projects
				"freee": "an open-source clone of SE4 being developed by Combat Wombat and ekolis. https://bitbucket.org/ekolis/freee",
				"eh": "Event Horizon - go ahead, ask me more on that. Or, what Canadians say at the end of every sentence. But I guess you knew that part already...",
				"event horizon": "a simple \"4X-lite\" created by Suicide Junkie. Gather resources on a looping hex map and build ships to attack the enemy mothership. Your mothership is your only means of construction, so defend it well!",
				"vectac": "Vector Tactics. Go on, ask me more!",
				"startext": "a early name for Vector Tactics.",
				"vector tactics": "SJ's remake of the old BEGIN game from back in the '90s, where you type commands like \"fire all torpedo\" and \"helm 180 5\" to fly a starship and fight battles with other starships.",
				"thancs": "Tactical Hex And Newtonian Combat Simulator. SJ's followup to Vector Tactics, this is a more detailed starship combat simulator. You now issue commands with keyboard and mouse, and you can design and build your own ships!",
				"autohost": "a program you can use to automatically process turns for PBW games in the background. http://imagemodserver.duckdns.org/other/MM/Autohost-IIIexe.rar",
				"autoclient": "a program you can use to automatically download and launch turns for PBW games. https://github.com/se5a/PBWAutoClient",
				"autopbw": "a program which combines the functionality of both the autohost and the autoclient, allowing you to both host and play games without manually downloading and uploading files. https://bitbucket.org/ekolis/autopbw",

				# buzzwords
				"eorging": "aggressively colonizing unclaimed planets in your ally's space to gain an economic advantage. May or may not be followed by a sudden backstab.",
				"glassing": "nuking a planet from orbit. So called because nukes can turn soil to glass...",
				"molly": "a ringworld. Apparently there was this actress called Molly Ringwald or something? Don't ask me...",
				"turtling": "developing high level stellar manipulation tech, then closing all the warp points to your systems and building gravitational shields to prevent new warp points from being opened. Essentially forces the game into a stalemate, so it's generally frowned upon.",
				"polaron man": "a superhero who can skip through shields like a polaron can. Is he a dot or is he a speck? If he's in a black hole does he get whacked? And what does Triangle Man think of him? Nobody knows...",
			}
		self.smashes = ["falcon PAWNCHES",
				  "wombo combos",
				  "grabs a smash ball and lays the smackdown on",
				  "multishines numerous projectiles back at",
				  "dumps 1,000,000 copies of Brawl on",
				  "spams Pikachu's down-B at",
				  "LANDMASTER's",
				  "shows Samus' Negative One Suit to",
				  "plays ""truth or dair"" with",]
		self.avgngames = ["Space Empires V",
					"Master of Orion ]|[",
					"Big Rigs Over the Road Racing",
					"E.T.: The Extra-Terrestrial"]
		self.avgnquotes = ["I'd rather have {creature} {verb} in my {bodypart} than play {game}!",
					 "{game} is a {adjective} {noun} full of {stuff} from {place}!",
					 "I have never seen a worse {noun} than the {adjective} pile of {stuff} that is {game}!",]
		self.avgnadjectives = ["shitty",
					"rotten",
					"disgusting",
					"vomit-inducing",
					"disgraceful",]
		self.avgnnouns = ["turd",
					"clusterfuck",
					"shitpickle",
					"blemish",
					"abomination",]
		self.avgnverbs = ["fuck",
					"shit",
					"piss",
					"vomit",
					"crap",]
		self.avgncreatures = ["the Kraken",
					"Satan himself",
					"Mecha-Hitler"
					"my own genderswapped clone",
					"a syphilitic whore",
					"the ghost of Abraham Lincoln",]
		self.avgnbodyparts = ["chungus",
					"asshole",
					"dick",
					"throat",]
		self.avgnstuffs = ["shit",
					 "poop",
					 "piss",
					 "vomit",
					 "diarrhea",
					 "crap",
					 "garbage",
					 "pus",]
		self.avgnplaces = ["the depths of Hell",
					 "Uranus",
					 "the sick, twisted mind of Derek Smart",]
		self.summons = ["spends 20 mana to cast 'summon greater {what}'.",
					 "performs arcane rituals to summon {what} from {place}.",
					 "summons {what} using a magic brew made of {bodypart} of {creature}.",
					 "sacrifices six hundred threescore and six {creature}s to summon {what}.",
					 "nonchalantly summons the {adjective} {what} with a wave of the hand",
					 "draws a pentagram in {stuff} to summon {what}.",
					 "constructs an altar out of {noun}s and summons {what}.",
					 "chants '{latin}, {latin}, {latin}!', thereby summoning {what}.",]
		self.summonadjectives = ["vile",
					"distasteful",
					"eldritch",
					"horrific",
					"horrendous",
					"abominable",
					"terrifying",]
		self.summonnouns = ["skull",
					"brimstone",
					"wormwood log",
					"cyst",
					"crystallized soul",]
		self.summonverbs = ["massacre",
					"slaughter",
					"ravish",
					"plunder",]
		self.summonlatins = ["veni",
					"vidi",
					"vici",
					"virgo",
					"libra",
					"pisces",
					"gemini",
					"cancer",
					"expecto",
					"patronam",
					"avada",
					"kedavra",
					"caveat",
					"emptor",
					"quando",
					"omni",
					"flunkus",
					"moritati",
					"semper",
					"fidelis",]
		self.summoncreatures = ["the Kraken",
					"Satan himself",
					"swamp rat",
					"nubile young virgin",
					"40 year old male virgin",
					"Denebian slime devil",
					"tauntaun",
					"Phong",
					"Drushocka",
					"Eee",
					"the Doctor",
					"you",
					"Superman",
					"Batman",
					"Spider-Man",
					"the Incredible Hulk",]
		self.summonbodyparts = ["eye",
					"ear",
					"nose",
					"lip",
					"genitalia",
					"nipple",
					"big toe",
					"pinky finger",
					"ring finger",
					"heart",
					"liver",
					"gallbladder",
					"spleen",
					"appendix",
					"brain",
					"entrails",]
		self.summonstuffs = ["vomit",
					 "feces",
					 "urine",
					 "rotting flesh",
					 "brains",
					 "tripe",
					 "slime",
					 "the void",]
		self.summonplaces = ["the depths of Hell",
					 "outer space",
					 "the Fortress of Solitude",
					 "the nth dimension",
					 "fluidic space",
					 "the core of the earth",
					 "thin air",
					 "his imagination",
					 "hyperspace",
					 "hammer space",]
		
	def kill(self, irc, msg, args, target):
		"""<target>

		"Kills" the target user or inanimate object with an action message.
		"""

		# check if target is immortal
		ltarget = target.lower(); # make sure we match a whole word
		for x in self.immortals.keys():
			if re.search(r'\b' + x + r'\b', ltarget):
				irc.reply(self.immortals[x]);
				return

		# OK, we can kill them
		text = self.PickRandom(self.attacks) + " " + target + " with " + self.PickRandom(self.weapons)
		irc.queueMsg(ircmsgs.action(ircutils.replyTo(msg), text))
		irc.noReply()
	kill = wrap(kill, ['text'])
	
	def phong(self, irc, msg, args, target):
		"""<target>

		"Phongs" the target user or inanimate object with an action message.
		"""
		text = self.PickRandom(self.phongs) + " " + target
		irc.queueMsg(ircmsgs.action(ircutils.replyTo(msg), text))
		irc.noReply()
	phong = wrap(phong, ['text'])

	def whatis(self, irc, msg, args, word):
		"""[<word>]

		Attempts to define the specified word. Right now I only know about a few things; I is dum.
		If no word is specified, lists all known words.
		"""
		if word == None:
			keys = self.definitions.keys()
			keys.sort()
			irc.reply("I know about lots of things! Ask me about: " + string.join(keys, ", "))
		else:
			lword = word.lower() # make sure all definition keys added to the dictionary are lowercase!
			if lword in self.definitions:
				irc.reply(word + " is " + self.definitions[lword])
			else:
				irc.reply("Sorry, I don't know what " + word + " means. Try using dict or google to look it up online?")
	whatis = wrap(whatis, [optional('text')])

	def smash(self, irc, msg, args, target):
		"""<target>

		"Smashes" the target user or inanimate object with an action message.
		"""
		text = self.PickRandom(self.smashes) + " " + target
		irc.queueMsg(ircmsgs.action(ircutils.replyTo(msg), text))
		irc.noReply()
	smash = wrap(smash, ['text'])

	def avgn(self, irc, msg, args, game):
		"""[<game>]

		Channels the wrath of the Angry Video Game Nerd at a game.
		If game is not specified, a random shitty game is chosen.
		"""
		text = self.PickRandom(self.avgnquotes)
		if game == None:
			game = self.PickRandom(self.avgngames) # pick a random game from our list of shitty games
		text = text.replace("{game}", game)
		for i in range(0, 10): # get different words for each replacement
			text = text.replace("{adjective}", self.PickRandom(self.avgnadjectives), 1)
			text = text.replace("{noun}", self.PickRandom(self.avgnnouns), 1)
			text = text.replace("{verb}", self.PickRandom(self.avgnverbs), 1)
			text = text.replace("{creature}", self.PickRandom(self.avgncreatures), 1)
			text = text.replace("{bodypart}", self.PickRandom(self.avgnbodyparts), 1)
			text = text.replace("{stuff}", self.PickRandom(self.avgnstuffs), 1)
			text = text.replace("{place}", self.PickRandom(self.avgnplaces), 1)
		irc.reply(text)
	avgn = wrap(avgn, [optional('text')])

	def summon(self, irc, msg, args, what):
		"""<what>

		Summons someone or something from who knows where...
		"""
		text = self.PickRandom(self.summons)
		text = text.replace("{what}", what)
		for i in range(0, 10): # get different words for each replacement
			text = text.replace("{adjective}", self.PickRandom(self.summonadjectives), 1)
			text = text.replace("{noun}", self.PickRandom(self.summonnouns), 1)
			text = text.replace("{verb}", self.PickRandom(self.summonverbs), 1)
			text = text.replace("{latin}", self.PickRandom(self.summonlatins), 1)
			text = text.replace("{creature}", self.PickRandom(self.summoncreatures), 1)
			text = text.replace("{bodypart}", self.PickRandom(self.summonbodyparts), 1)
			text = text.replace("{stuff}", self.PickRandom(self.summonstuffs), 1)
			text = text.replace("{place}", self.PickRandom(self.summonplaces), 1)
		irc.queueMsg(ircmsgs.action(ircutils.replyTo(msg), text))
		irc.noReply()
	summon = wrap(summon, ['text'])
	
	def PickRandom(self, array):
		num = self.rng.randint(0, len(array) - 1)
		return array[num]

Class = Verbs


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
