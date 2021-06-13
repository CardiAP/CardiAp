import numpy as np

from lib.analysis.peaks_calculation import calculate_peaks
from lib.analysis.peak_given import calculate_peaks_slice
from lib.analysis.statistical_functions import calculate_amplitudes, calculate_time_to_peaks, \
    calculate_times_to_half_peaks, calculate_taus
from lib.image.image_data import split_vertically_by


def analyze_image(image, min_dist_between_max_peaks, calibration, slice_width=0):
    image_analysis = _analyze_matrix(image, min_dist_between_max_peaks, calibration)
    slices_analysis = [_analyze_matrix_slice(matrix, min_dist_between_max_peaks, image_analysis, calibration) for matrix in
                       split_vertically_by(image, slice_width)] if slice_width > 0 else []

    return ({
        "image": image_analysis,
        "slices": slices_analysis
    })


def _analyze_matrix(matrix, min_dist_between_max_peaks, calibration):
    intensities = np.asarray(_mean_columns(matrix), dtype=np.int16)
    (max_peaks_positions, min_peaks_positions) = calculate_peaks(intensities, min_dist_between_max_peaks)
    max_peaks_intensities = _intensities_in_positions(intensities, max_peaks_positions)
    min_peaks_intensities = _intensities_in_positions(intensities, min_peaks_positions)

    return ({
        "intensities": intensities,
        "max_peaks_positions": max_peaks_positions,
        "max_peaks_intensities": max_peaks_intensities,
        "min_peaks_positions": min_peaks_positions,
        "min_peaks_intensities": min_peaks_intensities,
        "amplitudes": calculate_amplitudes(max_peaks_intensities, min_peaks_intensities),
        "times_to_peaks": calculate_time_to_peaks(max_peaks_positions, min_peaks_positions, calibration),
        "times_to_half_peaks": calculate_times_to_half_peaks(intensities, max_peaks_positions, min_peaks_positions, calibration),
        "tau_s": calculate_taus(intensities, max_peaks_positions, min_peaks_positions, calibration)
    })

def _analyze_matrix_slice(matrix, min_dist_between_max_peaks,result,calibration):
    intensities = np.asarray(_mean_columns(matrix), dtype=np.int16)
    (max_peaks_positions, min_peaks_positions) = calculate_peaks_slice(result, min_dist_between_max_peaks,intensities)
    max_peaks_intensities = _intensities_in_positions(intensities, max_peaks_positions)
    min_peaks_intensities = _intensities_in_positions(intensities, min_peaks_positions)

    return ({
        "intensities": intensities,
        "max_peaks_positions": max_peaks_positions,
        "max_peaks_intensities": max_peaks_intensities,
        "min_peaks_positions": min_peaks_positions,
        "min_peaks_intensities": min_peaks_intensities,
        "amplitudes": calculate_amplitudes(max_peaks_intensities, min_peaks_intensities),
        "times_to_peaks": calculate_time_to_peaks(max_peaks_positions, min_peaks_positions, calibration),
        "times_to_half_peaks": calculate_times_to_half_peaks(intensities, max_peaks_positions, min_peaks_positions, calibration),
        "tau_s": calculate_taus(intensities, max_peaks_positions, min_peaks_positions, calibration)
    })

def _mean_columns(slice):
    return np.asarray([float(np.mean(row)) for row in slice])


def _intensities_in_positions(intensities, positions):
    return [intensities[position] for position in positions]
