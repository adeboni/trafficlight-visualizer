import numpy as np
from struct import unpack

power = []

# Return power array index corresponding to a particular frequency
def piff(val, sample_rate, chunk):
   return int(4 * chunk * val/sample_rate)

def calculate_levels(matrix, weighting, data, chunk, sample_rate):
   # Convert raw data (ASCII string) to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')

   # Apply FFT - real data
   fourier = np.fft.rfft(data)

   # Remove last element in array to make it the same size as chunk
   fourier = np.delete(fourier, len(fourier) - 1)

   # Find average 'amplitude' for specific frequency ranges in Hz
   power = np.abs(fourier)

   lower_bound = 0
   upper_bound = 32
   for i in range(len(matrix)):
       mean = np.mean(power[piff(lower_bound, sample_rate, chunk) : piff(upper_bound, sample_rate, chunk):1])
       matrix[i] = int(mean) if np.isnan(mean) == False else 0
       lower_bound = upper_bound
       upper_bound = upper_bound << 1

   # Tidy up column values for the light matrix
   matrix = np.multiply(matrix, weighting)

   # Set all values smaller than first argument to 0, all greater than second argument to 4095
   matrix = matrix.clip(0, 4095) 
   return matrix