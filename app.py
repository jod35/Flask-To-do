from flask import Flask,render_template,redirect,request
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
import os



app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(app.root_path
,'todos.db')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False



db=SQLAlchemy(app)

fa=FontAwesome(app)


"""
Task
- id :int
- name : str
- complete :bool
"""

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    complete=db.Column(db.Boolean,default=False)


    def __repr__(self):
        return f'<Task {self.name}>'



@app.route('/')
def index():

    tasks=Task.query.order_by(Task.id.desc()).all()
    complete_tasks=Task.query.filter_by(complete=True).count()
    return render_template('index.html',tasks=tasks,complete_tasks=complete_tasks)


@app.route('/add',methods=["POST"])
def create_task():
    task=request.form.get('task')

    new_task=Task(name=task)

    db.session.add(new_task)

    db.session.commit()

    return redirect('/')


@app.route('/complete/<int:id>/')
def complete_task(id):
    task_to_update=Task.query.get(id)

    task_to_update.complete=True

    db.session.commit()

    return redirect('/')


@app.route('/delete/<int:id>/')
def delete_task(id):
    task_to_delete=Task.query.get(id)

    db.session.delete(task_to_delete)

    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)