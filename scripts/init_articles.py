#!/usr/bin/env python3
"""
初始化文章教程数据脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import ArticleTutorial, db
from datetime import datetime

def init_articles():
    """初始化文章教程数据"""
    
    # 示例文章数据
    articles_data = [
        {
            "title": "网络爬虫：Python数据采集与网页解析",
            "content": """
<h2>Python网络爬虫开发实战指南</h2>
<p>网络爬虫是一种自动化程序，用于从互联网上收集和提取数据。Python凭借其简洁的语法和丰富的库，成为爬虫开发的首选语言。</p>

<h3>核心爬虫库介绍</h3>
<ul>
<li><strong>Scrapy：</strong>功能强大的爬虫框架，支持分布式爬取和数据处理</li>
<li><strong>BeautifulSoup：</strong>HTML/XML解析库，轻松提取网页数据</li>
<li><strong>requests：</strong>简洁优雅的HTTP库，处理网络请求</li>
<li><strong>selenium：</strong>自动化测试工具，可处理JavaScript渲染的页面</li>
<li><strong>lxml：</strong>高性能XML和HTML解析器</li>
</ul>

<h3>快速入门示例</h3>
<ol>
<li>安装必要库: <code>pip install requests beautifulsoup4 lxml</code></li>
<li>基础爬虫示例:</li>
<pre><code>import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 提取所有链接
links = [a['href'] for a in soup.find_all('a', href=True)]
print(f'找到 {len(links)} 个链接')

# 提取文章标题
titles = soup.find_all('h1')
for title in titles:
    print(title.text.strip())</code></pre>
<li>Scrapy框架示例:</li>
<pre><code>import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blog'
    start_urls = ['https://example.com/blog']
    
    def parse(self, response):
        for article in response.css('article.post'):
            yield {
                'title': article.css('h2.title::text').get(),
                'author': article.css('span.author::text').get(),
                'date': article.css('span.date::text').get()
            }</code></pre>
</ol>

<h3>反爬虫策略应对</h3>
<ul>
<li><strong>设置合理延迟：</strong>time.sleep()避免请求过快</li>
<li><strong>使用代理IP：</strong>轮换IP地址防止封禁</li>
<li><strong>模拟浏览器行为：</strong>设置User-Agent和Headers</li>
<li><strong>处理验证码：</strong>使用OCR识别或手动处理</li>
</ul>

<h3>数据存储方案</h3>
<p>爬取的数据可以存储到多种格式：JSON文件、CSV文件、SQLite数据库、MySQL数据库、MongoDB等。根据数据规模和查询需求选择合适的存储方案。</p>

<h3>实战应用场景</h3>
<p>电商价格监控、新闻聚合、社交媒体数据收集、学术研究数据采集、竞品分析等。务必遵守robots.txt规则和相关法律法规。</p>
""",
            "summary": "全面介绍Python网络爬虫开发技术，从基础requests+BeautifulSoup到Scrapy框架，包含反爬虫策略和实战案例。",
            "author": "数据工程师",
            "category": "数据采集",
            "tags": "网络爬虫,Python,数据采集,网页解析,Scrapy",
            "difficulty_level": 3
        },
        {
            "title": "数据库：Python数据存储与管理",
            "content": """
<h2>Python数据库应用开发指南</h2>
<p>Python提供了丰富的数据库接口和ORM工具，简化数据存储与管理操作。</p>

<h3>核心数据库库与框架</h3>
<ul>
<li><strong>SQLAlchemy：</strong>强大的ORM框架，支持多种数据库后端</li>
<li><strong>psycopg2：</strong>PostgreSQL数据库适配器</li>
<li><strong>mysql-connector：</strong>MySQL官方Python驱动</li>
<li><strong>sqlite3：</strong>内置SQLite数据库模块</li>
<li><strong>Peewee：</strong>轻量级ORM框架，易于学习和使用</li>
</ul>

<h3>快速入门</h3>
<ol>
<li>安装核心库: <code>pip install sqlalchemy psycopg2-binary mysql-connector-python peewee</code></li>
<li>SQLAlchemy ORM示例:</li>
<pre><code>from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

