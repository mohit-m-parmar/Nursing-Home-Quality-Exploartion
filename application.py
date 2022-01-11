#!/usr/bin/env python
# coding: utf-8


import database

print("Select appropriate choice : ")
choice1 = input("1. Login\n2. Register\n")
if choice1 == "1":
    userId = input("Enter ID: ")
    pas = input("Enter password: ")
    res = database.login(userId,pas)

    if res == "Log-in Successfull":
        print(res)
    #if res == "yes":

        print("Select from the following options: ")
        choice = input("1. List of Facilities undergone through the quality check for the measurement year \n2. List of Facilities included/participated in Quality Check by Measurement Type \n3. List of Top rated Facilities For Albany County for the given input year \n4. List of Worst rated Facilities For CRDO Region for the given input year \n5. List of Nursing Home based on County \n6. Get Log Details of all users \n7. List of beds Available at Albany County \n")

        if choice == '1':
            print("Enter Measurment year - ")
            year = input()
            res = database.getFacilitiesByQualityCheck(year,userId)
            print(res)
            
        elif choice == '2':
            print("Select a Measurment Parameter : ")
            choice2 = input("1. J/K/L deficiency \n2. CMS five-star quality rating for staffing\n3. CMS five-star quality rating for health inspections \n")
            if choice2 == '1':
                res = database.getFacilitiesByMeasurementType("J/K/L deficiency",userId) 
                print(res)
            if choice2 == '2':
                res = database.getFacilitiesByMeasurementType("CMS five-star quality rating for staffing",userId) 
                print(res)
            if choice2 == '3':
                res = database.getFacilitiesByMeasurementType("CMS five-star quality rating for health inspections",userId) 
                print(res)
            
        elif choice == '3':
            print("Select a Year : ")
            choice2 = input("1. 2017 \n2. 2018\n3. 2019 \n")
            if choice2 == '1':
                res = database.getBestFacilities('2017',userId) 
                print(res)
            if choice2 == '2':
                res = database.getBestFacilities('2018',userId) 
                print(res)
            if choice2 == '3':
                res = database.getBestFacilities('2019',userId) 
                print(res)
            
        elif choice == '4':
            print("Select a Year : ")
            choice2 = input("1. 2017 \n2. 2018\n3. 2019 \n")
            if choice2 == '1':
                res = database.getBestFacilities('2017',userId) 
                print(res)
            if choice2 == '2':
                res = database.getBestFacilities('2018',userId) 
                print(res)
            if choice2 == '3':
                res = database.getBestFacilities('2019',userId) 
                print(res)

        elif choice == '5':
            print("Select a county name : ")
            choice2 = input("1. New York\n2. Rensselaer\n3. Albany \n4. Westchester\n")

            if choice2 == '1':
                res = database.getFacilityByCounty("New York",userId)
                print(res)
            elif choice2 == '2':
                res = database.getFacilityByCounty("Rensselaer",userId)
                print(res)
            elif choice2 == '3':
                res = database.getFacilityByCounty("Albany",userId)
                print(res)
            elif choice2 == '4':
                res = database.getFacilityByCounty("Westchester",userId)
                print(res)
            else:
                print('Incorrect choice') 
        elif choice == '6':
            res = database.getLogDetails()
            print(res)

        elif choice == '7':
                database.getTotalBedCapacity(userId) 
               
        else:
            print("Incorrect choice")
            

    else:
        print("invalid credentials")

elif choice1 == '2':
    id = input("Enter ID : ")
    password = input("Enter password : ")
    email = input("enter e-mail address : ")

    res = database.register(id,password,email)
    
