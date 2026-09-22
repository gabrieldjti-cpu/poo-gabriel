"""Lojinha de terminal com produtos, estoque e operações validadas."""


class Produto:
    """Representa um produto com preço e estoque protegidos."""

    def __init__(self, nome, preco, estoque=0):
        nome = str(nome).strip()
        if not nome:
            raise ValueError("O nome do produto não pode ficar vazio.")

        self.nome = nome
        self.__preco = 0
        self.__estoque = 0
        self.preco = preco
        self.estoque = estoque

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise TypeError("O preço deve ser um número.")
        if valor < 0:
            raise ValueError("O preço não pode ser negativo.")
        self.__preco = float(valor)

    @property
    def estoque(self):
        return self.__estoque

    @estoque.setter
    def estoque(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("O estoque deve ser um número inteiro.")
        if valor < 0:
            raise ValueError("O estoque não pode ser negativo.")
        self.__estoque = valor

    def exibir(self):
        """Imprime nome, preço e quantidade disponível."""
        print(f"{self.nome} | R$ {self.preco:.2f} | estoque: {self.estoque}")

    def vender(self, qtd):
        """Vende uma quantidade válida; retorna True somente se concluir."""
        if isinstance(qtd, bool) or not isinstance(qtd, int) or qtd <= 0:
            print("Venda recusada: a quantidade deve ser um inteiro positivo.")
            return False
        if qtd > self.estoque:
            print(
                f"Venda recusada: estoque insuficiente. Dispon�vel: {self.estoque}; "
                f"solicitado: {qtd}."
            )
            return False

        self.estoque -= qtd
        print(f"Venda realizada: {qtd} unidade(s) de {self.nome}.")
        return True

    def repor(self, qtd):
        """Acrescenta unidades ao estoque ou informa por que não foi possível."""
        if isinstance(qtd, bool) or not isinstance(qtd, int) or qtd <= 0:
            print("Reposição recusada: a quantidade deve ser um inteiro positivo.")
            return False

        self.estoque += qtd
        print(f"Reposição realizada: {qtd} unidade(s) de {self.nome}.")
        return True


def ler_inteiro(mensagem):
    """L� um inteiro sem encerrar o programa quando a entrada � inválida."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida: digite um número inteiro.")


def ler_preco(mensagem):
    """L� um preço; aceita ponto ou vírgula como separador decimal."""
    while True:
        try:
            return float(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("Preço inv�lido: digite um número, por exemplo 4.50.")


def listar(catalogo):
    """Mostra o catálogo numerado ou informa que está vazio."""
    if not catalogo:
        print("O catálogo está vazio. Cadastre um produto primeiro.")
        return False

    print("\n--- Catélogo ---")
    for numero, produto in enumerate(catalogo, start=1):
        print(f"{numero}. ", end="")
        produto.exibir()
    return True


def selecionar_produto(catalogo):
    """Retorna um produto selecionado, ou None para seleção inválida."""
    if not listar(catalogo):
        return None

    numero = ler_inteiro("Número do produto: ")
    if not 1 <= numero <= len(catalogo):
        print("Número de produto fora da lista.")
        return None
    return catalogo[numero - 1]


def menu():
    """Executa o menu da lojinha até a opção de saída."""
    catalogo = []

    while True:
        print(
            "\n=== Lojinha ===\n"
            "1. Cadastrar produto\n"
            "2. Listar catálogo\n"
            "3. Vender\n"
            "4. Repor estoque\n"
            "5. Sair"
        )
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do produto: ").strip()
            preco = ler_preco("Preço (use ponto ou vírgula decimal): R$ ")
            estoque = ler_inteiro("Estoque inicial (inteiro >= 0): ")
            try:
                produto = Produto(nome, preco, estoque)
            except (TypeError, ValueError) as erro:
                print(f"Cadastro recusado: {erro}")
            else:
                catalogo.append(produto)
                print(f"Produto '{produto.nome}' cadastrado com sucesso.")

        elif opcao == "2":
            listar(catalogo)

        elif opcao == "3":
            produto = selecionar_produto(catalogo)
            if produto is not None:
                qtd = ler_inteiro("Quantidade para vender: ")
                produto.vender(qtd)

        elif opcao == "4":
            produto = selecionar_produto(catalogo)
            if produto is not None:
                qtd = ler_inteiro("Quantidade para repor: ")
                produto.repor(qtd)

        elif opcao == "5":
            print("At� logo!")
            break

        else:
            print("Opção inválida. Escolha um número de 1 a 5.")


if __name__ == "__main__":
    menu()
