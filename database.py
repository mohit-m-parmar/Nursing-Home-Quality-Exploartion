#!/usr/bin/env python
# coding: utf-8


import psycopg2
import psycopg2.extras
from pandas import DataFrame
import pandas as pd
import json
from pymongo import MongoClient


conn = psycopg2.connect(user="nhq",
                        password="password",
                        host="127.0.0.1",
                        port="5432",
                        database="nursing_home")

# This method will check if the input credentials are valid or not.
def login(userId,pas):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM users WHERE userid = '%s' AND password = '%s'" % (userId,pas)
    cursor1.execute(query)
    user = cursor1.fetchone()
    if user:
        userId = user['userid']
        pas = user['password']
        return "Log-in Successfull"
    else:
        return "Invalid Credentials"

# This method will enter the record on new user into the database table.
def register(userId,password,email):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "INSERT INTO users VALUES (%s,%s,%s)"
    cursor1.execute(query,(userId,password,email))
    conn.commit()
    return print("User Registered Successfully ")

# This method will fetch the facility information for the given county.
def getFacilityByCounty(county,userid):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT facility_id, facility_name, city, county from facility where county = '%s'" %(county)
    cursor1.execute(query)
    dict_records = cursor1.fetchall()
    res = DataFrame(dict_records , columns = ["FACILITY ID","FACILITY NAME","CITY","COUNTY"])
    
    tableName = 'facility'
    logQuery = "INSERT INTO userlogs (userid,tablename,time,querylog) VALUES (%s,%s,current_timestamp,%s)"
    cursor1.execute(logQuery,(userid,tableName,query))
    conn.commit()
    
    return res

# This method will fetch the record of the facilities which undergone through the quality check for the input measurement year.
def getFacilitiesByQualityCheck(measurementYear,userid):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT facility.facility_id, facility.facility_name, nursing_home_quality.measurement_year FROM nursing_home_quality, facility WHERE nursing_home_quality.measurement_year = %s AND facility.facility_id = nursing_home_quality.facility_id" %(measurementYear)
    cursor1.execute(query)
    dict_records = cursor1.fetchall()
    res = DataFrame(dict_records, columns = ["FACILITY ID","FACILITY NAME","MEASUREMENT YEAR"])

    tableName = 'nursing_home_quality,facility'
    logQuery = "INSERT INTO userlogs (userid,tablename,time,querylog) VALUES (%s,%s,current_timestamp,%s)"
    cursor1.execute(logQuery,(userid,tableName,query))
    conn.commit()
    return res
 

# This method will fetch the records of Facilities which have been included in Particul measure Type.
def getFacilitiesByMeasurementType(measurementType,userid):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT DISTINCT facility.facility_name, facility.facility_id from facility JOIN nursing_home_quality ON facility.facility_id = nursing_home_quality.facility_id JOIN measurment ON nursing_home_quality.measure_id_number = (Select measurment.measure_id_number from measurment where measurment.measure_full_name = '%s') ORDER BY facility.facility_name " %(measurementType)
    cursor1.execute(query)
    dict_records = cursor1.fetchall()
    res = DataFrame(dict_records, columns = ["Facility Name" ,"Facility ID"])

    tableName = 'facility,nursing_home_quality,measurement'
    logQuery = "INSERT INTO userlogs (userid,tablename,time,querylog) VALUES (%s,%s,current_timestamp,%s)"
    cursor1.execute(logQuery,(userid,tableName,query))
    conn.commit()
    return res

# This method will return the records for the best facilities based on the year & for Albany County.
def getBestFacilities(year,userid):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    county= 'Albany'
    query = "SELECT DISTINCT facility.facility_name FROM facility JOIN public.nursing_home_quality ON facility.facility_id IN (SELECT nursing_home_quality.facility_id FROM nursing_home_quality WHERE nursing_home_quality.quintile='%s' AND nursing_home_quality.measurement_year=%s) WHERE facility.county = %s ORDER BY facility.facility_name"
    cursor1.execute(query,(1.0,year,county))
    dict_records = cursor1.fetchall()
    res = DataFrame(dict_records, columns = ["Facility Name"])

    tableName = 'facility,nursing_home_quality'
    logQuery = "INSERT INTO userlogs (userid,tablename,time,querylog) VALUES (%s,%s,current_timestamp,%s)"
    cursor1.execute(logQuery,(userid,tableName,query))
    conn.commit()

    return res


# This method will return the records for the worst facilities based on the year & for the region CRDO.
def getworstFacilities(year,userid):
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    region= 'CRDO'
    query = "SELECT DISTINCT facility.facility_name FROM facility JOIN public.nursing_home_quality ON facility.facility_id IN (SELECT nursing_home_quality.facility_id FROM nursing_home_quality WHERE nursing_home_quality.quintile='%s' AND nursing_home_quality.measurement_year=%s) WHERE facility.region = %s ORDER BY facility.facility_name"
    cursor1.execute(query,(5.0,year,region))
    dict_records = cursor1.fetchall()
    res = DataFrame(dict_records, columns = ["Facility Name"])

    tableName = 'facility,nursing_home_quality'
    logQuery = "INSERT INTO userlogs (userid,tablename,time,querylog) VALUES (%s,%s,current_timestamp,%s)"
    cursor1.execute(logQuery,(userid,tableName,query))
    conn.commit()

    return res

# This method will return the record for userlog. (Which Table & query is accessed by which user)
def getLogDetails():
    cursor1 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "select userid,tablename,time, querylog from userlogs"
    cursor1.execute(query)
    dict_records = cursor1.fetchall()
    res = DataFrame(dict_records, columns = ["UserID","Table Accessed","TIME","Query Triggered"])
    conn.commit()
    return res


# This method  will fetch number of beds available at Albany County (Will use non relation dataset)
def getTotalBedCapacity(userid):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.BedCensus
    collection = db["nursinghomebedcensus"]
    county_name = 'Albany'
    # for x in collection.find():
    #     print(x)
    file = "convertjson.json"
    with open(file) as f:
        data = json.load(f)
        x = data['response']['row'][0]['row']
        l_1=[]
        l_3 = []
        l_2 = []
    
        for i in x:
            l_1.append(i['county'])
            l_2.append(i['facility_name'])
            l_3.append(i['total_capacity']) 
                    
        d = {'county':l_1,'facility_name':l_2, 'total_capacity':l_3 }
        df = pd.DataFrame(d)

        for i in df.iterrows():
            x = i[1]
            x = list(x)
            # print(x)
            if x[0] == county_name:
                print(x)    
