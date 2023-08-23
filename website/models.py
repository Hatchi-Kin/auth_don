from sqlalchemy.sql import func
import bcrypt


from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self,username,text):
        self.username = username
        self.text = text

    def get_last_ten_posts():
        last_ten = Post.query.order_by(Post.id.desc()).limit(10).all()
        return last_ten



class HugPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_human = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self,is_human,username,text):
        self.is_human = is_human
        self.username = username
        self.text = text

    def get_last_ten_hugs():
        last_ten = HugPost.query.order_by(HugPost.id.desc()).limit(10).all()
        return last_ten
    


class BadWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)


    def get_random_bad_word():
        random_bad_word = BadWords.query.order_by(func.random()).first()
        word = random_bad_word.word
        definition = random_bad_word.definition
        return [word,definition]
    
