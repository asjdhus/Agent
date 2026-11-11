import os
import json


class filehistory_store:
    def __init__(self):
        self.history = []
        self.file_path=os.path.join(os.path.dirname(__file__),"file_history.json")
        if not os.path.exists(self.file_path):
            with open(self.file_path,"w") as f:
                json.dump([],f,indent=4)
        else:
            try:
                with open(self.file_path,"r",encoding="utf-8") as f:
                    self.history=json.load(f)
            except json.JSONDecodeError:
                # 历史文件损坏时重置为空列表，避免程序无法启动
                self.history=[]
    def get_history(self):
        # 返回副本，避免外部对列表的修改反过来影响内部 self.history（防止自引用）
        return list(self.history)
    
    def add_history(self,history:list):
        # 直接保存完整消息列表，而不是 append（append 会把整个列表再嵌套一层，甚至自引用）
        self.history = list(history)
        self._save()

    def _save(self):
        # 原子写入：先写临时文件再替换，避免写入中断导致文件被截断（丢失结尾括号）
        tmp_path = self.file_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
        os.replace(tmp_path, self.file_path)