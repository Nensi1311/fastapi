from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    zip_code: str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address


address_dict = {
    'city': 'Surat',
    'state': 'Gujarat',
    'zip_code': '395006'
}


address1 = Address(**address_dict)

patient_dict = {
    'name': 'Nensi',
    'gender': 'female',
    'age': 20,
    'address': address1
}

patient1 = Patient(**patient_dict)

print(patient1)
print("Name:", patient1.name)
print("Gender:", patient1.gender)
print("Age:", patient1.age)
print("City:", patient1.address.city)
print("State:", patient1.address.state)
print("Zip Code:", patient1.address.zip_code)



# Serialization

temp = patient1.model_dump()
print(temp)
print(type(temp))

temp2 = patient1.model_dump_json()
print(temp2)
print(type(temp2))

temp3 = patient1.model_dump(include=['name', 'age'])
print(temp3)
print(type(temp3))

temp4 = patient1.model_dump(exclude=['name', 'age'])
print(temp4)
print(type(temp4))

temp5 = patient1.model_dump(exclude={'address': ['state']})
print(temp5)
print(type(temp5))