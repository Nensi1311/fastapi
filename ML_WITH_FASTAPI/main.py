from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# import ml model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)


app = FastAPI()


tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


# Pydantic model for user input
class UserInput(BaseModel):
    Age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
    Weight: Annotated[float, Field(..., gt=0, description="Weight of the user in kg")]
    Height: Annotated[float, Field(..., gt=0, description="Height of the user in cm")]
    Income_LPA: Annotated[float, Field(..., gt=0, description="Income in LPA")]
    Smoker: Annotated[bool, Field(..., description="Is the user a smoker?")]
    City: Annotated[str, Field(..., description="City of the user")]
    Occupation: Annotated[Literal['Teacher', 'Clerk', 'Lawyer', 'Engineer', 'Doctor', 'Manager'], Field(..., description="Occupation of the user")]


    @computed_field
    @property
    def bmi(self) -> float:
        return self.Weight / ((self.Height / 100) ** 2)


    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.Smoker and self.bmi > 30:
            return 'High'
        elif self.Smoker and self.bmi > 27:
            return 'Medium'
        else:
            return 'Low'
        

    @computed_field
    @property
    def age_group(self) -> str:
        if self.Age < 25:
            return 'Young'
        elif 25 <= self.Age < 45:
            return 'Adult'
        elif 45 <= self.Age < 60:
            return 'Middle-aged'
        else:
            return 'Senior'
        
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.City in tier_1_cities:
            return 1
        elif self.City in tier_2_cities:
            return 2
        else:
            return 3
        


@app.post('/predict')
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'BMI': data.bmi,
        'Lifestyle_Risk': data.lifestyle_risk,
        'Age_Group': data.age_group,
        'City_Tier': data.city_tier,
        'Income_LPA': data.Income_LPA,
        'Occupation': data.Occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"predicted_category": prediction})