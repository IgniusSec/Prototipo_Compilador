from os import read
from ttoken import TOKEN

EXCLUDED_CHARS = [' ']

class Lexical:
    def __init__(self, arq_path):
        self.arq = arq_path
        try:
            file = open(arq_path, 'r')
            content = file.read()
            self.content = list(content)
            file.close()
        except FileNotFoundError:
            print("File not found!")
            return

        self.arq_size = len(self.content)
        self.index = 0
        self.token_atual = None
        self.linha = 1
        self.coluna = 0

    def end_of_file(self):
        return self.index >= self.arq_size

    def get_char(self):

        self.index += 1

    def unget_char(self, simbol):
        if simbol == '\n':
            self.linha -= 1
        if self.index > 0:
            self.index -= 1
        if self.coluna > 0:
            self.coluna -= 1

    def trash_comments(self, index):
        aux = index 
        while(self.content[aux] != '\n'):
            self.content.pop(aux)
        #tira o \n
        self.content.pop(aux)

    def trash_code(self):
        char = ""
        index = 0
        bars = 0
        while(char != '\0'):
            char = self.content[index]
            if char == '/':
                bars += 1
                if bars > 1:
                    self.trash_comments(index)
                    bars = 0
            else:
                bars = 0
            if char in EXCLUDED_CHARS:
                self.content.pop(index)
                index -= 1
            index += 1
            

    def get_token(self):
        estado = 1


        while
