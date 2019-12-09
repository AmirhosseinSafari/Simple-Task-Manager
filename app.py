from flask import Flask, render_template ,request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        
@app.route('/', methods=['POST','GET'])
def index():

    if(request.method == 'POST'):
        Task_Content = request.form['content']
        new_Task = Todo(content = Task_Content)

        try:
            db.session.add(new_Task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

        
    if(request.method == 'GET'): 

        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):

    Task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(Task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue removing your task'


@app.route('/update/<int:id>' , methods=['POST','GET'])
def update(id):

    Task_to_update = Todo.query.get_or_404(id)

    if(request.method == 'POST'):
        updated_task_content = request.form['content']
        Task_to_update.content = updated_task_content

        new_Task_To_Update = Todo(content = updated_task_content)

        try:
            db.session.add(new_Task_To_Update)
            db.session.delete(Task_to_update)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    
    if(request.method == 'GET'):
        return render_template('update.html', Task_to_update=Task_to_update)
      
        

if __name__ == "__main__":
    app.run(debug=True)