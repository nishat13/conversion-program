#!/usr/bin/env python

import json
import os
import mysql.connector as mysql
from dotenv import load_dotenv


def connect_db():
    load_dotenv()

    # get environment variables
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    connection = mysql.connect(
        host="127.0.0.1",
        port="3312",
        user=user,
        password=password,
        database="******"
    )
    return connection


def insert_entry(property_id, name, defintion, db, cursor):
    query = "INSERT INTO material_property (material_property_id, name, defintion) VALUES (%s, %s, %s)"
    values = (property_id, name, defintion)
    cursor.execute(query, values)
    db.commit()


if __name__ == "__main__":

    # get connection to database
    db = connect_db()
    cursor = db.cursor()

    # set up and read data from json file
    file_name = "data.json"
    json_obj = open(file_name).read()
    json_data = json.loads(json_obj)

    # insert root node
    insert_entry(json_data["property_id"], json_data["property_name"], json_data["property_name"], db, cursor)

    # go through second and third level children/nodes
    for group in json_data["child_properties"]:
        #insert_entry(group["property_id"], group["property_name"], group["property_name"], db, cursor)
        if group["child_properties"]:
            for child in group["child_properties"]:
                #insert_entry(child["property_id"], child["property_name"], child["property_name"], db, cursor)
                if child["child_properties"]:
                    for child2 in child["child_properties"]:
                        insert_entry(child2["property_id"], child2["property_name"], child2["property_name"], db, cursor)


    # # delete all rows in table
    # delete_all_query = "truncate table material_property"
    # cursor.execute(delete_all_query)
    # db.commit()

    cursor.close()
    db.close()


