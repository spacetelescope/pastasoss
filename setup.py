import numpy as np
from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.1'

AUTHORS = 'Tyler Baines'

DESCRIPTION = 'Predicting Accurate Spectral Traces for Astrophysical SOSS Spectra'

REQUIRES = [
    'numpy',
    'pytest',
]

setup(
    name='pastasoss',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/spacetelescope/pastasoss.git',
    author=AUTHORS,
    author_email='tbaines@stsci.edu',
    license='BSD',
    keywords=['astronomy', 'python'],
    classifiers=['Programming Language :: Python'],
    packages=find_packages(),
    install_requires=REQUIRES,
    include_package_data=True,
    include_dirs=[np.get_include()],
)
