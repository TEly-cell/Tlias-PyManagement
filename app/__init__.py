from . import games
from flask import Flask, jsonify, request
from datetime import datetime
from flask_login import login_required, current_user
from .db import db
from .models import Favorite, Material

from app.models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()

@app.route('/api/favorite/<int:material_id>', methods=['POST'])
@login_required
def toggle_favorite(material_id):
    # 检查资料是否存在
    material = Material.query.get_or_404(material_id)
    
    # 检查用户是否已收藏该资料
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        material_id=material_id
    ).first()
    
    if favorite:
        # 如果已收藏，则取消收藏
        db.session.delete(favorite)
        is_favorited = False
    else:
        # 如果未收藏，则添加收藏
        new_favorite = Favorite(
            user_id=current_user.id,
            material_id=material_id,
            created_at=datetime.utcnow()
        )
        db.session.add(new_favorite)
        is_favorited = True
    
    db.session.commit()
    return jsonify({
        'success': True,
        'favorited': is_favorited
    })