import unittest
import socket
from monitor import *

class MonitorTestCase(unittest.TestCase):


    def test_uptime(self):
        HOSTNAME = socket.gethostname()
        check_for_args(HOSTNAME)
        self.assertIsNotNone(check_for_args(HOSTNAME))

    def test_cpu(self):
        self.assertIsNotNone(get_cpu())

    def test_memory(self):
        self.assertIsNotNone(get_memory_usage())

    def test_uptime(self):
        self.assertIsNotNone(detect_uptime())

    def test_platform(self):
        self.assertTrue(detect_platform())

    def test_trasform_data(self):
        MEMORY = {'MEMORY_TOTAL': 7795118080, 'MEMORY_PERCENT': 70.1, 'MEMORY_AVAILABLE': 2328547328, 'MEMORY_FREE': 652152832, 'MEMORY_USED': 4820533248}
        CPU = "3.1/1.0/2.0/0.0/"
        UPTIME = "128898.8"
        LOGS = "True"
        self.assertTrue(isinstance(transform_data(MEMORY,CPU,UPTIME,LOGS),str))

if __name__ == "__main__":
    ar_list=["5570"]
    unittest.main(argv=ar_list)
