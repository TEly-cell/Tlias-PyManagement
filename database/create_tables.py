#!/usr/bin/env python3
"""
创建数据库表并初始化文章数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app
from app.models import db, ArticleTutorial
from datetime import datetime

def create_tables_and_init_data():
    """创建表并初始化数据"""
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✅ 数据库表创建完成")
        
        # 检查是否已有数据
        if ArticleTutorial.query.count() > 0:
            print("ℹ️  文章数据已存在，跳过初始化")
            return
        
        # 示例文章数据
        articles_data = [
            {
                "title": "Tlias智能学习系统使用指南",
                "content": """
<h2>欢迎使用Tlias智能学习系统</h2>
<p>Tlias是一个专为学习者设计的智能学习管理系统，帮助您更高效地组织和管理学习内容。</p>

<h3>核心功能介绍</h3>
<ul>
<li><strong>课程管理：</strong>创建和管理您的学习课程</li>
<li><strong>学习资料：</strong>上传和组织各类学习资料</li>
<li><strong>进度跟踪：</strong>实时记录和查看学习进度</li>
<li><strong>智能推荐：</strong>基于学习偏好推荐相关内容</li>
<li><strong>学习统计：</strong>详细的学习数据分析和报告</li>
</ul>

<h3>快速开始</h3>
<ol>
<li>注册并登录您的账号</li>
<li>在仪表板创建新的学习课程</li>
<li>为课程添加学习资料</li>
<li>开始学习并跟踪进度</li>
</ol>
""",
                "summary": "全面介绍Tlias智能学习系统的功能和使用方法，帮助新用户快速上手。",
                "author": "Tlias团队",
                "category": "入门指南",
                "tags": "新手入门,系统介绍,快速上手",
                "difficulty_level": 1
            },
            {
                "title": "如何高效创建学习课程",
                "content": """
<h2>创建高效学习课程的关键要素</h2>
<p>一个好的学习课程应该结构清晰、目标明确，并且能够激发学习兴趣。</p>

<h3>课程设计原则</h3>
<ul>
<li><strong>明确学习目标：</strong>每门课程都应该有清晰的学习目标</li>
<li><strong>合理的内容结构：</strong>从基础到进阶，循序渐进</li>
<li><strong>多样化的资料类型：</strong>结合文本、视频、测验等多种形式</li>
<li><strong>适当的难度梯度：</strong>既要有挑战性，又不能过于困难</li>
</ul>

<h3>实用技巧</h3>
<ol>
<li><strong>使用描述性标题：</strong>让学习者一眼就能看出课程内容</li>
<li><strong>添加详细描述：</strong>说明课程的学习目标和预期收获</li>
<li><strong>合理设置标签：</strong>便于分类和检索</li>
<li><strong>定期更新内容：</strong>保持课程的新鲜度和实用性</li>
</ol>
""",
                "summary": "详细介绍如何创建结构清晰、内容丰富的学习课程，提供实用的设计原则和技巧。",
                "author": "教育专家",
                "category": "进阶技巧",
                "tags": "课程设计,教学技巧,内容组织",
                "difficulty_level": 2
            },
            {
                "title": "学习资料最佳实践",
                "content": """
<h2>优化您的学习资料管理</h2>
<p>有效的学习资料管理是提高学习效率的关键。本文将分享一些最佳实践。</p>

<h3>资料分类策略</h3>
<ul>
<li><strong>按类型分类：</strong>文档、视频、音频、测验等</li>
<li><strong>按难度分级：</strong>入门、初级、中级、高级</li>
<li><strong>按标签组织：</strong>使用关键词便于检索</li>
<li><strong>按时间排序：</strong>最新的内容放在前面</li>
</ul>

<h3>内容质量控制</h3>
<ol>
<li><strong>内容准确性：</strong>确保所有信息都是准确和最新的</li>
<li><strong>格式一致性：</strong>保持统一的格式和风格</li>
<li><strong>适当的深度：</strong>根据目标受众调整内容深度</li>
<li><strong>互动元素：</strong>添加测验和练习增强参与度</li>
</ol>
""",
                "summary": "分享学习资料管理的最佳实践，包括分类策略、质量控制和定期维护的建议。",
                "author": "内容管理专家",
                "category": "最佳实践",
                "tags": "资料管理,内容优化,学习策略",
                "difficulty_level": 2
            }
        ]
        
        # 添加文章
        for article_data in articles_data:
            article = ArticleTutorial(
                title=article_data["title"],
                content=article_data["content"],
                summary=article_data["summary"],
                author=article_data["author"],
                category=article_data["category"],
                tags=article_data["tags"],
                difficulty_level=article_data["difficulty_level"],
                is_public=True
            )
            db.session.add(article)
        
        db.session.commit()
        print("✅ 文章教程数据初始化完成！")

if __name__ == "__main__":
    create_tables_and_init_data()