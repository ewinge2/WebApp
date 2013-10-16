#!/usr/bin/python
'''
File:webapp.py
@author: Anne Grosse, Jialun Luo, Eric Ewing

This program will generate an html page to display to the browser. It will print a summary of results
when user inputs are entered.
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
####################
# 		'''
# 		@todo: REDOCUMENT THIS !!!! 
# 		'''
####################
		self.html = open('CarlStats.html').read()

		self.data_source = DataSource.DataSource()
		self.years = self.data_source.get_years()
		
		'''default years are the latest years, if one year is selected as both the start
		and end year then the data for only that year is returned.'''
		end_year = max(self.years)
		self.start_year = end_year
		self.end_year = end_year
		
		self.genders = Genders()
		#############################################
		### MAKE USE OF THIS!!!!! IN THE STUBBED CODE
		#############################################
	
#		self.is_major_queried = False
#		
#		self.row_alt_template = '<tr class="alt">%s</tr>'
#		self.row_template = '<tr>%s</tr>'
#		self.table_data_template = '<td rowspan="%s">%s</td>'
#		self.data_template = '<td>%s</td>'
#
#		self.table_heading_template = '<th rowspan="%s">%s</th>'
#		self.table_template = '<table class="%s" border="%s" cellpadding="%s">%s</table>'

		self.majors = self.data_source.get_majors()
		self.input = []
		
		self.form = cgi.FieldStorage()
		
		self.table = Table(self.start_year, self.end_year, self.majors)
			
	def get_showsource_input(self):
		'''
		@param form: 
		Display source file as plain text
		'''
		showsource=''
		if 'showsource' in self.form:
			showsource = self.form['showsource'].value
			self.print_file_as_plain_text(showsource)
		
	def print_file_as_plain_text(self, fileName):
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
			print 'Content-type: text/plain\r\n\r\n',
			print '404 file not found, someone goofed.'
			pass
		print 'Content-type: text/plain\r\n\r\n',
		print text

	def display_chosen_gender(self):
		'''Show user-chosen gender as selected in the html form'''
		self.show_as_selected(self.gender, "checked")
		
	def dispaly_chosen_years(self):
		'''Show user-chosen year as selected in the html form'''
		yearTag = ' selected="selected"'
		self.show_as_selected(self.start_year, yearTag)
		endYearIndex = self.html.find(str('end_year'))
		self.show_as_selected(self.end_year, yearTag, endYearIndex)
		
	def display_chosen_majors(self):
		"""Show user-chosen major as selected in the html form"""
		for major in self.majors:
			if major in self.input:
				self.show_as_selected(major, "checked")

	def show_as_selected(self, name, tag, indexToStartLooking=0):
		"""
		@param name: the name to be shown as selected in the HTML form
		@param tag: a html select/check tag
		Find index of 'name'  and insert 'tag'(s);
		Helper method to displayChosen**** methods
		"""
		index = self.find_index_for_selection_tag(name, indexToStartLooking)
		self.insert_selection_tag(index, tag)

	def find_index_for_selection_tag(self, name, indexToStartLooking=0):
		'''
		@param name the name to be searched for
		@param indexToStartLooking the index at which to start searching the HTML code
		Returns the index of the HTML (stored as a string) at which a selection tag should be inserted 
		(helper method for DisplayChosen*** methods)
		'''
		nameQuotes = '\"' + str(name) + '\"'
		return self.html.find(nameQuotes, indexToStartLooking) + len(nameQuotes)
	
	def insert_selection_tag(self, index, tag):
		'''
		@param index index of HTML string at which tag is to be inserted
		@param tag the HTML tag to be inserted
		Inserts the given HTML tag at the given index in our stored HTML template for generating the page
		'''
		self.html = self.html[:index] + tag + self.html[index:]
	
	def generate_checkbox_html(self):
		'''
		Generates the HTML code to display checkboxes for each major in majorlist. 
		For now, we generate the majors each time instead of using a static major list because we might rename majors in our data_source.
		'''
		checkboxCode = ""
		for major in self.majors:
			checkboxCode += '<input type="checkbox" name="' + major +'" value=1>' + major + '<br>'
		return checkboxCode
	
	def get_major_input(self):
		gender = self.sanitize_gender_input(self.form)
		if "SelectAll" in self.form:
			self.input = self.majors
		elif "UnselectAll" in self.form:
			self.input = []
		else:
			selectedMajors = []
			for inputName in self.form:
				# check it's actually a major and isn't
				if inputName in self.majors:
					selectedMajors.append(inputName)
			self.input = selectedMajors
	
	def sanitize_gender_input(self):
		gender = "Both"
		if "gender" in self.form and (self.form["gender"].value == "Male" or self.form["gender"].value == "Female"):
			gender = self.form["gender"].value
		self.gender = gender
		return gender
	
	def get_yeat_input(self):
		'''
		Extract the user input about years
		'''
		try:
			if 'start_year' in self.form and 'end_year' in self.form:
				self.start_year = int(self.form['start_year'].value)
				self.end_year = int(self.form['end_year'].value)
			elif 'queryYear' in self.form:
				self.topMajorYear = int(self.form['queryYear'].value)
			self.sanitize_year_input()
		except Exception, e:
			pass
	
	def sanitize_year_input(self):
		'''Sanitize year input so that the year is an integer between our maximum year and minimum year'''
		if not self.start_year in self.years:
			self.start_year = max(self.years)
		if not self.end_year in self.years:
			self.end_year = max(self.years)
		if self.start_year > self.end_year:
			self.start_year = self.end_year
		self.table.start_year = self.start_year
		self.table.end_year = self.end_year

	def get_gender_input(self):
		'''Extract the user input about genders'''
		if "gender" in self.form:
			if self.form["gender"].value == "Male" or self.form["gender"].value == "Female" or self.form['gender'].value == 'Both':
				self.gender = self.form["gender"].value
			### if user messes with URL and gender isn't male or female, it's assigned default value of "both"
	
	def get_query_input(self):
		'''Extract the user input about query types'''		
		queryName = 'queryType' 
		if queryName in self.form and self.form[queryName].value == 'normal' and self.input:
			self.is_major_queried = True
	
	def get_input(self):
		'''Get user inputs from the python'''
		self.get_major_input()
		self.get_query_input()
		self.get_yeat_input()
		self.get_gender_input()
		self.get_showsource_input()
		
	def process_query(self):
		'''Generate and send different queries to the server based on what received query
		'''
		if self.is_major_queried:
			resultHtml = self.get_result_html() % self.table.generate_table(self.get_major_versus_num_grad_data())
			self.html = ''.join([self.html, resultHtml])

	def get_result_html(self):
		return open('CarlStatsResult.html').read()
	
