#!/usr/bin/env python3

from flask import Flask, jsonify, render_template, request, redirect
from flask import url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    todo = db.Column(db.String(200), nullable=False, unique=True)

    def to_json(self):
        return {'id': self.id, 'todo': self.todo}

    def __repr__(self):
        return f'<Todo({self.id}) {self.todo}>'


@app.route("/light-theme")
def todo_app_light():
    return render_template("base.html", title="Todo App - light",
                           bg_img="images/bg-img.jpg",
                           body_color="bg-white",
                           container_color="bg-white",
                           input_text_color="text-black",
                           input_bg_color="bg-gray-200",
                           todo_text_color="text-black",
                           todo_bg_color="bg-gray-200",
                           todo_list=Todo.query.all())


@app.route("/")
def todo_home():
    return redirect(url_for("todo_app_light"))


@app.route("/dark-theme")
def todo_app_dark():
    return render_template("base.html", title="Todo App - dark",
                           bg_img="images/bg-img-dark.jpg",
                           body_color="bg-slate-950",
                           container_color="bg-slate-800",
                           input_text_color="text-gray-100",
                           input_bg_color="bg-slate-700",
                           todo_text_color="text-gray-300",
                           todo_bg_color="bg-slate-700")


@app.route("/api/todos", methods=["POST", "GET", "DELETE", "PUT"])
def add():
    match request.method:
        case "GET":
            return jsonify([todo.to_json() for todo in Todo.query.all()])
        case "POST":
            json_object = request.get_json()
            todo = Todo(todo=json_object['todo'])
            db.session.add(todo)
            db.session.commit()
            return jsonify(todo.to_json())
        case "PUT":
            json_object = request.get_json()
            new_todo = json_object['todo']
            id = json_object["id"]
            todo = Todo.query.get(id)
            if not todo:
                abort(404)
            todo.todo = new_todo
            db.session.commit()
            return jsonify(todo.to_json())
        case "DELETE":
            json_object = request.get_json()
            id = json_object["id"]
            todo = Todo.query.get(id)
            if not todo:
                abort(404)
            db.session.delete(todo)
            db.session.commit()
            return jsonify(todo.to_json())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # for i in Todos.query.all():
        #     db.session.delete(i)
        # db.session.commit()
    app.run(debug=True)
