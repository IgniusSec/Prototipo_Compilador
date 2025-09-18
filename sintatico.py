from lexical import Lexical, PATH_FILE
from ttoken import TOKEN
import sys


class Sintatico:

    def __init__(self, lexico: Lexical):
        self.lexico = lexico
        self.lexico.token_atual = self.lexico.get_token()

    def error_message(self, token, linha, coluna):
        msg = TOKEN.msg(token)
        print(f"Comando mal utilizado: {msg} || Lin{linha} Col{coluna}")
        raise Exception("Command unknow")

    def test_lexico(self):
        self.lexico.token_atual = self.lexico.get_token()
        (token, lexema, linha, coluna) = self.lexico.token_atual
        while token != TOKEN.eof:
            self.lexico.print_token(self.lexico.token_atual)
            self.lexico.token_atual = self.lexico.get_token()
            (token, lexema, linha, coluna) = self.lexico.token_atual

    def consume(self, token_now):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token_now == token:
            if token != TOKEN.eof:
                self.lexico.token_atual = self.lexico.get_token()
        else:
            msg_token_lido = TOKEN.msg(token)
            msg_token_now = TOKEN.msg(token_now)
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msg_token_lido
                print(
                    f"Esperado: {msg_token_now} || Recebido: {msg}\nLin {linha} Col {coluna}"
                )
                raise Exception("Token unknow")

    """
        Prog -> inicio Coms fim.
    """

    def prog(self):
        self.consume(TOKEN.BEGIN)
        self.coms()
        self.consume(TOKEN.END)
        self.consume(TOKEN.pto)
        self.consume(TOKEN.eof)

    """
        Coms -> LAMBDA | Com Coms
    """

    def coms(self):
        init_com = [TOKEN.LEIA, TOKEN.ESCREVA, TOKEN.IF, TOKEN.ident, TOKEN.abreChave]
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token in init_com:
            self.com()
            self.coms()
        else:
            return

    """
        Com  -> Ler | Escrever | If | Atrib | Bloco
    """

    def com(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.LEIA:
            self.ler()
        elif token == TOKEN.ESCREVA:
            self.escrever()
        elif token == TOKEN.IF:
            self.iF()
        elif token == TOKEN.ident:
            self.atrib()
        elif token == TOKEN.abreChave:
            self.bloco()
        else:
            self.error_message(token, linha, coluna)

    """
        Ler  -> leia ( string, ident ) ;
    """

    def ler(self):
        self.consume(TOKEN.LEIA)
        self.consume(TOKEN.abrePar)
        self.consume(TOKEN.string)
        self.consume(TOKEN.virg)
        self.consume(TOKEN.ident)
        self.consume(TOKEN.fechaPar)
        self.consume(TOKEN.ptoVirg)

    """
        Escrever -> escreva ( string RestoEscrever
    """

    def escrever(self):
        self.consume(TOKEN.ESCREVA)
        self.consume(TOKEN.abrePar)
        self.consume(TOKEN.string)
        self.resto_escrever()

    """
        RestoEscrever -> , ident ) ; | ) ;
    """

    def resto_escrever(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            self.consume(TOKEN.ident)
            self.consume(TOKEN.fechaPar)
            self.consume(TOKEN.ptoVirg)
        elif token == TOKEN.fechaPar:
            self.consume(TOKEN.fechaPar)
            self.consume(TOKEN.ptoVirg)
        else:
            self.error_message(token, linha, coluna)

    """
        If -> if ( Exp ) Com RestoIf
    """

    def iF(self):
        self.consume(TOKEN.IF)
        self.consume(TOKEN.abrePar)
        self.exP()
        self.consume(TOKEN.fechaPar)
        self.com()
        self.resto_if()

    """
        RestoIf -> LAMBDA | else Com
    """

    def resto_if(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.ELSE:
            self.consume(TOKEN.ELSE)
            self.com()
        else:
            return

    """
        Bloco -> { Coms }
    """

    def bloco(self):
        self.consume(TOKEN.abreChave)
        self.coms()
        self.consume(TOKEN.fechaChave)

    """
        Atrib -> ident = Exp ;
    """

    def atrib(self):
        self.consume(TOKEN.ident)
        self.consume(TOKEN.atrib)
        self.exP()
        self.consume(TOKEN.ptoVirg)

    """
        Exp -> Nao RestoExp
    """

    def exP(self):
        self.nao()
        self.resto_exp()

    """
        RestoExp -> LAMBDA | and Nao RestoExp | or Nao RestoExp
    """

    def resto_exp(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.AND:
            self.consume(TOKEN.AND)
            # TODO: Verificar se pode trocar o Nao RestoExp por exP que seria o mesmo
            self.exP()
        elif token == TOKEN.OR:
            self.consume(TOKEN.OR)
            # TODO: Verificar se pode trocar o Nao RestoExp por exP que seria o mesmo
            self.exP()
        else:
            return

    """
        Nao -> not Nao | Rel
    """

    def nao(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.NOT:
            self.consume(TOKEN.NOT)
            self.nao()
        else:
            self.rel()

    """
        Rel -> Soma RestoRel
    """

    def rel(self):
        self.soma()
        self.resto_rel()

    """
        RestoRel -> LAMBDA | opRel Soma
    """

    def resto_rel(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        op_rel = [
            TOKEN.menor,
            TOKEN.maior,
            TOKEN.igual,
            TOKEN.menorIgual,
            TOKEN.maiorIgual,
        ]

        if token in op_rel:
            self.consume(token)
            self.soma()
        else:
            return

    """
        Soma -> Mult RestoSoma
    """

    def soma(self):
        self.mult()
        self.resto_soma()

    """
        RestoSoma -> LAMBDA | + Mult RestoSoma | - Mult RestoSoma
    """

    def resto_soma(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.mais:
            self.consume(TOKEN.mais)
            self.mult()
            self.resto_soma()
        elif token == TOKEN.menos:
            self.consume(TOKEN.menos)
            self.mult()
            self.resto_soma()
        else:
            return

    """
        Mult -> Uno RestoMult
    """

    def mult(self):
        self.uno()
        self.resto_mult()

    """
        RestoMult -> LAMBDA | * Uno RestoMult | / Uno RestoMult | % Uno RestoMult
    """

    def resto_mult(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.multiplica:
            self.consume(TOKEN.multiplica)
            self.uno()
            self.resto_mult()
        elif token == TOKEN.divide:
            self.consume(TOKEN.divide)
            self.uno()
            self.resto_mult()
        elif token == TOKEN.resto:
            self.consume(TOKEN.resto)
            self.uno()
            self.resto_soma()
        else:
            return

    """
        Uno -> + Uno | - Uno | Folha
    """

    def uno(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token == TOKEN.mais:
            self.consume(TOKEN.mais)
            self.uno()
        elif token == TOKEN.menos:
            self.consume(TOKEN.menos)
            self.uno()
        else:
            self.folha()

    """
        Folha -> num | ident | ( Exp )
    """

    def folha(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        save = None
        if token == TOKEN.num:
            save = lexema
            self.consume(TOKEN.num)
        elif token == TOKEN.ident:
            save = lexema
            self.consume(TOKEN.ident)
        elif token == TOKEN.abrePar:
            self.consume(TOKEN.abrePar)
            save = self.exP()
            self.consume(TOKEN.fechaPar)
        else:
            self.error_message(token, linha, coluna)

        return save


if __name__ == "__main__":
    path = "exemplo.toy"
    lex = Lexical(path)
    sintatico = Sintatico(lex)

    sintatico.prog()
