from django.test import TestCase
from extract import *

# Create your tests here.
class XMLExtractionTestCase(TestCase):
    
    def test_extract_users(self):
        '''Test the normal extraction of the users XML file.'''
        
        user_list = extract_users('xml_study/test_xml_files/users.xml')
        
        self.assertTrue('name' in user_list[0] and user_list[0]['name'] == 'adal')
        self.assertTrue('password' in user_list[0] and user_list[0]['password'] == 'password')
        self.assertTrue('email' in user_list[0] and user_list[0]['email'] == 'adal@swordfish.edu')
        
        self.assertTrue('name' in user_list[1] and user_list[1]['name'] == 'charlesb')
        self.assertTrue('password' in user_list[1] and user_list[1]['password'] == 'password')
        self.assertTrue('email' in user_list[1] and user_list[1]['email'] == 'charlesb@swordfish.edu')        
        
        self.assertTrue('name' in user_list[2] and user_list[2]['name'] == 'alant')
        self.assertTrue('password' in user_list[2] and user_list[2]['password'] == 'password')
        self.assertTrue('email' in user_list[2] and user_list[2]['email'] == 'alant@swordfish.edu')
        
    def test_extract_users_invalid_attrib(self):
        '''Test a bad XML users file with invalid attributes (having an extra).'''
        
        self.assertRaises(InvalidXMLError, extract_users, 'xml_study/test_xml_files/users_bad_attrib.xml')
        
    def test_extract_users_invalid_attrib_2(self):
        '''Test a bad XML users file with invalid attributes (having less than required).'''
                
        self.assertRaises(InvalidXMLError, extract_users, 'xml_study/test_xml_files/users_bad_attrib_2.xml')    
        
    def test_extract_users_invalid_non_empty_user(self):
        '''Test a bad XML users file with a non-empty user node.'''
            
        self.assertRaises(InvalidXMLError, extract_users, 'xml_study/test_xml_files/users_bad_non_empty_user.xml')
    
    def test_extract_users_invalid_node(self):
        '''Test a bad XML users file with invalid node.'''
                        
        self.assertRaises(InvalidXMLError, extract_users, 'xml_study/test_xml_files/users_bad_node.xml')    