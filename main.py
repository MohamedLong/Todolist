from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = "Secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/Todo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


# Creat the Database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


db.create_all()

# generate the form to be shown in the HTML


class Add(FlaskForm):
    title = StringField(label='Task Title', validators=[DataRequired()])
    task = StringField(label='Task Details', validators=[DataRequired()])

    submit = SubmitField(label="Submit")


@app.route('/', methods=['GET', 'POST'])
def home():
    list = db.session.query(Todo).all()
    add_form = Add()
    if add_form.validate_on_submit():

        upload = Todo(
            title=add_form.title.data,
            task=add_form.task.data,
            # completed=add_form.completed.data,
        )

        db.session.add(upload)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('index.html', add_form=add_form, list=list)


@app.route("/delete/<int:task_id>", methods=['POST', 'GET'])
def delete(task_id):
    db.session.query(Todo).filter_by(id=task_id).update({'deleted': True})
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/complete/<int:task_id>", methods=['POST', 'GET'])
def complete(task_id):
    db.session.query(Todo).filter_by(id=task_id).update({'completed': True})
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
