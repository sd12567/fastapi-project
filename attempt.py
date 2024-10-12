from fastapi import FastAPI,Body
from pydantic import BaseModel,Field
import json
import os

app=FastAPI()
filename='students.json'

class Student(BaseModel):
    name:str
    roll:int=Field(...,ge=1)



@app.post('/students/new')
async def add_student(new_student:Student=Body(...)):
    loaded=[]

    if os.path.getsize(filename)>0:
        with open(filename,'r') as file:
            loaded=json.load(file)
    
        if loaded:
            for item in list(loaded):
                 if item['roll']==new_student.roll:
                         return {"message":f"Student with roll-no {item['roll']} already exists!"}

    loaded.append(new_student.dict())

    with open(filename,'w') as file:
        json.dump(loaded,file)   
    return f"{new_student.name} with roll-no {new_student.roll} added successfully!"


@app.get('/students/view/{student_roll}')
def get_student_data(student_roll:int,student_name:str|None=None):
    loaded=[]
    with open(filename,'r') as file:
        loaded=json.load(file)
    for item in loaded:
        if item['roll']==student_roll:
            return {"message":f"Student name is {item['name']} and roll-no is {student_roll}"}
    return {"message":"Student not found!"}

    
@app.delete('/students/remove/{student_roll}')
def remove_student(student_roll:int,student_name:str|None=None):
    loaded=[]
    name:str|None
    f=0
    with open(filename,'r') as file:
        loaded=json.load(file)
    for item in loaded:
        if item['roll']==student_roll:
            name=item['name']
            loaded.remove(item)
            f=1
            break
    
    if f==0:
        return {"message":"Student not found!Cant be deleted"}
    with open(filename,'w') as file:
        json.dump(loaded,file)
    return {"message":f"Student {name} with {student_roll} was succesfully removed from records!"}




@app.put('/students/update/{student_roll}')
def update_student_record(student_roll:int,student_name:str):
    loaded=[]
    f=0
    old_name:str|None
    with open(filename,'r') as file:
        loaded=json.load(file)
    
    for item in loaded:
        if item['roll']==student_roll:
            f=1
            old_name=item['name']
            item['name']=student_name
            with open(filename,'w') as file:
                json.dump(loaded,file)
            break
    if f==0:
        return {"message":f"Student with roll-no {student_roll} does not exist"}
    return {"message":f"Name of student with roll-no {student_roll} updated from {old_name} to {student_name}"}
        
