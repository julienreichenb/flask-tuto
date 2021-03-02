from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from blog import db
from blog.models import User, BlogPost
from blog.posts.forms import BlogPostForm

posts = Blueprint('posts', __name__)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogPostForm()

    if form.validate_on_submit():
        post = BlogPost(title=form.title.data,
                        text=form.text.data,
                        user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Blog post created.')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


@posts.route('/<int:id>')
def post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post.html', post=post)


@posts.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = BlogPost.query.get_or_404(id)
    if post.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Blog post edited.')
        return redirect(url_for('posts.post', id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text

    return render_template('create_post.html', title='Editing your post', form=form)


@posts.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = BlogPost.query.get_or_404(id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted.')

    return redirect(url_for('core.index'))

