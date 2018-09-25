import json

filePath = "data/testData.json"

class Tester(object):
	"""docstring for Tester"""
	def __init__(self, arg=None):
		# super(Tester, self).__init__()
		self.arg = arg
		self.frequencyOneLetters = ['b','j','k','q','x','z','v']
		self.frequencyMapForPlaintext = {}
		self.content = None
		self.cipherText = None
		self.possiblePositions = []

	def readJsonFile(self):
		# print(len(self.cipherText.split(' ')))
		with open(filePath, 'r') as f:
			self.content = f.readlines()

	def generateMap(self):
		for index, plaintext in enumerate(self.content):
			self.frequencyMapForPlaintext[index] = {'text': plaintext}
			for letter in self.frequencyOneLetters: 
				self.frequencyMapForPlaintext[index][letter] = {'count': plaintext.count(letter), 'map': self.getAllIndexex(plaintext, letter)}

	def getAllIndexex(self, text, character):
		return [int(index) for index, i in enumerate(text) if i == character]

	def indexMapping(self):
		
		for key in self.frequencyMapForPlaintext.keys():
			tempDict = {}
			mapp = self.frequencyMapForPlaintext[key]
			for character in self.frequencyOneLetters:
				tempDict[character] = set()
				for index in mapp[character]['map']:
					tempDict[character].add(self.cipherText.split(' ')[index])

				flag = True
				for character in self.frequencyOneLetters:
					if character in tempDict.keys() and len(tempDict[character]) > 1: flag = False

			if flag: self.possiblePositions.append(key)

	def run(self):
		self.readJsonFile()
		self.generateMap()
		self.indexMapping()
		print(self.frequencyMapForPlaintext[self.possiblePositions[0]])

if __name__ == "__main__":
	Tester().run()
