#!/usr/bin/python

import argparse
import numpy as np
from scipy import signal
from scipy import fftpack
import matplotlib.pyplot as plt
import pandas as pd
from Hardware import DFlipFlop, Comparator, Integrator, DAC, Oscillator, Clock

def deltasigma(f, ampl, shape, samples, dc, noise, sr, osr, vref, periods, order):
    # period of input signal
    T = 1.0 / f

    # total time
    t = np.linspace(0.0, T * periods, samples)
    freq = np.fft.fftfreq(len(t), t[1] - t[0])

    # store results in dataframes
    results_time = pd.DataFrame([], index=t, columns=['out', 'integrator', 'in'])
    results_freq = pd.DataFrame([], index=freq, columns=['OUT', 'INTEGRATOR', 'IN'])

    # generate input signal
    x = Oscillator(f, shape, ampl, dc, noise)

    # oversampling
    Fs = sr * osr

    # sampling interval
    Ts = 1.0 / Fs

    # initialize
    dac_out = 0

    # clock
    clk = Clock(Fs)

    # Integrators
    int1 = Integrator()

    if order.lower() is 'second':
        int2 = Integrator()

    comparator = Comparator(dc)
    dff = DFlipFlop()
    dac = DAC(vref, dc)

    # outputs
    int_outs = []
    dff_outs = []

    for time in t:
        # first differential amplifier
        diff1 = x(time) - dac_out

        # first integrator
        int_out = int1(diff1)

        # second integrator optional
        if order is 'second':
            diff2 = diff1 - dac_out
            int_out = int2(diff2)

        int_outs.append(int_out)

        # comparator
        comp_out = comparator(int_out)

        # D Flip Flop
        q, nq = dff(comp_out, clk(time))
        dff_outs.append(q)

        # DAC
        dac_out = dac(q)

    results_time['in'] = x(t)
    results_time['integrator'] = int_outs
    results_time['out'] = dff_outs

    results_freq['IN'] = abs(x.fft(t))
    results_freq['INTEGRATOR'] = abs(fftpack.fft(int_outs))
    results_freq['OUT'] = abs(fftpack.fft(dff_outs))

    results_freq = results_freq[results_freq.index > 0]
    plot_results(results_time.drop('integrator', axis=1),
            results_freq['OUT'])

    plt.show()

def plot_results(t, f):
    fig, (time, freq) = plt.subplots(nrows=2, ncols=1)

    t.plot(ax=time, title='Time')
    time.grid(True)
    time.set(xlabel='Time (s)', ylabel='Volts (V)')

    f.plot(ax=freq, title='Frequency')
    freq.set(xlabel='Frequency (Hz)', ylabel='dB', xscale='log', yscale='log')
    freq.grid(True)
    freq.grid(which='minor', alpha=0.2)
    freq.grid(which='major', alpha=0.5)
    freq.tick_params(which='minor', bottom=False, left=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--freq', help='Input frequency', default=1000)
    parser.add_argument('-a', '--ampl', help='Input amplitude', default=1)
    parser.add_argument('-w', '--wave', help='Input waveform', default='sine')
    parser.add_argument('-s', '--samp', help='Input samples', default=1024)
    parser.add_argument('-d', '--dc', help='DC offset', default=0)
    parser.add_argument('-n', '--noise', help='Add noise', default=True)
    parser.add_argument('-sr', '--sr', help='Sampling rate', default=2000)
    parser.add_argument('-o', '--osr', help='Oversampling multiplier', default=64)
    parser.add_argument('-v', '--vref', help='Reference voltage', default=2.5)
    parser.add_argument('-p', '--per', help='Number of periods', default=50)
    parser.add_argument('-or', '--order', help='First or Second order', default='first')

    args = parser.parse_args()

    deltasigma(
            int(args.freq),
            float(args.ampl),
            args.wave,
            int(args.samp),
            float(args.dc),
            bool(args.noise),
            int(args.sr),
            int(args.osr),
            float(args.vref),
            int(args.per),
            args.order
            )

