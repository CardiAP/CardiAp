import cv2
import numpy as np


def apply_settings_to_image(image_path, settings):
    image_data = cv2.imread(image_path)
    if 'bright' in settings:
        image_data = _apply_bright(image_data, settings['bright'])

    if 'contrast' in settings:
        image_data = _apply_contrast(image_data, settings['contrast'])

    if 'filter_diameter' in settings and 'filter_sigma_color' in settings and 'filter_sigma_space' in settings:
        image_data = _apply_billateral_filter(image_data,
                                              settings['filter_diameter'],
                                              settings['filter_sigma_color'],
                                              settings['filter_sigma_space'])

    if 'cropping_coordinates' in settings:
        cropping_coordinates = settings['cropping_coordinates']
        image_data = crop_horizontal(image_data, cropping_coordinates['x_start'], cropping_coordinates['x_end'])
        image_data = crop_vertical(image_data, cropping_coordinates['y_start'], cropping_coordinates['y_end'])

    return cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)


def _apply_billateral_filter(image_data, diameter, sigma_color, sigma_space):
    return cv2.bilateralFilter(image_data, diameter, sigma_color, sigma_space)


def _apply_contrast(image_data, contrast):
    alpha_contrast = float(131 * (contrast + 127)) / (127 * (131 - contrast))
    gamma_contrast = 127 * (1 - alpha_contrast)

    return cv2.addWeighted(image_data, alpha_contrast, image_data, 0, gamma_contrast)


def _apply_bright(image_data, bright):
    if bright > 0:
        shadow = bright
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + bright

    alpha_brightness = (highlight - shadow) / 255
    gamma_brightness = shadow

    return cv2.addWeighted(image_data, alpha_brightness, image_data, 0, gamma_brightness)


# Receives 2d matrix with the intensity of each pixel in each position
# Returns 2d matrix with the intensity of each pixel in each position in gray scale an smoothed
# For smoothing we are using a bilateral filter:
# https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#bilateralfilter
def get_image_data(image):
    # TODO estos parametros queremos cambiarlos dependiendo de la imagen?
    image_matrix = cv2.bilateralFilter(image, 20, 300, 300)
    image_matrix = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)
    return image_matrix


def crop_vertical(image_matrix, pixel_start, pixel_end):
    return image_matrix[pixel_start:pixel_end]


def crop_horizontal(image_matrix, pixel_start, pixel_end):
    return image_matrix[0:len(image_matrix), pixel_start:pixel_end]


# Receives a 2d Martix and the with of the slice
# Returns a 3d Matrix that has the received matrix splited verticaly by the slice width
# Can raise ValueError if the slice width is bigger than the x axis of the image
# Examples:
# split_vertically_by[[1,2,3,4], [5,6,7,8]], 2) => [[[1,2],[5,6]], [[3,4],[7,8]]]
# split_vertically_by[[1,2,3], [5,6,7]], 2) => [[[1,2],[5,6]], [[3],[7]]]
def split_vertically_by(image_matrix, slice_width):
    image_width = len(image_matrix[0])
    if slice_width > image_width:
        raise ValueError(
            "The value of the slice width needs to be smaller than the len of the x axis"
        )

    left_over_count = image_width % slice_width
    width_to_split = image_width - left_over_count

    splited_columns = np.asarray([
        np.asarray(
            _split_column(row[0:width_to_split], slice_width) +
            [row[width_to_split:image_width]]) for row in image_matrix
    ])
    return np.transpose(splited_columns, (1, 0))


def _split_column(column, slice_width):
    return np.split(column, len(column) / slice_width)
