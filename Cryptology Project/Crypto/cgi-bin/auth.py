#!/usr/bin/env python3
import cgi
import cgitb
import sys
import os

# Enable CGI error reporting
cgitb.enable()

# Add the parent directory to sys.path to import main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from main.py
import main

def main():
    form = cgi.FieldStorage()

    action = form.getvalue('action')
    username = form.getvalue('username')
    password = form.getvalue('password')

    print("Content-Type: text/html\n")

    if action == 'register':
        if username and password:
            try:
                main.register(username, password)
                print("<html><body><h1>Registration Successful!</h1><p>Welcome, {}</p><a href='../index.html'>Back to Home</a></body></html>".format(username))
            except Exception as e:
                print("<html><body><h1>Registration Failed</h1><p>Error: {}</p><a href='../register.html'>Try Again</a></body></html>".format(str(e)))
        else:
            print("<html><body><h1>Invalid Input</h1><p>Username and password cannot be empty.</p><a href='../register.html'>Try Again</a></body></html>")

    elif action == 'login':
        if username and password:
            try:
                # Capture output from login function
                import io
                from contextlib import redirect_stdout

                f = io.StringIO()
                with redirect_stdout(f):
                    main.login(username, password)
                output = f.getvalue()

                if "LOGIN SUCCESSFUL" in output:
                    print("<html><body><h1>Login Successful!</h1><p>{}</p><a href='../index.html'>Back to Home</a></body></html>".format(output.strip()))
                else:
                    print("<html><body><h1>Login Failed</h1><p>{}</p><a href='../login.html'>Try Again</a></body></html>".format(output.strip()))
            except Exception as e:
                print("<html><body><h1>Login Failed</h1><p>Error: {}</p><a href='../login.html'>Try Again</a></body></html>".format(str(e)))
        else:
            print("<html><body><h1>Invalid Input</h1><p>Username and password cannot be empty.</p><a href='../login.html'>Try Again</a></body></html>")

    else:
        print("<html><body><h1>Invalid Action</h1><a href='../index.html'>Back to Home</a></body></html>")

if __name__ == "__main__":
    main()
