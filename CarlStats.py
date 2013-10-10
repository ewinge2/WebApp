#!/usr/bin/python
'''
File:webapp.py
Author: Anne Gross, Jialun "Julian" Luo
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
		
		self.startYear = 2013
		self.endYear = 2013
		
		self.majorList = open('majorList.txt').read().splitlines()
		self.majorChecked = {}
		self.isQueried = False
		
		self.rowTemplate = '<tr>%s</tr>'
		self.dataTemplate = '<td>%s</td>'
		self.tableHeadingTemplate = '<th>%s</th>'
	 	self.tableTemplate = '''	
	 	<table border=\"1\" cellpadding=\"10\">
		%s		
		</table>'''
	 	
	 	self.tableHtml = ''
	 	self.checkboxCode = ''
	 	
	 	self.gender = ['Male', 'Female', 'All Genders']
		
		for major in self.majorList:
			self.majorChecked[major] = 0
		

	def getInput(self):
		'''
		Get user inputs from the python
		'''
		form = cgi.FieldStorage()
		
		if 'startYear' in form and 'endYear' in form:
			self.startYear = int(form['startYear'].value)
			self.endYear = int(form['endYear'].value)
			
		for gender in self.gender:
			if gender in form:
				genderSelected = gender
						
		for major in self.majorList:
			'''
			get user inputs in the checkboxes
			'''
			try:
				if major in form:
					self.majorChecked[major] = int(form[major].value)
					self.isQueried = True
			except Exception, e:
				print "Content-type: text/html\r\n\r\n",
				print self.majorList
				print 'oops!'
				exit()
		
	def generateResult(self):
		self.content = open('CarlStatsResult.html').read() % self.tableHtml
		#also do other stuff...
	
	def produceCheckboxes(self):
		'''
		retain user inputs
		'''
		gender = ['Male', 'Female', 'All Genders']
		   
	    for major in self.majorList:
	        checked = ''
	        if self.majorChecked.get(major) == 1:
	            checked = 'checked="checked"'
	        self.checkboxCode += '<input type="checkbox" name="' + major + '" ' + checked + 'value=1>' + major +'<br>'
	
	def generateTableDataRow(self, majorName, listData):
		'''
		Add a row to the instance variable tableHtml
		'''
		row = self.dataTemplate % majorName
		for elem in listData:
			row = ''.join( [ row, self.dataTemplate % elem ] )
		row = self.rowTemplate % row
		self.tableHtml = ''.join([self.tableHtml, row])
	
	def generateTableYearRow(self):
		'''
		Generate the top row which includes the year span of query
		'''
		row = self.tableHeadingTemplate % 'Year'
		for year in range(self.startYear, self.endYear + 1):
			row = ''.join([row, self.tableHeadingTemplate % year])
		self.tableHtml = ''.join([self.tableHtml, row])
	
	def generateTable(self):
		self.tableHtml = self.tableTemplate % self.tableHtml

	def generate(self):
		'''
		Calling this to complete the html file
		'''
# 		stub
		if self.isQueried:
			stubList = [999, 1419, 1241, 1239, 2310]
			self.generateTableYearRow() 
			self.generateTableDataRow('stubMajor', stubList)
			self.generateTable()
			self.generateResult()
		print "Content-type: text/html\r\r\n\n",
		self.produceCheckboxes()
		output = ''.join([self.openingHtml % self.checkboxCode, self.content, self.closingHtml])
		print output

if __name__ == "__main__":
# 	try:
	site = CarlStats()
	site.getInput()
	site.generate()
# 	except Exception, e:
# 		print "Content-type: text/html\r\r\n\n",
# 		print 
# 		print
# 		print 'oops'
# 		exit()
# 	site.getInput()
# 	site.generate()
	


