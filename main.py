import logging
import warnings
from json import dump as to_json_file

from dotenv import dotenv_values

from big_query_client import BigQueryClient
from gen_ai import GenAI

logging.basicConfig(level=logging.INFO)

# Load environment variables into a dictionary
env = dotenv_values(".env")

# Ignore warnings about using end user credentials
warnings.filterwarnings(
    "ignore", "Your application has authenticated using end user credentials"
)

gen_ai_model = GenAI(
    api_key=env["GOOGLE_GEN_AI_API_KEY"],
    model_name=env["GOOGLE_GEN_AI_MODEL_NAME"],
    path_to_prompt=env["GEN_AI_PROMPT_PATH"],
)

model_generated_query = gen_ai_model.generate_query(
    PROJECT=env["BIG_QUERY_PROJECT"],
    DATASET=env["BIG_QUERY_DATASET"],
    ACTION=input("What action would you like to perform on the dataset? "),
)

big_query_client = BigQueryClient(project=env["BIG_QUERY_PROJECT"])

results = big_query_client.query(model_generated_query)

# Save results to a JSON file
with open("results.json", "w") as f:
    to_json_file(results, f, indent=4)
