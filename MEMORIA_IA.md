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

---
## 🎯 Próximos Passos (Lista de Tarefas Pendentes)
* Como o sistema base contendo o Hub Principal, os Módulos Avaliativos, Desempenho Isolado e o Observatório do Estudante estão 100% integrados e bonitos, ele já possui plenas ferramentas visuais comerciais para o usuário final.
* A recomendação oficial de continuidade técnica: **Deixar de rodar no localHost**. Realizar o deploy profissionalmente apontando a Master do respositório (GitHub) para uma infraestrutura gratuita como a *Streamlit Community Cloud*.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada pelo usuário)*
