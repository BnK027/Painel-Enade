TÍTULO DO TRABALHO: ANÁLISE DE MICRODADOS DO ENADE POR MEIO DE DASHBOARD INTERATIVO PARA GESTÃO ACADÊMICA

1 INTRODUÇÃO

O Exame Nacional de Desempenho dos Estudantes (Enade), componente curricular obrigatório, constitui-se como uma das principais ferramentas de diagnóstico da qualidade do ensino superior no Brasil. Para além da atribuição de conceitos, o exame gera um volume massivo de microdados que, se devidamente processados, oferecem um panorama detalhado sobre o processo de ensino-aprendizagem. No entanto, a complexidade inerente à estrutura desses dados brutos, disponibilizados anualmente pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep), muitas vezes limita sua utilização prática pelos Núcleos Docentes Estruturantes (NDE) e gestores acadêmicos.

A relevância da análise aprofundada dos microdados reside na possibilidade de transcender a nota final, permitindo uma investigação granular em duas frentes: o desempenho cognitivo e a percepção discente. No campo do desempenho, Sathler (2023) demonstra que a desagregação dos resultados em níveis de acertos e erros por questão é crucial para identificar temas de maior dificuldade e ajustar estratégias pedagógicas de forma direcionada. Essa perspectiva é reforçada por Cunha, Sales e Santos (2021), que propõem o uso de técnicas de análise automática de dados para extrair informações relevantes e monitorar a evolução das competências previstas nas Diretrizes Curriculares Nacionais (DCNs).

Complementarmente, a análise do Questionário do Estudante revela as condições de contorno que moldam o sucesso acadêmico. Como aponta Lima (2018), a percepção dos estudantes sobre a organização didático-pedagógica e a infraestrutura é um fator determinante para compreender os resultados obtidos no exame. Esta visão multidimensional é corroborada por Rodrigues (2024), que explora como as vivências acadêmicas impactam a adaptação ao ambiente universitário em cursos de Engenharia, evidenciando que os resultados acadêmicos são indissociáveis da experiência integral.

Apesar da riqueza informativa, a transição de relatórios estáticos para modelos de análise dinâmica ainda representa um desafio técnico nas Instituições Federais. Conforme discutido por Barreto e Freitas (2020), o uso de ferramentas de Business Intelligence (BI) surge como uma solução estratégica para a consolidação de dados e a visualização intuitiva de indicadores que auxiliam na gestão acadêmica. De fato, levantamentos recentes indicam que a criação de sistemas de análise de dados baseados no Enade é uma demanda crescente para suprir a carência de plataformas de visualização nas instituições (CRUZ; MACIEL, 2023).

Nesse contexto, este trabalho apresenta o desenvolvimento de um dashboard voltado para os cursos do Instituto Federal do Espírito Santo (Ifes), abrangendo o ciclo de 2017 a 2025. O objetivo é ter um ambiente de visualização de dados para auxiliar as avaliações dos cursos como por exemplo, ter o levantamento de acertos e erros de cada questão e identificar nos questionários quais foram os piores avaliados. Sendo uma ferramenta de suporte à decisão que contribua para uma melhor formação dos alunos nos cursos e transformando dados brutos em planos de ação institucionais.


2 O EXAME NACIONAL DE DESEMPENHO DOS ESTUDANTES (ENADE)

O Exame Nacional de Desempenho dos Estudantes (Enade) é um dos pilares da avaliação da educação superior no Brasil, instituído pela Lei nº 10.861/2004 como parte integrante do Sistema Nacional de Avaliação da Educação Superior (Sinaes). Sob a responsabilidade do Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep), o exame tem como objetivo principal aferir o desempenho dos estudantes em relação aos conteúdos programáticos, habilidades e competências previstas nas diretrizes curriculares de seus respectivos cursos (INEP, 2024).

2.1 Funcionamento e Estrutura da Prova

O Enade funciona em ciclos avaliativos trienais, agrupando áreas do conhecimento semelhantes a cada ano. A prova é composta por dois componentes principais:
● Formação Geral (FG): Avalia aspectos da formação ética, humanística e o compromisso social do estudante, comum a todos os cursos.
● Componente Específico (CE): Foca nas competências técnicas e conhecimentos científicos específicos da área de graduação.

A estrutura da prova mescla questões objetivas (múltipla escolha) e discursivas. Segundo Sathler (2023), a análise detalhada de acertos e erros nessas questões permite identificar o nível de proficiência dos alunos em tópicos específicos do currículo, transformando o resultado quantitativo em um diagnóstico qualitativo para o Núcleo Docente Estruturante (NDE).

2.2 Questionários e Percepção Discente

