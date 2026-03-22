# Memória de IA (AI Reasoning State)

Este arquivo foi criado para manter a persistência do raciocínio e das decisões arquiteturais tomadas durante o desenvolvimento do projeto **Painel - ENADE**, garantindo que o progresso não se perca ao trocar de máquina ou iniciar uma nova conversa.

## 🕒 Histórico Recente e Decisões Arquiteturais

### 1. Refatoração Premium e Multi-Páginas (21/03/2026)
* O aplicativo foi convertido de uma visualização única para um Hub de navegação via `st.session_state`. 
* As páginas agora são controladas pelas funções `show_home()`, `show_dashboard()`, `show_cursos()` e `show_estudantes()`.
* Desenvolvemos uma folha de CSS customizada utilizando tipografia **'Inter'**, glassmorphism (fundos translúcidos), e elementos focados no verde oficial do Instituto Federal do Espírito Santo (IFES).

### 2. Painel: Dados dos Cursos (22/03/2026)
Implementamos uma aba onde destrinchamos o desempenho acadêmico:
* **Raio-X da Prova:** Extraímos as chaves `Nota Bruta - FG` (Formação Geral) e `Nota Bruta - CE` (Componente Específico) que não eram usadas. Criamos um Gráfico de Barras Agrupado do Plotly para identificar se os estudantes estão com maior defasagem no básico ou no técnico.
* **Métrica de Evasão (Abstenção):** Mapeamos `Inscritos` x `Participantes` e desenhamos um BarChart em escala de vermelho apontando a abstenção percentual, servindo como alerta para as coordenações dos Campi.

### 3. Integração de Microdados: Informações do Estudante (22/03/2026)
O maior avanço técnico do projeto.
* Descobrimos que o INEP insere as respostas do *Questionário do Estudante* em abas ocultas `Arq_5` e `Arq_6` nos mesmos arquivos Excel agregados.
* **Engenharia de Dados (`load_microdata`)**: 
  - Criamos um cache secundário que varre essas abas linha por linha (microdados). 
  - Fizemos um `pd.merge` usando a chave estrangeira `CO_CURSO` para conseguir parear dados sem identificação nominal do estudante de volta à "Área de Avaliação" e "Campus".
* Visualizações entregues nesta página:
  - **Distribuição de Idade:** Histograma dinâmico mostrando a concentração demográfica dos egressos + Média geral exata.
  - **Distribuição de Gênero:** Gráfico de "Donut" revelando o balanceamento (% Masculino / % Feminino) dependendo dos filtros globais acionados.

### 4. Filtros Globais Dinâmicos
* Extraímos as antigas centenas de linhas de filtros repetidos para uma função helper compacta chamada `render_filters(source_data)`.
* Desta forma, o usuário agora define Ano, Campus, Curso e Modalidade na tela que desejar, e o sistema devolve o `dataframe` lapidado. Isso garante que a Dashboard de Cursos e a Dashboard de Estudantes operem sobre as mesmas bases sem conflito.

---
## 🎯 Próximos Passos (Lista de Tarefas Pendentes)
* O App está virtualmente completo sob o escopo proposto (Home + 3 Ambientes de Análise). 
* A próxima etapa técnica válida seria: **Hospedar de forma definitiva** o código na nuvem através do *Streamlit Community Cloud*, conectando-o ao repesitório do GitHub.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada)*
