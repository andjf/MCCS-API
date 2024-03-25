# MCCS-API
GitHub repository for API portion of the CS5934 Capstone Project for Marine Corps Community Services (MCCS/HQ USMC)

## Usage
It is recommended to use a python virtual environment.
Once you have created a new virtual environment, install the dependencies with the following command
```
python -m pip install -r requirements.txt
```
After dependencies are installed, you should be able to run the project using
```
python -m uvicorn server:app --host localhost --port 8080 --reload
```