engine = create_engine('sqlite:///mydb.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 添加数据
new_user = User(name='John', email='john@example.com')
session.add(new_user)
session.commit()

# 查询数据
users = session.query(User).all()
for user in users:
    print(user.name, user.email)</code></pre>
<li>原生SQL示例:</li>
<pre><code>import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')

# 插入数据
cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", ('Laptop', 999.99))
conn.commit()

# 查询数据
cursor.execute("SELECT * FROM products")
print(cursor.fetchall())

conn.close()</code></pre>
</ol>

<h3>应用场景</h3>
<p>企业应用数据存储、Web应用后端数据库、数据分析结果持久化、内容管理系统等领域。</p>
""",
            "summary": "介绍Python在数据库开发中的应用，包括SQLAlchemy、psycopg2、mysql-connector、sqlite3和Peewee等核心库的使用。",
            "author": "数据库专家",
            "category": "数据存储",
            "tags": "数据库,Python,SQLAlchemy,ORM,MySQL,PostgreSQL",
            "difficulty_level": 2
        },
        {
            "title": "学习资料管理最佳实践",
            "content": """
<h2>高效管理学习资料的系统化方法</h2>
<p>有效的学习资料管理是提高学习效率的关键。通过系统化的方法，可以更好地组织、查找和利用学习资源。</p>

<h3>资料分类策略</h3>
<ul>
<li><strong>按主题分类：</strong>将相似主题的内容归类存放</li>
<li><strong>按难度分级：</strong>使用1-5级难度标签标记内容复杂度</li>
<li><strong>按学习阶段：</strong>基础、进阶、高级、专家四个阶段</li>
<li><strong>按内容类型：</strong>视频、文档、代码示例、练习题等</li>
</ul>

<h3>质量控制标准</h3>
<ol>
<li><strong>内容准确性：</strong>确保信息来源可靠，内容准确无误</li>
<li><strong>时效性检查：</strong>定期更新过时内容，标记废弃资源</li>
<li><strong>实用性评估：</strong>优先保留可直接应用的知识</li>
<li><strong>完整性验证：</strong>确保每个主题都有完整的知识体系</li>
</ol>

<h3>定期维护流程</h3>
<ul>
<li><strong>每月审查：</strong>检查新增内容的质量和相关性</li>
<li><strong>季度整理：</strong>重新评估分类体系，调整标签</li>
<li><strong>年度清理：</strong>删除过时或低质量的内容</li>
<li><strong>用户反馈：</strong>收集使用者的改进建议</li>
</ul>

<h3>工具使用技巧</h3>
<p>充分利用Tlias的标签系统、搜索功能和进度跟踪，建立个人知识库。建议为重要内容添加详细备注，记录学习心得。</p>

<h3>协作分享建议</h3>
<p>在团队学习中，建立共享的资料库，制定统一的命名规范，定期交流使用心得，共同维护内容质量。</p>
""",
            "summary": "分享学习资料管理的最佳实践，包括分类策略、质量控制和定期维护的建议。",
            "author": "内容管理专家",
            "category": "最佳实践",
            "tags": "资料管理,内容优化,学习策略",
            "difficulty_level": 2
        },
        {
            "title": "利用学习统计提升效率",
            "content": """
<h2>数据驱动的学习优化</h2>
<p>通过分析学习统计数据，可以发现学习模式，优化学习策略，提高效率。</p>

<h3>关键指标解读</h3>
<ul>
<li><strong>完成率：</strong>反映学习进度和坚持程度</li>
<li><strong>学习时间：</strong>显示学习投入的时间分布</li>
<li><strong>活跃时段：</strong>找出最佳学习时间</li>
<li><strong>内容偏好：</strong>了解哪些类型的内容更受欢迎</li>
</ul>

<h3>分析技巧</h3>
<ol>
<li><strong>定期回顾：</strong>每周查看学习统计</li>
<li><strong>识别模式：</strong>找出高效学习的时间段</li>
<li><strong>调整策略：</strong>根据数据调整学习计划</li>
<li><strong>设定目标：</strong>基于数据设定合理的学习目标</li>
</ol>

<h3>实际案例</h3>
<p>通过分析发现，大多数用户在晚上8-10点学习效率最高，可以重点安排这个时间段学习难度较高的内容。</p>

<h3>进阶应用</h3>
<p>结合学习偏好和进度数据，系统可以智能推荐最适合的学习内容和时间安排。</p>
""",
            "summary": "介绍如何利用学习统计数据优化学习策略，提高学习效率和效果。",
            "author": "数据分析师",
            "category": "进阶技巧",
            "tags": "数据分析,效率优化,学习策略",
            "difficulty_level": 3
        },
        {
            "title": "新手常见错误及解决方案",
            "content": """
<h2>避免学习管理中的常见陷阱</h2>
<p>新手在使用学习管理系统时经常会遇到一些典型问题，本文总结了解决方案。</p>

<h3>常见错误类型</h3>
<ul>
<li><strong>内容过载：</strong>一次性添加过多学习资料</li>
<li><strong>缺乏规划：</strong>没有明确的学习路径和目标</li>
<li><strong>忽视复习：</strong>只关注新内容，忽略复习旧知识</li>
<li><strong>难度不匹配：</strong>选择过于简单或过于困难的内容</li>
</ul>

<h3>解决方案</h3>
<ol>
<li><strong>分阶段学习：</strong>将大目标分解为小任务</li>
<li><strong>制定计划：</strong>为每个课程设定明确的时间表</li>
<li><strong>定期复习：</strong>设置复习提醒，巩固已学知识</li>
<li><strong>难度适配：</strong>根据学习进度调整内容难度</li>
</ol>

<h3>最佳实践建议</h3>
<p>建议采用"少量多次"的学习策略，每次学习时间控制在30-45分钟，中间安排适当休息。</p>

<h3>工具使用技巧</h3>
<p>充分利用Tlias的提醒功能和进度跟踪，确保学习计划得到有效执行。</p>
""",
            "summary": "总结新手在使用学习管理系统时的常见错误，并提供实用的解决方案和最佳实践。",
            "author": "学习顾问",
            "category": "案例分析",
            "tags": "新手指导,问题解决,最佳实践",
            "difficulty_level": 1
        },
        {
            "title": "高级学习策略与技巧",
            "content": """
<h2>掌握高级学习技巧</h2>
<p>对于有一定基础的学习者，掌握高级策略可以进一步提升学习效果。</p>

<h3>深度学习策略</h3>
<ul>
<li><strong>费曼技巧：</strong>通过教授他人来检验理解程度</li>
<li><strong>间隔重复：</strong>利用记忆曲线安排复习时间</li>
<li><strong>主动回忆：</strong>不依赖提示，主动回忆所学内容</li>
<li><strong>交叉学习：</strong>混合不同类型的问题和主题</li>
</ul>

<h3>内容创作技巧</h3>
<ol>
<li><strong>创建思维导图：</strong>可视化知识结构</li>
<li><strong>制作学习卡片：</strong>便于随时复习</li>
<li><strong>录制学习笔记：</strong>通过讲解加深理解</li>
<li><strong>建立知识连接：</strong>将新知识与已有知识关联</li>
</ol>

<h3>时间管理</h3>
<p>采用番茄工作法，25分钟专注学习，5分钟休息，每4个番茄钟后长休息。</p>

<h3>学习社区参与</h3>
<p>积极参与讨论区，与其他学习者交流，分享经验和见解。</p>

<h3>持续改进</h3>
<p>定期评估学习效果，根据反馈调整策略，形成个性化的学习方法。</p>
""",
            "summary": "为进阶学习者提供高级学习策略和技巧，包括深度学习方法和个性化学习体系建设。",
            "author": "学习方法专家",
            "category": "进阶技巧",
            "tags": "高级策略,深度学习,时间管理",
            "difficulty_level": 4
        },
        {
            "title": "Django使用指南",
            "content": """
<h2>Django框架入门到精通</h2>
<p>Django是一个高级Python Web框架，遵循MTV架构，内置了许多实用功能。</p>

<h3>核心组件</h3>
<ul>
<li><strong>模型(Model)：</strong>处理数据存储和数据库交互</li>
<li><strong>视图(View)：</strong>处理用户请求和业务逻辑</li>
<li><strong>模板(Template)：</strong>生成HTML响应</li>
<li><strong>URL配置：</strong>路由管理</li>
<li><strong>表单：</strong>数据验证和处理</li>
</ul>

<h3>快速开始</h3>
<ol>
<li>安装Django: <code>pip install django</code></li>
<li>创建项目: <code>django-admin startproject myproject</code></li>
<li>创建应用: <code>python manage.py startapp myapp</code></li>
<li>定义模型并迁移数据库</li>
<li>编写视图和模板</li>
<li>配置URL并运行服务器</li>
</ol>

<h3>最佳实践</h3>
<p>使用Django REST framework构建API，利用中间件处理跨域请求，采用Celery处理异步任务。</p>
""",
            "summary": "全面介绍Django框架的核心概念、使用方法和最佳实践，适合Web开发初学者到中级开发者。",
            "author": "技术文档团队",
            "category": "后端开发",
            "tags": "Django,Python,Web开发,后端框架",
            "difficulty_level": 3,
            "is_public": True
        },
        {
            "title": "Flask教程：轻量级Web框架入门",
            "content": """
<h2>Flask轻量级Web框架详解</h2>
<p>Flask是一个使用Python编写的轻量级Web应用框架，以简洁灵活著称，非常适合小型项目和API开发。</p>

<h3>核心特性</h3>
<ul>
<li><strong>路由系统：</strong>简洁的URL映射</li>
<li><strong>模板引擎：</strong>使用Jinja2渲染HTML</li>
<li><strong>请求处理：</strong>简单的请求和响应管理</li>
<li><strong>扩展生态：</strong>丰富的第三方扩展</li>
<li><strong>轻量级设计：</strong>无固定依赖，按需扩展</li>
</ul>

<h3>快速入门</h3>
<ol>
<li>安装Flask: <code>pip install flask</code></li>
<li>创建基本应用:</li>
<pre><code>from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True)</code></pre>
<li>运行应用: <code>python app.py</code></li>
<li>访问 http://localhost:5000</li>
</ol>

