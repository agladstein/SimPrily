
import unittest
from main_tools.housekeeping import process_args
from summary_statistics.afs_stats_bitarray import Pi2


class TestFns(unittest.TestCase):
    '''
    def test_process_args(self):
        new_list = ["python2", "simprily.py", "./examples/eg1/param_file_eg1.txt",
        "./examples/eg1/model_file_eg1.csv", "1", "output_dir"]
        args = process_args(new_list)
        self.assertEquals(args["command"], "python2")
    '''
    def test_Pi2(self):
        spec = [3,2,1]
        n = len(spec) + 1
        theta = Pi2(spec, n)
        self.assertEquals(theta, round(3.3333333333333333, 10))
        #testing first, value next
      
        spec = [4,3,2,1]
        n = len(spec) + 1
        theta = Pi2(spec, n)
        self.assertEquals(theta, 5.0)

        spec = []
        n = len(spec) + 1
        theta = Pi2(spec, n)
        self.assertEquals(theta, [])


def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + ' / 100')
    
if __name__ == "__main__":
    main()