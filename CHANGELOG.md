# Changelog
-----
All noteable changes to this project will be documented in this file. 

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Change log adopted from the transitspectroscopy package by Nestor Espinoza. 

## [0.1.0] - 2023-05-03
### Added
- Developers: Tyler Baines and Mees Fix
- Basic setup and installation files. 
- First version of package under revision and under going testing.
- Updating code and updating data files in package. 

## [1.0.0] - Package first released
### Added
- Developers: Tyler Baines and Mees Fix
- Performed first release of the python package on github 
- have few people test including myself passed
- 

# [1.1.0] - 2023-08-29
### Added
- Updating packing to include new wavelength calibration reference file that 
are not apart of the JWST pipeline currently. 


# [1.1.0] - 2023-09-08
### Added
- modified some of the archeitecture for return outputs of trace and wavelength
predictions.
- refactoring the package to be in a more maintable state is being
planned but not implemented in this version (should be v1.1 now)
- need to push changes to ST main repo thus tag up with Mees again. 

# [1.1.0] - 2023-09-20
### Added
- updated demo notebook to include having to download a soss dataset from PID 1512
- finished integration of wavecal model and tested extensively in my dev branch
- updated the order 2 reference trace model which now extend from 600 to 1750
- readme has been update with some changes

# [1.2.0] - 2024-04-02
### Added
- Update order 2 trace model and wavelength solution to provide full support
  - jwst_niriss_gr700xd_order2_trace_refmodel_002.txt
  - jwst_niriss_gr700xd_wavelength_model_order2_002.json
- updated demo notebook showcasing order 2 completeness
- update readme to reflect additions/changes
- removing support for python 3.9 upon Astropy being deprecating Python 3.9 
so 3.10 will now be the the minimum version.
- also making additional to changes to some test and removing the duplicate
test folder that was present. 



# [1.2.1] - 2024-12-16
### Added
- removed unused .yml files and requirement.txt
- update pyproject.toml file with required pacakage as we as numpy support below version 2.0 to address open issue #13. 