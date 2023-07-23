import json
import Pyro.core
import sys


class Client:
    def __init__(self, url_server):
        Pyro.core.initClient()
        self.proxy = Pyro.core.getProxyForURI(url_server)
        print ("Client Python Pyro3: " + url_server)

    def print_files(self, files):
        for file in files:
            print("NUME: " + file["nume"] + " PATH: " + file["path"] + " HASH: " + file["hash"])
        print("\n")

    def find_all_files(self):
        files = json.loads(self.proxy.find_all_files())
        self.print_files(files)

    def find_files_containing_substring(self):
        substring = raw_input("Substring: ")
        files = json.loads(self.proxy.find_files_containing_substring(substring))
        self.print_files(files)

    def find_files_by_content_parts_text(self):
        content = raw_input("Content (text): ")
        files = json.loads(self.proxy.find_files_by_content_parts_text(content))
        self.print_files(files)

    def find_files_by_content_parts_binary(self):
        content = raw_input("Content (binary): ")
        files = json.loads(self.proxy.find_files_by_content_parts_binary(content))
        self.print_files(files)

    def find_files_with_duplicate_hash(self):
        files = json.loads(self.proxy.find_files_with_duplicate_hash())
        self.print_files(files)

    def menu(self, menu):
        for key in sorted(menu.keys()):
            print("\t" + key + ":  " + menu[key][0])

        try:
            choice = input("Option: ")
            _function = menu.get(str(choice))
            if isinstance(_function[1], dict):
                self.menu(_function[1])
            else:
                if _function[0] == "Back":
                    return
                _function[1]()
        except SystemExit:
            raise SystemExit
        except (TypeError, NameError):
            print("Invalid option\n")

        self.menu(menu)

    def stop(self):
        raise SystemExit

    def start(self):
        content_type_menu = {"1": ("Text: ", self.find_files_by_content_parts_text),
                             "2": ("Binary: ", self.find_files_by_content_parts_binary),
                             "3": ("Back", None)
                             }

        menu = {"1": ("Find all files", self.find_all_files),
                "2": ("Find files containing substring", self.find_files_containing_substring),
                "3": ("Find files by parts of content", content_type_menu),
                "4": ("Find files with duplicate content", self.find_files_with_duplicate_hash)
                }

        self.menu(menu)
        self.start()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        client = Client(sys.argv[1])
    else:
        client = Client("PYROLOC://localhost:7766/exec")

    client.start()
