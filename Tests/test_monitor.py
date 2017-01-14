import unittest
from monitor import *

class MonitorTestCase(unittest.TestCase):

    # Test if we get the host and ip args
    def test_args(self):
        HOSTNAME = socket.gethostname()
        check_for_args(HOSTNAME)
        self.assertIsNotNone(check_for_args(HOSTNAME))

    # Test if we get the cpu %
    def test_cpu(self):
        self.assertIsNotNone(get_cpu())

    # Test if we get the memory data
    def test_memory(self):
        self.assertIsNotNone(get_memory_usage())

    # Test if we get the uptime data
    def test_uptime(self):
        self.assertIsNotNone(detect_uptime())

    # Check platform
    def test_platform(self):
        self.assertTrue(detect_platform())

    # Test data transofrmation function
    def test_trasform_data(self):
        MEMORY = {'MEMORY_TOTAL': 7795118080, 'MEMORY_PERCENT': 70.1, 'MEMORY_AVAILABLE': 2328547328, 'MEMORY_FREE': 652152832, 'MEMORY_USED': 4820533248}
        CPU = "3.1/1.0/2.0/0.0/"
        UPTIME = "128898.8"
        LOGS = "True"
        self.assertTrue(isinstance(transform_data(MEMORY,CPU,UPTIME,LOGS),str))

    # Test the encryption process
    def test_encrypt_data(self):
        self.assertTrue(isinstance(encrypt_data("cris","this is a test string"), bytes))

    # Test if we receive a message back from server
    def test_send_data(self):
        data = "this is a test".encode()
        self.assertTrue(isinstance(send_encrypted_data(data),str))



if __name__ == "__main__":
    ar_list=["5570"]               # Specify the port here. It has to be exactly the same as the one you introduce at the start of the script
    unittest.main(argv=ar_list)
