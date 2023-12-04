#Razvan Rotundu 2022
#Simple website which generates names

from flask import Flask, render_template, request

#the name generation functions
from markovNames.nameWriter import makeName

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/generate", methods=["GET","POST"])
def generate():
    #If a form is submitted
    #if request.method == "POST":
        mode = request.form.get("gender")
        if mode == 'girl':
            input = 'FNtriple'
        if mode == 'boy':
            input = 'MNtriple'
        #check for boy

        #generate 5 names of the chosen type
        nameslist = []
        for i in range(5):
            name = makeName(input)

        #capitalize first letter
            name =list(name)
            name[0] = name[0].upper()
            name = "".join(name)

            nameslist.append(name)

        #return the generated template with the list
        return render_template("generated.html", list=nameslist)







