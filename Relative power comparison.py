
"""
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                        %
%                  Relative Band Power Comparison                        %
%                                                                        %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  Summary: EEG measures the electrical activity at a sensor relative to the 
  reference & ground electrode. This causes issues in comparing absolute power
  between conditions &/participants as impedance differences can cause 
  broadband shift in power. Relative power is often used as a substitute of
  absolute power as it supposedly normalizes w.r.t. the total power in the 
  window of interest. However, using relative power to compare different 
  conditions can cause spurious differences due to the nature of computation 
  and this code is used to simulate a set of PSDs to evaluate when they fail
  and show how flattened PSD is a better alternative to quantify changes in
  multiple bands.

 Credits: This script is made possible due to the wonderful FOOOF toolbox
 https://fooof-tools.github.io/fooof/
 Author: Akshay Sujatha Ravindran
 email: akshay dot s dot ravindran at gmail dot com
 Jan 23rd 2021
"""
from fooof.sim.gen import gen_power_spectrum
from fooof import FOOOF
import numpy as np
import matplotlib.pyplot as plt
from fooof.sim.transform import  translate_spectrum
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 10})


freq_range       = [0, 30]   # The frequency range to simulate in the PSD


## Parameter for first set of PSD 
aperiodic_params = [1, 1]     # aperiodic component [Offset, (*Knee), Exponent]
freq_res         =  0.5       # Frequency resolution for the simulated PSD  
nlv              =  0.02      # Define the amount of noise to add to the spectrum  
# Parameters for any periodic components [Center Freq, Peak/Power, Bandwidth],
# Multiple peaks can be added in square brackets separated by comma
periodic_params  = [[11, 0.5, 1],[ 5.5, 0.4, 1]] 


## Parameter for first set of PSD 
freq_res         =  0.5       # Frequency resolution for the simulated PSD  
nlv2              =  0.04      # Define the amount of noise to add to the spectrum   
delta_offset     = 0.5        # Offset to translate
periodic_params1  = [[11, 0.8, 1],[ 5, 0.3, 1]] 




# Simulate the PSD with the mentioned parameters
freqs, powers1    = gen_power_spectrum(freq_range, aperiodic_params,
                                      periodic_params, nlv, freq_res)



# Simulate the second PSD with the mentioned parameters
freqs, powers2    = gen_power_spectrum(freq_range, aperiodic_params,
                                      periodic_params1, nlv2, freq_res)
# In addition, translate the power of second psd to create broadband power shift by delta_offset dB
t_powers        = translate_spectrum(powers2, delta_offset)


# Using basic setting as the PSD is simulated and an easy fit. Check the fit
# when using real PSD and modify parameters for FOOOF object appropriately
fm_1              = FOOOF(verbose=False)  # Create FOOOF object for original
fm_2            = FOOOF(verbose=False)  # Create FOOOF object for modified
  
# Fit the FOOOF object to the PSD in the frequency range of interest  
fm_1.fit(freqs, powers1, freq_range)   
fm_2.fit(freqs, t_powers, freq_range)
Freq            = fm_2.freqs
                 
# Extract the Original, Periodic and Aperiodic components of first set 
spectrm_full     =   fm_1.power_spectrum.copy()
spctrm_flatten    =   fm_1._spectrum_flat.copy()
spectrm_aperiodic =   spectrm_full-spctrm_flatten


# Extract the Original, Periodic and Aperiodic components of second set  
spectrm_full_0     =   fm_2.power_spectrum.copy()
spctrm_flatten_0    =   fm_2._spectrum_flat.copy()
spectrm_aperiodic_0 =   spectrm_full_0-spctrm_flatten_0




# Visualize the fit
fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(nrows=2, ncols=2)
# Original PSD with notch filter
ax1.plot(Freq, (spectrm_full))
ax1.plot(Freq, (spectrm_full_0))
ax1.set_ylabel('Power (dB)')
ax1.set_title('Sig1 & translated Sig2 ')
ax1.set_xticks([])
ax1.set_ylim((-0.6,2))
ax1.set_xlim((0,Freq[-1]))




# Relative power 
ax2.plot(freqs[1:],(powers2[1:]/np.sum(powers2[1:])))
ax2.plot(freqs[1:], (t_powers[1:]/np.sum(t_powers[1:])))
ax2.set_title('Rel power (Sig2 & translated Sig2)')

ax2.set_ylabel('Power (dB)')
ax2.set_xlabel('Freq (Hz)')
#ax3.set_ylim((-0.6,2))
ax3.set_xlim((0,Freq[-1]))



# PSD with interpolation (57-63 Hz)
ax3.plot(Freq, (spctrm_flatten))
ax3.plot(Freq, (spctrm_flatten_0))
ax3.set_title('Periodic component (flattened)')
ax3.set_xticks([])
ax3.set_ylim((-0.6,2))
ax3.set_xlim((0,Freq[-1]))


# PSD with interpolation (58-62 Hz)
ax4.plot(freqs[1:],(powers1[1:]/np.sum(powers1[1:])))
ax4.plot(freqs[1:], (t_powers[1:]/np.sum(t_powers[1:])))
ax4.set_xlabel('Freq (Hz)')
ax4.set_title('Rel power (Sig1 & translated Sig2)')#
#ax3.set_ylim((-0.6,2))
ax4.set_xlim((0,Freq[-1]))


fig.savefig('interpolate_fooof.png', format='png', dpi=300)