import numpy as np

class ADSREnvelope():
    def __init__(self, NotaMusical, attack=0.2, decay=0.1, sustain=0.2, release=0.5, sustain_gain = 0.25, env_type='linear', exp_time_constants=8):
        self.attack       = attack
        self.decay        = decay
        self.sustain      = sustain
        self.release      = release                
        self.decay_cte    = exp_time_constants

        self.envelope     = np.ones_like(NotaMusical.sound_wave)
        self.num_samples  = NotaMusical.sound_wave.size
        self.sustain_amplitude = sustain_gain*NotaMusical.max_amplitude
        
        self.init_adsr_marks()
        if env_type=='linear':
            self.linear_envelope()
        elif env_type=='exp':
            self.exponential_envelope()
        elif env_type==None:
            pass
        else:
            raise Exception('Unknown Envelope Type')
         
    def linear_envelope(self):
        self.attack_modulation  = np.linspace(0, 1, self.attack_num_pts)
        self.decay_modulation   = np.linspace(1, self.sustain_amplitude, self.decay_num_pts)
        self.sustain_modulation = self.sustain_amplitude*np.ones(self.sustain_num_pts)
        self.release_modulation = np.linspace(self.sustain_amplitude,0, self.release_num_pts)
        self.generate_envelope()
        
    def exponential_envelope(self):
        self.attack_modulation  = self.rising_exp(1 , self.decay_cte, self.attack_num_pts)
        self.decay_modulation   = self.rising_exp(self.sustain_amplitude, self.decay_cte, self.decay_num_pts) \
                                + self.decay_exp(1, self.decay_cte, self.decay_num_pts)
        self.sustain_modulation = self.sustain_amplitude*np.ones(self.sustain_num_pts)
        self.release_modulation = self.decay_exp(self.sustain_amplitude, self.decay_cte, self.release_num_pts)
        self.generate_envelope()

    def generate_envelope(self):
        envelope = np.concatenate([self.attack_modulation,
                                   self.decay_modulation,
                                   self.sustain_modulation,
                                   self.release_modulation])
        self.envelope *= envelope

    def rising_exp(self, final_amplitude, time_constants, num_points):
        time_vector = np.linspace(0, time_constants, num_points)
        return final_amplitude*(1-np.exp(-time_vector))

    def decay_exp(self, initial_amplitude, time_constants, num_points):
        time_vector = np.linspace(0, time_constants, num_points)
        return initial_amplitude*(np.exp(-time_vector))

    def init_adsr_marks(self):
        # ADSR marks
        self.attack_end     = np.floor((self.attack*self.num_samples)).astype(int)
        self.decay_end      = np.floor((self.attack+self.decay)*self.num_samples).astype(int)
        self.sustain_end    = np.floor((self.attack+self.decay+self.sustain)*self.num_samples).astype(int)
        self.release_end    = self.num_samples

        self.attack_start   = 0
        self.decay_start    = self.attack_end  + 1
        self.sustain_start  = self.decay_end   + 1
        self.release_start  = self.sustain_end + 1

        # Num. of points in each piece
        self.attack_num_pts  = self.attack_end  - self.attack_start  + 1
        self.decay_num_pts   = self.decay_end   - self.decay_start   + 1
        self.sustain_num_pts = self.sustain_end - self.sustain_start
        self.release_num_pts = self.release_end - self.release_start + 1