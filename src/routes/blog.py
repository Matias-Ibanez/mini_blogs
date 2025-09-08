from flask import render_template, Blueprint, redirect, url_for
from src.forms import BlogForm
from src.models import BlogPost, db

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('index.html')


@blog.route('/add', methods=['GET', 'POST'])
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
    return render_template('index.html')
