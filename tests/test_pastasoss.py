import os
from pkg_resources import resource_filename

from pastasoss.soss_traces import rotate
from pastasoss.soss_traces import get_reference_trace
from pastasoss.soss_traces import REFERENCE_TRACE_FILES

from pastasoss.soss_wavemaps import extrapolate_to_wavegrid
from pastasoss.soss_wavemaps import calc_2d_wave_map
from pastasoss.soss_wavemaps import get_soss_wavemaps

from pastasoss.pipeline import write_soss_reffiles

from pastasoss.wavecal import get_wavecal_meta_for_spectral_order


def test_rotate():
    """Test rotate step to ensure that x coordinate input is return in the
    output when interpolating back onto the pixel column grid.  """
    x = [1, 2, 3, 4]
    y = [5, 6, 7, 8]

    x_coords, y_coords = rotate(x, y, 45., interp=True)

    assert x_coords == x


def test_load_wavecal_model_order1():
    """Test if wavecol model json files are loaded in correctly and properly
    stored in its datamodel object for order 1"""
    # polynomial expected number of coefficient and degree
    NCOEF = 20
    POLY_DEGREE = 5
    INTERCEPT = 2.761308747854264  # in units of microns

    # fitted x-pixel columns limits
    X_MIN_SCALER = 73.62893071613087
    X_MAX_SCALER = 2039.7420006352984

    # fitted PWCPOW offset (i.e., PWCPOS-245.76)
    PWCPOS_OFFSET_MIN_SCALER = -0.1035520000001781
    PWCPOS_OFFSET_MAX_SCALER = 0.1628820800781341

    # load order 1 wavecal model
    order1_metadata = get_wavecal_meta_for_spectral_order('order1')

    assert order1_metadata.order == 'order1'
    assert len(order1_metadata.coefficients) == NCOEF
    assert order1_metadata.poly_degree == POLY_DEGREE
    assert order1_metadata.intercept == INTERCEPT
    assert order1_metadata.scaler_data_min_[0] == X_MIN_SCALER
    assert order1_metadata.scaler_data_max_[0] == X_MAX_SCALER
    assert order1_metadata.scaler_data_min_[1] == PWCPOS_OFFSET_MIN_SCALER
    assert order1_metadata.scaler_data_max_[1] == PWCPOS_OFFSET_MAX_SCALER


def test_load_wavecal_model_order2():
    """Test if wavecol model json files are loaded in correctly and properly
    stored in its datamodel object for order 2"""

    # polynomial expected number of coefficient and degree
    NCOEF = 9
    POLY_DEGREE = 3
    INTERCEPT = 1.0957902455177815  # in units of microns

    # fitted x-pixel columns limits
    X_MIN_SCALER = 672.1379843340777
    X_MAX_SCALER = 1619.4246462385518

    # fitted PWCPOW offset (i.e., PWCPOS-245.76)
    PWCPOS_OFFSET_MIN_SCALER = -0.10355200000017817
    PWCPOS_OFFSET_MAX_SCALER = 0.1579992675781341

    # load order 1 wavecal model
    order2_metadata = get_wavecal_meta_for_spectral_order('order2')

    assert order2_metadata.order == 'order2'
    assert len(order2_metadata.coefficients) == NCOEF
    assert order2_metadata.poly_degree == POLY_DEGREE
    assert order2_metadata.intercept == INTERCEPT
    assert order2_metadata.scaler_data_min_[0] == X_MIN_SCALER
    assert order2_metadata.scaler_data_max_[0] == X_MAX_SCALER
    assert order2_metadata.scaler_data_min_[1] == PWCPOS_OFFSET_MIN_SCALER
    assert order2_metadata.scaler_data_max_[1] == PWCPOS_OFFSET_MAX_SCALER


def test_load_order1_trace_model():
    # load in the trace files
    ref_trace_file = REFERENCE_TRACE_FILES['order1']
    x, _, origin = get_reference_trace(ref_trace_file)

    # check origin is what is expected and the xlimits.
    origin = (int(origin[0]), int(origin[1]))
    x_min = min(x)
    x_max = max(x)
    x_limits = (x_min, x_max)

    assert origin == (1887, 54)
    assert x_limits == (4, 2043)


def test_load_order2_trace_model():
    # load in the trace files
    ref_trace_file = REFERENCE_TRACE_FILES['order2']
    x, _, origin = get_reference_trace(ref_trace_file)

    # check origin is what is expected and the xlimits.
    origin = (int(origin[0]), int(origin[1]))
    x_min = min(x)
    x_max = max(x)
    x_limits = (x_min, x_max)

    assert origin == (1677, 200)
    assert x_limits == (1000, 1750)


def test_get_soss_wavemaps():

    # Get wavemap of commanded PWCPOS
    cmd_wavemaps = get_soss_wavemaps()

    # Get wavemaps of different PWCPOS
    pwcpos = 245.8
    rot_wavemaps = get_soss_wavemaps(pwcpos)

    # Get spectrace values as well
    tra_wavemaps, tra_spectraces = get_soss_wavemaps(pwcpos, padding=True, spectraces=True)

    assert cmd_wavemaps.shape == (2, 256, 2048)
    assert tra_wavemaps.shape == (2, 296, 2088)
    assert tra_spectraces.shape == (2, 2, 5002)
    assert not np.all(cmd_wavemaps == rot_wavemaps)


def test_write_soss_reffiles():

    # Make the files
    pwcpos = 245.9
    wavemap_file = 'test_wavemap.fits'
    spectrace_file = 'spectrace_test.fits'
    write_soss_reffiles(pwcpos, wavemap_file, spectrace_file)

    # Compare template and new spectrace data to make sure things changed
    spectrace_template = resource_filename('pastasoss', 'pastasoss/data/jwst_niriss_spectrace_template.fits')
    spectrace_template_data = fits.getdata(spectrace_template)
    spectrace_new_data = fits.getdata(spectrace_file)
    assert not np.all(spectrace_new_data.Y == spectrace_template_data.Y)

    # Compare template and new wavemap data to make sure things changed
    wavemap_template = resource_filename('pastasoss', 'pastasoss/data/jwst_niriss_spectrace_template.fits')
    wavemap_template_data = fits.getdata(wavemap_template)
    wavemap_new_data = fits.getdata(wavemap_file)
    assert not np.all(wavemap_new_data == wavemap_template_data)

    # Delete tmp files
    os.remove(wavemap_file)
    os.remove(spectrace_file)
