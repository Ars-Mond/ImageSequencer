# Image Sequencer
This software program was created for the factorio mod at the request of ArsStels.

# Usage
1. In the "Input path" field, write or select the path to the folder with the images.
2. In the "Output path" field, write or select the path to the folder where the result will be uploaded.
3. Click "Create lua table".

#### Optional
_**P.s.** In the " Advanced" tab there is a parameter for overwriting and a field for setting the name of the lua file._

# Licence
_**AGPL-3.0**_

# Build
### Self-build application:
1. Download sources (repository).
2. Install virtualenv: `pip install virtualenv`
3. Install a python environment (venv): `python3 -m venv .venv`
4. Activate the python environment (venv): for windows `.venv/scripts/active` or for linux `source venv/bin/activate`
5. Run package installation: `pip install -r requirements.txt`
6. Run the build: `pyinstaller main.py -n ImageSequencer -i "./resources/icon.ico" --contents-directory "." --noconsole --onefile`