<h3>进阶应用</h3>
<p>使用Flask-SQLAlchemy进行数据库操作，Flask-RESTful构建API，Flask-Login实现用户认证，打造功能完善的Web应用。</p>
""",
            "summary": "从零开始学习Flask框架，掌握路由配置、模板渲染和扩展使用，适合Python开发者快速构建Web应用。",
            "author": "技术文档团队",
            "category": "后端开发",
            "tags": "Flask,Python,Web开发,轻量级框架",
            "difficulty_level": 2,
            "is_public": True
        },
        {
            "title": "Vue使用方法详解",
            "content": """
<h2>Vue.js前端框架实战指南</h2>
<p>Vue是一套用于构建用户界面的渐进式JavaScript框架，核心专注于视图层。</p>

<h3>核心概念</h3>
<ul>
<li><strong>响应式数据绑定：</strong>数据驱动视图更新</li>
<li><strong>组件化开发：</strong>复用UI组件</li>
<li><strong>虚拟DOM：</strong>提升渲染性能</li>
<li><strong>指令系统：</strong>简化DOM操作</li>
<li><strong>生命周期：</strong>控制组件创建到销毁的过程</li>
</ul>

<h3>快速入门</h3>
<ol>
<li>安装Vue: <code>npm install vue</code></li>
<li>创建Vue实例:</li>
<pre><code>const app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
})</code></pre>
<li>在HTML中使用:</li>
<pre><code>&lt;div id="app"&gt;
  {{ message }}
