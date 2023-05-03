from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Post, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'your-secret-key-goes-here'
# app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.template_folder = 'templates'

debug = DebugToolbarExtension(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    post = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("post/homepage.html", post=post)



@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


# User route

@app.route('/user')
def user_index():
    """Show a page with info on all users"""

    user = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user/index.html', user=user)


@app.route('/user/new', methods=["GET"])
def user_new_form():
    """Show a form to create a new user"""

    return render_template('user/new.html')


@app.route("/user/new", methods=["POST"])
def user_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/user")


@app.route('/user/<int:user_id>')
def user_show(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('user/show.html', user=user)


@app.route('/user/<int:user_id>/edit')
def user_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('user/edit.html', user=user)


@app.route('/user/<int:user_id>/edit', methods=["POST"])
def user_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/user")


@app.route('/user/<int:user_id>/delete', methods=["POST"])
def user_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/user")

# Posts route


@app.route('/user/<int:user_id>/post/new')
def post_new_form(user_id):
    """Show a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('post/new.html', user=user)


@app.route('/user/<int:user_id>/post/new', methods=["POST"])
def post_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/user/{user_id}")


@app.route('/post/<int:post_id>')
def post_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post/show.html', post=post)


@app.route('/post/<int:post_id>/edit')
def post_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post/edit.html', post=post)


@app.route('/post/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/user/{post.user_id}")


@app.route('/post/<int:post_id>/delete', methods=["POST"])
def post_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/user/{post.user_id}")