#	def generate_table_row(self, firstColumn, listData, endColumnNote, isHeader = False, \
#								firstColumnRowspan = 1, cellRowspan = 1, isColored = True):
#		'''Generate a table row in html text.'''
#		###############################################
#		### DOCUMENT THIS!!!!!!
#		###############################################
#		template = ''
#		row = ''
#		
#		'''initialize the template to either heading style or data cell style
#		according to the given boolean isHeader, whose default value is False 
#		'''
#		if isHeader:
#			template = html_templates.table_heading_template
#		else:
#			template = html_templates.table_data_template	
#		
#		if firstColumn:
#			'''	If a major name is given, put it at the first column and set its firstColumnRowspan (default = 1)'''
#			row = template % (firstColumnRowspan, firstColumn)
#			
#		'''Set the rowspan to cellRowspan because we are adding inner cells now'''
#		template = template % (cellRowspan, "%s")
#		
#		for elem in listData:
#			'''	insert all data from the given listData into the row'''
#			row = ''.join( [ row, template % elem ] )
#		
#		if endColumnNote:
#			'''Append the endColumnNote to the last column of this row'''
#			row = ''.join([row, template % (endColumnNote)])
#		
#		if isColored:
#			row = html_templates.row_alt_template % row
#		else:
#			row = html_templates.row_template % row
#		
#		return row
	
#	def generate_table_html(self, rowHtml, tableClass = None, border = 1, cellpadding = 5):
#		'''
#		Encapsulates given input with 
#		<table class="tableClass" border = "border" cellpadding = cellpadding> rowHtml </table>
#		'''
#		return html_templates.table_template % (tableClass, border, cellpadding, rowHtml)

#	def generate_table(self, dictionaryData, tableClass  = 'resultTable', border = 1, cellpadding = 7):
#		'''
#		@return: a well-formmatted table in html text.
#		Basically is <table> ... </table>
#		'''
#		headerYearRow = Table.generate_row('Year', range(self.start_year, self.end_year+1), 'GENDER', \
#							isHeader=True, firstColumnRowspan=1, cellRowspan=2, isColored=False)
#		headerMajorRow = Table.generate_row('MAJOR', [], '', isHeader=True,\
#							firstColumnRowspan=1, cellRowspan=1, isColored=False)
#
#		row = ''
#		rowsHtml = ''
#		isRowColored = True
#		
#		for major in self.majors:
#			majorName = major
# 			
#			for gender in dictionaryData:
#				if major in dictionaryData[gender]:
#					row = Table.generate_row(majorName, dictionaryData[gender][major], gender,\
#											 firstColumnRowspan=3, isColored = isRowColored)
#					rowsHtml = ''.join([rowsHtml, row])
#					'''This is to toggle the second line for values of different gender'''
#					majorName = None
#			'''This is used for switching colored row and not colored row between majors'''
#			isRowColored = not isRowColored
#		
#		rowsHtml = ''.join([headerYearRow, headerMajorRow, rowsHtml])
#		
#		return self.generate_table_html(rowsHtml, tableClass, border, cellpadding)
#
	def get_major_versus_num_grad_data(self):
		'''
		Query for every major in the self.input 
		@return : a dictionary {key == majorName, 
				value == [] a list of number of graduates ordered by ascending year}
		'''
		genderMajorNumGradDictionary = {}
		
		########################
		####   STUBBING THE FOR LOOP'S CONDITION FROM self.input to ['Male', 'Female', 'Both']
		########################
		for gender in ['Male', 'Female', 'Both']:
			genderMajorNumGradDictionary[gender] = {}
			for majorName in self.majors:
				if majorName in self.input:
					genderMajorNumGradDictionary[gender][majorName] = []
					rawData = self.data_source.get_graduates_in_year_range(self.start_year,\
															self.end_year, majorName, gender)
					for i in range(self.start_year, self.end_year+1):
						genderMajorNumGradDictionary[gender][majorName].append(rawData[i])
		return genderMajorNumGradDictionary

	def close_html(self):
		self.html = ''.join([self.html, '</body></html>'])

	def generate(self):
		############################
		####'''REDOCUMENT THIS !!!!!'''
		############################
		print "Content-type: text/html\r\r\n\n",
		self.html = self.html % self.generate_checkbox_html()
		self.dispaly_chosen_years()
		self.display_chosen_gender()
		self.display_chosen_majors()
		self.close_html()
		print self.html


