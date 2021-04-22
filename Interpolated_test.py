# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 10:19:25 2021

This Script explores how notch filtering can skew the exponent down.
The current interpolation is a simple version and causes sudden dip centered
around the line noise range. Depending on the window used for interpolating, 
the exponent varies. Care needs to be done while using it
@author: Akshay Sujatha Ravindran
"""


# Load the required libraries
import numpy as np
import scipy.io as sio
from fooof import FOOOF
from fooof.utils import interpolate_spectrum
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 11})

# Load the PSD
Loaded_data=sio.loadmat('data//interpolating_testV1.mat')
freq=Loaded_data['freq'] # Frequency
ps=Loaded_data['psd'].T # Power spectrum

# Frequency range to fit FOOOF with
freq_range_full = [1, 75] 
freq_range_short = [1, 55]




# Interpolate the notch filtered section
freqs1, ps_interpv1 = interpolate_spectrum(freq[0].copy(), ps[0].copy(), [57, 63])



# Interpolate the notch filtered section
freqs1, ps_interpv2 = interpolate_spectrum(freq[0].copy(), ps[0].copy(), [58, 62])


# Plot the original and interpolated power spectra
plt.figure()
plt.plot(freqs1,np.log10(ps[0]))
plt.plot(freqs1,np.log10(ps_interpv1))
plt.plot(freqs1,np.log10(ps_interpv2))
plt.xlabel('Freq (Hz)')
plt.ylabel('Power (dB)')



# Fit the FOOOF object on original power spectra
fm=FOOOF(verbose=False)  
fm.fit(freq[0], ps[0].copy(), freq_range_full)

# Fit the FOOOF object on original power spectra before 55
fm_short=FOOOF(verbose=False)  
fm_short.fit(freq[0], ps[0].copy(), freq_range_short)


# Fit the FOOOF object on interpolated power spectra (57-63)
fm_interpv1=FOOOF(verbose=False)  
fm_interpv1.fit(freq[0], ps_interpv1.copy(), freq_range_full)


# Fit the FOOOF object on interpolated power spectra (58-62)
fm_interpv2=FOOOF(verbose=False)  
fm_interpv2.fit(freq[0], ps_interpv2.copy(), freq_range_full)





# Visualize the fit
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
# Original PSD with notch filter
ax1.plot(fm.freqs, fm.power_spectrum)
ax1.plot(fm.freqs,fm.power_spectrum-fm._spectrum_flat)
ax1.set_ylabel('Power (dB)')
ax1.set_title('Original PSD')
ax1.set_xticks([])
ax1.annotate('Exp:' + str(np.round(fm.get_params('aperiodic', 'exponent'),decimals=2)),xy=(0.6,0.7),
           xycoords='axes fraction', fontsize=10,
                horizontalalignment='right', verticalalignment='bottom')
ax1.set_ylim((-3,2))
ax1.set_xlim((0,freq_range_full[1]))


# PSD with interpolation (57-63 Hz)
ax2.plot(fm_interpv1.freqs, fm_interpv1.power_spectrum)
ax2.plot(fm_interpv1.freqs,fm_interpv1.power_spectrum-fm_interpv1._spectrum_flat)
ax2.set_title('Interp PSD (57-63 Hz)')
ax2.set_xticks([])
ax2.annotate('Exp:' + str(np.round(fm_interpv1.get_params('aperiodic', 'exponent'),decimals=2)),xy=(0.6,0.7),
           xycoords='axes fraction', fontsize=10,
                horizontalalignment='right', verticalalignment='bottom')
ax2.set_ylim((-3,2))
ax2.set_xlim((0,freq_range_full[1]))


# Original PSD limited before notch filter frequency
ax3.plot(fm_short.freqs,fm_short.power_spectrum)
ax3.plot(fm_short.freqs,fm_short.power_spectrum-fm_short._spectrum_flat)
ax3.set_ylabel('Power (dB)')
ax3.set_xlabel('Freq (Hz)')
ax3.set_title('Short PSD')
ax3.annotate('Exp:' + str(np.round(fm_short.get_params('aperiodic', 'exponent'),decimals=2)),xy=(0.6,0.7),
           xycoords='axes fraction', fontsize=10,
                horizontalalignment='right', verticalalignment='bottom')
ax3.set_ylim((-3,2))
ax3.set_xlim((0,freq_range_full[1]))


# PSD with interpolation (58-62 Hz)
ax4.plot(fm_interpv2.freqs, fm_interpv2.power_spectrum)
ax4.plot(fm_interpv2.freqs,fm_interpv2.power_spectrum-fm_interpv2._spectrum_flat)
ax4.set_title('Interp PSD (58-62 Hz)')
ax4.set_xlabel('Freq (Hz)')
ax4.annotate('Exp:' + str(np.round(fm_interpv2.get_params('aperiodic', 'exponent'),decimals=2)),xy=(0.6,0.7),
           xycoords='axes fraction', fontsize=10,
                horizontalalignment='right', verticalalignment='bottom')
ax4.set_ylim((-3,2))
ax4.set_xlim((0,freq_range_full[1]))

fig.savefig('interpolate_fooof.png', format='png', dpi=300)