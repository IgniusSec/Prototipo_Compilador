from ttoken import TOKEN

EXCLUDED_CHARS = ["(", ")", ",", ";"]
BROKEN_CHARS = ["\n"]
END_FILE = "."
PATH_FILE = "exemplo.toy"


class Lexical:
    def __init__(self, arq_path):
        self.arq = arq_path
        try:
            file = open(arq_path, "r")
            content = file.read()
            self.content = list(content)
            file.close()
        except FileNotFoundError:
            print("File not found!")
            return

        self.arq_size = len(self.content)
        self.linha = 1
        self.coluna = 0

        # limpa o código
        self.trash_code()

        self.index = 0
        self.token_atual = None

    def end_of_file(self):
        return self.index >= self.arq_size

    # pega um char
    def get_char(self):
        char = self.content[self.index]
        self.index += 1
        if char == "\n":
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return char

    # devolve char
    def unget_char(self, simbol):
        if simbol == "\n":
            self.index += 1
        if self.index > 0:
            self.index -= 1
        if self.coluna > 0:
            self.coluna -= 1

    # remove comentarios
    def trash_comments(self, index):
        aux = index
        while self.content[aux] != "\n":
            self.content.pop(aux)
        # tira os \n pos comentário
        while self.content[aux] == "\n":
            self.content.pop(aux)
            self.linha += 1

    # limpa o código
    def trash_code(self):
        char = ""
        index = 0
        bars = 0
        while char != END_FILE:
            char = self.content[index]
            if char == "/":
                bars += 1
                if bars > 1:
                    self.trash_comments(index)
                    bars = 0
                    self.linha += 1
            elif char != "/" and bars > 0:
                bars = 0
            # Salta as string
            elif char == '"':
                index += 1
                while (self.content[index]) != '"':
                    index += 1
                index += 1
            elif char == " ":
                self.content.pop(index)
            else:
                index += 1

        # add \0 no fim para facilitar, caso seja necessário transformar em str
        self.content[index] = "\0"
        index += 1

        # remove qualquer espaço extra no fim do arquivo
        while index < len(self.content):
            self.content.pop(index)
            index += 1

        # atualiza tamanho do arquivo após remoção de comentários
        self.arq_size = len(self.content)

    """
        Retorna uma quadrupla com (tipo_token, token, linha do token, coluna do token)
    """

    def get_token(self):

        estado = 1
        lexema = ""
        char = self.get_char()

        if char == "\n":
            self.unget_char(char)
            char = self.get_char()

        lin = self.linha
        col = self.coluna

        while True:
            if char not in BROKEN_CHARS and char not in EXCLUDED_CHARS:
                lexema += char
            if estado == 1:
                # letra/simbolo
                if char.isalpha():
                    estado = 2
                # numeros
                elif char.isdigit():
                    estado = 3
                # inicio de string
                elif char == '"':
                    estado = 4
                elif char == "(":
                    return (TOKEN.abrePar, "(", lin, col)
                elif char == ")":
                    return (TOKEN.fechaPar, ")", lin, col)
                elif char == ",":
                    return (TOKEN.virg, ",", lin, col)
                elif char == ";":
                    return (TOKEN.ptoVirg, ";", lin, col)
                elif char == "+":
                    return TOKEN.mais, "+", lin, col
                elif char == "-":
                    return TOKEN.menos, "-", lin, col
                elif char == "*":
                    return TOKEN.multiplica, "*", lin, col
                elif char == "/":
                    return TOKEN.divide, "/", lin, col
                elif char == "%":
                    return TOKEN.porcent, "%", lin, col
                elif char == "<":
                    estado = 5
                elif char == ">":
                    estado = 6
                elif char == "=":
                    estado = 7
                elif char == "!":
                    estado = 8
                elif char == "\0":
                    return (TOKEN.eof, "<eof>", lin, col)
                else:
                    return (TOKEN.erro, lexema, lin, col)

            elif estado == 2:
                if char.isalnum():
                    estado = 2
                elif char in EXCLUDED_CHARS or char in BROKEN_CHARS:
                    self.unget_char(char)
                    return (TOKEN.ident, lexema, lin, col)
                else:
                    return (TOKEN.erro, lexema, lin, col)

            elif estado == 3:
                if char.isnumeric():
                    estado = 3
                elif char in EXCLUDED_CHARS:
                    self.unget_char(char)
                    return (TOKEN.num, lexema, lin, col)
                else:
                    return (TOKEN.erro, lexema, lin, col)

            # TODO: Atulizar caso seja necessário utilizar o caractere de escape '\'
            elif estado == 4:
                if char == '"':
                    return (TOKEN.string, lexema, lin, col)

            elif estado == 5:
                if char == "=":
                    return (TOKEN.menorIgual, lexema, lin, col)
                else:
                    return (TOKEN.menor, lexema, lin, col)

            elif estado == 6:
                if char == "=":
                    return (TOKEN.maiorIgual, lexema, lin, col)
                else:
                    return (TOKEN.maior, lexema, lin, col)

            elif estado == 7:
                if char == "=":
                    return (TOKEN.igual, lexema, lin, col)
                else:
                    return (TOKEN.atrib, lexema, lin, col)

            elif estado == 8:
                if char == "=":
                    return (TOKEN.diferente, lexema, lin, col)
                else:
                    return (TOKEN.NOT, lexema, lin, col)

            char = self.get_char()


if __name__ == "__main__":
    lex = Lexical(PATH_FILE)

    while not lex.end_of_file():
        tok = lex.get_token()
        print(tok)