class Table:
	'''a class capable of generating a table in html formatting'''
	def __init__(self, start_year, end_year, majors):
		self.start_year = start_year
		self.end_year = end_year
		self.majors = majors
	
	
	def generate_row(self, firstColumn, listData, endColumnNote, isHeader = False, \
								firstColumnRowspan = 1, cellRowspan = 1, isColored = True):
		'''Generate a table row in html text.'''
		###############################################
		### DOCUMENT THIS!!!!!!
		###############################################
		template = ''
		row = ''
		
		'''initialize the template to either heading style or data cell style
		according to the given boolean isHeader, whose default value is False 
		'''
		if isHeader:
			template = html_templates.table_heading_template
		else:
			template = html_templates.table_data_template	
		
		if firstColumn:
			'''	If a major name is given, put it at the first column and set its firstColumnRowspan (default = 1)'''
			row = template % (firstColumnRowspan, firstColumn)
			
		'''Set the rowspan to cellRowspan because we are adding inner cells now'''
		template = template % (cellRowspan, "%s")
		
		for elem in listData:
			'''	insert all data from the given listData into the row'''
			row = ''.join( [ row, template % elem ] )
		
		if endColumnNote:
			'''Append the endColumnNote to the last column of this row'''
			row = ''.join([row, template % (endColumnNote)])
		
		if isColored:
			row = html_templates.row_alt_template % row
		else:
			row = html_templates.row_template % row
		
		return row
	
	def generate_html(self, rowHtml, tableClass = None, border = 1, cellpadding = 5):
		'''
		Encapsulates given input with 
		<table class="tableClass" border = "border" cellpadding = cellpadding> rowHtml </table>
		'''
		return html_templates.table_template % (tableClass, border, cellpadding, rowHtml)
	
	def generate_table(self, dictionaryData, tableClass  = 'resultTable', border = 1, cellpadding = 7):
		'''
		@return: a well-formmatted table in html text.
		Basically is <table> ... </table>
		'''
		headerYearRow = self.generate_row('Year', range(self.start_year, self.end_year+1), 'GENDER', \
							isHeader=True, firstColumnRowspan=1, cellRowspan=2, isColored=False)
		headerMajorRow = self.generate_row('MAJOR', [], '', isHeader=True,\
							firstColumnRowspan=1, cellRowspan=1, isColored=False)

		row = ''
		rowsHtml = ''
		isRowColored = True
		
		for major in self.majors:
			majorName = major
			
			for gender in dictionaryData:
				if major in dictionaryData[gender]:
					row = Table.generate_row(majorName, dictionaryData[gender][major], gender,\
											 firstColumnRowspan=3, isColored = isRowColored)
					rowsHtml = ''.join([rowsHtml, row])
					'''This is to toggle the second line for values of different gender'''
					majorName = None
			'''This is used for switching colored row and not colored row between majors'''
			isRowColored = not isRowColored
		
		rowsHtml = ''.join([headerYearRow, headerMajorRow, rowsHtml])
		
		return self.generate_table_html(rowsHtml, tableClass, border, cellpadding)
	
class Genders:
	'''a quick python version of an enum contains the strings
	 of the genders and a list for checking sanitizing input'''
	male = 'Male'
	female = 'Female'
	both = 'Both'
	genders = ['Male','Female','Both']

	
class html_templates:
	'''enum for html templates'''
	row_alt_template = '<tr class="alt">%s</tr>'
	row_template = '<tr>%s</tr>'
	table_data_template = '<td rowspan="%s">%s</td>'
	data_template = '<td>%s</td>'
	table_heading_template = '<th rowspan="%s">%s</th>'
	table_template = '<table class="%s" border="%s" cellpadding="%s">%s</table>'


if __name__ == "__main__":
	site = CarlStats()
	site.get_input()
	site.process_query()
	site.generate()
