import psycopg2
from sets import Set

class DataSource:
    def __init__(self, _user = 'ewinge', _password = 'riker692puppy'):
        self.user = _user
        self.password = _password
        self.connection = psycopg2.connect(user = self.user, database = self.user, password = self.password)
        self.cursor = self.connection.cursor()
    
    def get_all_graduates_from_year(self, year, gender = 'Both'):
        """Returns a dictionary with keys equal to each major in the dataset
           and values equal to the number of graduates with specified gender
           and with majors that are the corresponding key.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           
           gender is a string. Throws an exception if specified gender 
           isn't 'Male', 'Female', or 'Both'. If gender is Both, graduates of 
           any gender are considered."""
        
        return {}
        
    def get_graduates_from_all_years(self, major = 'Total', gender = 'Both'):
        """Returns a dictionary with keys equal to each year in the dataset
           and values equal to the number of graduates with 
           the specified major and specified gender in a year.
           
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'Total', graduates of any major 
           are considered.
           
           gender is a string. Throws an exception if the specified gender
           isn't 'Male', 'Female', or 'Both'. If gender is Both, graduates of 
           any gender are considered."""
        return self.get_graduates_in_year_range(2000,2013,major,gender)
        
    def get_graduates_in_year_range(self, start_year, end_year, major = 'Total', gender = 'Both'):
        """Returns a dictionary of the total number of graduates with a given
           major and given gender in all years in the range specified by the user.
           
           year_start and year_end are integers. year_start and year_end specify
           the range of years for which the dictionary includes information on graduates.
           Throws an exception if year_start or year_end are not years in our dataset.
           
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'Total', graduates of any major 
           are considered.
           
           gender is a string. Throws an exception if the specified gender
           isn't 'Male', 'Female', or 'Both'. If gender is Both, graduates of 
           any gender are considered."""
        results = {}
        query = "SELECT majorcode FROM majors WHERE major = '%s';" %(major)
        self.cursor.execute(query)
        major = self.cursor.fetchone()[0]
        query = "SELECT gendercode FROM gender WHERE gender = '%s';" %(gender)
        self.cursor.execute(query)
        gender = self.cursor.fetchone()[0]
        query = "SELECT major, graduates FROM majorcounts WHERE (year BETWEEN %s AND %s) AND major = %s AND gender = %s;"%(start_year, end_year, major, gender)
        self.cursor.execute(query)
        for line in self.cursor.fetchall():
            for k,v in line:
                results.setdefault(k,[]).append(v)
        return results
        
    def get_graduates_from_year(self, year, major = 'Total', gender = 'Both'):
        """Returns the number of graduates in a given year with a given major
           and given gender. 
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'Total', graduates of any major 
           are considered.
           
           gender is a string. Throws an exception if the specified gender
           isn't 'Male', 'Female', or 'Both'. If gender is Both, graduates of 
           any gender are considered."""
        query = "SELECT majorcode FROM majors WHERE major = '%s';" %(major)
        self.cursor.execute(query)
        major = self.cursor.fetchone()[0]
        query = "SELECT gendercode FROM gender WHERE gender = '%s';" %(gender)
        self.cursor.execute(query)
        gender = self.cursor.fetchone()[0]
        query = "SELECT graduates FROM majorcounts WHERE year = %s AND major = %s AND gender = %s;"%(year,major,gender)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_number_of_degrees_from_year(self, year):
        """Returns the total number of degrees awarded in any major in a given 
           year. Note that this is different from the total number of graduates:
           some graduates may be awarded degrees in mutliple majors.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset."""
        query = "SELECT graduates FROM majorcounts WHERE year = %s AND gender = %s AND major = %s;" %(year,2,49)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_number_of_degrees_from_all_years(self):
        """Returns a dictionary of the total number of degrees awarded in any
           major for all years in the dataset. Keys are years and values are
           the corresponding number of degrees awarded. Note that the total
           number of degrees awarded is different from the total number of 
           graduates because some graduates may be awarded degrees in mutliple 
           majors."""
        total = 0
        query = "SELECT major, graduates FROM majorcounts WHERE major = %s AND gender = %s;" %(48,2)
        self.cursor.execute(query)
        for line in self.cursor.fetchall():
            total += line[0]
        return total


    
    def get_number_of_degrees_in_year_range(self, start_year, end_year):
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
        results = {}       
        for i in range(start_year, end_year + 1, 1):
            query = "SELECT major, graduates FROM majorcounts WHERE year = %s AND major = %s AND gender = %s;" %(i,48,2)
            self.cursor.execute(query)
            for k,v in self.cursor.fetchone():
                results[k].append(v)
        return results
           
    
    def get_majors(self):
        """Returns a list of all majors in the dataset."""
        list_of_majors = []
        query = "SELECT major FROM majors;"
        self.cursor.execute(query)
        for major in self.cursor.fetchall():
            list_of_majors.append(major)
        return list_of_majors
        
    def get_years(self):
        """Returns a Set of all years in the dataset."""
        set_of_years = Set([])
        query = "SELECT year FROM majorcounts;"
        self.cursor.execute(query)
        for year in self.cursor.fetchall():
            set_of_years.add(year)
        return set_of_years
        
        
        
