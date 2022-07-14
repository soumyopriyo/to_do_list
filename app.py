
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #SQLalchemy is use to  facilitates the communication between Python programs and databases
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'#/// is relative path and //// is absolut path
db=SQLAlchemy(app)
#******before creating db always start interactive python 3 shell as vsshell cannot parse python code******
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200), nullable=False) # we want the user to enter the name of the task, user st not leave it empty
    date_created=db.Column(db.DateTime,default=datetime.utcnow)# any time a new entrey is created the date it was created will automatially set the time it was created

    #fuction that return a str every time we create a element
    def __repr__(self):
        return '<Task %r>' % self.id #every time we create a element it will return a task and the id of the task



@app.route('/', methods=['POST','GET']) #by default it is GET but now we can do POST as well
# @ is telling Python to decorate the function index() with the decorator defined in app.route().
#  Basically, a decorator is a function that modifies the behaviour of another function.
def index():
    if request.method == 'POST':
        #return 'hello' #pass statement is used as a placeholder for future code. When the pass statement is executed, nothing happens, but 
                       #you avoid getting an error when empty code is not allowed. Empty code is not allowed in loops, function definitions, 
                       # class definitions, or in if statements.
        task_content= request.form['content']
        new_task=Todo(content=task_content)
        
        try:
            db.session.add(new_task) # adding to our db session
            db.session.commit()# commiting to the db
            return redirect('/')# redirect back to the index page
        except:
            return 'There was an issue adding the task'

    else:
        tasks=Todo.query.order_by(Todo.date_created).all()# it will look all the db contents and it will return the contents absed on the date it is created.
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')# int:id wil get the id of the task
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)# it will attempt to ge the task and if it does not ge tit it will 404
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a issue updating ur task'
    else:
        return render_template('update.html',task=task)

if __name__=="__main__":
    app.run(debug=True)