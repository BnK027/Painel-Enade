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

### 7. Overhaul Visual e CSS Premium (28/03/2026)
* A aplicação inteira recebeu uma injeção de CSS em nível de produção focado em *Glassmorphism*.
* A tipografia global foi revertida para **Inter** após testes, por conferir um aspecto mais sóbrio e tipicamente analítico ao dashboard em comparação à *Plus Jakarta Sans*.
* Refatoramos os contornos e sombras (*drop-shadows*) de todos os painéis e gráficos nativos do Plotly para parecerem componentes "flutuantes".
* Neutralizamos a "Barra Branca" anômala isolando o componente *ENUNCIADO DA QUESTÃO* em uma moldura/card sólida e válida, o que também evitou o corte do texto de enunciados longos.
* **Resolução Definitiva de Layouts e Texto Cortado:** 
  1. Corrigimos um erro onde as caixas de seleção (*Selectbox*) estavam achatando os textos horizontalmente na base das letras: ao remover de nosso CSS o `padding` minúsculo e fixar um `line-height: 1.6`, o *Streamlit* voltou a escalar naturalmente as listas com textos longos sem decepá-los.
  2. Impedimos o Plotly de ocultar finais de rótulos muito grandes contendo quebra de linha embutida (Ex: "NÃO SEI RESPONDER"). Injetando margens base irredutíveis (`b=100`), expandindo a altura do layout (`height=500`) e zerando ângulos textuais (`tickangle=0`), o Plotly passou a dispor até três ou quatro linhas perfeitamente legíveis na métrica de Respostas do Estudante.

### 8. Recuperação Avançada do Dicionário do Questionário do Estudante (28/03/2026)
* Como percebido durante a análise dos microdados, a aba `DICIONÁRIO_ARQUIVOS` não possuía o enunciado individualizado das questões formativas de Escala Likert (partindo de `QE_I27` em diante), agrupando-as sob o mesmo rótulo genérico.
* **Solução e Raciocínio (Metadados Ocultos):** Vasculhamos todos os arquivos locais do ENADE e descobrimos que **a aba `Microdados` contém o verdadeiro mapa de legendas na Coluna A e Coluna D**.
* Construimos um script iterativo de extração automatizado (`extract_missing_qe.py`) isolando e varrendo os metadados da Coluna A (onde os códigos `QE_I27` ao `QE_I82` residiam em linhas perdidas) conectando as chaves à Coluna D (onde residia o texto original do formulário lido pelo aluno).
* Exportamos as chaves recuperadas validando que as turmas contavam com exatas 68 questões oficiais nas versões padrão, pulando para 92 questões em 2021 (devido a perguntas sobre a pandemia). Todo esse conjunto léxico foi extraído com segurança para o repositório como um módulo utilizável (`qe_dictionary.py`).

### 9. Impacto da Pandemia de COVID-19 (Questionário do Estudante 2021) (29/03/2026)
* Após mapearmos as 92 questões exclusivas da edição de 2021 no dicionário (`qe_dictionary.py`), notamos que o Streamlit não renderizava perguntas acima do `QE_I81`. 
* **Diagnóstico de Engenharia de Dados**: Isolamos que o INEP armazenou os microdados relacionados à pandemia estritamente na planilha/arquivo sob a aba oculta `Arq_43` (diferente da aba `Arq_4` padrão das edições anteriores).
* **Solução:** Expandimos o motor de inferência da função `load_microdata()` no `app.py`, capturando o `Arq_43` de forma nativa e unificando-o ao ecossistema de memória principal.
* Na tela **QUEST. ESTUDANTE**, a aplicação agora descobre de forma dinâmica qual DataFrame (`df_arq4` comum ou `df_arq43` exclusivo da pandemia) abarca a Questão de I82 a I92 selecionada no *dropdown*, aplicando o cálculo de KPIs, Likerts (1 a 9) e ToolTips de forma invisível ao usuário final.

### 10. Filtros em Cascata Omnidirecional (Inteligência de Renderização) (29/03/2026)
* Para evitar que o usuário selecionasse um Campus e acidentalmente pudesse filtrar um Curso que não existe naquela unidade (ou vice-versa), re-arquitetamos a lógica da topologia de `render_filters()`.
* **Solução**: O Streamlit agora constrói listas de opções usando uma topologia baseada no `st.session_state`. Em vez de filtrar linearmente de cima para baixo, o sistema cruza virtualmente todas as categorias escolhidas: cada *caixa de seleção* carrega uma sub-matriz de dados filtrada ativamente por **todas as outras** regras vigentes.
* **Exemplo Omnidirecional**: Ao selecionar o ano de `2021`, a barra de **Curso** já omite graduações que não fizeram prova naquele ano, e a barra de **Campus** mostra apenas os campi que registraram participantes. Qualquer filtro que você toque, atualiza instantaneamente as opções exclusivas dos outros quatro, de forma completamente coesa, eliminando resultados vazios ou combinações matematicamente inviáveis.

