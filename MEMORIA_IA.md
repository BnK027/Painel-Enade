# Memória de IA (AI Reasoning State)

Este arquivo foi criado para manter a persistência do raciocínio e das decisões arquiteturais tomadas durante o desenvolvimento do projeto **Painel - ENADE**, garantindo que o progresso não se perca ao trocar de máquina ou iniciar uma nova conversa.

## 🕒 Histórico Recente e Decisões Arquiteturais

### 1. Refatoração Premium e Multi-Páginas (21/03/2026)
* O aplicativo foi convertido de uma tela única para um Hub de navegação via `st.session_state`. 
* As páginas agora são geridas de forma super limpa pelas sub-funções `show_home()`, `show_dashboard()`, `show_cursos()` e `show_estudantes()`.
* Desenvolvemos uma folha de CSS customizada utilizando tipografia **'Inter'**, glassmorphism (fundos translúcidos), e paleta de verdes de acordo com o manual da marca oficial do IFES.

### 2. Painel: Dados dos Cursos (22/03/2026)
Implementamos uma aba onde destrinchamos o desempenho acadêmico puro das turmas:
* **Raio-X da Prova:** Extraímos do INEP as chaves `Nota Bruta - FG` (Formação Geral) e `Nota Bruta - CE` (Componente Específico). Desenhamos um Gráfico de Barras Agrupado do Plotly para identificar objetivamente se os estudantes vão melhor no ciclo disciplinar básico ou nas metodologias técnicas de cada departamento acadêmico.
* **Métrica de Evasão (Abstenção):** Mapeamos matematicamente a razão entre *Inscritos* x *Participantes*. Desenhamos um BarChart em tons de vermelho apontando o percentual de abstenção como um alerta crucial para as coordenações dos Campi verificarem focos de abandono de prova.

### 3. Painel: Informações do Estudante (Integração de Microdados) (22/03/2026)
O maior avanço técnico e de Engenharia de Dados do projeto até agora. Construímos um ecossistema com 4 Gráficos interativos dedicados *apenas* à demografia desidentificada dos alunos:
* Programamos um loop sistêmico (Python) inteligente mapeando as abas `Arq_5`, `Arq_6`, `Arq_8` e `Arq_14`. Estas abas contém microdados encriptados do Inep (Questionário do Estudante).
* **Idade (`NU_IDADE`):** Plotamos a demografia usando um Histograma em blocos e contabilizamos a IDADE MÉDIA de acordo com os filtros de curso/campus na lateral.
* **Gênero (`TP_SEXO`):** Convertidas as strings cruas 'M' e 'F' conectadas à visualização em Rosca (Donut Chart) evidenciando o balanço dos gêneros na sala de aula.
* **Cor/Raça (`QE_I02`):** Invocamos Dicionários de Decodificação do ENADE ('A'-> Branca, 'B'-> Preta...) e plotamos o balanço de cotas e miscigenação em Gráficos de Barras Horizontais.
* **Renda Familiar (`QE_I08`):** Adicionamos uma segunda tradução de Dicionários Inep (`Arq_14`), transformando as letras num modelo de Barras Horizontais com a Renda Familiar Média, ajustando rigidamente e ordenando o Eixo Y para escalar das opções mais pobres ("Até 1,5 SM") para as famílias mais ricas ("Mais de 30 SM").

### 4. Filtros Globais Dinâmicos
* Extraímos as antigas centenas de linhas de sub-rótulos e filtros repetidos de cada página em prol de uma Função Helper arquitetural de ponta batizada `render_filters()`.
* Desta forma, o App inteiro filtra o dado global antes mesmo das sub-telas o renderizar, ou seja, filtrar o curso impacta diretamente todos os três novos painéis nativos de uma única vez. Código sem repetições. Limpo e eficiente!

### 5. Super-Página de Estudantes e Abas Analíticas (23/03/2026)
* A página **INFOS ESTUDANTE** foi inteiramente re-arquitetada visando suportar dezenas de gráficos em um sistema de "Abas" (`st.tabs()`), compartimentando a inteligência para não poluir a interface.
* Integramos 8 novas partições de Microdados ENADE (`Arq_10`, `Arq_11`, `Arq_16`, `Arq_17`, `Arq_21`, `Arq_29`, `Arq_31`, `Arq_32`) traduzindo fielmente as chaves do dicionário oficial estruturado pelo INEP.
* **Perfil Socioeconômico:** Implementado cruzamento de capital cultural (Escolaridade Parental nas categorias `QE_I04` e `QE_I05`) e dedicação profissional concorrente (Situação de Trabalho em `QE_I10`).
* **Acesso e Permanência:** Plotadas estatísticas vitais validando eficácia de Cotas/Ações Afirmativas (`QE_I15`) e dependência de Bolsas/Financiamentos Acadêmicos (`QE_I11`).
* **Rotina e Engajamento:** Comprovamos a intensidade acadêmica via Horas de Estudo extraclasse (`QE_I23`) unida aos motivadores originais de busca pela carreira técnica (`QE_I25`).
* **Resolução de Bug Crítico (Gráfico de Cotas):** Durante a criação da aba de Acesso e Permanência no `app.py`, um erro visual onde a biblioteca Plotly tentava buscar uma coluna Inexistente chamada `Relevância` quebrou a Tela de Estudantes *(ValueError)*. Removemos e refatoramos instantaneamente a linha de código duplicada (em tempo-real) e restauramos 100% da visualização e estabilidade do sistema local.

### 6. Painel: Questionário do Estudante (Processo Formativo) (28/03/2026)
* Adicionamos a aba **QUEST. ESTUDANTE**, conectada à extração de dados da partição `Arq_4` dos microdados.
* Mapeamos as questões socioeducacionais em formato Likert (1 a 6) para medir as percepções sobre professores, infraestrutura e formação cidadã.
* Implementamos o dicionário de variáveis via código, incorporando enunciados oficiais (ex: *QE_I27 a QE_I33*, *QE_I39* e *QE_I41*) extraídos do questionário.
* Desenvolvemos a interface baseada no modelo original: *BarChart* em Plotly (azul `#103d6d`), *tooltips* com percentuais convertidos das escalas Likert, e cartões de métricas dinâmicos (Inscritos e Participantes).

---
## 🎯 Próximos Passos (Lista de Tarefas Pendentes)
* Como o sistema base contendo o Hub Principal e os 5 módulos verticais encontram-se 100% integrados, analíticos e estáveis, a aplicação possui agora nivel pleno de maturidade *(Production-Ready)*.
* A infraestrutura de versionamento (**Git** e **GitHub Desktop**) já foi devidamente instalada na máquina (Winget).
* O próximo passo oficial é **realizar o controle de versão**, efetuando um *Commit* total do Painel ENADE utilizando a interface do GitHub Desktop.
* Finalmente, efetuar o **Deploy Master**: conectar este repositório git recém criado à infraestrutura de servidores da **Streamlit Community Cloud**, gerando um link público acessível.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada pelo usuário)*
