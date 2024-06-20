from flask import Flask, render_template,request, redirect
from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy

# Saare css files and images static folder m hogi 
app = Flask(__name__, static_url_path='/static')

# For creating database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)   


# Yaha par todo ek table h 
class Todo(db.Model):
    # Taking serial number by default 
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now(timezone.utc))

    # To make table 
    # s1: In terminal (env) open puthon
    # s2: from app import app,db
    # s3: with app.app_context():
    # db.create_all()
    # use sqlite viewer to view db file  

    def __repr__(self):
            return f"{self.sno} - {self.title}"

 
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def hello_world():
    return redirect("/vikas")


@app.route('/vikas',methods=["GET","POST"])
def world():
    if(request.method=="POST"):
        titl =request.form["title"]
        des = request.form["desc"]
        todo  = Todo(title = titl,desc = des)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/vikas")


@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if(request.method=="POST"):
        titl =request.form["title"]
        des = request.form["desc"]
        # todo ka title wo rakha jo hame form se mila h 
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = titl
        todo.desc = des
        db.session.add(todo)
        db.session.commit()
        return redirect("/vikas")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)




if __name__ == '__main__':  
        app.run(debug=True)
