import os
import glob

# 查找最近的日志文件
log_files = glob.glob('*.log')
if log_files:
    latest_log = max(log_files, key=os.path.getctime)
    print(f'最近的日志文件: {latest_log}')
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            print('\n日志内容:')
            print(f.read()[-5000:])  # 打印最后5000个字符
    except Exception as e:
        print(f'读取日志文件错误: {e}')
else:
    print('未找到日志文件')

# 检查应用是否有其他错误记录位置
app_log_path = os.path.join('logs', 'app.log')
if os.path.exists(app_log_path):
    print(f'\n找到应用日志文件: {app_log_path}')
    try:
        with open(app_log_path, 'r', encoding='utf-8') as f:
            print('日志内容:')
            print(f.read()[-5000:])  # 打印最后5000个字符
    except Exception as e:
        print(f'读取应用日志文件错误: {e}')