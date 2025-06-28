from flask import Flask, request
from caesar import rotate_string

app = Flask(__name__)
app.config['DEBUG']=True

form = """
<!DOCTYPE html>

<html>
    <head>
        <style>
            form {{
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }}
            textarea {{
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }}
        </style>
    </head>
    <body>
      
<form method="post" action="/caesar">
    <label for='message'>Rotate by:</label>
        <input type="text" name="rot" value="0">
        <br>
        <br>
    <textarea name="text">{0}</textarea>
        <br>
    <input type="submit">
</form>

    </body>
</html>
"""

@app.route("/caesar", methods=["POST", "GET"])
def encrypt():
    v_message = request.form['text']
    v_rot = request.form['rot']
    encrypted_message = rotate_string(v_message, int(v_rot))
    return form.format(encrypted_message)
 
@app.route("/", methods=["POST", "GET"])
def index():
    return form.format("")

app.run()