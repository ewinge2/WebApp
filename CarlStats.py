#!/usr/bin/python
'''
File:webapp.py
Author: Jialun "Julian" Luo
Last edited: 2013/10/9

This program will generate a html to the browser to display. It will print a summary or results
when user inputs are detected.
'''
import cgi
import DataSource
import cgitb

cgitb.enable()

class CarlStats:
	'''
	@summary: A class for generating a webpage specialized for our design. (Putting the content into a class
		so that instance variables are easier to manage.
	'''
	def __init__(self):
		'''
		initiate the Strings
			'openingHtml': contains <html> and the header info 
			'closingHtml': contains </body></html>
			
			load the names of majors from a .txt file into a list (this is a stub) 
		'''
		self.openingHtml = open('CarlStats.html').read()
		self.content = ''
		self.closingHtml = '''</body></html>'''
		
		self.startYear = 0
		self.endYear = 0
		self.majorList = open('majorList.txt').read().splitlines()
		self.majorChecked = {}
		self.isQueried = False
		
		self.rowTemplate = open('rowTemplate.html').read()
		self.dataTemplate = open('dataTemplate.html').read()
		self.tableHeadingTemplate = open('tableHeadingTemplate.html').read()
	 	self.tableTemplate = open('tableTemplate.html').read()
	 	
	 	self.tableHtml = ''
		
		for major in self.majorList:
			self.majorChecked[major] = 0
		

	def getInput(self):
		'''
		Get user inputs from the python
		'''
		form = cgi.FieldStorage()
		
		for major in self.majorList:
			'''
			get user inputs in the checkboxes
			'''
			try:
				if major in form:
					self.majorChecked[major]= form[major].value
					self.isQueried = True
			except Exception, e:
				print "Content-type: text/html\r\n\r\n",
				print self.majorList
				print 'oops!'
				exit()
		
	def generateResult(self):
		self.content = open('CarlStatsResult.html').read() % self.tableHtml
		#also do other stuff...
	
	def generateTableDataRow(self, dictionaryData):
		'''
		Add a row to the instance variable tableHtml
		'''
		row = ''
		for elem in dictionaryData:
			row = ''.join( [ row, self.dataTemplate % dictionaryData[elem] ] )
		row = self.rowTemplate % row
		self.tableHtml = ''.join([self.tableHtml, row])
	
	def generateTableHeaderRow(self):
		pass
	
	def generateTable(self):
		self.tableHtml = self.tableTemplate % self.tableHtml

	def generate(self):
		'''
		Calling this to complete the html file
		'''
# 		stub
		if self.isQueried:
			stubHeader = {'Year':'Year', 1943:1943, 1945:1945, 1949: 1949, 1920:1920}
			stubDict = {None: '', 1943:400, 1945:500, 1949: 600, 1920:610}
			site.generateTableHeaderRow(stubHeader)
			site.generateTableDataRow(stubDict)
			self.generateTable()
			site.generateResult()
		print "Content-type: text/html\r\r\n\n",
		output = ''.join([self.openingHtml, self.content, self.closingHtml])
		print output

if __name__ == "__main__":
	try:	
		site = CarlStats()
		site.getInput()
		site.generate()
	except Exception, e:
		print "Content-type: text/html\r\r\n\n",
		print e
		print 'oops'
		exit()
# 	site.getInput()
# 	site.generate()
	


