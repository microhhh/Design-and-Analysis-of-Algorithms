import sys
from tqdm import trange
import numpy as np
from imageio import imread, imwrite
from scipy.ndimage.filters import convolve


def calc_energy(img):
    # Sobel filter for horizontal
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # 3D horizontal filter for each channel: R, G, B
    filter_du = np.stack([filter_du] * 3, axis=2)

    # Sobel filter for Vertical
    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # 3D Vertical filter for each channel: R, G, B
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # We sum the energies in the red, green, and blue channels
    energy_map = convolved.sum(axis=2)
    return energy_map


def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in trange(c - new_c):
        img = carve_column(img)

    return img


def crop_r(img, scale_r):
    img = np.rot90(img, 1)
    img = crop_c(img, scale_r)
    img = np.rot90(img, -1)
    return img


def carve_column(img):
    width, height, _ = img.shape
    M, solution = minimum_seam(img)
    mask = np.ones((width, height), dtype=np.bool)

    j = np.argmin(M[-1])
    for i in reversed(range(width)):
        mask[i, j] = False
        j = solution[i, j]

    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((width, height - 1, 3))
    return img


def minimum_seam(img):
    width, height, _ = img.shape
    energy_map = calc_energy(img)
    M = energy_map.copy()
    solution = np.zeros_like(M, dtype=np.int)

    # dynamic programming with M(i,j)
    for i in range(1, width):
        for j in range(0, height):
            if j == 0:
                offset = np.argmin(M[i - 1, j:j + 2])
                solution[i, j] = offset + j
                min_energy = M[i - 1, offset + j]
            else:
                offset = np.argmin(M[i - 1, j - 1:j + 2])
                solution[i, j] = offset + j - 1
                min_energy = M[i - 1, offset + j - 1]

            M[i, j] += min_energy

    return M, solution


if __name__ == '__main__':
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    scale = 0.5

    img = imread(in_filename)
    print('------caving in columns--------')
    out = crop_c(img, scale)
    print('------caving in rows-----------')
    out = crop_r(out, scale)
    imwrite(out_filename, out)