Além da prova cognitiva, o Enade utiliza instrumentos de coleta de dados contextuais, sendo o Questionário do Estudante o mais relevante. Este instrumento investiga o perfil socioeconômico e a percepção do aluno sobre o processo formativo. Conforme aponta Lima (2018), os questionários abordam dimensões críticas, tais como:
● Organização Didático-Pedagógica: Avalia a clareza dos planos de ensino e a adequação das metodologias.
● Infraestrutura e Instalações Físicas: Verifica a qualidade de laboratórios, bibliotecas e salas de aula.
● Oportunidades de Ampliação da Formação: Questiona sobre bolsas de iniciação científica, monitoria e intercâmbios.

A identificação dos questionários pior avaliados é fundamental, pois, deficiências na infraestrutura ou na organização pedagógica podem atuar como variáveis intervenientes que prejudicam a vivência e o desempenho final dos alunos (LIMA, 2018; RODRIGUES, 2024).


3 METODOLOGIA

A metodologia deste trabalho consistiu no desenvolvimento de um dashboard analítico voltado aos cursos do Instituto Federal do Espírito Santo (Ifes), utilizando a linguagem Python e a biblioteca de visualização interativa Streamlit. O processo envolveu a coleta, o tratamento e a visualização de grandes volumes de microdados públicos disponibilizados pelo Inep.

3.1 Extração e Tratamento de Dados

O processo de Extração, Transformação e Carga (ETL) iniciou-se com a coleta dos microdados brutos do Enade, originalmente estruturados em múltiplos arquivos e em partições, uma medida do Inep para adequação à Lei Geral de Proteção de Dados (LGPD). Foi desenvolvida uma rotina para filtrar exclusivamente os registros pertencentes à instituição de interesse. Estes dados, abrangendo performance quantitativa, perfil sociodemográfico e as respostas do questionário do estudante, foram consolidados em arquivos otimizados, propiciando processamento e leitura ágeis pelo sistema.

Adicionalmente, foi executado um refinamento semântico. Tabelas oficiais do sistema e-MEC foram cruzadas com a base extraída para corrigir nomenclaturas genéricas ou ausentes e associar os alunos corretamente aos seus campi, garantindo a fidelidade e a integridade da base de dados analítica, o que corrobora com a necessidade de extração e tratamento rigoroso de microdados abordada por Cunha, Sales e Santos (2021).

3.2 Arquitetura da Interface e Funcionalidades

O dashboard foi projetado em uma arquitetura multipáginas gerenciadas via estados de sessão, o que confere ao aplicativo uma navegação fluida. A identidade visual foi estilizada em *Glassmorphism* (efeitos de translucidez) no CSS, alinhada à paleta de cores institucional, resultando em uma plataforma que se equipara a ferramentas corporativas de Business Intelligence aplicadas à gestão educacional, conforme proposto por Barreto e Freitas (2020).

Foi implementado um sistema de filtragem omnidirecional em que a seleção de uma variável de contexto (como o ano de avaliação, campus ou curso específico) refina instantaneamente as demais categorias. Esse modelo impede que o usuário faça combinações inexistentes de dados e assegura que a visualização seja sempre concisa e baseada na realidade acadêmica da amostra.


4 RESULTADOS E DISCUSSÃO

A aplicação desenvolvida entrega aos gestores, professores e membros de Núcleos Docentes Estruturantes um acervo de análises interativas distribuídas em abas temáticas, convertendo planilhas inacessíveis em inteligência educacional (CRUZ; MACIEL, 2023).

4.1 Painel de Cursos e Desempenho

O sistema evidencia o balanço de proficiência das turmas ao extrair e plotar graficamente as notas brutas das frações de Formação Geral (FG) e Componente Específico (CE). Destaca-se a implementação de um cálculo de evasão e abstenção (razão entre o número de inscritos e os que efetivamente realizaram a prova). Este indicador, exposto através de gráficos de barras em tons de alerta, permite que as coordenações monitorem os índices de ausência de forma tempestiva.

4.2 Análise do Componente Específico (CE)

Com o intuito de viabilizar uma investigação cirúrgica no conhecimento técnico dos estudantes, o painel integra uma aba dedicada à análise de cada questão do Componente Específico (CE1 ao CE27). Gráficos interativos exibem os índices percentuais de acerto frente às margens de erro, bem como a contabilização de alternativas assinaladas incorretamente, questões em branco ou anuladas. Mapas de calor (Heatmaps) facilitam a identificação visual imediata dos pontos fracos de uma turma em tópicos curriculares, possibilitando a intervenção cirúrgica na grade e nos projetos pedagógicos dos cursos. Este nível de detalhamento é fundamental para monitorar a evolução das competências discentes (CUNHA; SALES; SANTOS, 2021; SATHLER, 2023).

4.3 Perfil Demográfico e Integração Sociocultural

