from random import choice
from django.contrib.auth import get_user, get_user_model
import csv


def generate_ids(number_of_ids):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    ids = []
    for _ in range(number_of_ids):
        id_seq = []
        for _ in range(8):
            id_seq.append(choice(numbers))
        id = "".join(id_seq)
        ids.append(id)
    return ids


def create_dummy_accounts(number_of_accounts):
    ids = generate_ids(number_of_accounts)
    campuses = ["MC", "CC"]
    with open("dummy_accounts.csv", "w") as file:
        data_writer = csv.writer(file, dialect="excel")
        data_writer.writerow(["Student ID", "Password", "Campus"])

    for id in ids:
        try:
            password = get_user_model().objects.make_random_password(length=8)
            campus = choice(campuses)
            user = get_user_model().objects.create_user(
                username=id,
                password=password,
                campus=campus
            )
            with open("dummy_accounts.csv", "a") as file:
                data_writer = csv.writer(file, dialect="excel")
                data_writer.writerow([id, password, user.get_campus_display()])

            print(f"{ids.index(id) + 1} out of {len(ids)}")
        except KeyboardInterrupt as e:
            print(e)


if __name__ == "__main__":
    create_dummy_accounts()
