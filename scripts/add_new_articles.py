#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加新文章到数据库的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models import ArticleTutorial
from app.models import ArticleTutorial

def add_new_articles():
    """添加新文章到数据库"""
    
    app = create_app()
    with app.app_context():
        
        # 创建数据库表
        db.create_all()
        
        # 定义新文章数据
        new_articles = [
            {
                "title": "Pygame游戏开发: 从零开始构建2D游戏",
                "content": '''
<h2>Pygame: Python游戏开发的强大引擎</h2>
<p>Pygame是一个基于SDL库的Python游戏开发框架,提供了丰富的功能用于创建2D游戏,包括图形渲染,音频处理,输入管理,碰撞检测等核心游戏开发功能.</p>

<h3>核心功能与优势</h3>
<ul>
<li><strong>跨平台支持:</strong>Windows,macOS,Linux全平台兼容</li>
<li><strong>硬件加速:</strong>OpenGL加速的图形渲染</li>
<li><strong>音频系统:</strong>多声道音频播放和音效处理</li>
<li><strong>输入管理:</strong>键盘,鼠标,手柄等输入设备支持</li>
<li><strong>精灵系统:</strong>高效的2D精灵和动画管理</li>
</ul>

<h3>基础游戏框架</h3>
<pre><code>import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("我的游戏")
        self.clock = pygame.time.Clock()
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        # 游戏逻辑更新
        pass
    
    def draw(self):
        self.screen.fill((0, 0, 0))  # 黑色背景
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
</code></pre>

<h3>精灵和动画系统</h3>
<pre><code>class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        
        self.rect.x += self.velocity.x
        
        # 边界检测
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

# 使用精灵组
all_sprites = pygame.sprite.Group()
player = Player(400, 300)
all_sprites.add(player)
</code></pre>

<h3>碰撞检测和物理系统</h3>
<pre><code>class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1
    
    def update(self):
        self.rect.x += self.direction * 2
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

# 碰撞检测
enemies = pygame.sprite.Group()
enemy = Enemy(200, 200)
enemies.add(enemy)

# 在主循环中检测碰撞
hits = pygame.sprite.spritecollide(player, enemies, True)
if hits:
    print("玩家被击中!")
</code></pre>

<h3>音频和音效系统</h3>
<pre><code># 加载音效
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

# 播放音效
shoot_sound.play()

# 背景音乐
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # 循环播放
pygame.mixer.music.set_volume(0.5)
</code></pre>

<h3>游戏状态管理</h3>
<pre><code>class GameState:
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

class Game:
    def __init__(self):
        self.state = GameState.MENU
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == GameState.MENU:
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_p and self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
    
    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_pause()
</code></pre>

<h3>实用开发工具</h3>
<ul>
<li><strong>Tile地图编辑器:</strong>Tiled地图编辑工具集成</li>
<li><strong>精灵图集:</strong>TexturePacker资源优化</li>
<li><strong>字体渲染:</strong>pygame.font和自定义字体</li>
<li><strong>调试工具:</strong>FPS计数器和性能监控</li>
<li><strong>打包发布:</strong>PyInstaller打包成可执行文件</li>
</ul>

<h3>性能优化技巧</h3>
<ul>
<li><strong>脏矩形更新:</strong>只更新变化的屏幕区域</li>
<li><strong>精灵池:</strong>对象重用减少内存分配</li>
<li><strong>双缓冲:</strong>减少屏幕闪烁</li>
<li><strong>帧率控制:</strong>稳定的游戏循环</li>
</ul>

<h3>实际项目案例</h3>
<pre><code>class EducationalGame(Game):
    def __init__(self):
        super().__init__()
        self.questions = ["2+2=", "3*4=", "10-7="]
        self.answers = [4, 12, 3]
        self.current_question = 0
        self.score = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    answer = int(event.unicode)
                    if answer == self.answers[self.current_question]:
                        self.score += 10
                        print("正确!")
                    else:
                        print("错误!")
                    self.current_question = (self.current_question + 1) % len(self.questions)
</code></pre>
''',
                "summary": "全面介绍Pygame游戏开发框架,涵盖基础游戏架构,精灵系统,碰撞检测,音频处理,状态管理,以及教育游戏开发实例.",
                "author": "游戏开发工程师王强",
                "category": "精选",
                "tags": "Pygame,游戏开发,2D游戏,Python,游戏引擎,精灵动画",
                "difficulty_level": 2,
                "is_public": True
            },
            {
                "title": "Google Translate API集成: 构建多语言应用的完整方案",
                "content": '''
<h2>Google Translate API: 全球化的语言桥梁</h2>
<p>Google Translate API是一个强大的云端翻译服务,支持100多种语言的实时翻译,提供了RESTful API接口,可以轻松集成到各种应用中,实现网站国际化,移动应用本地化,以及企业级多语言解决方案.</p>

<h3>核心功能与优势</h3>
<ul>
<li><strong>广泛语言支持:</strong>支持100多种语言的互译</li>
<li><strong>实时翻译:</strong>毫秒级响应的云端翻译服务</li>
<li><strong>上下文感知:</strong>基于神经网络的智能翻译</li>
<li><strong>批量处理:</strong>支持大量文本的批量翻译</li>
<li><strong>格式保持:</strong>保持HTML,XML等格式的完整性</li>
</ul>

<h3>Python集成方案</h3>
<pre><code>from google.cloud import translate_v2 as translate
import os

# 设置认证
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-key.json'

class GoogleTranslator:
    def __init__(self):
        self.client = translate.Client()
    
    def detect_language(self, text):
        """检测文本语言"""
        result = self.client.detect_language(text)
        return {
            'language': result['language'],
            'confidence': result['confidence']
        }
    
    def translate_text(self, text, target_language='zh'):
        """翻译文本"""
        result = self.client.translate(
            text, 
            target_language=target_language,
            format_='text'
        )
        return {
            'original_text': result['input'],
            'translated_text': result['translatedText'],
            'detected_language': result['detectedSourceLanguage']
        }
    
    def translate_html(self, html_content, target_language='zh'):
        """翻译HTML内容"""
        result = self.client.translate(
            html_content,
            target_language=target_language,
            format_='html'
        )
        return result['translatedText']

# 使用示例
translator = GoogleTranslator()

# 检测语言
result = translator.detect_language("Hello, world!")
print(f"检测到的语言: {result['language']}, 置信度: {result['confidence']}")

# 翻译文本
translation = translator.translate_text("Hello, world!", target_language='zh')
print(f"翻译结果: {translation['translated_text']}")
</code></pre>

<h3>高级翻译特性</h3>
<pre><code>class AdvancedTranslator:
    def __init__(self):
        self.client = translate.Client()
    
    def batch_translate(self, texts, target_language='zh'):
        """批量翻译"""
        results = self.client.translate(
            texts,
            target_language=target_language
        )
        return [
            {
                'original': result['input'],
                'translated': result['translatedText'],
                'source_language': result['detectedSourceLanguage']
            },
            for result in results
        ]
    
    def translate_with_glossary(self, text, glossary_terms, target_language='zh'):
        """使用术语表翻译"""
        # 创建术语映射
        glossary_map = {term: translation for term, translation in glossary_terms.items()}
        
        # 先翻译
        translated = self.client.translate(text, target_language=target_language)
        
        # 应用术语表
        final_text = translated['translatedText']
        for term, translation in glossary_map.items():
            final_text = final_text.replace(term, translation)
        
        return final_text
    
    def get_supported_languages(self):
        """获取支持的语言列表"""
        languages = self.client.get_languages()
        return [
            {
                'code': lang['language'],
                'name': lang['name']
            }
            for lang in languages
        ]
</code></pre>

<h3>与Microsoft Translator和Amazon Translate对比</h3>
<pre><code>class TranslationService:
    def __init__(self, provider='google'):
        self.provider = provider
        if provider == 'google':
            from google.cloud import translate_v2 as translate
            self.client = translate.Client()
        elif provider == 'microsoft':
            import requests
            self.microsoft_key = 'your-microsoft-key'
            self.microsoft_endpoint = 'https://api.cognitive.microsofttranslator.com'
        elif provider == 'amazon':
            import boto3
            self.client = boto3.client('translate')
    
    def translate(self, text, target_language='zh'):
        if self.provider == 'google':
            return self.client.translate(text, target_language=target_language)
        elif self.provider == 'microsoft':
            url = f"{self.microsoft_endpoint}/translate"
            params = {'api-version': '3.0', 'to': target_language}
            headers = {'Ocp-Apim-Subscription-Key': self.microsoft_key}
            body = [{'text': text}]
            response = requests.post(url, params=params, headers=headers, json=body)
            return response.json()[0]
        elif self.provider == 'amazon':
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode='auto',
                TargetLanguageCode=target_language
            )
            return response['TranslatedText']

# 性能对比测试
def compare_services():
    text = "The quick brown fox jumps over the lazy dog"
    services = ['google', 'microsoft', 'amazon']
    
    for service in services:
        translator = TranslationService(service)
        start_time = time.time()
        result = translator.translate(text, 'zh')
        end_time = time.time()
        
        print(f"{service.upper()}: {result} (耗时: {end_time-start_time:.2f}s)")
</code></pre>

<h3>实时翻译应用</h3>
<pre><code>from flask import Flask, request, jsonify
import json

app = Flask(__name__)
translator = GoogleTranslator()

@app.route('/translate', methods=['POST'])
def translate_endpoint():
    data = request.json
    text = data.get('text')
    target_lang = data.get('target_language', 'zh')
    
    if not text:
        return jsonify({'error': '缺少文本参数'}), 400
    
    try:
        result = translator.translate_text(text, target_lang)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect', methods=['POST'])
def detect_language():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': '缺少文本参数'}), 400
    
    result = translator.detect_language(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
</code></pre>

<h3>错误处理和优化</h3>
<pre><code>class RobustTranslator:
    def __init__(self):
        self.client = translate.Client()
        self.max_retries = 3
        self.retry_delay = 1
    
    def translate_with_retry(self, text, target_language='zh'):
        \"\"\"带重试机制的翻译\"\"\"
        for attempt in range(self.max_retries):
            try:
                return self.client.translate(text, target_language=target_language)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay * (attempt + 1))
    
    def translate_with_cache(self, text, target_language='zh'):
        \"\"\"带缓存的翻译\"\"\"
        cache_key = f"{hash(text)}_{target_language}"
        
        # 检查缓存
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 翻译并缓存
        result = self.translate_with_retry(text, target_language)
        self.cache[cache_key] = result
        
        return result
    
    def validate_input(self, text):
        \"\"\"验证输入文本\"\"\"
        if not text or not isinstance(text, str):
            raise ValueError("无效的输入文本")
        
        if len(text) > 5000:  # Google API限制
            raise ValueError("文本过长,请分段翻译")
        
        return True
</code></pre>

<h3>实际应用案例</h3>
<pre><code>class WebsiteLocalizer:
    def __init__(self, translator):
        self.translator = translator
    
    def localize_html_page(self, html_content, target_language):
        """本地化HTML页面"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 翻译文本节点
        for text_node in soup.find_all(string=True):
            if text_node.parent.name not in ['script', 'style']:
                original_text = str(text_node)
                if original_text.strip():
                    translated = self.translator.translate_text(
                        original_text, 
                        target_language
                    )
                    text_node.replace_with(translated['translated_text'])
        
        return str(soup)
    
    def translate_json_content(self, json_data, target_language):
        """翻译JSON内容"""
        if isinstance(json_data, dict):
            return {
                key: self.translate_json_content(value, target_language)
                for key, value in json_data.items()
            }
        elif isinstance(json_data, list):
            return [
                self.translate_json_content(item, target_language)
                for item in json_data
            ]
        elif isinstance(json_data, str) and json_data.strip():
            result = self.translator.translate_text(json_data, target_language)
            return result['translated_text']
        else:
            return json_data

# 使用示例
localizer = WebsiteLocalizer(GoogleTranslator())

# 本地化HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

localized_html = localizer.localize_html_page(html_content, 'zh')
with open('index_zh.html', 'w', encoding='utf-8') as f:
    f.write(localized_html)
</code></pre>

<h3>成本优化和配额管理</h3>
<ul>
<li><strong>字符计数:</strong>监控API使用量避免超额费用</li>
<li><strong>缓存策略:</strong>减少重复翻译请求</li>
<li><strong>批量处理:</strong>合并多个文本减少API调用</li>
<li><strong>本地化处理:</strong>前端集成减少服务器请求</li>
</ul>
''',
                "summary": "详细介绍Google Translate API的核心功能,Python集成方案,高级翻译特性,以及与Microsoft,Amazon等翻译服务的对比和实际应用案例.",
                "author": "国际化开发专家林雨",
                "category": "精选",
                "tags": "Google Translate,API,多语言,翻译服务,国际化,Python集成",
                "difficulty_level": 3,
                "is_public": True
            },
            {
                "title": "BeautifulSoup网页解析: 优雅处理HTML/XML数据",
                "content": '''
<h2>BeautifulSoup: Python网页解析的瑞士军刀</h2>
<p>BeautifulSoup是一个用于解析HTML和XML文档的Python库,提供了简单灵活的API来导航,搜索和修改解析树,是Web数据提取和内容分析的首选工具.</p>

<h3>核心功能与优势</h3>
<ul>
<li><strong>容错解析:</strong>处理格式不规范的HTML</li>
<li><strong>多种解析器:</strong>lxml,html.parser,html5lib</li>
<li><strong>CSS选择器:</strong>类似jQuery的选择语法</li>
<li><strong>导航API:</strong>parent,sibling,next等关系导航</li>
<li><strong>数据提取:</strong>文本,属性,标签内容的提取</li>
</ul>

<h3>基础解析示例</h3>
<pre><code>from bs4 import BeautifulSoup
import requests

# 获取网页内容
url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# 提取数据
title = soup.title.text
links = [a['href'] for a in soup.find_all('a', href=True)]
images = [img['src'] for img in soup.find_all('img', src=True)]

# CSS选择器
titles = soup.select('h1, h2, h3')
articles = soup.select('div.article > p')
</code></pre>

<h3>高级数据提取</h3>
<ul>
<li><strong>嵌套数据提取:</strong>复杂HTML结构的解析</li>
<li><strong>正则表达式:</strong>模式匹配提取</li>
<li><strong>表格处理:</strong>HTML表格数据提取</li>
<li><strong>属性过滤:</strong>基于属性的精确选择</li>
</ul>

<h3>与MySQL和PostgreSQL集成</h3>
<pre><code>import pymysql
import psycopg2
from bs4 import BeautifulSoup

class DatabaseStorage:
    def __init__(self, db_type='mysql'):
        if db_type == 'mysql':
            self.connection = pymysql.connect(
                host='localhost',
                user='user',
                password='pass',
                database='scrapy_data'
            )
        elif db_type == 'postgresql':
            self.connection = psycopg2.connect(
                host='localhost',
                user='user',
                password='pass',
                database='scrapy_data'
            )
    
    def store_data(self, soup, table_name):
        \"\"\"存储解析数据到数据库\"\"\"
        cursor = self.connection.cursor()
        
        # 提取并存储数据
        for item in soup.find_all('div', class_='data-item'):
            data = {
                'title': item.find('h2').text,
                'content': item.find('p').text,
                'url': item.find('a')['href']
            }
            
            cursor.execute(f"""
                INSERT INTO {table_name} (title, content, url) 
                VALUES (%s, %s, %s)
            """, (data['title'], data['content'], data['url']))
        
        self.connection.commit()
        cursor.close()
</code></pre>

<h3>软件开发和应用集成</h3>
<ul>
<li><strong>API集成:</strong>RESTful API数据提取</li>
<li><strong>内容管理系统:</strong>CMS数据迁移</li>
<li><strong>电商数据:</strong>商品信息采集</li>
<li><strong>新闻聚合:</strong>RSS和新闻网站数据</li>
</ul>

<h3>性能优化与最佳实践</h3>
<ul>
<li><strong>解析器选择:</strong>lxml vs html.parser性能对比</li>
<li><strong>内存管理:</strong>大文件处理策略</li>
<li><strong>错误处理:</strong>健壮的错误恢复机制</li>
<li><strong>并发处理:</strong>多线程解析优化</li>
</ul>
''',
                "summary": "深入介绍BeautifulSoup网页解析库的核心功能,高级数据提取,与数据库的集成应用,以及性能优化和最佳实践.",
                "author": "Web开发工程师张敏",
                "category": "精选",
                "tags": "BeautifulSoup,网页解析,HTML,XML,数据提取,MySQL,PostgreSQL",
                "difficulty_level": 3,
                "is_public": True
            },
            {
                "title": "Scrapy爬虫框架: 高效数据采集与分布式爬取",
                "content": '''
<h2>Scrapy: Python爬虫领域的王者框架</h2>
<p>Scrapy是一个为了爬取网站数据,提取结构性数据而编写的应用框架,可以应用在包括数据挖掘,信息处理或存储历史数据等一系列的程序中.Scrapy使用了Twisted异步网络库来处理网络通讯,架构清晰,并且包含了各种中间件接口,可以灵活的完成各种需求.</p>

<h3>核心架构与组件</h3>
<ul>
<li><strong>引擎(Engine):</strong>整个系统的数据流处理</li>
<li><strong>调度器(Scheduler):</strong>接收引擎发过来的请求,压入队列中</li>
<li><strong>下载器(Downloader):</strong>下载网页内容,并将网页内容返回给蜘蛛</li>
<li><strong>蜘蛛(Spiders):</strong>用户编写用于分析下载器返回的响应</li>
<li><strong>项目管道(Item Pipeline):</strong>负责处理被蜘蛛提取出来的项目</li>
<li><strong>下载器中间件(Downloader Middlewares):</strong>引擎和下载器之间的钩子</li>
<li><strong>蜘蛛中间件(Spider Middlewares):</strong>引擎和蜘蛛之间的钩子</li>
<li><strong>调度中间件(Scheduler Middewares):</strong>引擎和调度器之间的钩子</li>
</ul>

<h3>基础爬虫开发</h3>
<pre><code>import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
</code></pre>

<h3>与BeautifulSoup集成</h3>
<pre><code>import scrapy
from bs4 import BeautifulSoup

class BeautifulSoupSpider(scrapy.Spider):
    name = 'bs4_spider'
    start_urls = ['https://example.com']

    def parse(self, response):
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 提取数据
        titles = [h2.text for h2 in soup.find_all('h2')]
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        yield {
            'page_title': soup.title.text,
            'headings': titles,
            'links': links
        }
</code></pre>

<h3>分布式爬虫部署</h3>
<pre><code># scrapy.cfg
[settings]
default = scrapy_project.settings

[deploy]
url = http://localhost:6800/
project = scrapy_project

# settings.py
BOT_NAME = 'scrapy_project'

SPIDER_MODULES = ['scrapy_project.spiders']
NEWSPIDER_MODULE = 'scrapy_project.spiders'

# 分布式配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
REDIS_URL = 'redis://localhost:6379'

# 并发配置
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 16
DOWNLOAD_DELAY = 3

# 中间件配置
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
</code></pre>

<h3>性能优化策略</h3>
<pre><code>class OptimizedSpider(scrapy.Spider):
    name = 'optimized'
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
    }
    
    def start_requests(self):
        urls = ['https://example.com/page/{}'.format(i) for i in range(1, 100)]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'download_timeout': 10}
            )
    
    def parse(self, response):
        # 使用XPath提取数据
        items = response.xpath('//div[@class="item"]')
        for item in items:
            yield {
                'title': item.xpath('.//h2/text()').get(),
                'price': item.xpath('.//span[@class="price"]/text()').get(),
                'url': item.xpath('.//a/@href').get()
            }
</code></pre>

<h3>反爬虫策略应对</h3>
<pre><code>class AntiBanSpider(scrapy.Spider):
    name = 'anti_ban'
    
    # 使用代理池
    def __init__(self):
        self.proxy_pool = [
            'http://proxy1:8080',
            'http://proxy2:8080',
            'http://proxy3:8080'
        ]
    
    def start_requests(self):
        for url in self.start_urls:
            proxy = random.choice(self.proxy_pool)
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'proxy': proxy},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
            )
    
    def parse(self, response):
        # 随机延迟
        time.sleep(random.uniform(1, 3))
        
        # 数据提取逻辑
        pass
</code></pre>

<h3>数据存储与管道</h3>
<pre><code>class MySQLPipeline:
    def __init__(self, mysql_uri, mysql_db):
        self.mysql_uri = mysql_uri
        self.mysql_db = mysql_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE')
        )
    
    def open_spider(self, spider):
        import pymysql
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            database='scrapy_data',
            charset='utf8mb4'
        )
        self.cursor = self.connection.cursor()
    
    def close_spider(self, spider):
        self.connection.close()
    
    def process_item(self, item, spider):
        sql = """
        INSERT INTO products (title, price, url, created_at) 
        VALUES (%s, %s, %s, NOW())
        """
        self.cursor.execute(sql, (
            item['title'],
            item['price'],
            item['url']
        ))
        self.connection.commit()
        return item
</code></pre>

<h3>监控与日志</h3>
<pre><code>import logging
from scrapy import signals

class StatsExtension:
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext
    
    def spider_closed(self, spider):
        stats = self.stats.get_stats()
        logging.info(f"爬虫 {spider.name} 完成")
        logging.info(f"总共抓取: {stats.get('item_scraped_count', 0)} 条数据")
        logging.info(f"总共请求: {stats.get('downloader/request_count', 0)} 个")
        logging.info(f"成功响应: {stats.get('downloader/response_count', 0)} 个")
        logging.info(f"失败请求: {stats.get('downloader/exception_type_count', 0)} 个")
</code></pre>

<h3>部署与调度</h3>
<ul>
<li><strong>Scrapyd:</strong>部署和管理爬虫服务</li>
<li><strong>Scrapy Cloud:</strong>云端爬虫部署平台</li>
<li><strong>定时任务:</strong>使用cron或Celery调度爬虫</li>
<li><strong>Docker容器化:</strong>容器化部署爬虫应用</li>
<li><strong>负载均衡:</strong>多节点分布式爬虫集群</li>
</ul>
''',
                "summary": "深入介绍Scrapy爬虫框架的核心架构,基础爬虫开发,分布式部署,性能优化,反爬虫策略应对,以及数据存储和监控管理.",
                "author": "数据采集专家陈明",
                "category": "精选",
                "tags": "Scrapy,爬虫,数据采集,分布式,反爬虫,数据存储",
                "difficulty_level": 3,
                "is_public": True
            }
        ]
        
        try:
              # 添加新文章
              for article_data in new_articles:
                  # 检查是否已存在相同标题的文章
                  existing_article = ArticleTutorial.query.filter_by(title=article_data["title"]).first()
                  if not existing_article:
                      article = ArticleTutorial(**article_data)
                      db.session.add(article)
                      print(f"正在添加文章: {article_data['title']}")
                  else:
                      print(f"文章已存在，跳过: {article_data['title']}")
              
              db.session.commit()
              print(f"成功添加 {len(new_articles)} 篇新文章!")
              
              # 显示添加的文章列表
              articles = ArticleTutorial.query.all()
              print("\n已添加的文章列表:")
              for article in articles:
                  print(f"- {article.title} ({article.category})")
                
        except Exception as e:
            db.session.rollback()
            print(f"添加文章时出错: {e}")
            raise

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        add_new_articles()