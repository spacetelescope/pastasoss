# import numpy as np
# from setuptools import setup

# setup(
#     include_dirs=[np.get_include()],
# )


from setuptools import setup

setup(
    name='pastasoss',
    version="0.1.0", 
    author='Tyler Baines',
    author_email = 'tbaines@stsci.edu',
    packages =['pastasoss'],

    description ='Predict Spectral Traces for Astro SOSS Spectra',
    package_dir = {"pastasoss":'pastasoss'},
    package_data={
        'pastasoss': ['data/*.txt']
    },
    include_package_data=True,
    include_dirs = ['pastasoss','pastasoss/data'],
    install_requires = ['numpy','matplotlib'],
    )