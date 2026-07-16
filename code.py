from abc import ABC,abstractmethod
import json
from  pathlib import Path
import os

database = "school_data.json"
data = {"students" : [], "teachers" : []}
if Path(database).exists():

    with open(database,"r") as f:

        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)

class persons(ABC):
    @abstractmethod
    def get_rolls():
        pass
    @abstractmethod
    def register():
        pass
    @abstractmethod
    def show_details():
        pass
    @staticmethod
    def email_varification(email):
        if "@" in email and "." in email:
            return True
        else:
            return False
    
    def attendence():
        pass


class students(persons):
    def get_rolls(self):
        return "student"
    def register(self):
        try:
            name = input("enter the name of the student :- ")
            Class = int(input("enter the class of the student")) 

            section = (input("enter the section of the student :- "))
            roll_no = int(input("enter the roll number:- "))
            email = input("enter the email id:- ")
            for i in data['students']:
                if i["roll_no"] == roll_no:
                    print("student already exists")
                    return
            data['students'].append({
                "name" : name,
                "Class" : Class,
                "roll_no": roll_no,
                "section":section,
                "email":email,
                "grades":{},
                "attendance":{}
            })
                           
            if not persons.email_varification(email):
                print("invalid email. It must contain '@' and '.' . ")
                return            
        except Exception as err:
            print(f"error occerred as {err}")
        
        save()
        print(f"student {name} registered successfully")

    def show_details(self):
        try:
            name = input("enter the name of the student:- ")
            roll_no = int(input("enter the roll number of the student"))
            for i in data['students']:
                if i["name"] == name and i["roll_no"] == roll_no:
                    print(f"Name :{i["name"]} ")
                    print(f"class :{i["Class"]} ")
                    print(f"section :{i["section"]} ")
                    print(f"roll number :{i["roll_no"]} ")
                    print(f"email:{i["email"]} ")
                    print(f"grades:{i["grades"]} ")
                    print(f" attendance : {i["attendance"]}")
                else:
                    print(f"no student named {name} exists")
        except Exception as err:
            print(f"error occerred as {err}")
    def add_grades(self):
        try:
            name = input("enter the name of the student:- ")
            roll_no = int(input("enter the roll no of the student:- "))
            subject = input("enter the subject :- ")
            marks = int(input("enter the marks :- "))

            for i in data['students']:
                if i["name"] == name and i["roll_no"] == roll_no:
                    i["grades"][subject] = marks
                    save()
                    print("grades added successfully")
                    return
                else:
                    print("student not found")
        except Exception as err:
            print(f"error occerred as {err}") 

    def attendance(self):
        try:
            name = input("enter the student name :- ")
            roll_no = int(input("enter the roll number of the student:- "))
            for i in data['students']:
                month = input("enter the month :- ")
                att = int(input("enter the attendance :- "))
                if i["name"] == name and i["roll_no"] == roll_no:
                    i["attendance"][month] = att
                    print("attendance added successfully")
                else:
                    print("student not found")

        except Exception as err:
            print(f"error occerred as {err}")
        save()
    
    def show_attendance(self):
        try:
            name =input("enter the name of the student :- ")
            roll_no = int(input("enter the roll no of the student:- "))
            for i in data['students']:
                if i["name"] == name and i["roll_no"] == roll_no:
                    print(f"attendance : {i["attendance"]}")
        except Exception as err:
            print(f" error occerred as {err}")

                   

class teachers(persons):
    def get_rolls(self):
        return "teachers"
    
    def register(self):
        try:
            name = input("enter the name of the teacher:- ")
            subject = input("enter the subject of the teacher") 
            empy_id = int(input("enter the employe id:- "))
            email = input("enter the email id:- ")
            for i in data['teachers']:
                if i["empy_id"] == empy_id:
                    print("teacher already exists")
                    return
            data['teachers'].append({
                "name" : name,
                "subject" : subject,
                "employee id": empy_id,
                "email":email,
                "attendance":{}
                
            })
                

            
            if not persons.email_varification(email):
                print("invalid email. It must contain '@' and '.' . ")
                return

            
        except Exception as err:
            print(f"error occerred as {err}")
        
        save()
        print(f"teacher {name} registered successfully")


    def show_details(self):
        try:
            name = input("enter the name of the teacher:- ")
            empy_id= int(input("enter the employee id of the teacher"))
            for i in data['teachers']:
                if i["name"] == name and i["employee id"] == empy_id:
                    print(f"Name :{i["name"]} ")
                    print(f"subject :{i["subject"]} ")
                    print(f"empy id:{i["employee id"]} ")
                    print(f"email:{i["email"]} ")
                    print(f"attendance : {i["attendance"]}")
                else:
                    print(f"no teacher named {name} exists")
        except Exception as err:
            print(f"error occerred as {err}") 

    def attendance(self):
        try:
            name = input("enter the teacher's name :- ")
            empy_id = int(input("enter the empy id of the teacher:- "))
            for i in data['teachers']:
                att = int(input("enter the attendance :- "))
                month = input("enter the month:- ")
                if i["name"] == name and i["employee id"] == empy_id:
                    i["attendance"][month] = att
                    print("attendence added successfully ")
                else:
                    print("teacher not found")

        except Exception as err:
            print(f"error occerred as {err}")
        save()
           
    def show_attendance(self):
        try:
            name =input("enter the name of the teacher :- ")
            empy_id = int(input("enter the empy id of the teacher:- "))
            for i in data['teachers']:
                if i["name"] == name and i["employee id"] == empy_id:
                    print(f"attendence : {i["attendance"]}")
                else:
                    print("teacher not found")
        except Exception as err:
            print(f" error occerred as {err}")   


print("enter '1' to register a student ")
print("enter '2' to register a teacher")
print("enter '3' to show the details of the student")
print("enter '4' to show  the teacher details")
print("enter '5' to add the grades of the students" )
print(" enter '6' to add attendence of the student")
print("enter '7' to add the attendence of the teacher")
print("enter '8' to show the attendence of the teacher")
print("enter '9' to show the attendence of the student")




choice = int(input("enter your choice :- "))
stu = students()
teach = teachers()
if choice == 1:
    stu.register()
elif choice == 2:
    teach.register()
elif choice == 3:
    stu.show_details()
elif choice == 4:
    teach.show_details()
elif choice == 5:
    stu.add_grades()
elif choice == 6:
    stu.attendance()
elif choice == 7:
    teach.attendance()
elif choice == 8:
    teach.show_attendance()
elif choice == 9:
    stu.show_attendance()
else:
    print("enter only the give options")

