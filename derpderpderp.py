'''
Created on Oct 12, 2013

@author: Eric
'''
import psycopg2

class DataSource:
    def __init__(self, _user = 'ewinge', _password = 'riker692puppy'):
        self.user = _user
        self.password = _password
        self.connection = psycopg2.connect(user = self.user, database = self.user, password = self.password)
        self.cursor = self.connection.cursor()
        self.total_graduates_code = self.get_code_of_total_graduates()
        self.total_majors_code = self.get_code_of_total_majors()
    
    def get_all_graduates_from_year(self, year, gender = 'Both'):
        """Returns a dictionary with keys equal to each major in the dataset
           and values equal to the number of graduates with specified gender
           and with majors that are the corresponding key.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           
           gender is a string. Throws an exception if specified gender 
           isn't 'Male', 'Female', or 'Both'. If gender is Both, graduates of 
           any gender are considered."""
        results = {}
        gender_code = self.convert_gender_to_code(gender)
        if(gender_code == 2):
            male_dict = self.get_all_graduates_from_year(year, 0)
            female_dict = self.get_all_graduates_from_year(year, 1)
            return self.add_dictionaries(male_dict, female_dict)
        
        majors = self.get_major_codes()
        for major in majors:
            query = "SELECT majors.major, majorcounts.graduates FROM majorcounts, majors WHERE majorcounts.year = %s AND majorcounts.gender = %s AND majorcounts.major = %s AND majors.majorcode = %s;" %(year, gender_code, major, major)
            self.cursor.execute(query)
            for k,v in self.cursor.fetchall():
                results.setdefault(k,[]).append(v)    
        return results

        
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
        """Returns key is year, value is counts,
            a dictionary of the total number of graduates with a given
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
        gender_code = self.convert_gender_to_code(gender)
        if gender_code == 2:
            male_dict = self.get_graduates_in_year_range(start_year, end_year, major, 0)
            female_dict = self.get_graduates_in_year_range(start_year, end_year, major, 1)
            return self.add_dictionaries(male_dict, female_dict)
        if major == 'Total' or major == self.get_code_of_total_graduates():
            major = self.get_code_of_total_graduates()
        else:
            query = "SELECT majorcode FROM majors WHERE major = '%s';" % (major)
            self.cursor.execute(query)
            major = self.cursor.fetchone()[0]
        query = "SELECT year, graduates FROM majorcounts WHERE (year BETWEEN %s AND %s) AND major = %s AND gender = %s;"%(start_year, end_year, major, gender_code)
        self.cursor.execute(query)
        for k,v in self.cursor.fetchall():
            results.setdefault(k,[]).append(v)
        return results
        
    def get_graduates_from_year(self, year, major = 'Total', gender = 'Both'):
        """Returns the number of graduates in a given year with a given major
           and given gender. 
           
           year is an integer.            
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'Total', graduates of any major 
           are considered.
           
           gender is a string. Throws an exception if the specified gender
           isn't 'Male', 'Female', or 'Both'. If gender is Both, graduates of 
           any gender are considered."""
        gender_code = self.convert_gender_to_code(gender)
        if gender_code == 2:
            male = self.get_graduates_from_year(year, major, 0)
            female = self.get_graduates_from_year(year, major, 1)
            return male + female   
  if(major == 'Total'):
            major = self.total_majors_code
        else:
            query = "SELECT majorcode FROM majors WHERE major = '%s';" %(major)
            self.cursor.execute(query)
            major = self.cursor.fetchone()[0]

        query = "SELECT graduates FROM majorcounts WHERE year = %s AND major = %s AND gender = %s;"%(year,major,gender_code)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_number_of_degrees_from_year(self, year):
        """Returns the total number of degrees awarded in any major in a given 
           year. Note that this is different from the total number of graduates:
           some graduates may be awarded degrees in mutliple majors.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset."""
        
        query = "SELECT graduates FROM majorcounts WHERE year = %s AND gender = %s AND major = %s;" %(year, 0, self.total_majors_code)
        self.cursor.execute(query)
        total = self.cursor.fetchone()[0]
       
        query = "SELECT graduates FROM majorcounts WHERE year = %s AND gender = %s AND major = %s;" %(year, 1, self.total_majors_code)
        self.cursor.execute(query)      
        total += self.cursor.fetchone()[0]
        return total
    
    def get_number_of_degrees_from_all_years(self):
        """Returns a dictionary of the total number of degrees awarded in any
           major for all years in the dataset. Keys are years and values are
           the corresponding number of degrees awarded. Note that the total
           number of degrees awarded is different from the total number of 
           graduates because some graduates may be awarded degrees in mutliple 
           majors."""
        male = {}
        total = {}
        query = "SELECT year, graduates FROM majorcounts WHERE major = %s AND gender = %s;" %(self.total_majors_code, 0)
        self.cursor.execute(query)
        for k,v in self.cursor.fetchall():
                male.setdefault(k,[]).append(v)
        query = "SELECT year, graduates FROM majorcounts WHERE major = %s AND gender = %s;" %(self.total_majors_code, 1)
        self.cursor.execute(query)
        for k,v in self.cursor.fetchall():
                total[k] = male[k][0] + v
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
        male = {}
        total = {}
        query = "SELECT year, graduates FROM majorcounts WHERE (year BETWEEN %s AND %s) AND major = %s AND gender = %s;" %(start_year, end_year, self.total_graduates_code, 0)
        self.cursor.execute(query)
        for k,v in self.cursor.fetchall():
    male[k] = v
        query = "SELECT year, graduates FROM majorcounts WHERE (year BETWEEN %s AND %s) AND major = %s AND gender = %s;" %(start_year, end_year, self.total_graduates_code, 1)
        self.cursor.execute(query)
        for k,v in self.cursor.fetchall():
    total[k] = male[k] + v
        return total
           
    
    def get_majors(self):
        """Returns a list of all majors in the dataset."""
        list_of_majors = []
        query = "SELECT major FROM majors;"
        self.cursor.execute(query)
        for major in self.cursor.fetchall():
            list_of_majors.append(major[0])
        return list_of_majors
        
    def get_years(self):
        """Returns a list of all years in the dataset."""
        list_of_years = []
        query = "SELECT year FROM majorcounts WHERE major = 0 AND gender = 0;"
        self.cursor.execute(query)
        for year in self.cursor.fetchall():
            list_of_years.append(year[0])
        return list_of_years

    def get_major_codes(self):
        '''returns a list of all possible major codes'''
        major_codes = []
        query = "SELECT majorcode FROM majors;"
        self.cursor.execute(query)
        for major in self.cursor.fetchall():
            major_codes.append(major[0])
        return major_codes
    
    def add_dictionaries(self, a, b):
        '''helper method merges two dictionaries without overwriting keys while summing the values'''
        for k in a:
            b[k][0] += a[k][0]
        return b
    
    def convert_gender_to_code(self, gender):
        '''converts string (Male, Female, Both) to numerical value used in the table'''
        if(gender == "Male"):
            return 0
        elif(gender == "Female"):
            return 1
        elif(gender == "Both"):
            return 2
        elif(gender == 0 or gender == 1):
            return gender
        else:
            return 2
    
    def get_code_of_total_graduates(self):
        '''returns the code for Total Number of Graduates'''
        query = "SELECT majorcode FROM majors WHERE major = 'Total Number of Graduates';" 
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_code_of_total_majors(self):
        '''returns the code for Total Majors'''
        query = "SELECT majorcode FROM majors WHERE major = 'Total Majors';" 
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
