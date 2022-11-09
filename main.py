import requests
from datetime import datetime
import os
import keys
# print(os.environ)

# WEIGHT_INPUT = input("What is your weight in kgs: ")
WEIGHT_INPUT = 72
# HEIGHT_INPUT_CM = input("What is your height in cm: ")
HEIGHT_INPUT_CM = 170
# AGE_INPUT = input("What is your age: ")
AGE_INPUT = 27
# GENDER_INPUT = input("What is your gender: ").lower()
GENDER_INPUT = "male"

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = keys.SHEET_ENDPOINT
print(sheet_endpoint)

MY_APP_KEY = keys.NT_APP_KEY
MY_APP_ID = keys.NT_APP_ID
header = {
    "x-app-id": MY_APP_ID,
    "x-app-key": MY_APP_KEY,
    "Content-Type": "application/json"
}
exercise_text = input("What exercise did you do: ")

exercise_params = {
    # "query": input("What exercise did you do today: "),
    "query": exercise_text,
    "gender": GENDER_INPUT,
    "weight_kg": WEIGHT_INPUT,
    "height_cm": HEIGHT_INPUT_CM,
    "age": AGE_INPUT
}

exercise_response = requests.post(url=EXERCISE_ENDPOINT, json=exercise_params, headers=header)
result = exercise_response.json()
# print(result)
# print(result["exercises"])

today = datetime.now()
today_formatted = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_formatted,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    bearer_headers = {
        "Authorization": f"Bearer {keys.TOKEN}"
    }
    sheety_response = requests.post(
        keys.SHEET_ENDPOINT,
        json=sheet_inputs,
        headers=bearer_headers
    )
    print(sheety_response.text)