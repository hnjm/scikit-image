import numpy as np
from ..transform import warp
from .._shared.utils import safe_as_int
from scipy.signal import get_window


def _rotational_mapping(output_coords, window_size):
    """Mapping function for creating circularly symmetric image.

    Parameters
    ----------
    output_coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the output image
    window_size : int
        Size of the output image along an axis (both axes will be equal length)

    Returns
    -------
    coords : ndarray
        `(M, 2)` array of `(col, row)` coordinates in the input image that
        correspond to the `output_coords` given as input.
    """
    window_size = safe_as_int(window_size)
    center = (window_size / 2) - 0.5
    rr = np.sqrt(((output_coords[:, 0] - center) ** 2) +
                 ((output_coords[:, 1] - center) ** 2))
    cc = np.zeros_like(rr)
    coords = np.column_stack((cc, rr))
    return coords


def _ndrotational_mapping(output_coords, window_size):
    """Mapping function for creating hyperspherically symmetric image.

    Parameters
    ----------
    output_coords : ndarray
        `(M, N)` array of coordinates for which to find corresponding input
        coordinates. The length of N is equal to the number of dimensions
        of the output image.

    Returns
    -------
    coords : ndarray
        `(M, N)` array of input coordinates corresponding to `output_coords`
    """
    window_size = safe_as_int(window_size)
    center = (window_size / 2) - 0.5
    coords = np.zeros_like(output_coords)
    coords[:, 0] = np.sqrt(((output_coords - center) ** 2).sum(axis=1))
    return coords


def get_window2(window, size):
    """Docstring here

    Parameters
    ----------
    window : string, float, or tuple
        The type of window to be created. Windows are based on
        `scipy.signal.get_window`.
    size : int
        The size of the window along either axis. Note that only square arrays
        are created (i.e., both axes are of equal length)
    Returns
    -------

    Notes
    -----
    This function is based on `scipy.signal.get_window` and thus can access
    all of the window types available to that function.


    Examples
    --------
    """
    w = get_window(window, size, fftbins=False)
    w = w[safe_as_int(np.floor(w.shape[0]/2)):]
    w = w[:, np.newaxis]
    window2d = warp(w, _rotational_mapping,
                    map_args={'window_size': size}, output_shape=(size, size))
    return window2d


def get_windownd(window, size, ndim):
    """Docstring here

    Parameters
    ----------
    window : string, float, or tuple
        The type of window to be created. Windows are based on
        `scipy.signal.get_window`.
    size : int
        The size of the window along each axis (all axes will be equal length).
    ndim : int
        The number of dimensions of the window.
    Returns
    -------

    Notes
    -----
    This function is based on `scipy.signal.get_window` and thus can access
    all of the window types available to that function.


    Examples
    --------
    """
    w = get_window(window, size, fftbins=False)
    w = w[safe_as_int(np.floor(w.shape[0]/2)):]
    # output_shape = [size for i in range(ndim)]

    # generate a list of all coordinates

    L = [np.arange(size) for i in range(ndim)]
    outcoords = np.hstack((np.meshgrid(*L))).swapaxes(0, 1).reshape(ndim, -1).T
    outcoords = outcoords.astype(np.double)

    coords = _ndrotational_mapping(outcoords, size)
    all_coords = np.dstack((coords, outcoords))
    for i in range(ndim-1):
        w = np.expand_dims(w, axis=1)
    return all_coords
    # return windownd
