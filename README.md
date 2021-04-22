# FOOOF-Parameterized-PSD-testing
## Evaluating fooof toolbox for parameterizing power spectra<br/>


### 1) Relative power vs Absolute power vs Periodic power 
EEG measures the electrical activity at a sensor relative to the 
  reference & ground electrode. This causes issues in comparing absolute power
  between conditions &/participants as impedance differences can cause 
  broadband shift in power. Relative power is often used as a substitute of
  absolute power as it supposedly normalizes w.r.t. the total power in the 
  window of interest. However, using relative power to compare different 
  conditions can cause spurious differences due to the nature of computation 
  and this code is used to simulate a set of PSDs to evaluate when they fail
  and show how flattened PSD is a better alternative to quantify changes in
  multiple bands. A pair of signals can be created using Relative power comparison.py file
  <br/><img src='/images/rel_power.jpg' width=500 align=center>
  <br/> 
  In general, relative power is better when reporting which band has the highest power difference. Comparing multiple bands can lead to spurious differences due to the nature of computation. Periodic power is a much more robust alternative to quantify multi-band differences.
  
    <br/>
    
 If power increase in two bands equally, their relationship in relative power is preserved in these bands but the power in other bands gets reduced even though in the original signal they are the same. Periodic power captures these differences well. Using absolute power on the other hand can cause artificial differences even due to simple broadband power differences which can also be due to non-physiological origins such as impedance differences.  Either relative power or parameterized PSD helps with it.
   <br/><img src='/images/1.jpg' width=500 align=center>
 
 
   <br/>    
 If the power increase is small and limited to only one band, the differences are not distorted by neither relative power nor periodic power
    <br/><img src='/images/2.jpg' width=500 align=center>
    
   <br/>        However, the same band power if increased more, after a point it starts distorting the rest of the PSD and the relationship will be altered. As can be seen, the rest of the band power gets artificially increased and can lead to spurious reporting.
       <br/><img src='/images/3.jpg' width=500 align=center>
       
       
          <br/>        When multiple bands increase but one (theta) is much bigger than the other (alpha), not even the increase in alpha power will be represented correctly (the relationship is flipped).
       <br/><img src='/images/4.jpg' width=500 align=center>
       
       
  <br/>      
### 2) Concern with notch filter and current interpolation method  <br/>
Interpolate_test.py script explores how notch filtering can skew the exponent down.
The current interpolation is a simple version and causes sudden dip centered
around the line noise range. Depending on the window used for interpolating, 
the exponent varies. Care needs to be done while using it

     <br/><img src='/images/interpolate_fooof.png' width=500 align=center>
