import numpy as np
from NotaMusical import NotaMusical

TONE_FREQ       = 261.63*(2**(-0/12))
NOTE_SPAN       = 2
MAX_AMPLITUDE   = 0.99
    
ATTACK_SPAN     = 40
DECAY_SPAN      = 60
SUSTAIN_SPAN    = 0
RELEASE_SPAN    = 0
SUSTAIN_GAIN    = 0
ENV_TYPE        = 'linear' # 'linear', 'exp' or None

OUTPUT_FILENAME = f'./outputs/{str(round(1e2*TONE_FREQ)/1e2)}_Hz_{str(round(1e2*NOTE_SPAN)/1e2)}_s_note_{ENV_TYPE}_envelope.wav'

if __name__=='__main__':

    adsr_params = np.array([ATTACK_SPAN, DECAY_SPAN, SUSTAIN_SPAN, RELEASE_SPAN]) + 1e-3
    adsr_params = adsr_params/adsr_params.sum()
    adsr_dict = {'attack':       adsr_params[0],
                 'decay':        adsr_params[1],
                 'sustain':      adsr_params[2],
                 'release':      adsr_params[3],
                 'sustain_gain': min(max(SUSTAIN_GAIN,0),1),
                 'env_type':     ENV_TYPE}
    
    Nota = NotaMusical(tone_freq=TONE_FREQ,
                       duration=NOTE_SPAN, 
                       max_amplitude=MAX_AMPLITUDE)

    Nota.generate_ADSR(adsr_dict)
    Nota.write_wave(filename=OUTPUT_FILENAME)