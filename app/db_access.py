from flask import g
from app import id_digitizer, DEBUG, table
import mysql.connector
from mysql.connector import errorcode


"""def connect_to_database():
    try:
        return mysql.connector.connect(
            host=id_digitizer.config['RDS_CONFIG']['host'],
            port=id_digitizer.config['RDS_CONFIG']['port'],
            user=id_digitizer.config['RDS_CONFIG']['user'],
            password=id_digitizer.config['RDS_CONFIG']['password'],
            database=id_digitizer.config['RDS_CONFIG']['database']
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)"""


'''def get_user_info():
    """
    retrieve all available user info from RDS
    :return:
    """
    cnx = connect_to_database()  # Create connection to db
    cursor = cnx.cursor(buffered=True)
    query = "SELECT * FROM ECE1779.user_list;"
    cursor.execute(query)
    rows = cursor.fetchall()  # Retrieve all rows that contains the count
    return rows'''


def get_user_info():
    """
    retrieve all available user info from DynamoDB
    :return:
    """
    response = response = table.scan()
    return response['Items']


'''def put_user_info(id_num, first_name, last_name, issue_date):
    """
    add the new user info into RDS, if ID duplicates, then update that entry
    :return:
    """
    cnx = connect_to_database()  # Create connection to db
    cursor = cnx.cursor(buffered=True)
    query = "SELECT * FROM ECE1779.user_list WHERE id_num = %s;"
    cursor.execute(query, (id_num,))
    row = cursor.fetchone()  # Retrieve the first row that contains the count
    if not row:  # the id_num doesn't exist
        query = "INSERT INTO ECE1779.user_list (id_num, first_name, last_name, issue_date) VALUE (%s, %s, %s, %s);"
        cursor.execute(query, (id_num, first_name, last_name, issue_date))
        cnx.commit()
        if DEBUG:
            print('New user found! Added to DB')
    else:  # the id_num exist, update the entry
        query = "UPDATE ECE1779.user_list SET first_name = %s, last_name = %s, issue_date = %s WHERE id_num = %s;"
        cursor.execute(query, (first_name, last_name, issue_date, id_num))
        cnx.commit()
        if DEBUG:
            print('User found in DB! Updating the profile')'''


def put_user_info(id_num, first_name, last_name, issue_date):
    """
    add the new user info into RDS, if ID duplicates, then update that entry
    :return:
    """
    response = table.put_item(
        Item={
            'Key': id_num,
            'FirstName': first_name,
            'LastName': last_name,
            'IssueDate': issue_date,
        }
    )
    return response


'''def delete_user_info(id_num):
    """
    delete the given user by id_num
    :return:
    """
    cnx = connect_to_database()  # Create connection to db
    cursor = cnx.cursor(buffered=True)
    query = "SELECT * FROM ECE1779.user_list WHERE id_num = %s;"
    cursor.execute(query, (id_num,))
    row = cursor.fetchone()  # Retrieve the first row that contains the count
    if not row:  # the id_num doesn't exist
        if DEBUG:
            print("User doesn't exist")
    else:
        query = "DELETE FROM ECE1779.user_list WHERE id_num = %s;"
        cursor.execute(query, (id_num, ))
        cnx.commit()
        if DEBUG:
            print('User found! Deleted from DB')'''


def delete_user_info(id_num):
    """
    delete the given user by id_num
    :return:
    """
    response = table.delete_item(
        Key={
            'Key': id_num
        }
    )
    return response
