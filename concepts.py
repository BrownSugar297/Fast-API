from fastapi import FastAPI,HTTPException,status,Response
from httpx import post
from pydantic import BaseModel,HttpUrl #for website
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()

class Student(BaseModel):
    name: str
    id: int
    dept: str
    sem: int
    email : str

import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="FastAPI",
            user="postgres",
            password="ash297",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection failed:", error)
        time.sleep(2)  
  


@app.post("/student")
def create_post(post: Student):
    cursor.execute("""INSERT INTO pstu (name, dept, id, sem, email) VALUES (%s, %s, %s, %s, %s) RETURNING *""",
                   (post.name, post.dept, post.id, post.sem,post.email))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/")
def ashik():
    cursor.execute("""SELECT * FROM pstu """)
    data=cursor.fetchall()
    return {"Data":data}


@app.get("/dept")
def ashik(): 
    return {"Department":"CSE"}



@app.get("/id")
def ashik():
    return {"ID": "2002026"}



@app.get("/student/{id}")
def get_pstu(id: int):
    cursor.execute("""SELECT * FROM pstu WHERE id = %s""", (id,))
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    return {"details": data}


@app.delete("/student/{id}")
def delete_pstu(id: int):
    cursor.execute("""DELETE FROM pstu WHERE id = %s RETURNING *""", (id,))
    deleted_student = cursor.fetchone()
    conn.commit()
    if not deleted_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/student/{id}")
def update_student(id: int, student: Student):
    cursor.execute("""UPDATE pstu SET name = %s,id = %s, dept = %s, sem = %s, email = %s WHERE id = %s RETURNING *""",
                   (student.name, student.id, student.dept, student.sem, student.email, id))
    updated_student = cursor.fetchone()
    conn.commit()
    if not updated_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    return {"details": updated_student}