from scipy import signal
from scipy import fftpack
import numpy as np
from math import floor

class Comparator(object):
    def __init__(self, dc):
        self.dc = dc

    def __call__(self, x):
        return self.dc + 1 if x > self.dc else self.dc

class DAC(object):
    def __init__(self, vref, dc=0):
        self.vref = vref
        self.dc = dc

    def __call__(self, x):
        return self.dc + self.vref if x > self.dc else self.dc - self.vref

class DFlipFlop(object):
    def __init__(self):
        self.q = 0
        self.prev_clk = -1

    def __call__(self, d, clk):
        if clk > self.prev_clk:
            self.q = d

        self.prev_clk = clk
        return self.q, self.nq

    @property
    def nq(self):
        return 1 if self.q == 0 else 0

class Integrator(object):
    def __init__(self):
        self.prev = 0

    def __call__(self, x):
        self.prev = x + self.prev
        return self.prev

class Oscillator(object):
    def __init__(self, f, waveform, amplitude=1, dc=0, noise=False):
        self.waveforms = {
                'sine':self.sine,
                'square':self.square,
                'triangle':self.triangle,
                'sawtooth':self.sawtooth
                }

        self.f = f
        self.T = 1.0 / self.f
        self.omega = 2 * np.pi * self.f
        self.waveform = waveform.lower()
        self.amplitude = amplitude
        self.dc = dc
        self.noise = noise

    def __len__(self):
        return len(self.sig)

    def __call__(self, t):
        return self.waveforms[self.waveform](t)

    def sine(self, t):
        return self.amplitude * np.sin(self.omega * t) + self.dc \
                + (self.add_noise(t) if self.noise else 0)

    def square(self, t):
        return self.amplitude * signal.square(self.omega * t) + self.dc \
                + (self.add_noise(t) if self.noise else 0)

    def triangle(self, t):
        return self.amplitude * signal.sawtooth(self.omega * t, width=0.5) + self.dc \
                + (self.add_noise(t) if self.noise else 0)

    def sawtooth(self, t):
        return self.amplitude * signal.sawtooth(self.omega * t) + self.dc \
                + (self.add_noise(t) if self.noise else 0)

    def add_noise(self, t):
        return np.random.randn(len(t) if hasattr(t, '__iter__') else 1)

    def fft(self, t):
        return fftpack.fft(self(t))

    @property
    def period(self):
        return self.T

    @property
    def frequency(self):
        return self.f

    @property
    def shape(self):
        return waveform

class Clock(Oscillator):
    def __init__(self, f, edge_time=5e-9, duty=0.5):
        super().__init__(f, 'square')
        self.edge_time = edge_time

    def prev_signal(self, time):
        return self.sig[self.time_index(time - self.edge_time)]

    def rising_edge(self, time):
        return True if self.sig(time) > self.prev_sig(time) else False
