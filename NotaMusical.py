import numpy as np
from numpy import pi
from scipy.io import wavfile

from ADSREnvelope import ADSREnvelope

class NotaMusical():
    def __init__(self, tone_freq, duration, max_amplitude=1, FS=44100):
        self.tone_freq          = tone_freq
        self.FS                 = FS
        self.TS                 = 1/FS
        self.duration           = duration
        self.max_amplitude      = max_amplitude
        self.angular_tone_freq  = 2*pi*tone_freq

        # initialize wave
        self.sound_wave    = self.wave_init()
        self.tone          = self.sound_wave
        
    def wave_init(self):
        time_vector = np.arange(0, self.duration, self.TS)
        wave_vector = self.max_amplitude*np.sin(self.angular_tone_freq*time_vector) 
        return wave_vector

    def generate_ADSR(self, adsr_dict):
        adsr = ADSREnvelope(self, **adsr_dict)
        self.sound_wave = adsr.envelope*self.sound_wave
        return None

    def write_wave(self, filename='output.wav'):
        wavfile.write(filename, self.FS, self.sound_wave)
        return None
