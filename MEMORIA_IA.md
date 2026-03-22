# Memória de IA (AI Reasoning State)

Este arquivo foi criado para manter a persistência do raciocínio e das decisões arquiteturais tomadas durante o desenvolvimento do projeto **Painel - ENADE**, garantindo que o progresso não se perca ao trocar de máquina.

## Decisões e Histórico Recente
* **Divisão de Dashboards e Marquee:** A ideia levantada na última sessão de dividir o sistema em `dashboard_first.py` e `dashboard_second.py`, junto com a implementação de um `<marquee>` para a taxa de ausentes, foi **abandonada** pelo usuário.
* **Estado Base:** O projeto continuará utilizando a estrutura atual e funcional concentrada no arquivo único `app.py` que está nesta máquina.
* **Design e Tema (21/03/2026):** Foi configurado um tema explícito do Streamlit através do arquivo `.streamlit/config.toml` para forçar o fundo branco (Light Mode) permanentemente. Adicionado também o verde do IFES (`#32A041`) como a cor primária padrão dos componentes, menus e botões.
* **Backup no GitHub (21/03/2026):** O projeto foi conectado ao repositório remoto sob a conta do usuário `Benincá`. Criado o arquivo `Salvar_No_Github.bat` para facilitar e automatizar os commits.

## Estado Atual
O painel está operando na base de código do `app.py` com o fundo branco configurado via Toml de Tema. Aguardando novo direcionamento de implementação de dados.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada para salvar seu raciocínio no OneDrive)*
