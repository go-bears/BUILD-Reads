import unittest
import server

class DatabaseTests(unittest.TestCase):
    
    def test_login(self):
        """test login page """
        
        test_client = server.app.test_client()
        result = test_client.get('/login')
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('Today is %s' % server.today_date, result.data)


if __name__ == "__main__":
    unittest.main()