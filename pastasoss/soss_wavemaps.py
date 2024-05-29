"""
Module to generate 2D SOSS wavemap arrays from 1D wavelength solutions

Author: Joe Filippazzo
Date: 02/28/2024
Usage:
import pastasoss
pwcpos = 245.8
wavemaps = pastasoss.get_soss_wavemaps(pwcpos)
"""

import numpy as np

from pastasoss.soss_traces import get_soss_traces, PWCPOS_CMD


def extrapolate_to_wavegrid(w_grid, wavelength, quantity):
    """
    Extrapolates quantities on the right and the left of a given array of quantity

    Parameters
    ----------
    w_grid : sequence
        The wavelength grid to interpolate onto
    wavelength : sequence
        The native wavelength values of the data
    quantity : sequence
        The data to interpolate

    Returns
    -------
    Array
        The interpolated quantities
    """
    sorted = np.argsort(wavelength)
    q = quantity[sorted]
    w = wavelength[sorted]

    # Determine the slope on the right of the array
    slope_right = (q[-1] - q[-2]) / (w[-1] - w[-2])
    # extrapolate at wavelengths larger than the max on the right
    indright = np.where(w_grid > w[-1])[0]
    q_right = q[-1] + (w_grid[indright] - w[-1]) * slope_right
    # Determine the slope on the left of the array
    slope_left = (q[1] - q[0]) / (w[1] - w[0])
    # extrapolate at wavelengths smaller than the min on the left
    indleft = np.where(w_grid < w[0])[0]
    q_left = q[0] + (w_grid[indleft] - w[0]) * slope_left
    # Construct and extrapolated array of the quantity
    w = np.concatenate((w_grid[indleft], w, w_grid[indright]))
    q = np.concatenate((q_left, q, q_right))

    # resample at the w_grid everywhere
    q_grid = np.interp(w_grid, w, q)

    return q_grid


def calc_2d_wave_map(wave_grid, x_dms, y_dms, tilt, oversample=2, padding=10, maxiter=5, dtol=1e-2):
    """Compute the 2D wavelength map on the detector.

    Parameters
    ----------
    wave_grid : sequence
        The wavelength corresponding to the x_dms, y_dms, and tilt values.
    x_dms : sequence
        The trace x position on the detector in DMS coordinates.
    y_dms : sequence
        The trace y position on the detector in DMS coordinates.
    tilt : sequence
        The trace tilt angle in degrees.
    oversample : int
        The oversampling factor of the input coordinates.
    padding : int
        The native pixel padding around the edge of the detector.
    maxiter : int
        The maximum number of iterations used when solving for the wavelength at each pixel.
    dtol : float
        The tolerance of the iterative solution in pixels.

    Returns
    -------
    Array
        An array containing the wavelength at each pixel on the detector.
    """
    os = np.copy(oversample)
    xpad = np.copy(padding)
    ypad = np.copy(padding)

    # No need to compute wavelengths across the entire detector, slightly larger than SUBSTRIP256 will do.
    dimx, dimy = 2048, 300
    y_dms = y_dms + (dimy - 2048)  # Adjust y-coordinate to area of interest.

    # Generate the oversampled grid of pixel coordinates.
    x_vec = np.arange((dimx + 2 * xpad) * os) / os - (os - 1) / (2 * os) - xpad
    y_vec = np.arange((dimy + 2 * ypad) * os) / os - (os - 1) / (2 * os) - ypad
    x_grid, y_grid = np.meshgrid(x_vec, y_vec)

    # Iteratively compute the wavelength at each pixel.
    delta_x = 0.0  # A shift in x represents a shift in wavelength.
    for niter in range(maxiter):

        # Assume all y have same wavelength.
        wave_iterated = np.interp(x_grid - delta_x, x_dms[::-1],
                                  wave_grid[::-1])  # Invert arrays to get increasing x.

        # Compute the tilt angle at the wavelengths.
        tilt_tmp = np.interp(wave_iterated, wave_grid, tilt)

        # Compute the trace position at the wavelengths.
        x_estimate = np.interp(wave_iterated, wave_grid, x_dms)
        y_estimate = np.interp(wave_iterated, wave_grid, y_dms)

        # Project that back to pixel coordinates.
        x_iterated = x_estimate + (y_grid - y_estimate) * np.tan(np.deg2rad(tilt_tmp))

        # Measure error between requested and iterated position.
        delta_x = delta_x + (x_iterated - x_grid)

        # If the desired precision has been reached end iterations.
        if np.all(np.abs(x_iterated - x_grid) < dtol):
            break

    # Evaluate the final wavelength map, this time setting out-of-bounds values to NaN.
    wave_map_2d = np.interp(x_grid - delta_x, x_dms[::-1], wave_grid[::-1], left=np.nan, right=np.nan)

    # Extend to full detector size.
    tmp = np.full((os * (dimx + 2 * xpad), os * (dimx + 2 * xpad)), fill_value=np.nan)
    tmp[-os * (dimy + 2 * ypad):] = wave_map_2d
    wave_map_2d = tmp

    return wave_map_2d


