from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
db = SQLAlchemy(app)

class Kanban(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200))
    status = db.Column(db.Integer)

@app.route("/")
def index():
    todos = Kanban.query.filter_by(status=0)
    doing = Kanban.query.filter_by(status=1)
    done = Kanban.query.filter_by(status=2)
    return render_template("index.html", todos=todos, doing=doing, done=done)

@app.route("/add", methods = ["POST"])
def add():
    todo = Kanban(text=request.form['todoitem'], status=0)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/todo/<id>")
def todo(id):
    todo = Kanban.query.filter_by(id=int(id)).first()
    todo.status = 0
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/doing/<id>")
def doing(id):
    doing = Kanban.query.filter_by(id=int(id)).first()
    doing.status = 1
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/done/<id>")
def done(id):
    done = Kanban.query.filter_by(id=int(id)).first()
    done.status = 2
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/remove/<id>")
def remove(id):
    remove = Kanban.query.filter_by(id=int(id)).first()
    db.session.delete(remove)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
