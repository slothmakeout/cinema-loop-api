from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    author = db.relationship('Account', backref=db.backref('posts', lazy=True))
    video = db.relationship('Video', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.id} by Author {self.author_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "video_id": self.video_id,
            "created_at": self.created_at.isoformat(),
            "title": self.title,
            "description": self.description
        }