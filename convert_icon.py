from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    """
    将PNG图片转换为ICO格式
    :param png_path: PNG文件路径
    :param ico_path: 输出的ICO文件路径
    """
    try:
        # 打开PNG图片
        img = Image.open(png_path)
        
        # 确保图片是RGBA模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 调整为256x256大小
        resized_img = img.resize((256, 256), Image.Resampling.LANCZOS)
        
        # 保存为ICO文件
        resized_img.save(
            ico_path,
            format='ICO',
            sizes=[(256, 256)]
        )
        
        print(f"成功将 {png_path} 转换为 {ico_path}")
        return True
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 当前目录下的文件
    png_file = "ps-jsx.png"
    ico_file = "ps-jsx.ico"
    
    if os.path.exists(png_file):
        convert_png_to_ico(png_file, ico_file)
    else:
        print(f"找不到文件: {png_file}") 