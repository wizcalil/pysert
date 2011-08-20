'''
Created on Aug 18, 2011

Contains all the data sets available in pyServ .

@author: nomemory
'''

import abc
import random
import re
import string
import sys

from xml.etree.ElementTree import ElementTree


#------------------------------------------------------------------------------
class AbstractDataSet(object):
    '''
    Abstract class base for data sets .
    Classes based on AbstractDataSet are dynamic and must implement 
    next_value() method .
    '''
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, ds_dict):
        '''
        Subclasses will have a dynamic structure based on the 
        ds_dict dictionary .  
        '''
        for (k, v) in ds_dict.items():
            self.__dict__[k] = v
    
    @abc.abstractmethod
    def next_value(self):
        return
#------------------------------------------------------------------------------
class RandomNumber(AbstractDataSet):
    '''
    ds_dict will contain the following:
            { 
                "floating" : "<boolean value>" ,
                "min": "<integer value>",
                "max": "<integer value>"
            }
    '''
    def next_value(self):
        '''
        Returns a random value based on in the ds_dict properties .
        '''
        func = random.uniform if self.floating == 'True' else random.randint
        return func(int(self.min), int(self.max))
#------------------------------------------------------------------------------
class RandomText(AbstractDataSet):
    '''
    ds_dict will contain the following .
    {
        "length" : "<integer value>"
        "uppercase" : "<boolean value>"
        "lowercase" : "<boolean value>"
    }
    '''
    def __init__(self, ds_dict):
        ''' 
        We will need to @override the constructor in order to add 
        the _letters property .
        '''
        super().__init__(ds_dict)
        self.letters = ' '
        if self.uppercase == 'True':
            self.letters = self.letters.replace(' ', '')
            self.letters = self.letters + string.ascii_uppercase
        if self.lowercase == 'True':
            self.letters = self.letters + string.ascii_lowercase
            self.letters = self.letters.replace(' ', '')
        
    def next_value(self):
        '''
        Returns a random string based on ds_dict properties 
        '''
        ret = ''
        iter = int(self.length)
        for i in range(iter):
            rd = random.randint(0, 1000) % len(self.letters)
            ret = ret + self.letters[rd] 
        return ret
#------------------------------------------------------------------------------
class Sequence(AbstractDataSet):
    '''
     ds_dict will contain the following:
        {
            "start" : "<integer value>",
            "increment" : "<integer value>"
        }
    '''
    def __init__(self, ds_dict):
        ''' 
        We will need to @override the constructor in order to add 
        the _cval property (current value in sequence) .
        '''
        super().__init__(ds_dict)
        self.__cval = int(self.start) - int(self.increment)
        
    def next_value(self):
        '''
        Returns the next value in the sequence by adding the increment to
        the current value
        '''
        self.__cval += int(self.increment)
        return self.__cval
#------------------------------------------------------------------------------
class DataSetBuilder(object):
    ''' 
    Returns a new instance of a data set based on 
    subclass name (see @get_name function) 
    '''
    def __init__(self):
        '''
        __classes will be a dictionary of AbstractDataSet subclasses 
        in the following form:
        {
            <__classname__1>:<__class_object__1>,
            <__classname__2>:<__class_object__2>,
            ...
        }
        '''
        #@PydevCodeAnalysisIgnore
        self.__classes = { c.__name__ : c for c in \
                        AbstractDataSet.__subclasses__()}
        
    def instantiate(self, name, ds_dict):
        ''' 
        Returns the instance of the class based on class name .
        Every object instantiated with this method will be instances
        of AbstractDataSet subclasses .
        '''
        return self.__classes[name](ds_dict)
#------------------------------------------------------------------------------
class DataSetEvaluator(object):
    def __init__(self, xml_filename):
        #Build element tree        
        self.__elem_tree = ElementTree()
        self.__elem_tree.parse(xml_filename)
        
        #Initialize class attributes
        self.instances = self.__get_instances()
        self.iterations = int(self.__get_iterations())
        self.template = self.__get_template()
    
    def __get_instances(self):
        '''
        Parse __elem_tree to determine and instantiate the data
        set objects present in the XML file . 
        '''
        #Obtain all the <dataset> elements from the XML file
        instances = {}
        dsb = DataSetBuilder()
        dataset_list = list(self.__elem_tree.iter("dataset"))
        for dataset in dataset_list:
            dataset_name = dataset.attrib['name']
            dataset_type = dataset.attrib['type']
            # Create the ds_dict for the Abstract Data Set subclasses
            ds_dict = {key:value for (key,value) in dataset.attrib.items() if \
                        key != 'name' and key != 'type'}
            #Build instances of Data Sets  
            instances[dataset_name] = dsb.instantiate(dataset_type, ds_dict)
        return instances
    
    def __get_iterations(self):
        '''
        Returns the number of iterations (how many subsequent lines
        to generate)
        '''
        return int(self.__elem_tree.getroot().attrib['iterations'])
    
    def __get_template(self):
        '''
        Retrieves the template string from the XML file 
        '''
        return self.__elem_tree.findall('template')[0].text
    
    def write_output(self, output=sys.stdout):
        '''
        Parse the template and write the output to a stream .
        The default stream is sys.stdout . 
        '''
        def inner_subst(matchobj):
            '''
            Function needed for re.sub()
            '''
            #Removing unneeded characters from key
            key = matchobj.group(0)
            for c in ['{','#','}']:
                key = key.replace(c,'')
            return str(self.instances[key].next_value())
        # Find all #{data_set_names} and replace them with
        # self.instances[data_set_name].next_value()
        regex = '(?:^|(?<=[^#]))#{\w+}'
        for i in range(self.iterations):
             output.write(re.sub(regex, inner_subst, self.template) + '\n')
#------------------------------------------------------------------------------

if __name__ == '__main__':
    dsv = DataSetEvaluator('tmpl.xml')  
    print(dsv.template)
    dsv.write_output()
    rs = RandomText({'length' : '10', 'uppercase':'False', 'lowercase':'True'})
    print(rs.next_value())
