# Ataque cardíaco no Japão: jovens versus adultos

Estudo comparativo do risco de ataque cardíaco em jovens e adultos japoneses


<a target="_blank" rel="noopener noreferrer" href="https://www.kaggle.com/datasets/ashaychoudhary/heart-attack-in-japan-youth-vs-adult" style="background-color: white;padding: 7px;">View on Kaggle</a>

## Sobre o conjunto de dados

Este conjunto de dados oferece uma exploração aprofundada de incidentes de ataque cardíaco no Japão, com foco nas diferenças entre grupos etários jovens e adultos. Com a crescente prevalência de doenças cardiovasculares em todo o mundo, este conjunto de dados fornece insights críticos sobre os perfis de saúde, fatores de risco e gatilhos potenciais associados a ataques cardíacos entre dois grupos demográficos distintos.

O conjunto de dados abrange uma variedade de recursos, incluindo:

Idade e dados demográficos: detalhamento de casos de ataque cardíaco por jovens e adultos, permitindo análise direcionada de fatores de risco específicos da idade. Indicadores médicos: variáveis ​​como níveis de colesterol, pressão arterial em repouso, frequência cardíaca máxima alcançada e níveis de açúcar no sangue em jejum. Resultados eletrocardiográficos: dados sobre resultados eletrocardiográficos em repouso para avaliar a funcionalidade cardíaca. Métricas físicas: informações como índice de massa corporal (IMC) e angina induzida por exercício. Fatores comportamentais: indicadores de estilo de vida como atividade física, dieta e outros hábitos contribuintes, quando disponíveis. Este conjunto de dados é um recurso valioso para:

Cientistas e analistas de dados: Ideal para modelagem preditiva, como classificação e agrupamento usando aprendizado de máquina. Profissionais de saúde: Para avaliar e abordar riscos de saúde específicos por idade e identificar oportunidades de intervenção precoce. Formuladores de políticas: Útil na elaboração de políticas de saúde pública voltadas para a redução de riscos cardiovasculares. Educadores e pesquisadores: Uma fonte rica para pesquisa acadêmica e estudos de caso. Ao analisar este conjunto de dados, as partes interessadas podem identificar padrões e correlações que contribuem para riscos de ataque cardíaco, desenvolver sistemas de alerta precoce e criar programas de intervenção personalizados. Quer você pretenda realizar análises estatísticas, visualizar tendências ou treinar modelos preditivos, este conjunto de dados oferece uma base sólida para explorar a dinâmica da saúde cardiovascular no Japão.

Observação: é aconselhável realizar o pré-processamento adequado e levar em consideração considerações éticas ao usar este conjunto de dados para análise.

## Prompt

Um prompt foi construido para criar o sistema em Python:

```text

Escreva um código em python que leia um arquivo csv com a seguinte estrutura:

Age,Gender,Region,Smoking_History,Diabetes_History,Hypertension_History,Cholesterol_Level,Physical_Activity,Diet_Quality,Alcohol_Consumption,Stress_Levels,BMI,Heart_Rate,Systolic_BP,Diastolic_BP,Family_History,Heart_Attack_Occurrence,Extra_Column_1,Extra_Column_2,Extra_Column_3,Extra_Column_4,Extra_Column_5,Extra_Column_6,Extra_Column_7,Extra_Column_8,Extra_Column_9,Extra_Column_10,Extra_Column_11,Extra_Column_12,Extra_Column_13,Extra_Column_14,Extra_Column_15

Estes campos acima listado tem caracteres acentuados, crie uma função no momento do carregamento do arquivo CSV que substitua o nome dos campos transformando em snake_case removendo espaços, caracteres em maiusculo,caracteres acentuados e caractere especiais.

Com estes dados da estrutura de campos listado acima crie o programa que use a biblioteca pygame para mostrar botões com alguns insigths de ciência de dados e ao clicar no botão o gráfico e exibido da analise.

Sugira alguns insights que podem ser utilizados baseado na descrição do conjunto de dados a seguir:

Sobre o conjunto de dados
Este conjunto de dados oferece uma exploração aprofundada de incidentes de ataque cardíaco no Japão, com foco nas diferenças entre grupos etários jovens e adultos. Com a crescente prevalência de doenças cardiovasculares em todo o mundo, este conjunto de dados fornece insights críticos sobre os perfis de saúde, fatores de risco e gatilhos potenciais associados a ataques cardíacos entre dois grupos demográficos distintos.

O conjunto de dados abrange uma variedade de recursos, incluindo:

Idade e dados demográficos: detalhamento de casos de ataque cardíaco por jovens e adultos, permitindo análise direcionada de fatores de risco específicos da idade. Indicadores médicos: variáveis ​​como níveis de colesterol, pressão arterial em repouso, frequência cardíaca máxima alcançada e níveis de açúcar no sangue em jejum. Resultados eletrocardiográficos: dados sobre resultados eletrocardiográficos em repouso para avaliar a funcionalidade cardíaca. Métricas físicas: informações como índice de massa corporal (IMC) e angina induzida por exercício. Fatores comportamentais: indicadores de estilo de vida como atividade física, dieta e outros hábitos contribuintes, quando disponíveis. Este conjunto de dados é um recurso valioso para:

Cientistas e analistas de dados: Ideal para modelagem preditiva, como classificação e agrupamento usando aprendizado de máquina. Profissionais de saúde: Para avaliar e abordar riscos de saúde específicos por idade e identificar oportunidades de intervenção precoce. Formuladores de políticas: Útil na elaboração de políticas de saúde pública voltadas para a redução de riscos cardiovasculares. Educadores e pesquisadores: Uma fonte rica para pesquisa acadêmica e estudos de caso. Ao analisar este conjunto de dados, as partes interessadas podem identificar padrões e correlações que contribuem para riscos de ataque cardíaco, desenvolver sistemas de alerta precoce e criar programas de intervenção personalizados. Quer você pretenda realizar análises estatísticas, visualizar tendências ou treinar modelos preditivos, este conjunto de dados oferece uma base sólida para explorar a dinâmica da saúde cardiovascular no Japão.

Observação: é aconselhável realizar o pré-processamento adequado e levar em consideração considerações éticas ao usar este conjunto de dados para análise.

Sobre o programa em python: 

Ao clicar em um destes botões abre uma nova tela e ao clicar em qualquer parte da nova tele a fecha.

Na parte superior da tela principal antes dos botões deve adicionar o titulo:
"Ataque cardíaco no Japão: jovens versus adultos"

Estes botões acima devem ficar um abaixo do outro na cor azul com bordas arredondadas suavemente no centro da tela. 

Atenção para os campos com acentuação pois isso pode causar erros trate esta exceção.


```