import os
import sys
MSGONE = "Please enter the name of the dictionary file with the path:"
MSGTWO = "Please enter the name of the plaintext file with the path:"
MSGTHREE = "Please enter the cipher text:"
linebreak = '\n'


class CLIInterface(object):
	"""docstring for CLIInterface"""
	# def __init__(self, arg=None):
	# 	# super(CLIInterface, self).__init__()
	# 	self.arg = arg

	def doesFileExists(self, fileName):
		temp = os.path.isfile(fileName)
		while not temp:
			p = input('File not found! Please retry'+linebreak)
			temp = os.path.isfile(p)
			if temp: return p
		return fileName

	def run(self):
		dictionaryFile = input(MSGONE+linebreak)
		dictionaryFile = self.doesFileExists(dictionaryFile)

		plaintextFile = input(MSGTWO+linebreak)
		plaintextFile = self.doesFileExists(plaintextFile)

		ciphertext = input(MSGTHREE+linebreak)
		# ciphertext = self.doesFileExists(ciphertext)

		print("Thank you!")
		print("Now working the magic! : : )")

		return {'dictionaryFile': dictionaryFile, 'plaintextFile': plaintextFile, 'ciphertext': ciphertext}