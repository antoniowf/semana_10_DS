 ![Logo](./images/logo.png)

# Agenda 10 Desenvolvimento de Sistemas I
 [![Python](https://img.shields.io/badge/Python-3.12.3-3776AB?logo=python&logoColor=white)](https://www.python.org/)
---

**Aluno: Antonio Wenceslau de Freitas**  
**Cód. cadastro: SP20AO0206046**

## Plano de organização das funções e procedimentos

Primeiramente foi proposto para a IA modelo **Gemini 3 Fast**, que atuasse conforme o prompt apresentado no enunciado:  
*“Eu quero que você atue como um especialista em desenvolvimento de sistemas e gestor de projetos. Vou apresentar minha ideia de como organizar funções e procedimentos para calcular notas em uma escola. Seu papel é me apresentar dilemas de decisão, sugerir alternativas, questionar minhas escolhas e propor possíveis melhorias na estrutura do código. Me desafie a justificar cada decisão, considerando clareza, eficiência e reutilização das funções”.*

Com base no output da IA foi separado e estruturado o código baseado na *estrutura do ano letivo*, *regras de aprovação e médias, média anual, status do aluno (relação de frequencia e notas) e por fim exame de recuperação.* A partir dessas solicitações de estrutura foi possível visualizar dois objetos **Aluno** e **Bimestre**. Ignorando as funções inicializadoras da classe temos as seguintes classes e funções:

- **Classe Bimestre:**  
  - **Função** @staticmethod \- \_validar\_nota  
  - **Função \- Média**  
- **Classe Aluno:**  
  - **Função \- Adiciona Bimestre**  
  - **Função \- Media Anual**  
  - **Função \- Status**  
  - **Função \- Resultado Exame**  
- **Função \- Ler Float**  
- **Função \- Main**

## Justificativa para cada decisão tomada e código.

O código foi estruturado utilizando Classes a fim de deixar a manutenção do código mais viável e melhor leitura. Primeiramente é declarada a classe Bimestre contendo os atributos nota1, nota2 e tp, com seus respectivos pesos declarados, caso a instituição de ensino pretenda alterar o valor dos pesos de cada nota, é possível alterar de forma prática no código.

*class* Bimestre:  
   *def* \_\_init\_\_(*self*, *nota1*, *nota2*, *tp*, *pesos*\=(4, 4, 2)):  
       *self*.\_validar\_nota(*nota1*, 'nota1')  
       *self*.\_validar\_nota(*nota2*, 'nota2')  
       *self*.\_validar\_nota(*tp*, 'tp')

Em seguida foi criada uma instrução para verificar se os valores dos pesos de cada nota são valores válidos. Caso não sejam um ValueError acontece, apontando para o usuário corrigir os pesos.

       if len(*pesos*) \!= 3 or any(peso \<= 0 for peso in *pesos*):  
           raise ValueError('Os pesos devem conter três valores positivos.')

Um StaticMethod foi utilizado a fim de verificar se a nota inserida pelo usuário está dentro de 0 e 10, caso contrário o código levanta um ValueError.

   @staticmethod  
   *def* \_validar\_nota(*nota*, *nome*):  
       if not 0 \<= *nota* \<= 10:  
           raise ValueError(*f*'{*nome*} deve estar entre 0 e 10.')

A primeira função do código é a média aritmética ponderada das notas, calculando a soma dos valores inseridos multiplicado pelo peso de cada nota dividido pela soma dos pesos em si.

   *def* media(*self*):  
       peso\_nota1, peso\_nota2, peso\_tp \= *self*.pesos  
       soma\_ponderada \= (  
           *self*.nota1 \* peso\_nota1  
           \+ *self*.nota2 \* peso\_nota2  
           \+ *self*.tp \* peso\_tp  
       )  
       return soma\_ponderada / sum(*self*.pesos)

$MB=\frac{(N1\times 4)+(N2\times 4)+(TP\times 2)}{10}$

Dentro da classe Aluno foi necessário criar uma função chamada adiciona\_bimestre, essa função se deu necessária devido a utilização de  uma lista que armazena os valores  de cada nota do bimestre.

   *def* adiciona\_bimestre(*self*, *bimestre*):  
       if not isinstance(*bimestre*, Bimestre):  
           raise TypeError('bimestre deve ser uma instância de Bimestre.')  
       *self*.bimestres.append(*bimestre*)

Foi feita a necessidade de criar uma função de média anual segundo a estrutura solicitada pela IA, baseada no calculo.

$MA=\frac{M{B}_{1}+M{B}_{2}+M{B}_{3}+M{B}_{4}}{4}$  
A função seguinte foi a status, ela verifica os dois valores média anual e frequência, seguindo a seguinte estrutura lógica:

**Aprovado Direto:** Se $MA\geq 7,0$ **E** Frequência $\geq$ 75%.  
**Reprovado por Faltas:** Se Frequência \< 75%, independentemente da nota.  
**Em Recuperação Final:** Se Frequência $\geq$ 75% **E** $5,0\leq MA<7,0$.  
**Reprovado Direto:** Se Frequência $\geq$ 7\\\$ **E** $MA<5,0$.

Em Python a estrutura da função ficou da seguinte maneira.

   *def* status(*self*):  
       ma \= *self*.media\_anual()  
        
       if *self*.frequencia \< 0.75:  
           return 'Reprovado por Falta'  
        
       if ma \>= 7:  
           return 'Aprovado'

       if ma \>= 5:  
           return 'Recuperação final'

       return 'Reprovado'

Conforme solicitado na estrutura proposta, existe uma necessidade de um exame caso o aluno fique de *recuperação final*, dando uma segunda chance para aprovação. Sabendo dessa problemática foi estruturado o seguinte calculo para aprovação nesse requisito, neste caso o aluno está aprovado caso a media final seja maior ou igual a 5, caso contrário ele está automaticamente reprovado.

$MF=\frac{MA+NR}{2}$

Em Python a estrutura se dá pelo seguinte código:

   *def* resultado\_exame(*self*, *nota\_exame*):  
       Bimestre.\_validar\_nota(*nota\_exame*, 'nota\_exame')  
       media\_final \= (*self*.media\_anual() \+ *nota\_exame*) / 2  
       return 'Aprovado' if media\_final \>= 5 else 'Reprovado'

Foi preciso criar uma função chamada ler\_float, essa função valida um número decimal informado pelo usuário, definindo o valor permitido de frequencia (entre 0 e 100), notas de bimestre (entre 0 e 10\) e nota do exame final (entre 0 e 10).

*def* ler\_float(*mensagem*, *minimo*, *maximo*):  
   while True:  
       try:  
           valor \= float(input(*mensagem*).replace(',', '.'))  
       except ValueError:  
           print('Digite um número válido.')  
           continue

       if *minimo* \<= valor \<= *maximo*:  
           return valor  
       print(*f*'Digite um valor entre {*minimo*} e {*maximo*}.')

Por fim temos a função main, ela sendo a função principal, que inicialmente faz uma apresentação pelo CLI, e solicita os inputs do usuário.  
Foi utilizado um laço for para solicitar cada nota de cada bimestre, e assim sendo armazenados na lista bimestres da classe Aluno. A saída em seguida são as médias bimestrais e anual do aluno e seu status, caso o status seja igual a ‘Recuperação Final’, ele pede a nota do exame final, apresentado se o aluno está aprovado ou reprovado.

*def* main():  
   print('Bem vindo a calculadora de aprovação UniEscola')  
   nome \= input('Insira o nome do aluno \-\> ')  
   disciplina \= input('Insira a disciplina a ser avaliada \-\> ')  
   frequencia \= ler\_float('Insira a frequência em porcentagem \-\> ', 0, 100) / 100  
   aluno \= Aluno(nome, disciplina, frequencia)

   for numero\_bimestre in range(1, 5):  
       nota1 \= ler\_float(*f*'Insira Nota 1 \- {numero\_bimestre}º Bimestre: ', 0, 10)  
       nota2 \= ler\_float(*f*'Insira Nota 2 \- {numero\_bimestre}º Bimestre: ', 0, 10)  
       tp \= ler\_float(*f*'Insira Nota do Trabalho \- {numero\_bimestre}º Bimestre: ', 0, 10)  
       aluno.adiciona\_bimestre(Bimestre(nota1, nota2, tp))

   print('-' \* 50)  
   print(*f*'Média do 1º bimestre: {aluno.bimestres\[0\].media()*:.2f*}')  
   print(*f*'Média Anual: {aluno.media\_anual()*:.2f*}')  
   status \= aluno.status()  
   print(*f*'Situação do aluno: {status}')

   if status \== 'Recuperação final':  
       nota\_exame \= ler\_float('Insira a nota do exame final: ', 0, 10)  
       print(*f*'Situação final: {aluno.resultado\_exame(nota\_exame)}')

## Resumo do diálogo com a IA

**Objetivo:** Projetar e refatorar um sistema de cálculo e gestão de notas escolares em Python com foco em boas práticas de arquitetura.  
**Regras de Negócio:** Ano dividido em 4 bimestres (N1, N2 e Trabalho Prático com pesos parametrizáveis), exigência de frequência mínima de 75%, e critérios definidos para aprovação direta, reprovação e exame de recuperação final.  
**Evolução do Design:** O código inicial passou por melhorias críticas para corrigir inconsistências matemáticas, eliminar valores rígidos (*hardcoded*), aplicar programação defensiva com validações robustas e integrar o fluxo completo de recuperação final na interface de linha de comando.  
**Resultado:** Solução orientada a objetos limpa, modular e resiliente, separando responsabilidades entre as classes `Bimestre` e `Aluno`, e preparada para manutenções futuras.