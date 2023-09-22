import sys
sys.path.append('../config/')
import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from imports import *
from settings import *
from advanced_settings import *

def main():
    aux_lib.initial_checks()
    preprocess.preprocess()
    preprocess.train_methods()
    process.downscale()
    postprocess.bias_correction()
    postprocess.plot_results()

if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print('Elapsed time: ' + str(end - start))