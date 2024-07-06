from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Practice(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
        # return super().__repr__()

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # print('post req',request.form['title','desc'])
        # print('post req',title,desc)

        todo = Practice(title=title, desc=desc)
        # todo = Practice(title="First Todo", desc="Start Learning flask")
        db.session.add(todo)
        db.session.commit()
    todo = Practice.query.all()
    return render_template('index.html', todo=todo)
    # return 'Hello, World!'

@app.route('/a')
def hello_worldd():
    todo = Practice.query.all()
    print(todo)
    return render_template('index.html', todo=todo)
    # return 'Hey, Fahad!'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Practice.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    # print(todo)
    # return render_template('index.html', todo=todo)
    # return 'Hey, Fahad!'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Practice.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')
    
    todo = Practice.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    # print(todo)
    # return render_template('index.html', todo=todo)
    # return 'Hey, Fahad!'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)