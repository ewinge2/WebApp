import psycopg2


class DataSource:
    def __init__(self):
        '''
        @attentions: You need to fill in the psw password, dbn database name (which is just your username)
        and usn username. Otherwise, it will not connect to anywhere
        '''
        psw = ''
        dbn = ''
        usn = ''
        comm = psycopg2.connect(database = dbn, user=usn, password=psw)
        self.cursor = comm.cursor()
        

    def get_all_graduates_from_year(self, year, gender = 'T'):
        """Returns a dictionary with keys equal to each major in the dataset
           and values equal to the number of graduates with specified gender
           and with majors that are the corresponding key.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           
           gender is a string. Throws an exception if specified gender 
           isn't 'male', 'female', or 'all'. If gender is all, graduates of 
           any gender are considered."""
        return {}
        
    def get_graduates_from_all_years(self, major = 'all', gender = 'T'):
        """Returns a dictionary with keys equal to each year in the dataset
           and values equal to the number of graduates with 
           the specified major and specified gender in a year.
           
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'all', graduates of any major 
           are considered.
           
           gender is a string. Throws an exception if the specified gender
           isn't 'male', 'female', or 'all'. If gender is all, graduates of 
           any gender are considered."""
        return {}
        
    def getNumGraduateInYearSpan(self, startYear, endYear, major = '', gender = 'T'):
        '''
        @return: a list of number of graduates of a specific major 
        in the given year span, ordered by year ascendingly.
        '''
        if not major:
            'if no major is given, cancel this execution, because I have not figured out what exactly happened'
            return
        
        query = 'SELECT graduates FROM majors WHERE year >= %s AND year <= %s AND major=\'%s\'AND gender=\'%s\' ORDER BY year ASC;'
        query = query % (startYear, endYear, major, gender)
        
        self.cursor.execute(query)
        rawDataList = self.cursor.fetchall()
        numGraduateInYearSpan = []
        for data in rawDataList:
            numGraduateInYearSpan.append(data[0])           
        return numGraduateInYearSpan
        
    def get_graduates_from_year(self, year, major = 'all', gender = 'T'):
        """Returns the number of graduates in a given year with a given major
           and given gender. 
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'all', graduates of any major 
           are considered.
           
           gender is a string. Throws an exception if the specified gender
           isn't 'male', 'female', or 'all'. If gender is all, graduates of 
           any gender are considered."""
        return 0
    
    def get_number_of_degrees_from_year(self, year):
        """Returns the total number of degrees awarded in any major in a given 
           year. Note that this is different from the total number of graduates:
           some graduates may be awarded degrees in mutliple majors.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset."""
        return 0
    
    def get_number_of_degrees_from_all_years(self):
        """Returns a dictionary of the total number of degrees awarded in any
           major for all years in the dataset. Keys are years and values are
           the corresponding number of degrees awarded. Note that the total
           number of degrees awarded is different from the total number of 
           graduates because some graduates may be awarded degrees in mutliple 
           majors."""
        return {}
    
    def get_number_of_degrees_in_year_range(self, year_start, year_end):
        """Returns a dictionary of the total number of degrees awarded in any
           major for all years in the user-specified range. Keys are years and 
           values are the corresponding number of degrees awarded. Note that the
           total number of degrees awarded is different from the total number of 
           graduates because some graduates may be awarded degrees in mutliple 
           majors.
           
           year_start and year_end are integers. year_start and year_end 
           specify the range of years for which the dictionary contains information
           on degrees. Throws an exception if year_start or year_end are not 
           years in our dataset."""
        return {}
