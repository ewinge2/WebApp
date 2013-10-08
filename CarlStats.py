#!/usr/bin/python

import cgi

class CarlStats:
	def __init__(self):
		self.initialContent = open('CarlStats.html').read()
		self.major = ''
		self.startYear = ''
		self.debug = ''

	def getInput(self):
		form = cgi.FieldStorage()
		if 'startYear' in form:
			self.startYear = form['startYear'].value
			self.debug = self.startYear

	def generate(self):
		self.getInput()
		print "Content-type: text/html\r\r\n\n"  
		output = self.initialContent % (self.major, self.startYear, self.debug)
		print output 

if __name__ == "__main__":	
	site = CarlStats()
	site.generate()

# 	site.getInput()
# 	site.generate()
	


