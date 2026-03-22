# Memória de IA (AI Reasoning State)

Este arquivo foi criado para manter a persistência do raciocínio e das decisões arquiteturais tomadas durante o desenvolvimento do projeto **Painel - ENADE**, garantindo que o progresso não se perca ao trocar de máquina.

## Decisões e Histórico Recente
* **Design Premium (21/03/2026):** O aplicativo possui pacote de UI/CSS moderno com uso intenso do Verde do IFES.
* **Sistema Multi-Paginas e Landing Page (21/03/2026):** O aplicativo foi refatorado. Agrupamos lógicas visuais nas funções `show_home()`, `show_dashboard()`, e agora `show_alunos()`. Tudo inicia na tela Hub navegando pelo menu de estado.
* **Dashboards de Alunos e Exploração de Dados (22/03/2026):** Foi adicionado um botão secundário para analisar "Informações dos Alunos". 
   * **Gráfico 1:** Identificou-se que o INEP quebra os resultados em Conhecimentos Gerais (FG) e Específicos (CE). Plotly gera um Bar agrupado apontando a eficiência nos eixos por curso.
   * **Gráfico 2:** Taxa de Evasão (Abstenção) foi trazida de volta como um ranking bar chart de tons vermelhos, alertando por Campus os níveis mais crônicos. A lógica isola e faz cache dos Inscritos x Participantes.
   * **Filters Refactoring:** Os filtros drop-downs agora utilizam o modelo de Função Helper `render_filters()`, não repetindo código e ativando os mesmos filtros nas duas telas de análises!

## Estado Atual
Painel completo e complexo com UX em 3 ambientes integrados sem arquivos separados. Aguardando novo feedback.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada para salvar seu raciocínio no OneDrive)*