def get_soss_wavemaps(pwcpos=PWCPOS_CMD, padding=False, spectraces=False):
    """
    Generate order 1 and 2 2D wavemaps from the rotated SOSS trace positions

    Parameters
    ----------
    pwcpos : float
        The pupil wheel position
    padding : bool
        Include 20px padding on map edges (only needed for reference files)
    spectraces : bool
        Return the interpolated spectraces as well

    Returns
    -------
    Array, Array
        The 2D wavemaps and corresponding 1D spectraces
    """
    traces_order1, traces_order2 = get_soss_traces(pwcpos=pwcpos, order='12', interp=True)

    # Make wavemap from trace center wavelengths, padding to shape (296, 2088)
    wavemin = 0.5
    wavemax = 5.5
    nwave = 5001
    wave_grid = np.linspace(wavemin, wavemax, nwave)

    # Extrapolate wavelengths for order 1 trace
    xtrace_order1 = extrapolate_to_wavegrid(wave_grid, traces_order1.wavelength, traces_order1.x)
    ytrace_order1 = extrapolate_to_wavegrid(wave_grid, traces_order1.wavelength, traces_order1.y)
    spectrace_1 = np.array([xtrace_order1, ytrace_order1])

    # Set cutoff for order 2 where it runs off the detector
    o2_cutoff = 1783
    print(traces_order1.wavelength, traces_order1.x, traces_order2.wavelength, traces_order2.x)
    w_o2_tmp = traces_order2.wavelength[:o2_cutoff]
    w_o2 = np.zeros(2048) * np.nan
    w_o2[:o2_cutoff] = w_o2_tmp

    # Fill for column > 1400 with linear extrapolation
    m = w_o2[o2_cutoff - 1] - w_o2[o2_cutoff - 2]
    dx = np.arange(2048 - o2_cutoff) + 1
    w_o2[o2_cutoff:] = w_o2[o2_cutoff - 1] + m * dx

    # Extrapolate wavelengths for order 2 trace
    xtrace_order2 = extrapolate_to_wavegrid(wave_grid, w_o2, traces_order2.x)
    ytrace_order2 = extrapolate_to_wavegrid(wave_grid, w_o2, traces_order2.y)
    spectrace_2 = np.array([xtrace_order2, ytrace_order2])

    # Make wavemap from wavelength solution for order 1
    wavemap_1 = calc_2d_wave_map(wave_grid, xtrace_order1, ytrace_order1, np.zeros_like(xtrace_order1), oversample=1, padding=20)

    # Make wavemap from wavelength solution for order 2
    wavemap_2 = calc_2d_wave_map(wave_grid, xtrace_order2, ytrace_order2, np.zeros_like(xtrace_order2), oversample=1, padding=20)

    # Remove padding if necessary
    if not padding:
        wavemap_1 = wavemap_1[20:-20, 20:-20]
        wavemap_2 = wavemap_2[20:-20, 20:-20]

    if spectraces:
        return np.array([wavemap_1, wavemap_2]), np.array([spectrace_1, spectrace_2])

    else:
        return np.array([wavemap_1, wavemap_2])
