from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Video  # Убедитесь, что путь к модели Videos корректный

videos_bp = Blueprint("videos", __name__)


@videos_bp.route("/videos", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    videos_list = [video.to_dict() for video in videos]
    return jsonify(videos_list), 200


@videos_bp.route("/videos/<int:video_id>", methods=["GET"])
def get_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"msg": "Video not found"}), 404
    return jsonify(video.to_dict()), 200

@videos_bp.route('/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    # Находим видео по ID
    video = Video.query.get(video_id)
    if not video:
        # Видео не найдено, возвращаем ошибку 404
        return jsonify({"msg": "Video not found"}), 404
    
    # Видео найдено, удаляем его из базы данных
    db.session.delete(video)
    db.session.commit()

    # Возвращаем сообщение об успешном удалении
    return jsonify({"msg": "Video deleted successfully"}), 200

@videos_bp.route("/videos", methods=["POST"])
def add_video():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"msg": "Missing URL"}), 400

    new_video = Video(url=url)
    db.session.add(new_video)
    db.session.commit()

    return jsonify(new_video.to_dict()), 201
