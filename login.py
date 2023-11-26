import streamlit as st
import streamlit_authenticator as sauth
from signup import sign_up, fetch_users
import signup as db

st.set_page_config(page_title='TestApp', initial_sidebar_state='collapsed')

st.title(":green[RFC Registration]")

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['mail'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    creds = {'usernames': {}}
    print("Retrieved users:", users)
    for i in range(len(emails)):
        creds['usernames'][usernames[i]] = {'name': emails[i], 'password': passwords[i]}

    print("Creds:", creds)

    authenticator = sauth.Authenticate(creds, cookie_name='Streamlit', key='aaaaaa', cookie_expiry_days=3)
    email, authentication_status, username = authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:

        if username in usernames:

            if authentication_status:
                st.subheader('Home Page')
                st.markdown('''Welcome mannnnn''')

                st.sidebar(f'Welcome {user}')
                authenticator.logout('Logout', 'sidebar')

            #elif not authentication_status:
             #   with info:
              #      st.error('Incorrect password or username')
            elif not authentication_status:
                with info:
                    st.error('Incorrect password or username. Check your credentials.')
                    st.error(f'Error message from authentication system: {info}')

            else:
                with info:
                    st.warning('Please feed in your creds')
        else:
            with info:
                st.warning('Username does not exist, please sign up!!')


except Exception as e:
    st.exception(e)
    st.success('Refresh Page')
