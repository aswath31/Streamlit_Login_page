import datetime
# import os
# from dotenv import load_dotenv
import streamlit as st
import streamlit_authenticator as stauth
from deta import Deta
import re

# Connection to deta DB
# load_dotenv(".env")
# Deta_Key= os.getenv("Deta_Key")
Deta_Key = 'd0mpudvyub2_VZ5rS4ahL8uVeN9ZtMTKQJiqDyNKvJ6H'
deta = Deta(Deta_Key)

# passing base name created in deta cloud
db = deta.Base('Login_Auth')

# Inserting data into data_base

# inserts users in DB and records time of insertion
"""def insert_user(email, first_name, last_name,dob, password):
    signup_date = str(datetime.datetime.now())
    return db.put({'mail': email, 'first_name': first_name, 'last_name': last_name, 'DOB': dob,'password': password,
                   'date_of_signup': signup_date})
"""


def insert_user(email, username, password):
    signup_date = str(datetime.datetime.now())
    return db.put({'mail': email, 'username': username, 'password': password,
                   'date_of_signup': signup_date})


# dob
# 'DOB': dob,
# testing the data insertion in deta DB
# print(insert_user('test1@gmail.com','ftest','ltest','12**34'))
# status:200

def fetch_users():
    users_in_db = db.fetch()
    return users_in_db.items


# testing the data fetch from deta DB
# print(fetch_users())
# 200

def get_user_emails():
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['mail'])
    return emails


# test
# print(get_user_emails())
# 200

"""
def get_firstnames():
    users = db.fetch()
    firstnames = []
    for user in users.items:
        firstnames.append(user['first_name'])
    return firstnames
"""


def get_username():
    username = []
    users = fetch_users()  # Assuming this function fetches user data
    for user in users:
        if 'username' in user:  # Check if 'username' key exists
            username.append(user['username'])
    return username


# test
# print(get_firstnames())
# 200

"""""
def get_lastnames():
    users = db.fetch()
    lastnames = []
    for user in users.items:
        lastnames.append(user['last_name'])
    return lastnames
"""


# function to validate the email entered by the user
# check email validity and returns true if valid else false


def validate_email(email):
    # testmail001@gamil.com
    pattern_to_verify_email = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern_to_verify_email, email):
        return True
    else:
        False


# function to validate the firstname entered by the user
# check name validity and returns true if valid else false


"""
def validate_firstname(first_name):
    pattern_to_verify_name = "^[a-zA-Z0-9]*$"

    if re.match(pattern_to_verify_name, first_name):
        return True
    else:
        False
"""


def validate_username(username):
    pattern_to_verify_name = "^[a-zA-Z0-9]*$"

    if re.match(pattern_to_verify_name, username):
        return True
    else:
        False


# function to validate the lasttname entered by the user
# check name validity and returns true if valid else false


"""
def validate_lastname(last_name):
    pattern_to_verify_name = "^[a-zA-Z0-9]*$"

    if re.match(pattern_to_verify_name, last_name):
        return True
    else:
        False

"""


# Login page using streamlit form
def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':green[User Registration]')
        email = st.text_input('Email', placeholder='Enter your Email')
        username = st.text_input('User Name', placeholder='Enter your Name')
        # last_name = st.text_input('Last Name', placeholder='Enter your Last Name')
        # dob = st.date_input('Date of Birth')
        # dob_str = dob.isoformat()
        password = st.text_input('Password', placeholder='Enter your Password', type='password')
        confirm_password = st.text_input('Confirm Password', placeholder='Confirm your password', type='password')

        # validation of user inputs
        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_username():
                            if len(username) >= 2:
                                #          if validate_lastname(last_name):
                                #             if last_name not in get_lastnames():
                                #                if len(last_name) >=2:
                                if len(password) >= 8:
                                    if password == confirm_password:
                                        # At this point user will be added in DB
                                        # We can even use hashed password to hide the visibility of exact password in DB
                                        hashed_pass = stauth.Hasher([confirm_password]).generate()
                                        insert_user(email, username, hashed_pass)
                                        # dob_str
                                        # insert_user(email,first_name,last_name,dob_str,hashed_pass)
                                        st.success('Account Created!!!')

                                    else:
                                        st.warning('Password not matching')
                                else:
                                    st.warning('Password is too short')
                            # else:
                            #   st.warning('Lastname is too short')
                            # else:
                            #   st.warning('Lastname already Exists')
                            # else:
                            #   st.warning('Invalid Lastname')
                            else:
                                st.warning('username is too short')
                        else:
                            st.warning('username Already Exists')
                    else:
                        st.warning('Invalid Firstname')
                else:
                    st.warning('Email Already Exists')
            else:
                st.warning('Invalid Email')
        # alignment for submit button in our app as this is located at left most corner


        sb1, sb2, sb3, sb4, sb5 = st.columns(5)
        with sb3:
            st.form_submit_button('Submit')

if __name__ == '__main__':
    sign_up()
