"""

Daniel "lytedev" Flanagan
http://dmf.me

The song class containing all Song data and the logic for parsing a song from a text file.

"""

import sys
from os import path
from map import Map
from verse import Verse

songs_dir = path.abspath(path.dirname(sys.argv[0]) + "/Songs/")

class Song(object):
	def __init__(self):
		self.file = ""
		self.title = ""
		self.verses = []
		self.maps = []
		self.currentVerse = -1
		self.currentMap = -1

	@staticmethod
	def load(f):
		s = Song()
		raw_path = songs_dir+"/"+f+".txt"
		if path.exists(raw_path):
			s.file = path.abspath(raw_path)
		else:
			print("File doesn't exist {0}".format(path.abspath(raw_path)))
			return False
		return s.reload()

	def reload(self):
		if not path.exists(self.file):
			return False

		self.verses = []
		f = open(self.file)
		if not f: 
			print("Failed to open file {0}".format(self.file))
			return False
		self.loadVerses(self.loadHeader(f))
		self.verses.insert(0, Verse("Title", self.title))
		self.addVerse("Empty Slide")

		return self

	def addVerse(self, title, content = ""):
		if isinstance(title, Verse):
			title.name = title.name.strip()
			title.content = title.content.strip()
			self.verses.append(title)
		else:
			title = title.strip()
			self.verses.append(Verse(title, content.strip()))

	def loadHeader(self, f):
		self.title = ""
		for line in f:
			l = line.strip()
			if self.title == "" and l == "":
				pass
			elif self.title != "" and l == "":
				break
			elif l[0] == "#" or (len(l) > 1 and l[0:2] == "//"):
				pass
			elif l != "" and self.title == "":
				self.title = l
			elif self.title != "" and ":" in l:
				m = Map.fromLine(line)
				self.maps.append(m)
		return f

	def loadVerses(self, f):
		vh = []
		v = Verse()
		gvn = 1
		for line in f:
			l = line.strip()
			if l == "":
				if v.name.strip() != "":
					self.addVerse(v)
					vh.append(v.name)
					v = Verse()
			elif l[0] == "#" or l[0:2] == "//":
				pass
			elif l[0] == "(":
				l = l.strip("()")
				vh.append(l)
				pass 
			elif ":" in l and v.name == "":
				v.name = line.partition(':')[0]
				v.content = ""
			elif v.name == "" and l != "":
				v.name = "Generated Verse "+str(gvn)
				v.content = l+"\n"
				gvn+=1
			elif l != "" and v.name != "":
				v.content += l+"\n"
		if v.name.strip() != "":
			v.content = v.content.strip()
			self.addVerse(v)
			v = Verse()

		self.verses.append(Verse("Title", self.title))
		self.verses.append(Verse("Empty Verse", ""))

		defaultMap = Map()
		vh.insert(0, "Title")
		vh.append("Empty Verse")
		defaultMap.verses = vh
		self.maps.append(defaultMap)

	def getCurrentMap(self):
		numMaps = len(self.maps)
		if numMaps == 0: return False
		self.currentMap = max(0, min(self.currentMap, numMaps - 1))
		return self.maps[self.currentMap]

	def getVerseByName(self, name):
		for v in self.verses: 
			if v.name == name:
				return v
		return False

	def getCurrentVerse(self):
		map = self.getCurrentMap()
		if map == False: return False
		currentVerse = map.getCurrentVerseName()
		return self.getVerseByName(currentVerse)

	def nextVerse(self):
		return self.getVerseByName(self.getCurrentMap().nextVerse())

	def previousVerse(self):
		return self.getVerseByName(self.getCurrentMap().previousVerse())

	def isAtStart(self):
		return self.getCurrentMap().isAtStart()

	def isAtEnd(self):
		return self.getCurrentMap().isAtEnd()

	def restart(self): 
		return self.getVerseByName(self.getCurrentMap().restart())

	def __str__(self):
		return '<Song Object {Title: '+self.title+'}>'
