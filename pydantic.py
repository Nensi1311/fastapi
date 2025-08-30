from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    #name: str = Field(max_length=50)

    # metadata example
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nensi'])]
   
    # take input only in email format
    email: EmailStr
    
    # take input only in url format
    linkedin_url: AnyUrl
    
    age: int = Field(gt=0, lt=100)
    
    #weight: float = Field(gt=0)
    # strict not allow type conversion
    weight: Annotated[float, Field(gt=0, strict=True)]
    height: float = Field(gt=0)
    married: Annotated[bool, Field(default=None, description='Is the patient married?')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

    # field validator for data validation only on single field
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']

        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of: {valid_domains}")

        return value
    

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    

    # mode = before/after, default=after
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age must be between 0 and 100")


    # model validator for data validation on multiple fields
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Emergency contact is required for patients above 60 years")
        return model


    # computed field
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi


def insert_patient_data(patient: Patient):
    print("Name: ", patient.name)
    print("Email: ", patient.email)
    print("LinkedIn URL: ", patient.linkedin_url)
    print("Age: ", patient.age)
    print("Weight: ", patient.weight)
    print("Married: ", patient.married)
    print("Allergies: ", patient.allergies)
    print("Contact Details: ", patient.contact_details)
    print("BMI: ", patient.calculate_bmi)
    print('Inserted')


def update_patient_data(patient: Patient):
    print("Name: ", patient.name)
    print("Email: ", patient.email)
    print("LinkedIn URL: ", patient.linkedin_url)
    print("Age: ", patient.age)
    print("Weight: ", patient.weight)
    print("Married: ", patient.married)
    print("Allergies: ", patient.allergies)
    print("Contact Details: ", patient.contact_details)
    print("BMI: ", patient.calculate_bmi)
    print('Updated')


patient_info = {
    'name': 'Nensi',
    'email': 'nensi@hdfc.com',
    'linkedin_url': 'https://www.linkedin.com/in/nensi',
    'age': 65,
    'weight': 45.0,
    'height': 1.75,
    'married': False,
    'allergies': ['pollen', 'nuts'],
    'contact_details': {
        'phone': '123-456-7890',
        'emergency': '987-654-3210'
    }
}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