&lt;/div&gt;</code></pre>
<li>运行应用并查看结果</li>
</ol>

<h3>进阶技巧</h3>
<p>使用Vue Router实现路由管理，Vuex进行状态管理，Vue CLI搭建项目，结合Element UI等组件库快速开发企业级应用。</p>
""",
            "summary": "全面介绍Vue.js前端框架的核心概念、使用方法和进阶技巧，适合前端开发初学者到中级开发者。",
            "author": "技术文档团队",
            "category": "前端开发",
            "tags": "Vue,JavaScript,前端开发,Web框架",
            "difficulty_level": 3,
            "is_public": True
        },
        {
            "title": "HTTP协议详解",
            "content": """
<h2>HTTP协议基础与实践</h2>
<p>HTTP（超文本传输协议）是用于传输超媒体文档（如HTML）的应用层协议，是Web的基础。</p>

<h3>核心概念</h3>
<ul>
<li><strong>请求-响应模型：</strong>客户端发送请求，服务器返回响应</li>
<li><strong>无状态：</strong>服务器不保留客户端状态</li>
<li><strong>方法：</strong>GET、POST、PUT、DELETE等</li>
<li><strong>状态码：</strong>表示请求处理结果（200、404、500等）</li>
<li><strong>头部：</strong>传递附加信息（Content-Type、Authorization等）</li>
</ul>

<h3>请求结构</h3>
<pre><code>GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html</code></pre>

<h3>响应结构</h3>
<pre><code>HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 123

&lt;html&gt;&lt;body&gt;Hello World&lt;/body&gt;&lt;/html&gt;</code></pre>

<h3>进阶主题</h3>
<p>了解HTTPS加密原理，HTTP/2的多路复用，RESTful API设计规范，以及常见的安全问题如CSRF、XSS防护。</p>
""",
            "summary": "详细讲解HTTP协议的基础概念、请求响应结构和进阶主题，帮助开发者深入理解Web通信原理。",
            "author": "技术文档团队",
            "category": "网络基础",
            "tags": "HTTP,网络协议,Web基础,通信原理",
            "difficulty_level": 2,
            "is_public": True
        }
    ]
    
    # 创建数据库表
    db.create_all()
    
    # 添加文章
    for article_data in articles_data:
        # 检查是否已存在相同标题的文章
        existing_article = ArticleTutorial.query.filter_by(title=article_data["title"]).first()
        if not existing_article:
            article = ArticleTutorial(
                title=article_data["title"],
                content=article_data["content"],
                summary=article_data["summary"],
                author=article_data["author"],
                category=article_data["category"],
                tags=article_data["tags"],
                difficulty_level=article_data["difficulty_level"],
                is_public=article_data.get("is_public", True)
            )
            db.session.add(article)
            print(f"添加文章: {article_data['title']}")
        else:
            print(f"文章已存在，跳过: {article_data['title']}")
    
    db.session.commit()
    print("✅ 文章教程数据初始化完成！")

if __name__ == "__main__":
    from run import app
    with app.app_context():
        init_articles()