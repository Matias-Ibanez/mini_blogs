from flask import Flask
from src.routes.blog import blog
from src.models import db

app = Flask(__name__)
app.register_blueprint(blog)
app.config['SECRET_KEY'] = 'tu_clave_secreta_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
