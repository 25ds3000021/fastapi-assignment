from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

students = []

with open("q-fastapi.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students.append(
            {
                "studentId": int(row["studentId"]),
                "class": row["class"]
            }
        )


@app.get("/api")
async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):

    if not class_:
        return {"students": students}

    filtered_students = [
        student
        for student in students
        if student["class"] in class_
    ]

    return {"students": filtered_students}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)