# Memória de IA (AI Reasoning State)

Este arquivo foi criado para manter a persistência do raciocínio e das decisões arquiteturais tomadas durante o desenvolvimento do projeto **Painel - ENADE**, garantindo que o progresso não se perca ao trocar de máquina.

## Decisões e Histórico Recente
* **Divisão de Dashboards:** A ideia levantada na última sessão de dividir o sistema em múltiplos arquivos foi **abandonada**. Mantemos tudo em `app.py`.
* **Design e Tema (21/03/2026):** Foi configurado um tema explícito do Streamlit através do arquivo `.streamlit/config.toml` forçando o fundo branco e o verde base.
* **Fita de Elementos (Marquee - 21/03/2026):** A fita de rolagem de abstenções, que faria parte da ideia original, foi reimplementada e adaptada diretamente na base estável do `app.py`. A lógica desenvolvida encontra as colunas 'Inscritos' e 'Participantes' ignorando espaços em branco nos cabeçalhos distorcidos do Inep. O componente injeta uma *div* HTML limpa processando (1 - Participantes/Inscritos).

## Estado Atual
O painel exibe um Marquee fluído no topo mostrando as abstenções. Ele está pronto para receber Deploy no 'share.streamlit.io'. Aguardando novas decisões e funcionalidades.

*(Este arquivo continuará sendo atualizado a cada nova funcionalidade implementada para salvar seu raciocínio no OneDrive)*
