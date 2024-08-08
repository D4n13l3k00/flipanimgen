from numba import jit
import numpy as np


@jit(nopython=True)
def clamp(color):
    return max(0, min(255, color))


@jit(nopython=True)
def floyd_steinberg_dither(image):
    height, width = (image.shape[0], image.shape[1])

    for y in range(0, height - 1):
        for x in range(1, width - 1):
            old_p = image[y, x]
            new_p = np.round(old_p / 255.0) * 255
            image[y, x] = new_p

            quant_error_p = old_p - new_p

            image[y, x + 1] = clamp(
                image[y, x + 1] + quant_error_p * 0.4375
            )  # 7 / 16.0
            image[y + 1, x - 1] = clamp(
                image[y + 1, x - 1] + quant_error_p * 0.1875
            )  # 3 / 16.0
            image[y + 1, x] = clamp(
                image[y + 1, x] + quant_error_p * 0.3125
            )  # 5 / 16.0
            image[y + 1, x + 1] = clamp(
                image[y + 1, x + 1] + quant_error_p * 0.0625
            )  # 1 / 16.0

    return image
