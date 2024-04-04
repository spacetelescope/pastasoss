## **Predicting Accurate Spectral Traces in Astrophysical SOSS Spectra** (PASTASOSS)

**Author**: Tyler Baines

**Affiliation**: Science Support Analyst, NIRISS/SOSS Team, Space Telescope Science Institute (STScI)

**Email**: tbaines@stsci.edu

----

## Overview

When JWST operates in the NIRISS/SOSS mode, the rotation of the pupil wheel, responsible for positioning the GR700XD grism into the optical path, does not consistently align with its expected position (i.e., there is a slight rotational offset). This variability, with shifts of just a few fractions of a degree from the commanded position, leads to noticeable changes in the positions of spectral traces (with the greatest changes observed at redder wavelength) for NIRISS/SOSS observations from one visit to another. These variations can result in differences in the wavelength solutions between visits, potentially impacting data accuracy. 

To address these challenges and ensure accurate data analysis and spectral extraction, we introduce **PASTASOSS**, a robust tool to designed to predict the positions and associated wavelength values of the GR700XD spectral traces with sub-pixel precision. Currently, the tools supports spectral orders 1 and 2, with plans to extend support to order 3 in the future. PASTASOSS provides trace position models for both Order 1 and Order 2, which accurately represent the positions when the GR700XD is located in its commanded positions. Additionally, it offers a global wavelength solution based on the pupil wheel position, ensuring precise spectral calibration. It's worth noting that the reference files included in this package are not apart of the official JWST reference files system at this time. However, they serve as essential resources for achieving precise spectral trace predictions in the face of instrument variatation. 

As more NIRISS/SOSS observations become increasingly available, we are commited to continually updating the tool and reference data models to ensure its accuracy and relevance. 

* *Note: Please be aware that the spectral trace positions provided are based on the `SUBSTRIP256` subarray configuration. We have not conducted accuracy tests using the `SUBSTRIP96` subarray or analyzed/compared trace positions with the `F277W` filter. While we believe that the tool should function adequately with these configurations, we advise users to proceed with caution and use them at their own discretion, as thorough testing has not yet been completed.* 

## Supported Spectral Trace Ranges

| Spectral Order | Trace Position Model (Pixels)  | Wavelength Solution Model ($\mu m$)| PWCPOS (deg)      | 
| :------------- | :----------------------------: | :--------------------------------: | :----------:      |
| Order 1        | [4, 2043]                      | [0.85, 2.83]                       | [245.656, 245.923]|
| Order 2        | [0, 1750+]                     | [0.60, 1.42]                       | [245.656, 245.923]|
| Order 3        | Unsupported                    | Unsupported                        | Unsupported       |

## Installation

To install the package via pip, use the following command:

```bash
pip install pastasoss
```

Alternatively, you can clone the repository and navigate to directory:

```bash
git clone https://github.com/spacetelescope/pastasoss.git
cd pastasoss
pip install .
```

## Usage

To use the package:

```python
import pastasoss

# predict gr700xd traces position for order 1
pastasoss.get_soss_traces(245.84, order='1')

# predict gr700xd traces position for order 2
pastasoss.get_soss_traces(245.84, order='2')

# predict gr700xd traces position for orders 1 and 2
pastasoss.get_soss_traces(245.84, order='12')
```

## Demo

A concise demonstration [notebook](https://github.com/tbainesUA/pastasoss/blob/develop/notebooks/pastasoss_demo.ipynb) is included with the package. We encourage users to explore it for a quick introduction to **PASTASOSS**. 


## Get Involved

We welcome community feedback to improve and expand PASTASOSS. 



If you make use of this code, please cite: 
- [Characterization of the visit-to-visit Stability of the GR700XD Spectral Traces for NIRISS/SOSS Observations](https://ui.adsabs.harvard.edu/abs/2023arXiv231107769B/abstract)
- [Characterization of the visit-to-visit Stability of the GR700XD Wavelength Calibration for NIRISS/SOSS Observations](https://ui.adsabs.harvard.edu/abs/2023jwst.rept.8571B/abstract)
