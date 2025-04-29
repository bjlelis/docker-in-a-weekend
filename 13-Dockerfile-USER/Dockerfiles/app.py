from flask import Flask
import os
import pwd
import grp

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Get the current user's ID and name
    user_id = os.getuid()
    user_name = pwd.getpwuid(user_id).pw_name
    
    # Get the current group's ID and name
    group_id = os.getgid()
    group_name = grp.getgrgid(group_id).gr_name

    # Return a response displaying both the user and the group
    return f'Hello from user: {user_name} (UID: {user_id}) and group: {group_name} (GID: {group_id})!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)