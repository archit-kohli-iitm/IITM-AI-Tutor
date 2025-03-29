import json

UNETHICAL_RESPONSE = "Sorry I can't answer questions about graded assignments or anything beyond this course"
INVALID_RESPONSE = "Sorry but this query does not seem to be related to this subject, Is there something else I can help you with?"
ERROR_RESPONSE = "Getting too many requests at the moment, please try again later"
NOT_FOUND_RESPONSE = "Sorry, but I dont have information related to this week/lecture in my system, maybe try something else"

categories = ["VALID","INVALID","UNETHICAL"]

with open("application/mapping.json") as file:
    week2pdf = json.load(file)

title2lecture = {
    week2pdf[week][lecture]["Title"] : (week, lecture)
    for week in week2pdf
    for lecture in week2pdf[week]
}

week2assgn = {
    "Week 1": "https://drive.google.com/file/d/1spNLcnflFrWCM7vrUdCcHrnKT040FsjL/view?usp=drive_link",
    "Week 3": "https://drive.google.com/file/d/1NMYJdN37pWneG-5qevgpJhZy2MQlWh82/view?usp=drive_link",
    "Week 4": "https://drive.google.com/file/d/1wxPIbLQEokdfqn1tvog7CWIH0XW836Bv/view?usp=drive_link",
    "Week 5": "https://drive.google.com/file/d/1P-IHNhwMYrVVYk2GR3FQVEJwiHflNy7d/view?usp=drive_link",
    "Week 6": "https://drive.google.com/file/d/1iy0mCJ-T_PH0-sU5oX8KqZfag7jvV0v0/view?usp=drive_link",
    "Week 7": "https://drive.google.com/file/d/1_yadHiEflEM9v2KyzgQp3Y_T5AJIEduC/view?usp=drive_link",
    "Week 8": "https://drive.google.com/file/d/1xH0MH_QTZlibzxiUzZYx-xGbx10dHmZB/view?usp=drive_link",
    "Week 9": "https://drive.google.com/file/d/1bKgCy-LI9SJHQKeGByKYqkVWSAVVg9sd/view?usp=drive_link",
    "Week 10": "https://drive.google.com/file/d/1p4TvM5aKM7aLZ3GvYwfLLVrLaQFaEwJl/view?usp=drive_link",
}