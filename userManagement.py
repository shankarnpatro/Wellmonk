import csv
import requests
import time
from datetime import timedelta

Api_endpoint = "https://nutrimaker.quintuslabs.in/api/users/register/"
loginApi = "https://nutrimaker.quintuslabs.in/api/users/login/"

def csv_f():

    with open('register.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if 'first_name' not in row:
                user_register(Api_endpoint, row[0], row[1], row[2], row[3])
                login(loginApi, row[1], row[3])

            line_count += 1


def user_register(Api_endpoint, user_name, phone, email, password):

    record = {'user_name': user_name, "phone": int(phone), "email": email, "password": password}
    # print(record)
    r = requests.post(url=Api_endpoint, data=record)
    if r.status_code == 201:
        response = r.content
        print(response)
    elif r.status_code == 404:
        response = r.content
        print(response)
    else:
        print("alredy Exist")

def login(loginApi, phone, password):

    record = {"phone": phone, "password":password}
    r = requests.post(url=loginApi, data=record)
    print(r.status_code)
    print(r.content)



start_time = time.time()
elapsed_time_secs = time.time() - start_time

msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
print(msg)


csv_f()
