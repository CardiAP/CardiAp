import numpy as np

from lib.analysis.peaks_calculation import calculate_peaks, PeaksError
from lib.analysis.peak_given import calculate_peaks_slice
from lib.analysis.statistical_functions import calculate_amplitudes, calculate_time_to_peaks, \
    calculate_times_to_half_peaks, tau_estimation, TausError
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
    intensities = savitzky_golay(intensities, 25, int(len(intensities)/min_dist_between_max_peaks), deriv=1, rate=1)
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
        "tau": 0
    })

def _analyze_matrix_slice(matrix, min_dist_between_max_peaks,result,calibration):
    intensities = np.asarray(_mean_columns(matrix), dtype=np.int16)
    intensities = savitzky_golay(intensities, 25, int(len(intensities)/min_dist_between_max_peaks), deriv=1, rate=1)
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
        "tau": 0
    })

def _mean_columns(slice):
    return np.asarray([float(np.mean(row)) for row in slice])


def _intensities_in_positions(intensities, positions):
    return [intensities[position] for position in positions]

def derivate_date(array):
    return np.gradient(array, axis=None, edge_order=1)

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
  12         the length of the window. Must be an odd integer number.
  13     order : int
  14         the order of the polynomial used in the filtering.
  15         Must be less then `window_size` - 1.
  16     deriv: int
  17         the order of the derivative to compute (default = 0 means only smoothing)
  18     Returns
  19     -------
  20     ys : ndarray, shape (N)
  21         the smoothed signal (or it's n-th derivative).
  22     Notes
  23     -----
  24     The Savitzky-Golay is a type of low-pass filter, particularly
  25     suited for smoothing noisy data. The main idea behind this
  26     approach is to make for each point a least-square fit with a
  27     polynomial of high order over a odd-sized window centered at
  28     the point.
  40     References
  41     ----------
  42     .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
  43        Data by Simplified Least Squares Procedures. Analytical
  44        Chemistry, 1964, 36 (8), pp 1627-1639.
  45     .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
  46        W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
  47        Cambridge University Press ISBN-13: 9780521880688
  48     """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(int(window_size))
        order = np.abs(int(order))
    except ValueError as msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')