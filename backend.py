import json


students = []


class Student:
    def __init__(self, name, roll, marks):
        self.name = name
        self.roll = roll
        self.marks = marks

    def get_grade(self):
        if self.marks >= 17:
            return "A"
        elif self.marks >= 13:
            return "B"
        elif self.marks >= 8:
            return "C"
        else:
            return "Fail"

    def to_dict(self):
        return {
            "name": self.name,
            "roll": self.roll,
            "marks": self.marks
        }



def load_students():   # Load data
    global students
    try:
        with open("students.json", "r") as file:
            data = json.load(file)
            students = [Student(d["name"], d["roll"], d["marks"]) for d in data]
    except FileNotFoundError:
        students = []


def save_students():
    with open("students.json", "w") as file:
        data = [s.to_dict() for s in students]
        json.dump(data, file, indent=4)


def add_student(name, roll, marks):
    if marks < 0 or marks > 20:
        return "Marks must be between 0 and 20"

    for s in students:
        if s.roll == roll:
            return "Roll number already exists"

    s = Student(name, roll, marks)
    students.append(s)
    save_students()

    return "Student added successfully"


def get_all_students():
    return students


def search_student(roll):
    for s in students:
        if s.roll == roll:
            return s
    return None


def delete_student(roll):
    for s in students:
        if s.roll == roll:
            students.remove(s)
            save_students()
            return "Student deleted successfully"

    return "Student not found"