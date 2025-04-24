import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class ContaIterador:
    def __init__(self, contas):
        pass
    
    def __iter__(self):
        pass
    
    def __next__(self):
        pass
    
    
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
        
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            return True      
        
        else:
            print("Operação falhou! O valor informado é inválido.")
            
            
        return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        return True
    
class ContaCorrente(Conta):
        def __init__(self, numero, cliente, limite=500, limite_saques=3):
            super().__init__(numero, cliente)
            self._limite = limite
            self._limite_saques = limite_saques
            
        def sacar(self, valor):
            numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "saque"])
            
            execedeu_limite = valor > self._limite
            execedeu_saques = numero_saques >= self._limite_saques
            
            if execedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")
            
            elif execedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")
                
            else:
                return super().sacar(valor)
            
            return False
        
        def __str__(self):
            return f"""\Agência:{self.agencia}
                        C/C:\t\t{self.numero}
                        Titular:\t{self.cliente.nome}
                        """
                        
class Historico:
        def __init__(self):
            self._transacoes = []
            
        @property
        def transacoes(self):
            return self._transacoes
        
        def adicionar_transacao(self, transacao):
            self._transacoes.append({"tipo": transacao.__class__.__name__,
                                     "valor": transacao.valor,
                                    "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
            
        def gerar_relatorio(self, tipo_trasacao=None):
            pass
        
class Transacao(ABC):
         @property
         @abstractmethod
         def valor(self):
             pass
         
         @abstractmethod
         def registrar(self, conta):
             pass
class Saque(Transacao):
        def __init__(self, valor):
            self._valor = valor
            
        @property
        def valor(self):
            return self._valor
        
        def registrar(self, conta):
            sucesso_transacao = conta.sacar(self.valor)
            
            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)
                
class Deposito(Transacao):
        def __init__(self, valor):
            self._valor = valor
            
        @property
        def valor(self):
           return self._valor
            
        def registrar(self, conta):
            sucesso_transacao = conta.depositar(self.valor)
            
            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)
                
def log_transacao(func):
        return func
        
def menu():
        menu = """\n
        ============== MENU ==============
        [d] \tDepositar
        [s] \tSacar
        [e] \tExtrato
        [nc] \tNova Conta
        [lc] \tListar Contas
        [nu] \tNovo Usuário
        [q] \tSair
        => """
        return input(textwrap.dedent(menu))
    
    
def filtrar_cliente(cpf, clientes):
        clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    
    
def recuperar_conta_cliente(cliente):
        if not cliente.contas:
            print("Cliente não possui contas.")
            return 
        
        return cliente.contas[0]
    
@log_transacao
def depositar(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente: 
            print("Cliente não encontrado.")
            return
        
        valor = float(input("Informe o valor a ser depositado: "))
        transacao = Deposito(valor)
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return 
        
        cliente.realizar_transacao(conta, transacao)
        
@log_transacao
def sacar(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        valor = float(input("Informe o valor a ser sacado: "))
        transacao = Saque(valor)
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        cliente.realizar_transacao(conta, transacao)
        
    
@log_transacao
def exibir_extrato(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente:
            print("Cliente não encontrado.")
            return
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return    
        
        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes
        
        extrato = ""
        if not transacoes:
            extrato = "Não foram realizadas movimentações."
        else:
            for transacao in transacoes:
                extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
                
        print(extrato)
        print(f"\nSaldo: R$ {conta._saldo:.2f}")
        print("=========================================")
        
        
@log_transacao
def criar_cliente(clientes):
        cpf = input("Informe o CPF (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if cliente:
            print("Cliente já cadastrado com este CPF!.")
            return           
        
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")
        
        cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
        
        clientes.append(cliente)
        
        print("Cliente cadastrado com sucesso!")
        
        
@log_transacao
def criar_conta(numero_conta, clientes, contas):
         cpf = input("Informe o CPF do cliente: ")
         cliente = filtrar_cliente(cpf, clientes)
        
         if not cliente:
            print("Cliente não encontrado, fluxo de criação de conta encerrado!.")
            return        
        
         conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
         contas.append(conta)
         cliente.contas.append(conta)
        
         print("Conta criada com sucesso!")
         
def listar_contas(contas):
        for conta in contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
            
def main():
        clientes = []
        contas = []
        
        while True:
            opcao = menu()
            
            if opcao == "d":
                depositar(clientes)
                
            elif opcao == "s":
                sacar(clientes)
                
            elif opcao == "e":
                exibir_extrato(clientes)
                
            elif opcao == "nu":
                criar_cliente(clientes)
                
            elif opcao == "nc":
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
                
            elif opcao == "lc":
                listar_contas(contas)
                
            elif opcao == "q":
                print("Obrigado por utilizar nossos serviços!")
                break
            else:
                print("Opção inválida, por favor selecione novamente a opção desejada.")
                
main()            
                
                             
               
                
                
                         
                                                    
                     
