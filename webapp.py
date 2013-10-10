#!/usr/bin/python
'''
File:webapp.py
Authors: Anne Grosse and Jialun "Julian" Luo
Last edited: 2013/10/10

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
		self.gender = "Both"
	
		self.isQueried = False
		
		self.rowTemplate = '<tr>%s</tr>'
		self.dataTemplate = '<td>%s</td>'
		self.tableHeadingTemplate = '<th>%s</th>'
	 	self.tableTemplate = open('tableTemplate.html').read()
	 	
	 	self.tableHtml = ''
	 	
		self.majorList = open('majorList.txt').read().splitlines()
		self.majorInput = {}
		self.initializeMajorInput()
		self.genderList = ['Male', 'Female', 'Both']
	
	def initializeMajorInput(self):
	    for major in self.majorList:
			self.majorInput[major] = 0
	    
	def showYearAsSelected(self, year, indexToStartLooking):
	    html = self.openingHtml[indexToStartLooking:]
	    stYr = '"' + str(year) + '"'
	    stYrPos = html.find(stYr) + len(stYr)
	    self.openingHtml = self.openingHtml[:indexToStartLooking] + html[:stYrPos] + ' selected="selected"' + html[stYrPos:]
	    
	def displayChosenGender(self):
	    html = self.openingHtml
	    gdrStr = '"' + self.gender + '"'
	    gdrPos = html.find(gdrStr) + len(gdrStr)
	    self.openingHtml = html[:gdrPos] + " checked" + html[gdrPos:]
	    
	def displayChosenYears(self):
	    self.showYearAsSelected(self.startYear, 0)
	    endIndex = self.openingHtml.find(str(self.endYear))
	    self.showYearAsSelected(self.endYear, endIndex)
	    
	def displayChosenMajors(self):
	    for major in self.majorList:
	        if self.majorInput.get(major) == 1:
	            self.showMajorAsSelected(major)
        
	def showMajorAsSelected(self, major):
	    html = self.openingHtml
	    mjrStr = '"' + major + '"'
	    mjrPos = html.find(mjrStr) + len(mjrStr)
	    self.openingHtml = html[:mjrPos] + ' checked="checked"' + html[mjrPos:]
	
	def getMajorInput(self, form):
	    for major in self.majorList:
			'''
			get user inputs in the checkboxes
			'''
			if major in form:
					self.majorInput[major]= int(form[major].value)
					self.isQueried = True
	
	def getYearInput(self, form):
	    if 'startYear' in form and 'endYear' in form:
			try: self.startYear = int(form['startYear'].value)
			except Exception, e:
			    pass
			try: self.endYear = int(form['endYear'].value)
			except Exception, e:
			    pass
	        ### if startYear or endYear isn't an int, assigns them default value of 2013
	        ### there will still be an issue when using DataSource.py if startYear > endYear
	
	def getGenderInput(self, form):
	    if "gender" in form:
	        if form["gender"].value == "Male" or form["gender"].value == "Female":
	            self.gender = form["gender"].value
	        ### if user messes with URL and gender isn't male or female, it's assigned default value of "both"
	
	def getInput(self):
		'''
		Get user inputs from the python
		'''
		form = cgi.FieldStorage()
		
		self.getYearInput(form)
		self.getMajorInput(form)
		self.getGenderInput(form)
		
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
		row = self.tableHeadingTemplate % 'Year'
		for year in range(int(self.startYear), int(self.endYear)):
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
			stubHeader = {'Year':'Year', 1943:1943, 1945:1945, 1949: 1949, 1920:1920}
			stubDict = {None: '', 1943:400, 1945:500, 1949: 600, 1920:610}
			site.generateTableHeaderRow()
			site.generateTableDataRow(stubDict)
			self.generateTable()
			site.generateResult()
		print "Content-type: text/html\r\r\n\n",
		self.displayChosenYears()
		self.displayChosenGender()
		self.displayChosenMajors()
		output = ''.join([self.openingHtml, self.content, self.closingHtml])
		print output

if __name__ == "__main__":
	site = CarlStats()
	site.getInput()
	site.generate()

	


