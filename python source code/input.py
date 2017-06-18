# -*- coding: utf-8 -*-

class MyException(Exception):
    pass

try:
    role = input("Enter the role (admin, analyst, user): ")
    if(role not in ["admin", "analyst", "user"]):
        raise MyException('Error: Please, set role from list: [admin, analyst, user]')
    print("Role successfuly set to ", role)
    
except MyException as error:
    print(11)