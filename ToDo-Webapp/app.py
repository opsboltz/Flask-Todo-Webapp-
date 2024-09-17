from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    # Encoding for the DB
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  # Fixed capitalization here
    complete = db.Column(db.Boolean)  # Fixed capitalization here


@app.route('/')
def index():
    # Show all todos
    todo_list = Todo.query.all()
    #Rendering the Tempalte as well as the Todo Varible
    return render_template('index.html', todo_list=todo_list)


@app.route("/add", methods=['POST'])
def add():
    #add new item
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    #Updating Item
    #Finding Todo_id
    todo = Todo.query.filter_by(id=todo_id).first()
    #Change to complete
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #Removeing Item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables within app context


    app.run(debug=True)
