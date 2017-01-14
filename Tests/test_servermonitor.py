import unittest
from servemonitor import *
import xml.etree.ElementTree as ET


class ServerTestCase(unittest.TestCase):

    # Test if we get the host and ip args
    def test_start_parsing(self):
        self.assertTrue(start_parsing("data.xml"))

    def test_check_mail_aler(self):
        tree = ET.parse(filename)   # PARSE
        root = tree.getroot()
        for child in root:
            self.assertTrue(check_mail_alert(child,"cristi26.gabor@gmail.com"))

    def test_send_email_function(self):

        fromaddr='cristi26.gabor@gmail.com'
        memory_limit='memory 70'
        gmail_password="password"
        cpu_limit='56'
        self.assertTrue(send_email_function(fromaddr,memory_limit, cpu_limit,gmail_password))


if __name__ == "__main__":
    unittest.main()
