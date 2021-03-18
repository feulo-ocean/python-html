from flask import Flask

app = Flask("microblog")


#aqui vai comentário
@app.route("/")
def index():
    return "Olá Mundo"

app.run()