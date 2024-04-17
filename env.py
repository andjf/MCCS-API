from dotenv import dotenv_values

try:
    with open(".env") as f:
        pass
except FileNotFoundError:
    raise FileNotFoundError(
        "The .env file is missing. Please create one in the project root directory."
    )

env = dotenv_values(".env")
