# Wavecal module for handling the wavelength calibration model. For now we
# will use the reference json files that has all the model information. Ideally
# we would like to use just the train model for production but for now this is
# this is fine.

import json
from dataclasses import dataclass
from functools import partial
from typing import Any, Dict

import numpy as np
import numpy.typing as npt
from pkg_resources import resource_filename

# explicitly defining the commanded position here as well (this is temp)
PWCPOS_CMD = 245.76

# reference wavecal models pkg filepaths
REFERENCE_WAVECAL_MODELS = {
    "order1": resource_filename(
        __name__, "data/jwst_niriss_gr700xd_wavelength_model_order1.json"
    ),
    "order2": resource_filename(
        __name__, "data/jwst_niriss_gr700xd_wavelength_model_order2.json"
    ),
    # order 3 currently unsupport ATM. Will be support in the future: TBD
}


@dataclass
class NIRISS_GR700XD_WAVECAL_META:
    order: str
    coefficients: npt.NDArray[np.float64]
    intercept: npt.NDArray[np.float64]
    scaler_data_min_: float
    scaler_data_max_: float


def load_wavecal_model(filename: str) -> Dict[str, Any]:
    with open(filename, "r") as file:
        wavecal_model = json.load(file)
    return wavecal_model


def get_wavecal_meta_for_spectral_order(
    order: str,
) -> NIRISS_GR700XD_WAVECAL_META:
    # get the reference wavecal file name
    if order not in REFERENCE_WAVECAL_MODELS:
        raise ValueError(
            "{order} is not a valid input: use either 'order 1', 'order 2', or 'order 3'."
        )

    reference_filename = REFERENCE_WAVECAL_MODELS[order]

    wavecal_model = load_wavecal_model(reference_filename)

    # model coefficients
    coefficients = wavecal_model["model"]["coef"]
    intercept = wavecal_model["model"]["intercept"]

    # info for scaling inputs
    scaler_data_min_ = wavecal_model["model"]["scaler"]["data_min_"]
    scaler_data_max_ = wavecal_model["model"]["scaler"]["data_max_"]

    return NIRISS_GR700XD_WAVECAL_META(
        order, coefficients, intercept, scaler_data_min_, scaler_data_max_
    )


def get_wavelengths(
    x: np.ndarray, pwcpos: float, wavecal_meta: NIRISS_GR700XD_WAVECAL_META
) -> np.ndarray:
    """Get the associated wavelength values for a given spectral order"""
    if wavecal_meta.order == "order1":
        wavelengths = wavecal_model_order1_poly(x, pwcpos, wavecal_meta)
    elif wavecal_meta.order == "order2":
        # raise NotImplementedError("Order 2 not implemented")
        wavelengths = wavecal_model_order2_poly(x, pwcpos, wavecal_meta)
    elif wavecal_meta.order == "order3":
        raise ValueError("Order 3 not supported at this time")
    else:
        raise ValueError("not a valid order")

    return wavelengths


def min_max_scaler(x, x_min, x_max):
    # scaling the input x values
    x_scaled = (x - x_min) / (x_max - x_min)
    return x_scaled


def wavecal_model_order1_poly(
    x, pwcpos, wavecal_meta: NIRISS_GR700XD_WAVECAL_META
):
    """compute order 1 wavelengths"""
    x_scaler = partial(
        min_max_scaler,
        **{
            "x_min": wavecal_meta.scaler_data_min_[0],
            "x_max": wavecal_meta.scaler_data_max_[0],
        },
    )

    pwcpos_offset_scaler = partial(
        min_max_scaler,
        **{
            "x_min": wavecal_meta.scaler_data_min_[1],
            "x_max": wavecal_meta.scaler_data_max_[1],
        },
    )

    def get_poly_features(x: np.array, offset: np.array) -> np.ndarray:
        # polynomial features
        poly_features = np.array(
            [
                x,
                offset,
                x**2,
                x * offset,
                offset**2,
                x**3,
                x**2 * offset,
                x * offset**2,
                offset**3,
                x**4,
                x**3 * offset,
                x**2 * offset**2,
                x * offset**3,
                offset**4,
                x**5,
                x**4 * offset,
                x**3 * offset**2,
                x**2 * offset**3,
                x * offset**4,
                offset**5,
            ]
        )
        return poly_features

    # extract model weights and intercept
    coef = wavecal_meta.coefficients
    intercept = wavecal_meta.intercept

    # get pixel columns and then scaled
    x_scaled = x_scaler(x)

    # offset
    offset = np.ones_like(x) * (pwcpos - PWCPOS_CMD)
    offset_scaled = pwcpos_offset_scaler(offset)

    # polynomial features
    poly_features = get_poly_features(x_scaled, offset_scaled)
    wavelengths = coef @ poly_features + intercept

    return wavelengths


def wavecal_model_order2_poly(
    x, pwcpos, wavecal_meta: NIRISS_GR700XD_WAVECAL_META
):
    """compute order 1 wavelengths"""
    x_scaler = partial(
        min_max_scaler,
        **{
            "x_min": wavecal_meta.scaler_data_min_[0],
            "x_max": wavecal_meta.scaler_data_max_[0],
        },
    )

    pwcpos_offset_scaler = partial(
        min_max_scaler,
        **{
            "x_min": wavecal_meta.scaler_data_min_[1],
            "x_max": wavecal_meta.scaler_data_max_[1],
        },
    )

    def get_poly_features(x: np.array, offset: np.array) -> np.ndarray:
        # polynomial features
        # polynomial features
        poly_features = np.array([
            x, offset, x**2, x * offset,
            offset**2, x**3,  x**2 * offset,
            x * offset**2, offset**3
        ])
        return poly_features

    coef = wavecal_meta.coefficients
    intercept = wavecal_meta.intercept

    # get pixel columns and then scaled
    x_scaled = x_scaler(x)

    # offset
    offset = np.ones_like(x) * (pwcpos - PWCPOS_CMD)
    offset_scaled = pwcpos_offset_scaler(offset)

    # polynomial features
    poly_features = get_poly_features(x_scaled, offset_scaled)
    wavelengths = coef @ poly_features + intercept

    return wavelengths
