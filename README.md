# MCCS-API
GitHub repository for API portion of the CS5934 Capstone Project for Marine Corps Community Services (MCCS/HQ USMC)

## Usage
It is recommended to use a python virtual environment.
Once you have created and activated the new virtual environment, install the dependencies with the following command
```
python -m pip install -r requirements.txt
```

After dependencies are installed, you should be able to run the project using
```
python -m uvicorn app.server:app --reload
```

You can omit the `--reload` argument if you aren't editing the contents of the server and just need to run it.

## Auth with Google Cloud
Once `gcloud` has been initialized, the following should be run:
```
gcloud auth application-default login
```

