from flask import Flask
from src.routes.blog import blog
from src.models import db, User
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.register_blueprint(blog)
app.config['SECRET_KEY'] = 'tu_clave_secreta_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
