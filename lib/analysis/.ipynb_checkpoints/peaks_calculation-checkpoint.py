from peakutils import indexes
import numpy as np

class PeaksError(ValueError):
    def feature(self):
        return "peak"

def calculate_peaks(vector, min_dist_between_max_peaks):
    max_peaks = _max_peaks_positions(vector, min_dist_between_max_peaks)
    min_peaks = _min_peaks_positions(vector, max_peaks)

    return max_peaks, min_peaks


def _max_peaks_positions(vector, min_dist_between_max_peaks):
    if len(vector) == 0:
        raise PeaksError("Empty vector")

    threshold = 1.0 / max(vector) if (max(vector) > 0) else 0
    possible_max_peaks = indexes(np.array(vector), thres=threshold, min_dist=min_dist_between_max_peaks)
    intensity_avg = sum(vector) / len(vector)
    max_peaks = [max_peak for max_peak in possible_max_peaks if vector[max_peak] > intensity_avg/8]

    if len(max_peaks) == 0: raise PeaksError("Peaks not found")

    return max_peaks


# For the calculation of minimum peaks we need at least 1 maximum peak
def _min_peaks_positions(intensities, max_peaks):
    minimums = []
    last_max = 0
    for max_index in max_peaks:
        minimums.append(minimo_bl(intensities[last_max:max_index]) + last_max)
        last_max = max_index

    minimums.append(minimo_bl(intensities[last_max:len(intensities)]) + last_max)


    return minimums
    
def minimo_bl (vector):
    b = -min((x, -i) for i, x in enumerate(vector))[1]
    return b
