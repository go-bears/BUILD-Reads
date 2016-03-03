import server
import unittest



class LoadPages(unittest.TestCase):
    
    def test_login_status_code(self):
        """test login page """
        
        test_client = server.app.test_client()
        result = test_client.get('/login')
        
        # tests if login pages load
        self.assertEqual(result.status_code, 200)
    

    def test_newuser_status_code(self):
        """test reading session page log """
        
        test_client = server.app.test_client()
        result = test_client.get('/reading_session"')    
        
        # tests if login pages load
        self.assertEqual(result.status_code, 200)


class DataDisplays(unittest.TestCase):
    
    def test_date_renders(self):
        """ tests if date loads on login """
        
        test_client = server.app.test_client()
        result = test_client.get('/login')
        
        self.assertIn('Today is %s' % server.today_date, result.data)
    # def test_load_user_detail(self):
    #     """test is user details page loads """
        
    #     test_client = server.app.test_client()
    #     result = test_client.get('/reading_session/user/6')    
        
        
    #     # tests if login pages load
    #     self.assertEqual(result.status_code, 200)


# class TestDbQueries(unittest.TestCase):
    
    

        
        



    
if __name__ == "__main__":
    unittest.main()