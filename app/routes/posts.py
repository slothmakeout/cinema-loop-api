from flask import Blueprint, jsonify, request
from app import db
from app.models import Post

posts_bp = Blueprint("posts", __name__)

# Получение всех постов
@posts_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    posts_list = [post.to_dict() for post in posts]
    return jsonify(posts_list), 200

# Получение поста по id
@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify(post.to_dict()), 200
    else:
        return jsonify({'msg': 'Post not found'}), 404


# Создание нового поста
@posts_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    author_id = data.get('author_id')
    video_id = data.get('video_id')
    title = data.get('title')
    description = data.get('description')

    if not author_id or not video_id:
        return jsonify({'msg': 'Missing author_id or video_id'}), 400

    new_post = Post(author_id=author_id, video_id=video_id, title=title, description=description)
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201


# Обновление поста по id
@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'msg': 'Post not found'}), 404

    post.title = data.get('title', post.title)
    post.description = data.get('description', post.description)
    db.session.commit()

    return jsonify(post.to_dict()), 200

# Удаление поста по id
@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': f'Post with id {post_id} was deleted.'}), 200
    else:
        return jsonify({'msg': 'Post not found'}), 404

# Получение всех постов пользователя по id
@posts_bp.route('/users/<int:author_id>/posts', methods=['GET'])
def get_posts_by_author(author_id):
    posts = Post.query.filter_by(author_id=author_id).all()
    if posts:
        posts_list = [post.to_dict() for post in posts]
        return jsonify(posts_list), 200
    else:
        return jsonify({'msg': 'No posts found for the given author'}), 404

# Получение всех постов, связанных с видео по id
@posts_bp.route('/videos/<int:video_id>/posts', methods=['GET'])
def get_posts_by_video(video_id):
    posts = Post.query.filter_by(video_id=video_id).all()
    if posts:
        posts_list = [post.to_dict() for post in posts]
        return jsonify(posts_list), 200
    else:
        return jsonify({'msg': 'No posts found for the given video'}), 404
      
# Поиск
@posts_bp.route('/posts/search', methods=['GET'])
def search_posts():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'msg': 'Missing or empty query parameter'}), 400

    # Ищем посты, где title или description содержат ключевые слова
    posts = Post.query.filter(
        (Post.title.ilike(f'%{query}%')) | (Post.description.ilike(f'%{query}%'))
    ).all()

    if posts:
        # Преобразуем найденные посты в словари
        posts_list = [post.to_dict() for post in posts]
        return jsonify(posts_list), 200
    else:
        return jsonify({'msg': 'No posts found matching the query'}), 404