#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import os, sys
import argparse

def main():
    mpl.rcParams['agg.path.chunksize'] = 10000

    parser = argparse.ArgumentParser(description="FFT on a wav file")
    parser.add_argument("file")
    args = parser.parse_args()

    # change working directory as necessary
    wkdir = args.file.split('/')[:-1]
    wkdir = '/'.join(wkdir)
    if wkdir:
        os.chdir(wkdir)

    # extract file path
    file_name = args.file.split('/')[-1]
    file_path = os.path.join(os.getcwd(), file_name)
    if not os.path.isfile(file_path):
        print(f"File '{file_name}' does not exist", file=sys.stderr)
        sys.exit(1)

    # extract data
    rate, data = wav.read(file_name)
    if True:
        print(f"Channels: {data.shape[1]}")
        print(f"Length:   {data.shape[0]/rate}s")
    data = data[:,2]
    data_norm = [(i/2**8.0)*2-1 for i in data]
    
    # frequency label
    k = list(range(len(data)))
    T = len(data)/rate
    freqlabel = [i/T for i in k]

    # plot
    fft_out = fft(data_norm)
    plt.plot(freqlabel, np.abs(fft_out))
    plt.xlim([0,1000])
    plt.show()

if __name__ == "__main__":
    main()
