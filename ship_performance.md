# Conjunto de dados de agrupamento de desempenho de navios

Melhorando a eficiência dos navios por meio de insights baseados em dados


<a target="_blank" rel="noopener noreferrer" href="https://www.kaggle.com/datasets/jeleeladekunlefijabi/ship-performance-clustering-dataset" style="background-color: white;padding: 7px;">View on Kaggle</a>

## Sobre o conjunto de dados

O Ship Performance Dataset é uma coleção sintética, porém realista, de dados projetados para representar métricas e atributos operacionais importantes de vários tipos de navios no Golfo da Guiné. Este conjunto de dados é personalizado para entusiastas de análise de dados marítimos, praticantes de aprendizado de máquina e profissionais interessados ​​em explorar problemas de clustering, predição e otimização na indústria marítima.

### Motivação
O setor marítimo é um dos componentes mais críticos do comércio global, contribuindo significativamente para o crescimento econômico e a sustentabilidade. Entender o desempenho do navio, a eficiência de combustível e os fatores de custo operacional são essenciais para melhorar a tomada de decisões e minimizar o impacto ambiental.

Este conjunto de dados tem como objetivo fornecer uma plataforma para explorar tendências de desempenho de navios, identificar padrões e resolver desafios marítimos do mundo real por meio de abordagens baseadas em dados.

### Recursos do conjunto de dados

O conjunto de dados consiste em 2736 linhas e 24 colunas, com recursos categorizados em tipos numéricos e categóricos. Abaixo estão alguns destaques principais:

#### Características numéricas

* Speed_Over_Ground_knots: Velocidade média do navio sobre a água (em nós).
* Engine_Power_kW: Potência do motor (em quilowatts).
* Distance_Traveled_nm: Distância total percorrida pelo navio (em milhas náuticas).
* Custo_operacional_USD: Custo operacional total por viagem (em USD).
* Revenue_per_Voyage_USD: Receita gerada por viagem (em USD).
* Eficiência_nm_por_kWh: Eficiência energética calculada em milhas náuticas por quilowatt-hora.

#### Características Categóricas

* Ship_Type: Tipo de navio (por exemplo, petroleiro, navio porta-contêineres, transportador de peixes, graneleiro).
* Route_Type: Tipo de rota de transporte (por exemplo, curta distância, longa distância, transoceânica).
* Engine_Type: Tipo de motor (por exemplo, Diesel, Óleo Combustível Pesado).
* Maintenance_Status: Condição de manutenção do navio (por exemplo, Razoável, Crítico, Bom).
* Weather_Condition: Condições climáticas predominantes durante as viagens (por exemplo, calmo, moderado, agitado).

### Possíveis casos de uso

* Análise Exploratória de Dados (EDA): Identificar tendências e padrões no desempenho e na eficiência operacional do navio.
* Análise de agrupamento: segmente navios com base em métricas de desempenho e atributos categóricos.
Otimização: analise as compensações entre custos operacionais e receita para melhorar a lucratividade.

### Reconhecimento

Este conjunto de dados foi gerado sinteticamente e curado para se assemelhar a dados de desempenho de navios do mundo real. Embora reflita cenários marítimos realistas, não é originário de empresas de transporte ou embarcações reais.

## Prompt

Um prompt foi construido para criar o sistema em Python:

```text

Escreva um código em python que leia um arquivo csv com a seguinte estrutura:

Date,Ship_Type,Route_Type,Engine_Type,Maintenance_Status,Speed_Over_Ground_knots,Engine_Power_kW,Distance_Traveled_nm,Draft_meters,Weather_Condition,Cargo_Weight_tons,Operational_Cost_USD,Revenue_per_Voyage_USD,Turnaround_Time_hours,Efficiency_nm_per_kWh,Seasonal_Impact_Score,Weekly_Voyage_Count,Average_Load_Percentage

Estes campos acima listado tem caracteres acentuados, crie uma função no momento do carregamento do arquivo CSV que substitua o nome dos campos transformando em snake_case removendo espaços, caracteres em maiusculo,caracteres acentuados e caractere especiais.

Com estes dados da estrutura de campos listado acima crie o programa que use a biblioteca pygame para mostrar botões com alguns insigths de ciência de dados e ao clicar no botão o gráfico e exibido da analise.

Sugira alguns insights que podem ser utilizados baseado na descrição do conjunto de dados a seguir:

Sobre o conjunto de dados 

O Ship Performance Dataset é uma coleção sintética, porém realista, de dados projetados para representar métricas e atributos operacionais importantes de vários tipos de navios no Golfo da Guiné. Este conjunto de dados é personalizado para entusiastas de análise de dados marítimos, praticantes de aprendizado de máquina e profissionais interessados ​​em explorar problemas de clustering, predição e otimização na indústria marítima.

O conjunto de dados consiste em 2736 linhas e 24 colunas, com recursos categorizados em tipos numéricos e categóricos. Abaixo estão alguns destaques principais:

Características numéricas

Speed_Over_Ground_knots: Velocidade média do navio sobre a água (em nós).
Engine_Power_kW: Potência do motor (em quilowatts).
Distance_Traveled_nm: Distância total percorrida pelo navio (em milhas náuticas).
Custo_operacional_USD: Custo operacional total por viagem (em USD).
Revenue_per_Voyage_USD: Receita gerada por viagem (em USD).
Eficiência_nm_por_kWh: Eficiência energética calculada em milhas náuticas por quilowatt-hora.

Características Categóricas

Ship_Type: Tipo de navio (por exemplo, petroleiro, navio porta-contêineres, transportador de peixes, graneleiro).
Route_Type: Tipo de rota de transporte (por exemplo, curta distância, longa distância, transoceânica).
Engine_Type: Tipo de motor (por exemplo, Diesel, Óleo Combustível Pesado).
Maintenance_Status: Condição de manutenção do navio (por exemplo, Razoável, Crítico, Bom).
Weather_Condition: Condições climáticas predominantes durante as viagens (por exemplo, calmo, moderado, agitado).


Sobre o programa em python: 

Ao clicar em um destes botões abre uma nova tela e ao clicar em qualquer parte da nova tela a mesma fecha.

Na parte superior da tela principal antes dos botões deve adicionar o titulo:
"Conjunto de dados de agrupamento de desempenho de navios"

Estes botões acima devem ficar um abaixo do outro na cor azul com bordas arredondadas suavemente no centro da tela. 

Adicione mais um botão que mostra todas as estatísticas do comando "desc_stats = df.describe(include='all').T" estas estatisticas devem ser geradas como um arquivo html onde cada campo deve ser exibido em um card com suas estatisticase, apos gerar o arquivo abre em uma nova tela renderizando o html.

Atenção para os campos com acentuação pois isso pode causar erros trate esta exceção.


```