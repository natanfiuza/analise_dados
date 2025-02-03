# Dados demográficos: população, raça, dados de gênero do condado

Dados demográficos em nível de condado: população, raça, gênero


<a target="_blank" rel="noopener noreferrer" href="https://www.kaggle.com/datasets/ashaychoudhary/heart-attack-in-japan-youth-vs-adult" style="background-color: white;padding: 7px;">View on Kaggle</a>

## Sobre o conjunto de dados
Demografia em nível de condado: população, raça, gênero
Visão geral
Este conjunto de dados fornece uma análise detalhada de informações demográficas para condados nos Estados Unidos , derivadas da Pesquisa da Comunidade Americana (ACS) de 2023 do US Census Bureau . Os dados incluem contagens populacionais por gênero, raça e etnia, juntamente com identificadores exclusivos para cada condado usando códigos FIPS de estado e condado .

Recursos do conjunto de dados
O conjunto de dados inclui as seguintes colunas:

*   Condado: Nome do condado.
*   Estado: Nome do estado ao qual o condado pertence.
*   Código FIPS do estado: código do Padrão Federal de Processamento de Informações (FIPS) para o estado.
*   Código FIPS do condado: código FIPS do condado.
*   FIPS: códigos FIPS combinados de estados e condados, um identificador exclusivo para cada condado.
*   População total: população total do condado.
*   População masculina: Número de homens no condado.
*   População feminina: Número de mulheres no condado.
*   Total de respostas sobre raça: total de respostas relacionadas à raça registradas na pesquisa.
*   Branco Somente: Número de indivíduos que se identificam somente como Brancos.
*   Negro ou afro-americano sozinho: Número de indivíduos que se identificam apenas como negros ou afro-americanos.
*   Hispânico ou latino: Número de indivíduos que se identificam como hispânicos ou latinos.

## Prompt

Um prompt foi construido para criar o sistema em Python:

```text

Escreva um código em python que leia um arquivo csv com a seguinte estrutura:

County,State,State FIPS Code,County FIPS Code,FIPS,Total Population,Male Population,Female Population,Total Race Responses,White Alone,Black or African American Alone,Hispanic or Latino

Estes campos acima listado tem caracteres acentuados, crie uma função no momento do carregamento do arquivo CSV que substitua o nome dos campos transformando em snake_case removendo espaços, caracteres em maiusculo,caracteres acentuados e caractere especiais.

Com estes dados da estrutura de campos listado acima crie o programa que use a biblioteca pygame para mostrar botões com alguns insigths de ciência de dados e ao clicar no botão o gráfico e exibido da analise.

Sugira alguns insights que podem ser utilizados baseado na descrição do conjunto de dados a seguir:

Sobre o conjunto de dados
Demografia em nível de condado: população, raça, gênero

Visão geral
Este conjunto de dados fornece uma análise detalhada de informações demográficas para condados nos Estados Unidos , derivadas da Pesquisa da Comunidade Americana (ACS) de 2023 do US Census Bureau . Os dados incluem contagens populacionais por gênero, raça e etnia, juntamente com identificadores exclusivos para cada condado usando códigos FIPS de estado e condado .

Recursos do conjunto de dados
O conjunto de dados inclui as seguintes colunas:

Condado: Nome do condado.
Estado: Nome do estado ao qual o condado pertence.
Código FIPS do estado: código do Padrão Federal de Processamento de Informações (FIPS) para o estado.
Código FIPS do condado: código FIPS do condado.
FIPS: códigos FIPS combinados de estados e condados, um identificador exclusivo para cada condado.
População total: população total do condado.
População masculina: Número de homens no condado.
População feminina: Número de mulheres no condado.
Total de respostas sobre raça: total de respostas relacionadas à raça registradas na pesquisa.
Branco Somente: Número de indivíduos que se identificam somente como Brancos.
Negro ou afro-americano sozinho: Número de indivíduos que se identificam apenas como negros ou afro-americanos.
Hispânico ou latino: Número de indivíduos que se identificam como hispânicos ou latinos.


Sobre o programa em python: 

Ao clicar em um destes botões abre uma nova tela e ao clicar em qualquer parte da nova tele a fecha.

Na parte superior da tela principal antes dos botões deve adicionar o titulo:
"Dados demográficos: população, raça, dados de gênero do condado"

Estes botões acima devem ficar um abaixo do outro na cor azul com bordas arredondadas suavemente no centro da tela. 

Adicione mais um botão que mostra todas as estatísticas do comando abaixo:
desc_stats = df.describe(include='all').T

Atenção para os campos com acentuação pois isso pode causar erros trate esta exceção.


```