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
		
		self.database = DataSource.DataSource()
		
		self.minYear = 2001
		self.maxYear = 2013
		
		self.startYear = 2013
		self.endYear = 2013
		self.gender = "Both"
	
		self.isQueried = False
		
		self.rowAltTemplate = '<tr class="alt">%s</tr>'
		self.rowTemplate = '<tr>%s</tr>'
		self.dataTemplate = '<td>%s</td>'
		self.tableHeadingTemplate = '<th rowspan="%s">%s</th>'
	 	self.tableTemplate = '<table class="resultTable" border="1" cellpadding="7">%s</table>'
	 	
	 	self.isRowColored = 0
	 	
	 	self.tableHtml = ''
	 	
	 	#Initialize majorInput to {majorName:0}
		self.majorList = self.database.get_majors()
		self.majorInput = {}
		self.setAllMajorsInput(0)
		
		
		
		
		self.debug = 0
	
	
	def setAllMajorsInput(self, value):
		'''
		Sets the value of all majors in majorInput to the passed in value
		'''
		for major in self.majorList:
			self.majorInput[major] = value


	def getShowsourceInput(self, form):
		'''
		'''
		showsource=''
		if 'showsource' in form:
			showsource = form['showsource'].value
			self.printFileAsPlainText(showsource)
		
	def printFileAsPlainText(self,fileName):
	    ''' 
	    	Credit: Jeff Ondich
	    	Prints to standard output the contents of the specified file, preceded
	        by a "Content-type: text/plain" HTTP header.
	    '''
	    text = ''
	    try:
	        f = open(fileName)
	        text = f.read()
	        f.close()
	    except Exception, e:
	        pass
	
	    print 'Content-type: text/plain\r\n\r\n',
	    print text

	def displayChosenGender(self):
		'''Show user-chosen gender as selected in the html form'''
		self.showAsSelected(self.gender, "checked")
	    
	def displayChosenYears(self):
		'''Show user-chosen year as selected in the html form'''
		yearTag = ' selected="selected"'
		self.showAsSelected(self.startYear, yearTag)
		endYearIndex = self.openingHtml.find(str('endYear'))
		self.showAsSelected(self.endYear, yearTag, endYearIndex)
	    
	def displayChosenMajors(self):
	    """Show user-chosen major as selected in the html form"""
	    majorCheckTag = "checked"
	    for major in self.majorList:
	        if self.majorInput.get(major) == 1:
	            self.showAsSelected(major, majorCheckTag)

	def showAsSelected(self, name, tag, indexToStartLooking=0):
		"""
		@param name: the name to be shown as selected in the HTML form
		@param tag: a html select/check tag
		Find index of 'name'  and insert 'tag'(s);
		Helper method to displayChosen**** methods
		"""
		index = self.findIndexForSelectionTag(name, indexToStartLooking)
		self.insertSelectionTag(index, tag)

	def findIndexForSelectionTag(self, name, indexToStartLooking=0):
		'''
		@param name the name to be searched for
		@param indexToStartLooking the index at which to start searching the HTML code
		Returns the index of the HTML (stored as a string) at which a selection tag should be inserted 
		(helper method for DisplayChosen*** methods)
		'''
		nameQuotes = '\"' + str(name) + '\"'
		return self.openingHtml.find(nameQuotes, indexToStartLooking) + len(nameQuotes)
	
	def insertSelectionTag(self, index, tag):
		'''
		@param index index of HTML string at which tag is to be inserted
		@param tag the HTML tag to be inserted
		Inserts the given HTML tag at the given index in our stored HTML template for generating the page
		'''
		self.openingHtml = self.openingHtml[:index] + tag + self.openingHtml[index:]
	
	def generateCheckboxCode(self):
		'''
		Generates the HTML code to display checkboxes for each major in majorlist. 
		For now, we generate the majors each time instead of using a static major list because we might rename majors in our database.
		'''
		checkboxCode = ""
		for major in self.majorList:
			checkboxCode += '<input type="checkbox" name="' + major +'" value=1>' + major + '<br>'
		return checkboxCode
	
	def getMajorInput(self, form):
	    '''
	    Extract the user input about majors
	    '''
	    if "SelectAll" in form:
	    	#user chose all majors
	    	self.setAllMajorsInput(1)
	    elif "UnselectAll" in form:
	    	#user chose no majors
	    	self.setAllMajorsInput(0)
	    else:		
	    	for major in self.majorList:
				'''
				for each major individually selected by user, record this information
				'''
				if major in form:
						self.majorInput[major]= 1
						self.isQueried = True
	
	def getYearInput(self, form):
	    '''
	    Extract the user input about years
	    '''
	    if 'startYear' in form and 'endYear' in form:
			try: self.startYear = int(form['startYear'].value)
			except Exception, e:
			    pass
			try: self.endYear = int(form['endYear'].value)
			except Exception, e:
			    pass

			if self.startYear < self.minYear:
				self.startYear = self.minYear
			elif self.startYear > self.maxYear:
				self.startYear = self.maxYear
			
			if self.endYear > self.maxYear:
				self.endYear = self.maxYear
			elif self.endYear < self.minYear:
				self.endYear = self.minYear
			
			if self.endYear < self.startYear:
				self.endYear = self.startYear
			
			
				

		
	        ### if startYear or endYear isn't an int, assigns them default value of 2013
	        ### there will still be an issue when using DataSource.py if startYear > endYear
	
	def getGenderInput(self, form):
	    '''
	    Extract the user input about genders
	    '''
	    if "gender" in form:
	        if form["gender"].value == "Male" or form["gender"].value == "Female" or form['gender'].value == 'Both':
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
		self.getShowsourceInput(form)
		
		
		
	def generateResult(self):
		'''Generate html text for result
		'''
		self.content = open('CarlStatsResult.html').read() % self.tableHtml
		#also do other stuff...
	
	
	
	
	def generateTableDataRow(self, majorName, listData):
		'''
		Add a row to the instance variable tableHtml
		'''
		row = self.dataTemplate % majorName
		for elem in listData:
			row = ''.join( [ row, self.dataTemplate % elem ] )
		if (self.isRowColored % 2):
			row = self.rowTemplate % row
		else:
			row = self.rowAltTemplate % row
		self.isRowColored += 1
		self.tableHtml = ''.join([self.tableHtml, row])
	
	def generateTableYearRow(self):
		'''
		Generate the top row which depends on the year span
		'''
		row = self.tableHeadingTemplate % (1, 'YEAR')
		for year in range(self.startYear, self.endYear + 1):
			row = ''.join([row, self.tableHeadingTemplate % (2, year)])
		row = self.rowTemplate % row
		majorHeading = self.tableHeadingTemplate % (1, 'MAJOR')
		row = ''.join([row, self.rowTemplate % majorHeading])
		self.tableHtml = ''.join([self.tableHtml, row])
	
	def generateTable(self):
		self.tableHtml = self.tableTemplate % self.tableHtml

	
	def queryData(self):
		if self.isQueried:
			
			self.generateTableYearRow()
			for major in self.majorList:
				if self.majorInput[major] != 0:
					'''
					@todo: gender specification hasn't been implemented yet!!!
					'''
					try:
						majorName = major
						majorNumGradDict = self.database.get_graduates_in_year_range(self.startYear, \
																self.endYear, majorName, self.gender)
						numGradList = []
						for year in range(self.startYear, self.endYear+1):
							numGradList.append(majorNumGradDict[year])
	
						self.generateTableDataRow(majorName, numGradList)
					except:
						print 'content-type: text/plain\r\n\r\n',
						print majorName
						print majorNumGradDict
						exit()
			self.generateTable()
			self.generateResult()

	

	def generate(self):
		'''
		Calling this to complete the html file
		'''
		
		print "Content-type: text/html\r\r\n\n",
		self.openingHtml = self.openingHtml % self.generateCheckboxCode()
		self.displayChosenYears()
		self.displayChosenGender()
		self.displayChosenMajors()
		output = ''.join([self.openingHtml, self.content, self.closingHtml])
		print output
		

if __name__ == "__main__":
	site = CarlStats()
	site.getInput()
	site.queryData()
	site.generate()

	

