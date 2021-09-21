#!/usr/bin/env python3
import os, json
import cgi
import secret
# Python 3.7 versus Python 3.8
try:
    from cgi import escape #v3.7
except:
    from html import escape #v3.8
def _wrapper(page):
    """
    Wraps some text in common HTML.
    """
    return ("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 24em;
                color: #333;
                background-color: #fdfdfd
            }

            .spoilers {
                color: rgba(0,0,0,0); border-bottom: 1px dashed #ccc
            }
            .spoilers:hover {
                transition: color 250ms;
                color: rgba(36, 36, 36, 1)
            }

            label {
                display: flex;
                flex-direction: row;
            }

            label > span {
                flex: 0;
            }

            label> input {
                flex: 1;
            }

            button {
                font-size: larger;
                float: right;
                margin-top: 6px;
            }
        </style>
    </head>
    <body>
    """ + page + """
    </body>
    </html>
    """)

def login_page():
    """
    Returns the HTML for the login page.
    """

    return _wrapper(r"""
    <h1> Welcome! </h1>

    <form method="POST" action="hello.py">
        <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
        <label> <span>Password:</span> <input type="password" name="password"></label>

        <button type="submit"> Login! </button>
    </form>
    """)

def secret_page(username=None, password=None):
    """
    Returns the HTML for the page visited after the user has logged-in.
    """
    if username is None or password is None:
        raise ValueError("You need to pass both username and password!")

    return _wrapper("""
    <h1> Welcome, {username}! </h1>

    <p> <small> Pst! I know your password is
        <span class="spoilers"> {password}</span>.
        </small>
    </p>
    """.format(username=escape(username.capitalize()),
               password=escape(password)))

def main():
    envObjs = dict(os.environ)
    json_object = json.dumps(envObjs, indent=4)

    form = cgi.FieldStorage()
    username = form.getvalue("username")
    password = form.getvalue("password")
    if username == secret.username and password == secret.password:
        print("Set-Cookie: username=" + username) 
        print("Set-Cookie: password=" + password)

    print("Content-Type:text/html\r\n\r\n")
    print("<span class=\"spoilers\">")
    print(json_object)
    print("</span>")
    print("<div></div>")
    print("<b>QUERY_STRING: %s</b>" % envObjs["QUERY_STRING"]);

    print("<h1>POSTed Login Data</h1>")
    print("<p>" + "username: ", username, "password: ", password, "</p>")

    cookies = envObjs["HTTP_COOKIE"].split("; ")
    cookieDict = {}
    for cookie in cookies:
        if cookie == "": continue
        cookieDict[cookie.split("=")[0]] = cookie.split("=")[1]

    if ("password" in cookieDict and "username" in cookieDict and cookieDict["password"] == secret.password and cookieDict["username"] == secret.username):
        print(secret_page(cookieDict["username"], cookieDict["password"]))
    else:
        print(login_page())

if __name__ == "__main__":
    main()