import json
import uuid
from pathlib import Path
from datetime import date
 
 
data_file = Path(__file__).with_name("data.json")
 
 
#==========take the data================
def load_data():
    with open(data_file, "r") as f:
        return json.load(f)
    
#===============rewrite the data==========
def save_data(x):
    with open(data_file, "w") as f : 
        json.dump(x, f, indent = 4)
 
def add_patient(first_name, last_name, phone_number, phone_number2, age, sex, details):
    data = load_data()
 
    new_patient = {
        "id" : str(uuid.uuid4()),
        "first name" : first_name,
        "last name" : last_name,
        "phone number" : phone_number,
        "phone number2" : phone_number2,
        "age" : age,
        "sex" : sex,
        "details" : details,
        "consultation history" : []
    }
     
    data["patients"].append(new_patient)
    save_data(data)
 
def delete_patient(patient_id):
    data = load_data()
    # Remove from patients list
    data["patients"] = [p for p in data["patients"] if p["id"] != patient_id]
    # Also remove from waiting room if present
    data["waiting room"] = [w for w in data["waiting room"] if w["id"] != patient_id]
    save_data(data)
 
def send_to_waiting_room(patient_id):
    data = load_data()
    for i in data["waiting room"]:
        if i["id"] == patient_id:
            return False
    new_entry = {
        "id" : patient_id,
        "date" : str(date.today()),
        "paid" : 0
    }
    data["waiting room"].append(new_entry)
    save_data(data)
    return True
 
def send_to_consulted(patient_id, amount_paid):
    data = load_data()
    today = str(date.today())
 
    # Remove from waiting room
    data["waiting room"] = [w for w in data["waiting room"] if w["id"] != patient_id]
 
    # Add to consulted patients
    new_entry = {
        "id": patient_id,
        "date": today,
        "paid": amount_paid
    }
    data["consulted patients"].append(new_entry)
 
    # Add to the patient's consultation history
    for p in data["patients"]:
        if p["id"] == patient_id:
            p["consultation history"].append({
                "date": today,
                "paid": amount_paid
            })
            break
 
    save_data(data)
 
#================clean up everyday consultation history and waiting room================
def clean_up():
    data = load_data()
    today = str(date.today())
    data["waiting room"] = [
        i for i in data["waiting room"]
        if i["date"] == today
    ]
    data["consulted patients"] = [
        i for i in data["consulted patients"]
        if i["date"] == today
    ]
    save_data(data)