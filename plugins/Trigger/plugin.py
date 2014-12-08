###
# Copyright (c) 2014, Ed Kolis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#	 this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#	 this list of conditions, and the following disclaimer in the
#	 documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#	 contributors to this software may be used to endorse or promote products
#	 derived from this software without specific prior written consent.
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
import supybot.callbacks as callbacks
import supybot.dbi as dbi
import supybot.conf as conf
import random

class FrequencyDB(plugins.DbiChannelDB):
		class DB(dbi.DB):
			class Record(dbi.Record):
				__fields__ = [
					'frequency',
					]
			def get(self, channel, **kwargs):
				rec = self.__parent.get(1)
				if rec is None:
					rec = self.__parent.add(self.Record(1, frequency = 0))
				return rec.frequency;
			def set(self, channel, frequency, **kwargs):
				rec = self.__parent.get(1)
				if rec is None:
					rec = self.__parent.add(self.Record(1, frequency = frequency))
				else:
					rec = self.__parent.chage(1, frequency)

class Trigger(callbacks.Plugin):
	"""Add the help for "@plugin help Trigger" here
	This should describe *how* to use this plugin."""
				

	def __init__(self, irc):
		self.__parent = super(Trigger, self)
		self.__parent.__init__(irc)
		self.frequencyDB = plugins.DB('Trigger Frequency', {'flat': FrequencyDB})()
		random.seed()
		# TODO - move these to a user editable DB
		self.triggers = {
				"Xintis": "We must never speak of that bot again!",
				"ChancellorGerath": "Someone talking about me behind my back?",
			}

	def die(self):
		self.__parent.die()
		self.frequencyDB.close()

	def inFilter(self, irc, msg):
		if msg.channel is None:
			return msg
		if (random.randrange(0, 100) < self.GetFrequency(msg.channel)):
			(recipients, text) = msg.args
			for trigger in triggers:
				if trigger.lower() in text.lower():
					irc.reply(triggers[trigger]);
					return msg # only one trigger per message!

	def setFrequency(self, irc, message, args, channel, percent):
		"""[<channel>] <percent>

		Sets the trigger frequency in percent for <channel>.
		<channel> is only necessary if the message isn't sent in
		the channel itself.
		"""
		if channel is None:
			return
		# TODO - check user privileges
		self.frequencyDB.set(channel, percent)
	setFrequency = wrap(setFrequency, ['channeldb', 'int'])

	def getFrequency(self, irc, message, args, channel):
		"""[<channel>]

		Gets the trigger frequency in percent for <channel>.
		<channel> is only necessary if the message isn't sent in
		the channel itself.
		"""
		if channel is None:
			return;
		irc.reply("Trigger frequency is {0}%.".format(self.frequencyDB.get(channel)))
	getFrequency = wrap(getFrequency, ['channeldb'])

	def GetFrequency(self, channel):
		if channel is None:
			return 0;
		records = self.frequencyDB.get(channel);
		if len(records) > 0:
			return records[0].frequency
		else:
			return 0


Class = Trigger


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79: