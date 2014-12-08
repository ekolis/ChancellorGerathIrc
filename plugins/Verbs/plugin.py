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
				"disintegrates"
			]
		self.weapons = ["a knife", "a katana", "a bazooka", "an ICBM", "a depleted uranium cannon", "a phased polaron beam", "a wave motion gun", "a copy of MOO3", "a range check error in se5.exe"]
		self.phongs = ["does horrible, unspeakable things to", "does kind, pleasant things for", "offers a trade and research treaty to", "colony-spams the systems belonging to"]
		self.definitions = {
				# space empires games
				"se4": "Space Empires IV. The fourth game in the Space Empires series, released in 2000. Considered to be the high point of the series by many (hipsters?), much like Super Smash Bros Melee, which was coincidentally released around the same time.",
				"seiv": "Space Empires IV. The fourth game in the Space Empires series, released in 2000. Considered to be the high point of the series by many (hipsters?), much like Super Smash Bros Melee, which was coincidentally released around the same time.",
				"se5": "Space Empires V. The fifth game in the Space Empires series, released in 2006. Considered to be the low point of the series by many (hipsters?), much like Super Smash Bros Brawl, which was coincidentally released around the same time.",
				"sev": "Space Empires V. The fifth game in the Space Empires series, released in 2006. Considered to be the low point of the series by many (hipsters?), much like Super Smash Bros Brawl, which was coincidentally released around the same time.",
				"se10": "Space Empires X. The tenth game in the Space Empires series, released in 2069. This game introduces a large number of innovations to the series, such as first person perspective and haptic feedback. It was the most popular game in the series by far, being played by billions of people around the world.",
				"sex": "Space Empires X. The tenth game in the Space Empires series, released in 2069. This game introduces a large number of innovations to the series, such as first person perspective and haptic feedback. It was the most popular game in the series by far, being played by billions of people around the world.",
				"starfury": "a spinoff of the Space Empires series in the action-RPG genre, released in 2003. Now you too can be a starship captain, and crash your ship into asteroids the size of planets!",

				# websites
				"pbw": "a website where you can play Space Empires (as well as several other turn-based strategy games) online, using an automated PBEM-style simultaneous turns system: http://pbw.spaceempires.net",
				"senet": "the most prominent fan site for the Space Empires series: http://www.spaceempires.net",

				# mods
				"stock": "the game without any mods. As the series progressed, this got less and less balanced... fortunately the game also got more and more moddable!",
				"cb": "Carrier Battles. Go on, ask me more!",
				"carrier battles": "Suicide Junkie's total conversion of SE4 to give it a sort of \"World War II in space\" feel. It plays nothing at all like stock. Go on, give it a try! http://imagemodserver.duckdns.org/other/MM/SE4/Mods/CarrierBattles/",
				"stellar warfare": "not a Star Wars mod, despite what it sounds like. It's a total conversion for SE5 to make it more tactical, created by ekolis. http://edkolis.exofire.net/swmod.php",
				"invasion": "an SE4 mod by Combat Wombat which features MORE OF EVERYTHING, because more stuff is good!",
				"bm": "Balance Mod. Go on, ask me more!",
				"balance mod": "a mod for SE5 created by Captain Kwok, which may have singlehandedly saved SE5, since the stock game was so horribly imbalanced.",

				# people
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

				# bots
				"chancellorgerath": "Its-a me! Chancellor Gerath of the Phong Confederation!",
				"xintis": "Who's that? Does he rule some empire I should be eorging?",

				# races
				"phong": "the most industrious race of sentient beings in the entire galaxy. We're friendly. Also we have crystalline tech. Did I mention we're friendly? Can I colonize those rock planets you're not using?",
				"zynarran": "the mortal enemy of the Phong.",

				# fan projects				
				"freee": "an open-source clone of SE4 being developed by Combat Wombat and ekolis. https://bitbucket.org/ekolis/freee",
				"eh": "Event Horizon - go ahead, ask me more on that. Or, what Canadians say at the end of every sentence. But I guess you knew that part already...",
				"event horizon": "a simple \"4X-lite\" created by Suicide Junkie. Gather resources on a looping hex map and build ships to attack the enemy mothership. Your mothership is your only means of construction, so defend it well!",
				"vectac": "Vector Tactics. Go on, ask me more!",
				"startext": "a early name for Vector Tactics.",
				"vector tactics": "SJ's remake of the old BEGIN game from back in the '90s, where you type commands like \"fire all torpedo\" and \"helm 180 5\" to fly a starship and fight battles with other starships.",
				"thancs": "Tactical Hex And Newtonian Combat Simulator. SJ's followup to Vector Tactics, this is a more detailed starship combat simulator. You now issue commands with keyboard and mouse, and you can design and build your own ships!",

				# buzzwords
				"eorging": "aggressively colonizing unclaimed planets in your ally's space to gain an economic advantage. May or may not be followed by a sudden backstab.",
			}
		self.smashes = [
				  "falcon PAWNCHES",
				  "wombo combos",
				  "grabs a smash ball and lays the smackdown on",
				  "multishines numerous projectiles back at",
				  "dumps 1,000,000 copies of Brawl on",
				  "spams Pikachu's down-B at",
				  "LANDMASTER's",
				  "shows Samus' Negative One Suit to",
				  "plays ""truth or dair"" with",
			]
		
	def kill(self, irc, msg, args, target):
		"""<target>

		"Kills" the target user or inanimate object with an action message.
		"""
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
	
	def PickRandom(self, array):
		num = self.rng.randint(0, len(array) - 1)
		return array[num]

Class = Verbs


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
