from typing import Any
import zipfile
import virtual_file_system
import csv
import json

FILE = "archive.zip"
CONF = "conf.csv"
class Shell:
    def __init__(self) -> None:
        self.root = virtual_file_system.Root([])
        self.current = self.root
        self.history = []
        self.file = ""
        self.log = []
        self.user = ""
        self.computer = ""  
        self.log_path = ""
        
    def read_config(self, path: str) -> Any:
        with open(path, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            self.user, self.computer, self.file, self.log_path = next(csv_reader)
        
    def load_fs_from_zip(self) -> None:
        with zipfile.ZipFile(self.file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                path = list(filter(None, file_info.filename.split("/")))
                if file_info.is_dir():
                    self.root.add_content(path, True)
                else:
                    self.root.add_content(path, False, zip_ref.read(file_info.filename).decode())
            zip_ref.close()
        # self.root.print_tree()
    
    def cd(self, path: str) -> None:
        if path == "..":
            if self.current.path == "/":
                return
            self.current = self.current.parent
            return
        if path == ".":
            return
        if path == "/":
            self.current = self.root
            return
        
        if path[0] == "/":
            path = ["/"] + list(filter(None, path.split("/")))
        else:
            path = list(filter(None, path.split("/")))
        
        try:
            curr, is_folder = self.current.move(path)
        except ValueError as e:
            print(e)
            return
        if is_folder:
            self.current = curr
        else:
            print(f"cd: not a directory: {path}")
    
    def ls(self, path: str = "") -> None:
        if path == "":
            print(' '.join(self.current.return_content_names()))
        else:
            name = path.rfind("/")
            if path[0] == "/":
                path = ["/"] + list(filter(None, path.split("/")))
            else:
                path = list(filter(None, path.split("/")))
            try:
                self.temp, temp_is_folder = self.current.move(path)
            except ValueError as e:
                print(e)
                return
            if temp_is_folder:
                content_names = self.temp.return_content_names()
                print(' '.join(content_names) if len(content_names) >= 2 else content_names[0])
            else:
                print(path)
        
    def rm(self, path: str) -> None:
        if path[0] == "/":
            path = ["/"] + list(filter(None, path.split("/")))
        else:
            path = list(filter(None, path.split("/")))
        if len(path) == 1:
            self.current.delete_file_by_name(path[0])
            return
        name = path[-1]
        try:
            folder, is_folder = self.current.move(path)
            if is_folder:
                raise ValueError(f"rm: {name}: is a folder")
        except ValueError as e:
            print(e)
            return
        # print(f"rm name: {name}")
        folder.delete_file_by_name(name)
    
    def cat(self, path: str) -> None:
        # print("cat")
        if path[0] == "/":
            path = ["/"] + list(filter(None, path.split("/")))
        else:
            path = list(filter(None, path.split("/")))
        # print(path)
        if len(path) == 1:
            # print("len(path) == 1")
            file = self.current.get_content_by_name(path[0])
            if file is None or not file.is_file():
                print("Invalid path")
                return
            else:
                print(file.get_text())
                return
        name = path[-1]
        try:
            folder, is_folder = self.current.move(path)
        except ValueError as e:
            print(e)
            return
        file = folder.get_content_by_name(name)
        if not file.is_file():
            print("Invalid path")
            return
        else:
            print(file.get_text())
            return
    
    def find(self, path: str) ->None:
        name = path.rfind("/")
        if path[0] == "/":
            path = ["/"] + list(filter(None, path.split("/")))
        else:
            path = list(filter(None, path.split("/")))
        self.temp = self.current.move(path)
        if self.temp.is_file():
            print(name)
            return
        else:
            self.temp.get_content_by_name(name).print_with_path()
            return

            
        
    def create_log(self) -> None:
        all_logs = []
        for action in self.log:
            log_entry = {
                "user": self.user,
                "action": action
            }
            all_logs.append(log_entry)
        with open(self.log_path, "w") as file:
            json.dump(all_logs, file)
        
        
    def user_input(self) -> None:
        while True:
            user_input = input(f"{self.user + "@" + self.computer}:{self.current.path}$")
            command = list(filter(None, user_input.split(" ")))
            self.log.append(user_input)
            if len(command) == 0:
                continue
            if command[0] == "exit":
                break
            if command[0] == "cd":
                if len(command) != 2:
                    print("Invalid command")
                    continue
                self.cd(command[1])
            elif command[0] == "ls":
                if len(command) > 2:
                    print("error of input")
                    continue
                elif len(command) == 2:
                    self.ls(command[1])
                else:
                    self.ls()
            elif command[0] == "cat":
                if len(command) != 2:
                    print("Invalid command")
                    continue
                self.cat(command[1])
            elif command[0] == "rm":
                if len(command) != 2:
                    print("Invalid command")
                    continue
                self.rm(command[1])
            else:
                print(f"Invalid command: {command[0]}")
    

if __name__ == "__main__":
    shell = Shell()
    shell.read_config(CONF)
    shell.load_fs_from_zip()
    shell.user_input()
    shell.create_log()