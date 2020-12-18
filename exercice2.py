from requests import *
import unittest

class TestAPIMethods(unittest.TestCase):
    server_ip, server_port = '127.0.0.1', 8080 
    def test_publication_id(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publication/0")
        self.assertIn('Louise A. Dennis', r1.text)
    
if __name__ == '__main__':
    unittest.main()
