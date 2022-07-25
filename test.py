import unittest
import requests 
import time
PORT = 8000
HOST = "localhost"

ENDPOINT_HELLO = f"http://{HOST}:{PORT}/hello"
ENDPOINT_PROTECTED_HELLO = f"http://{HOST}:{PORT}/protected_hello"


class TestServerEndpoints(unittest.TestCase):   
    def test_get_hello_code(self):
        # Just in case server still processing other response
        time.sleep(0.1)
        response = requests.get(ENDPOINT_HELLO)
        self.assertEqual(response.status_code, 200)

    def test_post_hello_code(self):
        time.sleep(0.1)
        response = requests.post(ENDPOINT_HELLO, data=[(1, 2), ("a", "b")])
        self.assertEqual(response.status_code, 200)

    def test_get_hello_content(self):
        time.sleep(0.1)
        response = requests.get(ENDPOINT_HELLO)
        self.assertEqual(response.content, b"<h3>Hello, User</h3> Here is your resourse Unprotected resourse")

    def test_post_hello_content(self):
        time.sleep(0.1)
        response = requests.post(ENDPOINT_HELLO, data=[(1, 2), ("a", "b")])
        self.assertEqual(response.content, b"<h3>Hello, User</h3> Here is your resourse " 
            b"Unprotected resourse\n\nYou've sent me this: 1=2&a=b"
        )
    
    def test_get_protected_hello_code(self):
        time.sleep(0.1)
        response = requests.get(ENDPOINT_PROTECTED_HELLO, headers={"Authorization": "foo"})
        self.assertEqual(response.status_code, 200)

    def test_get_protected_hello_code_with_wrong_token(self):
        time.sleep(0.1)
        response = requests.get(ENDPOINT_PROTECTED_HELLO, headers={"Authorization": "bar"})
        self.assertEqual(response.status_code, 404)

    def test_post_protected_hello_code(self):
        time.sleep(0.1)
        response = requests.post(ENDPOINT_PROTECTED_HELLO, data=[(1, 2), ("a", "b")], headers={"Authorization": "foo"})
        self.assertEqual(response.status_code, 200)

    def test_get_protected_hello_content(self):
        time.sleep(0.1)
        response = requests.get(ENDPOINT_PROTECTED_HELLO, headers={"Authorization": "foo"})
        self.assertEqual(response.content, b"<h3>Hello, User</h3> Here is your resourse Protected resourse")

    def test_post_protected_hello_content(self):
        time.sleep(0.1)
        response = requests.post(ENDPOINT_PROTECTED_HELLO, data=[(1, 2), ("a", "b")], headers={"Authorization": "foo"})
        self.assertEqual(response.content, b"<h3>Hello, User</h3> Here is your resourse " 
            b"Protected resourse\n\nYou've sent me this: 1=2&a=b")

    def test_get_absent_route(self):
        time.sleep(0.1)
        response = requests.get(f'{ENDPOINT_HELLO}very_uknown_smth')
        self.assertEqual(response.status_code, 404)

    def test_put_hello_code(self):
        time.sleep(0.1)
        response = requests.put(ENDPOINT_HELLO, data=[(1, 2), ("a", "b")])
        self.assertEqual(response.status_code, 400)
        
    


if __name__ == '__main__':
    unittest.main()