### 11. Redesign Premium Light Mode / UI Inspirada em Glassmorphism (29/03/2026)
* O solicitante nos forneceu uma referência em layout contendo um dashboard clássico de Data Science, porém solicitou que utilizássemos o formato "Modo Claro" em união à paleta de cores institucional do IFES (tons de verde). 
* Extrapolamos essa ideia e estilizamos **100% dos visuais nativos** do Streamlit. 
* **Configuração Core (`config.toml`)**: Forçamos a UI base para interagir no espectro `light`, com fundos brancos acinzentados (`#F4F7F6`) e tipografia azul escuro (`#103d6d`).
* **Glassmorphism Claro**: Adicionamos ao CSS as transparências translúcidas fosfatizadas (`rgba(255, 255, 255, 0.75)`) acompanhados de desfoque (`backdrop-filter: blur(20px)`), criando uma volumetria de painéis limpos muito similar aos melhores painéis de BI corporativos.
* Gráficos do Plotly herdaram papéis e plot backgrounds transparentes para que as barras e eixos "flutuem" harmoniosamente dentro dos cartões em brancos com subtons de primárias verdes (`#32A041` e `#2c8c44`).

---
### 12. Otimização Mobile e Legibilidade de Gráficos (08/05/2026)
* Implementamos uma melhoria crítica na visualização de dados para dispositivos móveis, focada na aba de **Questões do Estudante**.
* **Rotação de Legendas:** Ajustamos o ângulo dos rótulos do eixo X em todos os gráficos de barra para **-90 graus**. Isso impede que nomes de categorias longos (como "Concordo Totalmente") se sobreponham em telas estreitas de celulares.
* **Layout Responsivo:** Refatoramos a exibição dos enunciados das questões. No desktop, eles mantêm um layout centralizado e elegante; no mobile, expandem-se para largura total, garantindo leitura confortável.
* **Ajustes de Margem:** Expandimos a margem inferior dos gráficos (`margin-bottom=150`) e aumentamos a altura total para `600px`, permitindo que o Plotly renderize todo o texto das legendas sem cortes.

### 13. Integração e Engenharia de Dados do ENADE 2017 (08/05/2026)
* Realizamos a extração e consolidação dos **Microdados ENADE 2017** (padrão LGPD fragmentado em 42 arquivos TXT).
* **Processo de ETL:** Criamos um script de extração (`extract_2017.py`) que filtrou os 877 registros do IFES (`CO_IES: 1808`) entre mais de 500 mil linhas, unificando dados de performance (notas), sociodemográficos e respostas do questionário em um novo arquivo `Enade_2017_Ifes.xlsx`.
* **Identificação de Cursos:** Implementamos uma lógica de mapeamento cruzado com a base de 2021 para recuperar nomes reais de cursos e campi que não constavam nos microdados brutos de 2017.
* **Nova Visualização:** Desenvolvemos a `views/visao_2017.py` e atualizamos o roteador do `app.py` para incluir o ano de 2017 como uma nova plataforma analítica funcional.

### 14. Resolução de Conflitos Git e Limites de Armazenamento (08/05/2026)
* Corrigimos um erro de *Push* rejeitado pelo GitHub devido ao limite de **100MB por arquivo** (causado pelos arquivos TXT brutos de 2017 que possuem até 134MB).
* **Saneamento do Repositório:** Atualizamos o `.gitignore` para excluir permanentemente a pasta `microdados_Enade_2017_LGPD/` e limpamos o histórico local de commits (`git reset --soft`), garantindo que apenas a base consolidada e leve de 2017 seja enviada para a nuvem.

---
### 15. Integração e Engenharia de Dados do ENADE 2018 (08/05/2026)
* Expandimos a arquitetura para suportar o **ENADE 2018**.
* Desenvolvemos a `views/visao_2018.py`, seguindo o padrão de "Abas" (Notas, Cursos, Estudante, Questionário) e garantindo a consistência visual com os anos de 2017, 2019 e 2021.
* Implementamos a lógica de filtragem omnidirecional para o ano de 2018, conectando os microdados demográficos e de questionário.

### 17. Saneamento de Dados ENADE 2017 via EMEC (10/05/2026)
* Realizamos uma limpeza profunda na base `Enade_2017_Ifes.xlsx` utilizando a planilha oficial `Dados Cursos EMEC finalizado.xlsx`.
* **Correção de Nomenclatura:** Eliminamos 15 ocorrências de nomes genéricos (ex: "Curso 123569") substituindo-os pelos nomes reais extraídos do EMEC.
* **Refino Geográfico (Campi):** Mapeamos a coluna `CAMPUS` para todos os registros que estavam marcados como "IFES (Sede)" ou "Desconhecido", utilizando a relação Código de Curso -> Município -> Nome do Campus oficial.
* **Integridade da Base:** As correções foram replicadas em todas as abas críticas (`Enade`, `Microdados` e `Cursos`), garantindo que tanto os gráficos consolidados quanto os de microdados sociodemográficos exibam os rótulos corretos.

