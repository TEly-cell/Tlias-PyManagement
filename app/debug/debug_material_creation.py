from app import app, db
from app import MaterialForm, Material, Course
from flask import request, session
from werkzeug.datastructures import FileStorage, MultiDict
import io
import os

# 模拟表单提交数据
form_data = {
    'title': '测试资料',
    'content': '这是测试内容',
    'url': 'https://example.com/video.mp4',
    'type': 'video',
    'duration': '30',
    'difficulty': '3',
    'tags': '测试,视频',
    'submit': '添加资料'
}

# 获取一个测试课程ID
with app.app_context():
    # 确保有一个测试课程
    test_course = Course.query.first()
    if not test_course:
        print('没有找到测试课程，创建一个新的...')
        from app import User
        test_user = User.query.first()
        if not test_user:
            print('错误: 没有找到用户，无法创建测试课程')
            exit(1)
        test_course = Course(name='测试课程', description='用于测试的课程', user_id=test_user.id)
        db.session.add(test_course)
        db.session.commit()
        print(f'已创建测试课程，ID: {test_course.id}')
    else:
        print(f'找到测试课程，ID: {test_course.id}')

    # 模拟请求上下文
    with app.test_request_context(f'/material/create/{test_course.id}', method='POST'):
        # 设置CSRF令牌
        session['csrf_token'] = 'test_csrf_token'
        form_data['csrf_token'] = 'test_csrf_token'

        # 设置表单数据为MultiDict
        request.form = MultiDict(form_data)
        # 模拟空文件上传
        request.files = MultiDict({'file_upload': FileStorage(stream=io.BytesIO(b''), filename='')})

        # 创建表单实例
        form = MaterialForm(csrf_enabled=False)  # 禁用CSRF验证以便测试
        print('表单验证结果:', form.validate())

        # 打印表单错误
        if not form.validate():
            print('表单错误:')
            for field, errors in form.errors.items():
                print(f'  {field}: {errors}')
        else:
            # 尝试创建资料
            try:
                new_material = Material(
                    title=form.title.data,
                    content=form.content.data,
                    url=form.url.data,
                    type=form.type.data,
                    duration=int(form.duration.data) if form.duration.data else None,
                    difficulty=int(form.difficulty.data),
                    tags=form.tags.data,
                    file_path=None,
                    course_id=test_course.id
                )
                db.session.add(new_material)
                db.session.commit()
                print(f'成功创建测试资料，ID: {new_material.id}')
            except Exception as e:
                print(f'创建资料时出错: {e}')
                db.session.rollback()