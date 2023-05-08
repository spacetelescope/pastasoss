# module to predict SOSS trace positions for a given spectral order(s) 
# given the  a pupil wheel position angle taken from the "PWCPOS" fits
# header keyword. 

from typing import  Tuple, Union

import numpy as np
import os
from pkg_resources import resource_filename

# __all__ = ['rotate', 'get_reference_traces_positions', 'get_trace_from_reference_transform']

PWCPOS_CMD = 245.7600  # reference commanded position angle for the GR700XD

DATADIR = resource_filename('pastasoss', 'data')

# order 3 currently unsupport ATM. Will be support in the future: TBD
REFERENCE_TRACE_FILES = {
    'order1':'pastasoss/data/jwst_niriss_gr700xd_order1_trace_refmodel.txt',
    'order2':'pastasoss/data/jwst_niriss_gr700xd_order2_trace_refmodel.txt', 
}


def rotate(x: np.ndarray, y: np.ndarray, angle: float, origin: Tuple[float, float]=(0, 0), interp: bool=True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies a rotation transformation to a set of 2D points.

    Parameters
    ----------
    x : np.ndarray
        The x-coordinates of the points to be transformed.
    y : np.ndarray
        The y-coordinates of the points to be transformed.
    angle : float
        The angle (in degrees) by which to rotate the points.
    origin : Tuple[float, float], optional
        The point about which to rotate the points. Default is (0, 0).
    interp : bool, optional
        Whether to interpolate the rotated positions onto the original x-pixel column values. Default is True.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        The x and y coordinates of the rotated points.

    Examples
    --------
    >>> x = np.array([0, 1, 2, 3])
    >>> y = np.array([0, 1, 2, 3])
    >>> x_rot, y_rot = rotate(x, y, 90)
    """
    # shift to rotate about center    
    xy_center = np.atleast_2d(origin).T
    xy = np.vstack([x, y]) 
    
    # Rotation transform matrix
    radians = np.radians(angle)
    c, s = np.cos(radians), np.sin(radians)
    R = np.array([[c, -s], 
                  [s,  c]])
    
    # apply transformation
    x_new, y_new = R @ (xy - xy_center) + xy_center
    
    # interpolate rotated positions onto x-pixel column values (default)

    if interp:
        y_new = np.interp(x, x_new, y_new)
        return x, y_new
    else:
        return x_new, y_new
    

def get_reference_traces_positions(file: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Load in the reference trace positions given a file associated with a given spectral order.

    Parameters
    ----------
    file : str
        The path to the file containing the reference trace positions.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        A tuple containing the x, y positions and origin of the reference traces.

    Raises
    ------
    IOError
        If the file cannot be found or read.

    Examples
    --------
    >>> x, y, origin = get_reference_traces_positions('reference_trace_filename.txt')
    """
    traces = np.loadtxt(file)
    origin = traces[0]
    x = traces[1:,0]
    y = traces[1:,1]
    return x, y, origin


def get_trace_from_reference_transform(pwcpos: float, order: str='123', interp: bool=True) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """
    Gets gr700xd trace position given the pupil wheel positions angle provided in the FITS header under keyword PWCPOS. 
    Traces for a given spectral order are predict by perform a rotation transformation on the reference trace positions.
    This methods yield sub-pixel performance and will be improved upon in later interations as more NIRISS/SOSS observations
    become available. 

    Parameters
    ----------
    pwcpos : float
        The pupil wheel positions angle provided in the FITS header under keyword PWCPOS.
    order : str, optional
        The spectral order to compute the new traces for. Default is '123'. 
        Support for order 3 will be added at a later date.
    interp : bool, optional
        Whether to interpolate the rotated positions onto the original x-pixel column values. 
        Default is True.

    Returns
    -------
    Union[Tuple[np.ndarray, np.ndarray], List[Tuple[np.ndarray, np.ndarray]]]
        If `order` is '1', a tuple of the x and y coordinates of the rotated points for the first spectral order.
        If `order` is '2', a tuple of the x and y coordinates of the rotated points for the second spectral order.
        If `order` is '3' or a combination of '1', '2', and '3', a list of tuples of the x and y coordinates of the 
        rotated points for each spectral order.

    Raises
    ------
    ValueError
        If `order` is not '1', '2', '3', or a combination of '1', '2', and '3'.

    Examples
    --------
    >>> x_new, y_new = get_trace_from_reference_transform(2.3)
    """
    
    norders = len(order)
    
    if norders > 3:
        raise ValueError('order must be: 1, 2, 3, or combination, Example of 123')
   
    if norders > 1:
        # recursively compute the new traces for each order
        return [get_trace_from_reference_transform(pwcpos, odr) for odr in order]
    
    elif order == '1' :
        trace_file = os.path.join(DATADIR, REFERENCE_TRACE_FILES['order1'])
        x, y, origin = get_reference_traces_positions(trace_file)

    elif order == '2':
        trace_file = os.path.join(DATADIR, REFERENCE_TRACE_FILES['order2'])
        x, y, origin = get_reference_traces_positions(trace_file)

    elif order == '3':
        print('Order 3 is not yet supported as of yet. Will be supported in the future')
        return 
       
    x_new, y_new = rotate(x, y, pwcpos-PWCPOS_CMD, origin, interp=interp)

    return x_new, y_new 

