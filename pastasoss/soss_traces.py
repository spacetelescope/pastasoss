# module to predict SOSS trace positions for a given spectral order(s) 
# given the  a pupil wheel position angle taken from the "PWCPOS" fits
# header keyword. 

import numpy as np

PWCPOS_CMD = 245.76  # reference commanded position angle for the GR700XD

reference_trace_files = {
    'order1':'jw_soss_order1_refmodel.txt',  # reference trace positions file for order 1
    'order2':'jw_soss_order2_refmodel.txt',  # reference trace positions file for order 2 (TBD)
    'order3':'jw_soss_order3_refmodel.txt',  # reference trace positions file for order 3 (TBD)
}

def rotate(x, y, angle, origin=(0,0), interp=True):
    """Rotation transformation"""
    
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
    

def get_reference_traces_positions(file):
    """
    load in the reference trace positions given the file associated
    with the a given spectral order.
    """
    traces = np.loadtxt(file)
    origin = traces[0]
    x = traces[1:,0]
    y = traces[1:,1]
    return x, y, origin


def get_trace_from_reference_transform(pwcpos, order='123', interp=True):

    """Predict trace positions given p"""
    
    norders = len(order)
    
    if norders > 3:
        raise ValueError('order must be: 1, 2, 3, or combination, Example of 123')
   
    if norders > 1:
        # recursively compute the new traces for each order
        return [get_trace_from_reference_transform(pwcpos, odr) for odr in order]
    elif order == '1' :
        x, y, origin = get_reference_traces_positions(reference_trace_files['order1'])
    elif order == '2':
        # x, y, origin = get_reference_traces_positions(reference_trace_files['order2'])
        raise NotImplementedError
    else:# order == '3':
        #x, y, origin = get_reference_traces_positions(reference_trace_files['order2'])
        raise NotImplementedError
       
    x_new, y_new = rotate(x, y, pwcpos-PWCPOS_CMD, origin, interp=interp)

    return x_new, y_new 

