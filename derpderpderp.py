import psycopg2


class DataSource:
    def __init__(self):
        psw = 'meow372pony'
        dbn = 'luoj'
        usn = 'luoj'
        comm = psycopg2.connect(database = dbn, user=usn, password=psw)
        self.cursor = comm.cursor()
        
        
        self.mainDatabaseName = 'majorcounts'
        self.majorNameDBName = 'majors'
        self.genderDBName = 'genders'
        

    def get_all_graduates_from_year(self, year, gender = 'Both'):
        """Returns a dictionary with keys equal to each major in the dataset
           and values equal to the number of graduates with specified gender
           and with majors that are the corresponding key.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           
           gender is a string. Throws an exception if specified gender 
           isn't 'male', 'female', or 'all'. If gender is all, graduates of 
           any gender are considered."""
        return {}
        
    def get_graduates_from_all_years(self, major = 'all', gender = 'Both'):
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
    
    
    def get_graduates_in_year_range(self, year_start, year_end, major_input = 'Total', gender_input = 'Both'):
        """Returns a dictionary of the total number of graduates with a given
           major_input and given gender_input in all years in the range specified by the user.
           
           year_start and year_end are integers. year_start and year_end specify
           the range of years for which the dictionary includes information on graduates.
           Throws an exception if year_start or year_end are not years in our dataset.
           
           major_input is a string. Throws an exception if the specified major_input isn't 
           a major_input in our dataset. If major_input is 'Total', graduates of any major_input 
           are considered.
           
           gender_input is a string. If the specified gender
           isn't 'Male' or 'Female', graduates of 
           any gender are considered.
           
           @return: a list of number of graduates of a specific major_input 
           in the given year span, ordered by year ascendingly.
        """
        major = major_input
        
        gender = self.sanitize_gender_input(gender_input)
        
        if "'" in major:
            '''This is to take care of the single quote in major_input name'''
            major = major.replace("'","\\\'")
            
            

        majorCodeQuery = 'SELECT majorcode FROM majors WHERE major = \'%s\'' % major
        self.cursor.execute(majorCodeQuery)
        majorCode = self.cursor.fetchall()[0][0]
        
        
        genderCodeQuery = 'SELECT genderCode FROM gender WHERE gender = \'%s\'' % gender
        self.cursor.execute(genderCodeQuery)
        genderCode = self.cursor.fetchall()[0][0]
        
        query = 'SELECT year, graduates FROM majorcounts WHERE year \
                 >= %s AND year <= %s AND major=\'%s\'AND gender=\'%s\' ORDER BY year ASC;'
        query = query % (year_start, year_end, majorCode, genderCode)
        
        
        self.cursor.execute(query)
        rawDataList = self.cursor.fetchall()
        numGraduateInYearSpan = {}
        for data in rawDataList:
            numGraduateInYearSpan[data[0]] = data[1]
        return numGraduateInYearSpan

    
    def get_top_N_popular_major_in_year(self, year, topN = 5, gender_input = 'Both'):
        '''Return a list of tuples of most popular majors and the number of graduates in those majors
        @param year: The year of query
        @param topN: Default to be 5, how many top majors you want to query
        '''
        gender = self.sanitize_gender_input(gender_input)
        query = 'SELECT majors.major, majorcounts.graduates FROM majorcounts \
                    WHERE year = %s ORDER BY DESC LIMIT %s' % (year, topN)
        self.cursor.execute(query)
        rawDataList = self.cursor.fetchall()
        topMajorGradTupleInYear = {}
        for data in rawDataList:
            topMajorGradTupleInYear[data[0]] = data[1]
        
        


    def get_graduates_from_year(self, year, major = 'all', gender = 'Both'):
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
    
    def get_majors(self):        
        """Returns a list of all majors in the dataset."""
        
        query = 'SELECT major FROM %s ORDER BY majorcode ASC;' % self.majorNameDBName
        self.cursor.execute(query)
        rawDataList = self.cursor.fetchall()
        numGraduateInYearSpan = []
        for data in rawDataList:
            numGraduateInYearSpan.append(data[0])
        return numGraduateInYearSpan
        
    def get_years(self):
        """Returns a list of all years in the dataset."""
        query = 'SELECT year FROM '
        return []
    
    def sanitize_gender_input(self, gender_input):
        if gender_input != 'Male' or gender_input != 'Female' or gender_input != 'Both':
            gender_input = 'Both'
        return gender_input
