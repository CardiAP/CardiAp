from math import log

import numpy as np
from numpy.linalg import lstsq

MIN_POSITIONS_OUT_OF_BOUND = "The min_peaks_positions are not indexes of the intensities parameter"

MAX_POSITIONS_OUT_OF_BOUND = "The max_peaks_positions are not indexes of the intensities parameter"

EMPTY_INTENSITIES = "The intensities cannot be empty"
BAD_MAX_AND_MIN_LENGTHS = "The min peaks list needs to be bigger by 1 elements than the max peaks list"
MIN_PEAKS_ARE_REQUIRED = "At least 1 min peak is required"
MAX_PEAKS_ARE_REQUIRED = "At least 1 max peak is required"


def _maxs_mins_input_validation(max_peaks, min_peaks):
    assert len(max_peaks) > 0, MAX_PEAKS_ARE_REQUIRED
    assert len(min_peaks) > 0, MIN_PEAKS_ARE_REQUIRED
    assert len(min_peaks) - len(max_peaks) == 1, BAD_MAX_AND_MIN_LENGTHS


def _intensities_validations(intensities, max_peaks_positions, min_peaks_positions):
    intensities_length = len(intensities)
    max_max_peak = max(max_peaks_positions)
    min_max_peak = min(max_peaks_positions)
    max_min_peak = max(min_peaks_positions)
    min_min_peak = min(min_peaks_positions)

    assert intensities_length > 0, EMPTY_INTENSITIES
    assert max_max_peak < intensities_length, MAX_POSITIONS_OUT_OF_BOUND
    assert max_min_peak < intensities_length, MIN_POSITIONS_OUT_OF_BOUND
    assert min_max_peak >= 0, MAX_POSITIONS_OUT_OF_BOUND
    assert min_min_peak >= 0, MIN_POSITIONS_OUT_OF_BOUND


def calculate_amplitudes(max_peaks_intensities, min_peaks_intensities):
    _maxs_mins_input_validation(max_peaks_intensities, min_peaks_intensities)

    amplitudes = []
    for i in range(0, len(min_peaks_intensities) - 1):
        amplitude = (max_peaks_intensities[i] - min_peaks_intensities[i]) / min_peaks_intensities[i]
        amplitudes.append(amplitude)
    return amplitudes


def calculate_time_to_peaks(max_peaks_positions, min_peaks_positions, calibration=1):
    _maxs_mins_input_validation(max_peaks_positions, min_peaks_positions)

    return [(max_peak - min_peak) * calibration for (min_peak, max_peak) in
            np.column_stack((min_peaks_positions[0:len(min_peaks_positions) - 1], max_peaks_positions))]


def calculate_times_to_half_peaks(intensities, max_peaks_positions, min_peaks_positions, calibration=1):
    _maxs_mins_input_validation(max_peaks_positions, min_peaks_positions)
    _intensities_validations(intensities, max_peaks_positions, min_peaks_positions)

    half_time_to_peaks = []
    for (min_index, max_index) in np.column_stack(
            (min_peaks_positions[0:len(min_peaks_positions) - 1], max_peaks_positions)):
        half_intensity_between_peaks = intensities[max_index] - ((intensities[max_index] - intensities[min_index]) / 2)

        half_max_index = 0
        intensities_between_peaks = intensities[min_index:max_index]

        for i in range(0, len(intensities_between_peaks)):
            if intensities_between_peaks[i] >= half_intensity_between_peaks:
                half_max_index = i
                break

        half_time_to_peaks.append(half_max_index * calibration)

    return half_time_to_peaks


def _calculate_tau(times, intensities):
    if len(times) == 0 or len(intensities) == 0:
        return 0
    else:
        x_axis = np.asarray([[1, t] for t in times])
        y_axis = np.asarray([log(intensity) for intensity in intensities]).T
        (w, _, _, _) = lstsq(x_axis, y_axis, rcond=None)
        return -1.0 / w[1]


def calculate_taus(intensities, max_peaks_positions, min_peaks_positions, calibration=1):
    _maxs_mins_input_validation(max_peaks_positions, min_peaks_positions)
    _intensities_validations(intensities, max_peaks_positions, min_peaks_positions)

    taus = []
    times = np.asarray(range(0, len(intensities))) * calibration
    for (max_index, min_index) in np.column_stack((max_peaks_positions, min_peaks_positions[1:len(min_peaks_positions)])):
        time_between_peaks = np.asarray(times[max_index:min_index])
        intensities_between_peaks = np.asarray(intensities[max_index:min_index])

        taus.append(_calculate_tau(time_between_peaks, intensities_between_peaks))

    return taus
