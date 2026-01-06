from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel, Field,computed_field
from typing import Annotated,Literal,Optional

app = FastAPI()

# define pydantic model for patient data validation
class Patient(BaseModel):
    id: Annotated[str, Field(...,example="P001", description="Unique identifier for the patient")]
    name: Annotated[str, Field(...,example="Saikat Santra", description="Full name of the patient")]
    city: Annotated[str, Field(...,example="Kolkata", description="City where the patient resides")]
    age: Annotated[int, Field(...,ge=0, le=100, example=30, description="Age of the patient")]
    gender: Annotated[Literal["male", "female", "other"], Field(...,example="male", description="Gender of the patient")]
    height: Annotated[float, Field(...,ge=0,example=1.75, description="Height of the patient in meters")]
    weight: Annotated[float, Field(...,ge=0,example=70.2, description="Weight of the patient in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

# pydantic model for updating patient data
class UpdatePatient(BaseModel):
    name:Annotated[Optional[str], Field(default=None,example="Saikat Santra", description="Full name of the patient")]
    city:Annotated[Optional[str], Field(default=None,example="Kolkata", description="City where the patient resides")]
    age:Annotated[Optional[int], Field(default=None,ge=0, le=100, example=30, description="Age of the patient")]
    gender:Annotated[Optional[Literal["male", "female", "other"]], Field(default=None,example="male", description="Gender of the patient")]
    height:Annotated[Optional[float], Field(default=None,ge=0,example=1.75, description="Height of the patient in meters")]
    weight:Annotated[Optional[float], Field(default=None,ge=0,example=70.2, description="Weight of the patient in kilograms")]

# function to load patient data from JSON file
def load_data():
    try:
        with open("patients_200.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {"error": "patients_200.json file not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in patients_200.json"}

# function to save patient data to JSON file
def save_data(data):
    with open('patients_200.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def index():
    return {"message": "patients management system API"}

@app.get("/about")
def about():
    return {"message": "This is the about page of the patients management system API"}

@app.get("/view")
def view():
    data = load_data()
    return data

#path parameter
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    #load all the data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

#query parameter
@app.get("/sort")
def sort(sort_by: str = Query(..., description = "The field to sort patients by", example="bmi"),order: str = Query("asc", description="The order of sorting: asc or desc", example="asc")):
    data = load_data()
    valid_fields = ["height", "weight", "bmi", "age"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid order: {order}. Valid orders are: asc, desc")
    
    sort_order = True if order == "desc" else False
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1].get(sort_by, 0), reverse=sort_order))

    return dict(sorted_data)

# Create new patient using POST method
@app.post("/crate")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


#update existing patient using PUT method
@app.put("/update/{patient_id}")
def update_patient(patient: UpdatePatient, patient_id: str = Path(..., description="The ID of the patient to update", example="P001")):

    #load all patient data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #load existing patient data
    existing_patient_data = data[patient_id]

    #updated patient fields
    updated_data = patient.model_dump(exclude_unset=True) #exclude unset fields will give only those fields which user has provided in the request body

    for key, value in updated_data.items():
        existing_patient_data[key] = value

    # now we need to recalculate bmi and verdict if height or weight is updated
    # we will convert this existing_patient_data to pydantic model and then access bmi and verdict properties
    # Patient model requires all fields so we need to provide all fields
    
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_data['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_data)
    #-> pydantic object -> dict
    existing_patient_data = patient_pydandic_obj.model_dump(exclude='id')

    #save back the updated data
    data[patient_id] = existing_patient_data

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated successfully'})

# delete patient using DELETE method
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str = Path(..., description="The ID of the patient to delete", example="P001")):
    #load all patient data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #delete the patient
    del data[patient_id]

    #save back the updated data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})

