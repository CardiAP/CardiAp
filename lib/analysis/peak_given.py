from peakutils import indexes
import numpy as np


def calculate_peaks_slice(vector, min_dist_between_max_peaks,matrix):

    max_peaks = _max_peaks_positions(vector, min_dist_between_max_peaks)
    min_peaks = _min_peaks_positions(matrix, max_peaks)

    return max_peaks, min_peaks


def _max_peaks_positions(results,intensities):
    max_peaks = results['max_peaks_positions']
    
    return max_peaks


# For the calculation of minimum peaks we need at least 1 maximum peak
def _min_peaks_positions(intensities, max_peaks):
    minimums = []
    last_max = 0
    for max_index in max_peaks:
        minimums.append(np.array(intensities[last_max:max_index]).argmin() + last_max)
        last_max = max_index

    minimums.append(np.array(intensities[last_max:len(intensities)]).argmin() + last_max)

    return minimums