### 18. Análise de Performance: Componente Específico (CE) (11/05/2026)
* Implementamos uma funcionalidade granular para analisar o desempenho dos alunos questão por questão na parte objetiva do **Componente Específico (CE1 a CE27)**.
* **Engenharia de Dados (Arq_3B):** Refatoramos o motor de carregamento no `app.py` para processar a aba `Arq_3B` (respostas individuais codificadas) e `Arq_3` (gabaritos oficiais).
* **Módulo Compartilhado (`quest_especifico.py`):** Criamos uma visualização isolada e protegida que impede a mistura de dados entre cursos diferentes (essencial, pois cada CE é único por área).
* **Visualizações Avançadas:**
    * **Gráfico de Acertos vs Erros:** Barras agrupadas com percentuais e quantidades absolutas.
    * **Heatmap de Desempenho:** Mapa de calor (Red-to-Green) para identificação instantânea de questões críticas.
    * **Tabela de Indicadores:** Detalhamento de questões anuladas, brancas e ausências.
* **Integração Sistêmica:** A nova aba **📊 QUEST. ESPECÍFICO** foi integrada nas visões de 2018, 2019, 2021 e 2022.

### 19. Redação e Exportação do Artigo Acadêmico (12/05/2026)
* Elaboramos um rascunho completo de artigo científico descrevendo a metodologia, arquitetura (Streamlit + Antigravity) e funcionalidades do painel, seguindo a estrutura de tópicos solicitada.
* **Exportação para PDF:** Desenvolvemos um script de automação (`fpdf2`) para converter o rascunho Markdown em um documento PDF formatado com tipografia Unicode (DejaVuSans) para suportar caracteres da língua portuguesa.
* **Organização de Workspace:** Conforme solicitação do usuário, o artigo e seus scripts foram mantidos fora da estrutura de código fonte do Dashboard para manter o repositório focado exclusivamente na aplicação. O PDF final foi movido para a pasta de Documentos principal do usuário.

### 20. Script de Deploy Cirúrgico e Manutenção (12/05/2026)
* Criamos o **`Salvar_Producao_Github.bat`**, um script automatizado que realiza o deploy no GitHub adicionando apenas os arquivos estritamente necessários para o funcionamento no Streamlit Cloud.
* Isso evita problemas de limite de tamanho (bloqueando arquivos binários pesados ou backups de microdados LGPD) e garante que o ambiente de produção esteja sempre sincronizado e leve.

### 21. Módulo de Ranking do Questionário do Estudante (Top 3 Positivas/Negativas) (16/05/2026)
* **Visualização Analítica Centralizada:** Desenvolvemos o módulo `views/quest_ranking.py` para calcular e renderizar a percepção discente do Questionário do Estudante (`QE_I`). Ele calcula a porcentagem de concordância (Likert 4, 5, 6) e discordância (Likert 1, 2, 3) para cada questão.
* **Componentes Interativos:** A interface agora expõe três selectboxes complementares: a lista geral de perguntas, as **Top 3 avaliações mais positivas** e as **Top 3 avaliações mais negativas**.
* **Deduplicação de Código:** Refatoramos e atualizamos de forma integrada todas as visões anuais (`visao_2017.py` a `visao_2022.py`) para utilizar este módulo unificado, eliminando lógica duplicada e facilitando manutenções futuras.

### 22. Atualizações do Artigo Científico e Referências (COBENGE 2026) (16/05/2026)
* **Aprimoramento do Manuscrito:** Revisamos o artigo para a submissão do COBENGE 2026 com base nos feedbacks do Prof. Wagner, refinando a introdução, metodologia e discussões.
* **Consolidação Bibliográfica:** Adicionamos novas referências e citações pertinentes do campo de Business Intelligence educacional e avaliação do ENADE (ex: Lima 2018, Sathler 2023, Otsubo 2024, Barreto & Freitas 2020).
* **Compilação Automatizada para Word:** Desenvolvemos o script `make_docx.py` para compilar o arquivo Markdown `Documentos Artigo/Artigo_Completo_Citado.md` em um arquivo formatado `.docx` (`Documentos Artigo/Artigo_Completo_Citado.docx`) de acordo com as regras de submissão do evento.

