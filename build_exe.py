import PyInstaller.__main__
import os

# 确保所需文件存在
required_files = ['ps-jsx.ico', 'mao.png']
for file in required_files:
    if not os.path.exists(file):
        print(f"错误: 找不到文件 {file}")
        exit(1)

PyInstaller.__main__.run([
    'main.py',
    '--name=PS-JSX-Manager',
    '--windowed',
    '--icon=ps-jsx.ico',
    '--add-data=ps-jsx.ico;.',
    '--add-data=mao.png;.',
    '--noconfirm',
    '--clean',
    '--onefile',
    # 添加调试信息
    '--debug=all'
]) 