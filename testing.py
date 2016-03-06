import server
from  server_helper_funct import *
import unittest
from model import Site, Book





######################################################################


class LoadPages(unittest.TestCase):
    
    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        
#         server._old_sites_list = server.sites_list
        server.sites_list = [Site(name="Berkeley Arts Magnet"),
                            Site(name="Young Adult Project")]


    def test_login_status_code(self):
        """test login page """
        
        result = self.client.get('/login')
        
        # tests if login pages load
        self.assertEqual(result.status_code, 200)
    

    def test_newuser_status_code(self):
        """test reading session page log """
        

        
        result = self.client.get('/new_user')    
        
        # tests if login pages load
        self.assertEqual(result.status_code, 200)


    def test_mentor_detail_status_code(self):
        """test mentor detail page loads """

        result = self.client.get('/mentor_detail')    

        
    #     result = self.client.get('/mentor_detail')    
        
    #     # tests if login pages load
    #     self.assertEqual(result.status_code, 200)
        


    # def tearDown(self):
    #     """Do at end of every test."""
    
    #     server.sites_list = self._old_sites_list
    #     server.book_list = self._old_book_list


class DataDisplays(unittest.TestCase):
    
    def test_date_renders(self):
        """ tests if date loads on login """
        
        test_client = server.app.test_client()
        result = test_client.get('/login')
        
        self.assertIn('Today is %s' % server.today_date, result.data)


    
class TestHelperFunctions(unittest.TestCase):
    
    def test_avatar(self):
        """Test if string for avatar image returned"""
        
        
        self.assertEqual(type(pick_avatar()), str)
        
    def test_calculate_badges(self):
        """Test if reading time length matches appropriate badge """
        
        self.assertEqual(calculate_badges(time_length=20), 1)
    
    def test_convert_url_to_img_tag(self):
        
        self.assertEqual(type(convert_url_to_img_tag(url="https")), str)
        
    
if __name__ == "__main__":
    unittest.main()