Cruzando diferentes partições criptografadas do questionário do estudante, o sistema projeta painéis demográficos e socioeconômicos da instituição. As visualizações reúnem dados da idade média da amostra estudantil, distribuição de gênero em formato gráfico e estatísticas sobre autodeclaração étnico-racial.

Através de rotinas no código que acionam dicionários internos do Inep, respostas em códigos são traduzidas ativamente. Assim, indicadores como renda familiar, escolaridade dos pais e vinculação dos estudantes a políticas de acesso (como cotas e bolsas de pesquisa) são exibidos graficamente, elucidando a influência do capital sociocultural e das políticas de auxílio na adaptação e trajetória formativa (RODRIGUES, 2024).

4.4 Percepção sobre o Processo Formativo e Pandemia

Na aba "Questionário do Estudante", as questões aplicadas na Escala Likert, que avaliam a organização didático-pedagógica e a infraestrutura, são dispostas com seus enunciados completos. O dashboard calcula a porcentagem exata de satisfação ou insatisfação dos estudantes.

O desenvolvimento também endereçou as variações interanuais das edições do exame. Destaca-se o mapeamento dinâmico que detecta a edição atípica de 2021, integrando automaticamente as novas questões formuladas sobre os impactos da pandemia de Covid-19 no aprendizado e avaliando o grau de adaptação das turmas ao regime de estudos remoto.


5 CONSIDERAÇÕES FINAIS

O desenvolvimento do Painel Enade no presente trabalho demonstra como a ciência de dados e o design de interfaces são determinantes para transformar a montanha de microdados disponibilizada pelo Inep em decisões táticas palpáveis. A consolidação destas informações sociodemográficas e cognitivas em um ambiente intuitivo preenche uma lacuna tecnológica fundamental nos processos de avaliação de cursos (BARRETO; FREITAS, 2020; CRUZ; MACIEL, 2023). 

Por permitir a identificação instantânea de vulnerabilidades no aprendizado técnico (através da análise do Componente Específico) e levantar os pontos críticos relatados pela própria percepção do estudante, o dashboard cumpre sua premissa. Ele atua como um recurso de inteligência institucional, fornecendo os insumos baseados em dados (data-driven) necessários para o constante aperfeiçoamento da educação em engenharia no Brasil.


REFERÊNCIAS

BARRETO, I. M. S.; FREITAS, A. E. S. Gerando inteligência através de microdados: uma proposta de business intelligence para a área de ensino do Instituto Federal da Bahia (IFBA). Cadernos de Educação, Tecnologia e Sociedade, [S. l.], v. 13, n. 4, p. 463-473, 2020. Disponível em: https://doi.org/10.14571/brajets.v13.n4.463-473. Acesso em: 16 maio 2026.

BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep). Enade. Disponível em: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enade. Acesso em: 16 maio 2026.

CRUZ, B. B.; MACIEL, K. A. SAEN: Um sistema de análise de dados baseado em resultados do ENADE. In: ESCOLA REGIONAL DE COMPUTAÇÃO DO CEARÁ, MARANHÃO E PIAUÍ (ERCEMAPI), 11., 2023. Anais [...]. Porto Alegre: SBC, 2023. Disponível em: https://doi.org/10.5753/ercemapi.2023.236410. Acesso em: 16 maio 2026.

CUNHA, R.; SALES, C.; SANTOS, R. Análise automática com os microdados do Enade para melhoria do ensino dos cursos de Ciência da Computação. In: WORKSHOP SOBRE EDUCAÇÃO EM COMPUTAÇÃO (WEI), 29., 2021. Anais [...]. Porto Alegre: SBC, 2021. Disponível em: https://sol.sbc.org.br/index.php/wei/article/view/15912. Acesso em: 16 maio 2026.

LIMA, B. A. T. Análise da percepção dos discentes sobre a formação na universidade por meio do questionário do estudante do ENADE. 2018. 45 f. Monografia (Graduação em Licenciatura em Química) – Centro de Ciências Agrárias, Universidade Federal da Paraíba, Areia, 2018. Disponível em: https://repositorio.ufpb.br/jspui/handle/123456789/15239. Acesso em: 16 maio 2026.

RODRIGUES, R. O.; BARBOSA, R. T. O.; RODRIGUES, E. B. Vivências acadêmicas: adaptação de estudantes do curso de Engenharia Civil. Avaliação: Revista da Avaliação da Educação Superior, Campinas, v. 29, e024005, 2024. Disponível em: https://doi.org/10.1590/1982-57652024v29id282350. Acesso em: 16 maio 2026.

SATHLER, L. H. Dashboard dos resultados do Ifes no Enade de Sistemas de Informação dos anos de 2017 e 2021. 2023. 69 f. Monografia (Graduação em Sistemas de Informação) – Instituto Federal do Espírito Santo, Serra, 2023. Disponível em: https://repositorio.ifes.edu.br/handle/123456789/4184. Acesso em: 16 maio 2026.
