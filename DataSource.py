class DataSource:
    def __init__(self):
        pass
    
    def get_all_graduates_from_year(self, year, gender = 'all'):
        """Returns a dictionary of the number of graduates with each 
           major in a given year. Each key is a major, with value equal 
           to the number of graduates with that major and with the 
           specified gender.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset.
           gender is a string. Throws an exception if specified gender 
           isn't 'male', 'female', or 'all'. If gender is all, graduates of 
           any gender are considered."""
        return {}
        
    def get_graduates_from_all_years(self, major = 'all', gender = 'all'):
        """Returns a dictionary of the total number of graduates with a 
           given major in all years in the dataset. Each key 
           is a year, with value equal to the number of graduates with 
           the specified major in that year. If no major was specified, the 
           dictionary contains values equal to the total number of graduates 
           in a year.
           
           major is a string. Throws an exception if the specified major isn't 
           a major in our dataset. If major is 'all', graduates of any major 
           are considered.
           gender is a string. Throws an exception if the specified gender
           isn't 'male', 'female', or 'all'. If gender is all, graduates of 
           any gender are considered."""
        return {}
        
    def get_graduates_from_year(self, year, major = 'all', gender = 'all'):
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
        """Returns the total number of degrees awarded in any major. Note
           that this is different from the total number of graduates:
           some graduates may be awarded degrees in mutliple majors.
           
           year is an integer. Throws an exception if the specified year 
           isn't a year in our dataset."""
        return 0
        
        
    def get_number_of_degrees_from_year_span(self, startYear, endYear, step = 1):
        '''
        @return :return a list whose keys are years (int) and whose values are numbers of degrees
        '''
        
        return []
    
    def get_number_of_degrees_from_all_years(self):
        """Returns a list of the total number of degrees awarded in any
           major for all years in the dataset. Note that this is 
           different from the total number of graduates: some graduates 
           may be awarded degrees in mutliple majors."""
        return []
           
    def get_majors(self):
        """Returns a list of all majors in the dataset."""
        return []
        
    def get_years(self):
        """Returns a list of all years in the dataset."""
        return []
