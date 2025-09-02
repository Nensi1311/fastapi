from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated, Dict
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


    @field_validator('City')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v


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



class PredictionResponse(BaseModel):
    Predicted_Category: str = Field(
        ..., description="Predicted insurance premium category",
        example="Medium"
    )
    Confidence: float = Field(
        ..., description="Model's confidence score for the predicted class (range: 0 to 1)",
        example=0.85
    )
    Class_Probabilities: Dict[str, float] = Field(
        ..., description="Class probabilities for each category",
        example={"Low": 0.1, "Medium": 0.15, "High": 0.85}
    )


# human readable
@app.get('/')
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API"}


# machine readable
@app.get('/health')
def health_check():
    return {
        "Status": "Done",
        "Model Loaded": model is not None
    }


class_labels = model.classes_.tolist()

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'BMI': data.bmi,
        'Lifestyle_Risk': data.lifestyle_risk,
        'Age_Group': data.age_group,
        'City_Tier': data.city_tier,
        'Income_LPA': data.Income_LPA,
        'Occupation': data.Occupation
    }])


    try: 
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        confidence = max(probabilities)
        class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))
        return JSONResponse(status_code=200, content={"Response": prediction, "Confidence": round(confidence, 2), "Class Probabilities": class_probs})


    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})