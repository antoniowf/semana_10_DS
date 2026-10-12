class Bimestre:
    def __init__(self, nota1, nota2, tp, pesos=(4, 4, 2)):
        self._validar_nota(nota1, 'nota1')
        self._validar_nota(nota2, 'nota2')
        self._validar_nota(tp, 'tp')

        if len(pesos) != 3 or any(peso <= 0 for peso in pesos):
            raise ValueError('Os pesos devem conter três valores positivos.')

        self.nota1 = nota1
        self.nota2 = nota2
        self.tp = tp
        self.pesos = tuple(pesos)

    @staticmethod
    def _validar_nota(nota, nome):
        if not 0 <= nota <= 10:
            raise ValueError(f'{nome} deve estar entre 0 e 10.')

    def media(self):
        peso_nota1, peso_nota2, peso_tp = self.pesos
        soma_ponderada = (
            self.nota1 * peso_nota1
            + self.nota2 * peso_nota2
            + self.tp * peso_tp
        )
        return soma_ponderada / sum(self.pesos)

class Aluno:
    def __init__(self, nome, disciplina, frequencia):
        if not 0 <= frequencia <= 1:
            raise ValueError('A frequência deve estar entre 0 e 1.')

        self.nome = nome
        self.disciplina = disciplina
        self.frequencia = frequencia
        self.bimestres = []

    def adiciona_bimestre(self, bimestre):
        if not isinstance(bimestre, Bimestre):
            raise TypeError('bimestre deve ser uma instância de Bimestre.')
        self.bimestres.append(bimestre)
        
    def media_anual(self):
        if not self.bimestres:
            raise ValueError('O aluno ainda não possui bimestres cadastrados.')
        return sum(b.media() for b in self.bimestres) / len(self.bimestres)
    
    def status(self):
        ma = self.media_anual()
        
        if self.frequencia < 0.75:
            return 'Reprovado por Falta'
        
        if ma >= 7:
            return 'Aprovado'

        if ma >= 5:
            return 'Recuperação final'

        return 'Reprovado'
    
    def resultado_exame(self, nota_exame):
        Bimestre._validar_nota(nota_exame, 'nota_exame')
        media_final = (self.media_anual() + nota_exame) / 2
        return 'Aprovado' if media_final >= 5 else 'Reprovado'


def ler_float(mensagem, minimo, maximo):
    while True:
        try:
            valor = float(input(mensagem).replace(',', '.'))
        except ValueError:
            print('Digite um número válido.')
            continue

        if minimo <= valor <= maximo:
            return valor
        print(f'Digite um valor entre {minimo} e {maximo}.')


def main():
    print('Bem vindo a calculadora de aprovação UniEscola')
    nome = input('Insira o nome do aluno -> ')
    disciplina = input('Insira a disciplina a ser avaliada -> ')
    frequencia = ler_float('Insira a frequência em porcentagem -> ', 0, 100) / 100
    aluno = Aluno(nome, disciplina, frequencia)

    for numero_bimestre in range(1, 5):
        nota1 = ler_float(f'Insira Nota 1 - {numero_bimestre}º Bimestre: ', 0, 10)
        nota2 = ler_float(f'Insira Nota 2 - {numero_bimestre}º Bimestre: ', 0, 10)
        tp = ler_float(f'Insira Nota do Trabalho - {numero_bimestre}º Bimestre: ', 0, 10)
        aluno.adiciona_bimestre(Bimestre(nota1, nota2, tp))

    print('-' * 50)
    print(f'Média do 1º bimestre: {aluno.bimestres[0].media():.2f}')
    print(f'Média Anual: {aluno.media_anual():.2f}')
    status = aluno.status()
    print(f'Situação do aluno: {status}')

    if status == 'Recuperação final':
        nota_exame = ler_float('Insira a nota do exame final: ', 0, 10)
        print(f'Situação final: {aluno.resultado_exame(nota_exame)}')


if __name__ == '__main__':
    main()
