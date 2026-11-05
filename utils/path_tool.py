#为整个工程提供统一的绝对路径
import os


def get_project_root() -> str:    
    #获取工程所在根目录
    project_root = os.path.abspath(__file__)   #获取当前文件的绝对路径 Agent/utils/path_tool.py
    project_root = os.path.dirname(project_root)   #获取当前文件所在目录 Agent/utils
    project_root = os.path.dirname(project_root)   #获取当前文件所在目录的父目录 Agent
    return project_root


def get_abs_path(relative_path: str) -> str:  #传递相对路径得到绝对路径
    return os.path.join(get_project_root(), relative_path)

if __name__ == '__main__':
    print(get_abs_path('config/config.txt'))
    