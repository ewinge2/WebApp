#!/usr/bin/python

import cgi

class webpageInterface:
	def __init__(self):
		self.initialContent = open('CarlStats.html').read()
		self.major = ''
		self.year = ''
		self.debug = ''

	def getInput(self):
		form = cgi.FieldStorage()

	def generate(self):
		self.getInput()
		print "Content-type: text/html\r\r\n\n"  
# 		(self.major, self.year)
		output = self.initialContent % (self.major, self.year, self.debug)
		print output 

if __name__ == "__main__":	
	site = webpageInterface()
	site.generate()

	


