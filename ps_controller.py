from photoshop.api import Application

class PhotoshopController:
    def __init__(self):
        self.app = Application()

    def run_jsx_script(self, script_path):
        """
        运行JSX脚本
        
        Args:
            script_path (str): JSX脚本的完整路径
        """
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                jsx_content = file.read()
            self.app.doJavaScript(jsx_content)
        except Exception as e:
            raise Exception(f"执行脚本时出错: {str(e)}") 