### 23. Estruturação da Análise de Candidato x Vaga (Módulo Standalone) (16/05/2026)
* **Análise do Processo Seletivo:** Estruturamos o módulo `views/visao_cand_vaga.py` para processar dados de concorrência dos processos seletivos do IFES (`Cand_Vaga_Unico.xlsx`).
* **Indicadores e Gráficos:** O painel standalone apresenta KPIs de inscritos, vagas e relação candidato/vaga, acompanhados de gráficos de concorrência de cursos (Top 15), distribuição por modalidade de ensino, vagas vs inscritos por campus e histórico semestral.

### 24. Validação de Consistência e Limpeza de Metadados (18/05/2026)
* **Scripts de Validação:** Desenvolvemos scripts de inspeção (`scratch/check_raw_xlsx.py`) para validar o alinhamento das colunas e a consistência das abas de microdados e informações cadastrais entre todas as planilhas consolidadas (`Enade_2017_Ifes.xlsx` a `Enade_2022_Ifes.xlsx`).

### 25. Correção de Inércia no Seletor do Questionário do Estudante (12/06/2026)
* **Resolução de Bug no st.selectbox:** Corrigimos uma falha na aba "Questão do Estudante" onde os usuários precisavam selecionar uma questão intermediária antes de conseguir atualizar o gráfico para a primeira opção do ranking selecionado.
* **Uso de Placeholders Dinâmicos:** Resolvemos a inércia implementando `index=None` nos selectboxes de rankings e definindo o parâmetro `placeholder` dinamicamente com o valor do primeiro elemento (`opcoes[0]`, `pos_opts[0]`, `neg_opts[0]`). Isso mantém a pergunta visível, mas força o acionamento do callback de atualização ao clicar.
* **Ajuste de Cor de Placeholder via CSS:** Adicionamos regras CSS personalizadas no `app.py` para garantir que o texto do placeholder (que agora é a nossa questão destacada por padrão) seja renderizado na cor escura institucional (`#103d6d` com opacidade total), eliminando o tom cinza-claro esmaecido padrão do Streamlit.

### 26. Esclarecimento de Acesso a Planilhas no MS Excel (15/06/2026)
* **Problema de Visibilidade de Abas:** Identificamos que a ausência de visualização direta de abas importantes (como `Arq_3B` do arquivo de 2019) no Microsoft Excel deve-se ao limite de espaço na interface de visualização, que oculta partes das 41 planilhas internas.
* **Instrução de Navegação:** Orientamos o usuário a acessar a lista completa de abas ocultas clicando com o botão direito nas setas de paginação de planilhas no canto inferior esquerdo do Excel.
* **Manutenção do Código-Fonte:** O usuário optou por rejeitar qualquer alteração ou cópia temporária de arquivos via código, mantendo o carregamento de dados do painel do Streamlit inalterado para preservar a arquitetura de leitura atual.

### 27. Engenharia de Dados: Criação do Arq_3B para 2017 (15/06/2026)
* **Reconstrução de Dados Faltantes:** Identificamos que a planilha original de 2017 não possuía a aba derivada `Arq_3B` (que mapeia acertos granulares por questão no Componente Específico).
* **Script de ETL Especializado:** Criamos um script autônomo (`extract_ce_2017.py`) que processou o arquivo bruto massivo de 566MB (`Enade 2017.xlsm`), capturando a aba `microdados2017_arq3`.
* **Desmembramento Dinâmico:** Quebramos as strings de gabarito `DS_VT_ACE_OFG` (8 caracteres) e `DS_VT_ACE_OCE` (27 caracteres) em colunas atômicas matemáticas (`Ob1` a `Ob8` e `CE1` a `CE27`).
* **Injeção Silenciosa:** Anexamos com sucesso as planilhas faltantes `Arq_3` e `Arq_3B` ao consolidado `Enade_2017_Ifes.xlsx`, habilitando nativamente o painel de "Questões Específicas" também para 2017.

---
## 🎯 Próximos Passos (Lista de Tarefas Pendentes)
* `[x]` **Análise de Componente Específico:** Implementado para 2018-2022.
* `[x]` **Artigo do Projeto:** Rascunho inicial e PDF gerados e entregues.
* `[x]` **Destaques do Questionário (Top 3 Positivas/Negativas):** Módulo e visualizações implementadas.
* `[x]` **Revisão Bibliográfica do Artigo:** Atualizada com as sugestões do professor.
* `[x]` **Integração CE 2017:** Verificar se os microdados de 2017 permitem a mesma análise de acertos/erros por questão (a estrutura do `Arq_3B` em 2017 costuma ser diferente).
* `[ ]` **Integração da Visão Candidato x Vaga:** Avaliar a inclusão definitiva do painel no menu principal do `app.py`.
* `[ ]` **Deploy Master:** Realizar o push final via `Salvar_Producao_Github.bat` e verificar o link oficial.
* `[ ]` **Revisão Final de Coerência:** Validar se os nomes de cursos mapeados via EMEC in 2017 estão consistentes com as outras visões.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada)*


