from django.contrib.auth import get_user_model
import csv


def create_accounts(x):
    campus = "CC"
    with open("city-campus.csv", "r") as file:
        data_reader = csv.reader(file, delimiter=",")
        students_data = [data for data in data_reader]
        total_number = len(students_data)
        for student_data in students_data[x:]:
            get_user_model().objects.create_user_account_and_send_mail(
                student_id=student_data[0],
                email=student_data[1],
                campus=campus
            )
            print(f"==============> {students_data[x:].index(student_data) + 1} out of {total_number-x}")


if __name__ == "__main__":
    create_accounts()