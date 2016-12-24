import sys, os, tempfile
import re
from queue import Queue
from subprocess import call


def try_exec(decorating):
    def wrapper(*args):
        try:
            return decorating(*args)
        except IOError:
            print()
            print('Невозможно открыть файл')
        except ValueError:
            print()
            print('Неверный формат ввода')
        except:
            print()
            print('Неизвестная ошибка:')
            raise
    return wrapper


class App:
    def __init__(self):
        self.editor = os.environ.get('EDITOR', 'nano')
        self.editing_graph = None
        self.current_file = None

    @try_exec
    def bfs(self):
        print()
        print('Введите начальную вершину:')
        start = int(input())
        graph = self.get_dict()
        graph[start]['passed'] = True
        q = Queue()
        q.put(graph[start])
        print()
        print('  -> %i' % start)
        while not q.empty():
            pas = q.get()
            for adj in pas['adjacences']:
                if not graph[adj]['passed']:
                    graph[adj]['passed'] = True
                    q.put(graph[adj])
                    print('%i -> %i' % (pas['number'], adj))

    @try_exec
    def get_dict(self):
        pure = self.get_pure_string()
        lines = pure.split("\n")
        dict = {}
        for line in lines:
            if ')' in line:
                parts = line.split(')')
                dict[int(parts[0])] = {
                    'adjacences': [int(x) for x in parts[1].split(',')],
                    'passed': False,
                    'number': int(parts[0])
                }
        return dict

    @try_exec
    def edit_graph(self, content=''):
        with open(self.current_file, 'w+t') as file:
            file.write(content)
            file.flush()
            call([self.editor, file.name])

            file.seek(0)
            self.editing_graph = file.read()

    @try_exec
    def open_graph(self):
        print('\nВведите путь к файлу:')
        path = input()
        with open(path, 'r') as file:
            file.seek(0)
            self.editing_graph = file.read()
            self.current_file = path
        self.edit_graph(self.editing_graph)

    @try_exec
    def new_graph(self):
        print('\nВведите путь к файлу:')
        path = input()
        with open(path, 'r') as file:
            self.current_file = path
        content = """# введите список смежности графа\n# пример:\n# 1)2,3\n# 2)1,3\n# 3)2,1\n"""
        self.edit_graph(content)

    def print_graph(self):
        print()
        print('Список Смежности:')
        print(self.get_pure_string())

    def get_pure_string(self):
        pure = re.sub(re.compile("#.*?\n"), "", self.editing_graph)
        pure.strip()
        return pure

    def print_menu(self):
        print('0) Выход')
        print('1) Открыть файл')
        print('2) Новый файл')
        if self.editing_graph:
            print('3) Редактировать')
        if self.current_file:
            print('4) Печатать список смежности')
            print('5) Обход в ширину')
        print('Введите цифру команды:')

    def run(self):
        while True:
            self.print_menu()

            ans = input()
            if ans == '0':
                exit()
            elif ans == '1':
                self.open_graph()
            elif ans == '2':
                self.new_graph()
            elif ans == '3' and self.editing_graph:
                self.edit_graph(self.editing_graph)
            elif ans == '4' and self.current_file:
                self.print_graph()
            elif ans == '5' and self.current_file:
                self.bfs()
            print()

if __name__ == '__main__':
    app = App()
    app.run()
