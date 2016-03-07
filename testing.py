import server
from  server_helper_funct import *
import unittest
from model import Site, Book, Badge, User, Rating, db


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

######################################################################


class LoadPages(unittest.TestCase):
    
    def setUp(self):
        """Set up dependencies for web pages' loading """

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        
        # server._old_sites_list = server.sites_list
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

        server.book_list = [Book(title="Smoke and Mirrors"),
                            Book(title="American Gods")]
        server.badges_list = [Badge(name="Meteorite Badge"),
                            Book(title="Moon Badge ")]
        badge = Badge(badge_id=0)



        result = self.client.get('/mentor_detail')    
  
        
        # tests if login pages load
        self.assertEqual(result.status_code, 200)
        


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
        """Test url converted to string """
        
        self.assertEqual(type(convert_url_to_img_tag(url="https")), str)

    def test_convert_str_to_datetime(self):
        """Test function produce datetime object """

        self.assertEqual((birthday_format('2004-01-01')), 
                              date(int(2004), int(01), int(01)))

    # def test_display_badges(self):

    #     badges_list = server.badges_list

    #     self.assertEqual(type(display_badges(badges_list)), dict)
        
    def test_format_site_chart(self):
        """Test function produces dict object"""

        self.assertEqual(type(format_site_chart()), dict)


    def test_reading_confidence(self):
        """Test function produces dict object """

        self.assertEqual(type(reading_confidence()), dict)




class SeleniumTests(unittest.TestCase):

    def setUp(self):
        """Setup as Firefox testing browser """

        self.driver = webdriver.Firefox()


    def test_title(self):
        """Test title is BUILD project """

        driver = self.driver
        self.driver.get('http://127.0.0.1:5000/login')

        self.assertIn("BUILD reads", driver.title)

    def test_login_form(self):
        """Test login form submission."""

        driver = self.driver
        self.driver.get('http://127.0.0.1:5000/login')

        input_first = driver.find_element_by_name('first_name')
        input_first.send_keys("ammy")

        input_last = driver.find_element_by_name('last_name')
        input_first.send_keys("keung")



    def test_login_button(self):
        driver = self.driver
        self.driver.get('http://127.0.0.1:5000/login')

        login_btn = driver.find_elements_by_tag_name('input')
        # login_btn.click()
        
        # user_type = 
        # user_type.send_keys("scholar")

        # 
        # 

        # last_name = driver.find_element_by_name("last_name")
        # user_type.send_keys("keung")

        # password = driver.find_element_by_name("password")
        # user_type.send_keys("password")


        # user_type.send_keys(Keys.RETURN)
        # assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()


class DatabaseTests(unittest.TestCase):
    """Tests for database"""

    def setUp(self):
        """Set up database for testing purposes"""

        self.app = server.app.test_client()
        self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///testdb'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


        db.app = app
        db.init_app(app)
        db.create_all()


    def test_create_user(self):
        """Create test user """

        user = User(first_name='Test', last_name="Test")
        user.commit_to_db

        self.assertEqual(user.first_name, 'Test')

        db.session.rollback()


if __name__ == "__main__":
    
    unittest.main()

