from typing import List, Union, Tuple


class Window():
    def __init__(self, path : str, parent : 'Folder'):
        super().__init__()
        self.path = path
        self.parent = parent
        self.name = path.split("/")[-1]
    
    def get_prev_path(self):
        if self.path == "/":
            return self.path
        return self.parent.path
           
    def is_file(self):
        return isinstance(self, File)
    
    def print_tree(self, deep = 0):
        print(" " * deep * 4, self.name)
        if not self.is_file():
            for item in self.content:
                item.print_tree(deep + 1)
    
    def print_with_path(self, path: str = ""):
        path = path + "/" + self.name
        print(path)
        if not self.is_file():
            for item in self.content:
                item.print_with_path(path)

class File(Window):
    def __init__(self, path, parent: 'Folder', text: str):
        super().__init__(path, parent)
        self.text = text
    
    def get_text(self):
        # print("texting..:", self.text)
        return self.text

class Folder(Window):
    def __init__(self, path, parent: 'Folder'):
        super().__init__(path, parent)
        self.content = []
        self._validate_content()
        
    def _validate_content(self):
        for item in self.content:
            if not isinstance(item, (Folder, File)):
                raise ValueError("Invalid content")
    
    def get_root(self):
        if self.path == "/":
            return self
        return self.parent.get_root()
    
    def move(self, path: List[str]) -> Tuple['Folder', bool]: # bool - is_folder
        if len(path) == 0:
            if self.is_file():
                # print("returning parent: ", self.paren.path)
                return self.parent, False
            else:
                # print("last not a file: ", self.path)
                return self, True
        
        name = path.pop(0)
        if name == "..":
            return self.parent.move(path)
        if name == ".":
            return self.move(path)
        if name == "/":
            return self.get_root().move(path)
        if name in self.return_content_names():
            if self.get_content_by_name(name).is_file():
                return self, False
            return self.get_content_by_name(name).move(path)
        raise ValueError(f"Invalid path {self.path + '/' + name if self.path != "/" else "/" + name} does not exist")
        
            
    
    def remove_content(self, content: Union[File, 'Folder']):
        self.content.remove(content)
        self._validate_content()
    
    def check_content(self, content: Union[File, 'Folder']):
        return content in self.content
    
    def get_content(self):
        return self.content
    
    def get_content_by_name(self, name: str):
        for item in self.content:
            if item.name == name:
                return item
        return None
    
    def return_content_names(self):
        return [item.name for item in self.content]
    
    def delete_file_by_name(self, name: str):
        if name in self.return_content_names():
            if not self.get_content_by_name(name).is_file():
                print(f"rm: {name}: is a folder")
                return
            self.remove_content(self.get_content_by_name(name))
        else:
            print(f"rm: {name}: No such file or directory")
    
class Root(Folder):
    def __init__(self, content : List[Window], parent = None):
        super().__init__("~", content)
    
    def add_content(self, path: List[str], is_folder: bool, text = ""):
        item = path[-1]
        path = path[:-1]
        try:
            folder, _ = self.move(path)
        except ValueError as e:
            raise ValueError(f"Invalid path {'/'.join(path)[1:]} does not exist")
        # print(f'path after move in add_content: {path}')
        # print(f"Adding {item} to {folder.path}")
        folder_path = folder.path if folder.path != "/" else ""
        total_path = folder_path + "/" + item
        # print(f"Total path: {total_path}")
        # print("parent path: ", folder.path)
        # print(f"adding {item} to {folder.path} with flag {is_folder}")
        folder.content.append(Folder(total_path, folder) if is_folder else File(total_path, folder, text))
        