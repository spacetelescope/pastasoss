## **Predicting Accurate Spectral Traces in Astrophysical SOSS Spectra** (PASTASOSS)

**Author**: Tyler Baines, NIRISS/SOSS STScI Science Support Analyst 

**Email**: tbaines@stsci.edu

----

## Overview

PASTASOSS is a powerful tool designed to predict the position and associated wavelength wavelength values of the GR700XD spectral traces in NIRISS/SOSS observations with the GR700XD with sub-pixel accuracy. It currently supports spectral orders 1 and 2, with plans for future support for order 3. Order 1 and 2 trace position models are provided along with their respective wavelength solutions. It is important to note that the reference files included in this package are not apart of the offical JWST reference files system at this time. 

As more NIRISS/SOSS observations become increasingly available, we are commited to continually updating the tool and reference data models to ensure its accuracy and relevance. 

Please be aware that the spectral trace positions provided are based on the `SUBSTRIP256` subarray configuration. We have not conducted accuracy tests using the `SUBSTRIP96` subarray or analyzed/compared trace positions with the `F277W` filter.

## Spectral Trace Position Ranges

For each spectral order, the **current position ranges** of the spectral traces are defined as:

- **Order 1:** The spectral trace positions ('x') range from pixel column 4 to 2043.
- **Order 2:** The spectral trace positions ('x') span from pixel column 1000 to 1750, with upcoming support for an extended range down to pixel column 650.
- **Order 3:** TBD.

Additionally, it's important to note that the **wavelength calibration model** for **Order 1** has full coverage while **Order 2** has partial coverage. 

The GR700XD pupil wheel tolerance is 245.76 $\pm$ 0.1651 degrees.

## Installation

To install the package via pip, use the following command:

```bash
pip install pastasoss
```

Altneratively, you can clone the repository and navigate to directory:

```bash
pip install .
```

## Usage

To use the package:

```bash
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
Community feedback  and contribution is encouraged! 


If you make use of this code, please cite: TBD