# app.py

from flask import Flask, render_template
import connexion

app = connexion.App(__name__, specification_dir="./")
app.add_api("flexpower_api_defn.yml")
#change to point at my yml file (call flexpower)


#connects the URL route "/" to the function home; process is called 'decorating'
@app.route("/")
def home():
    return render_template("home.html")
#render_template is a library function and home is a template page

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    #this is necessary because my Mac already uses the default port 5000 for airplay
