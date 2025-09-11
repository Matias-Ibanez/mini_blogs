from flask import render_template, Blueprint, redirect, url_for, request, flash
from src.forms import BlogForm, RegisterForm, LoginForm
from src.models import BlogPost, User, db
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('index.html')


@blog.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("Ya te registraste con ese correo, iniciá sesión en su lugar.")
            return redirect(url_for('blog.login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('blog.index'))

    return render_template("register.html", form=form)


@blog.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))

        user = result.scalar()

        if not user:
            flash("Ese correo no existe, por favor intentá de nuevo.")
            return redirect(url_for('blog.login'))

        elif not check_password_hash(user.password, password):
            flash('Contraseña incorrecta, por favor intentá de nuevo.')
            return redirect(url_for('blog.login'))
        else:
            login_user(user)
            return redirect(url_for('blog.index'))

    return render_template("login.html", form=form)


@blog.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        name = form.name.data
        image_url = form.image_url.data
        content = form.content.data

        new_post = BlogPost(title=title, subtitle=subtitle, author=name, img_url=image_url, body=content)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('blog.index'))

    return render_template('add.html', form=form)


@blog.route('/blogs', methods=['GET', 'POST'])
@login_required
def blogs():
    blogs = [blog.to_dict() for blog in db.session.query(BlogPost).all()]
    return render_template('blogs.html', blogs=blogs)


@blog.route('/blog_post/<int:id>', methods=['GET', 'POST'])
def blog_post(id):
    print(id)
    blog_content = db.session.query(BlogPost).filter(BlogPost.id == id).first()
    return render_template('blog.html', blog_content=blog_content)


@blog.route('/remove/<int:id>', methods=['GET', 'POST'])
def remove(id):
    blog_content = db.session.query(BlogPost).filter(BlogPost.id == id).first()
    db.session.delete(blog_content)
    db.session.commit()
    return redirect(url_for('index.html'))
