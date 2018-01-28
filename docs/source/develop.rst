##############
For Developers
##############

- If you use import a new Python package make sure you add it to the requirements.txt file then create the requirements.in. This will insure that the package installed in the virtual environment and Docker image.

::

    pip-compile --output-file requirements.txt requirements.in

