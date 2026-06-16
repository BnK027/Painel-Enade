# Manual de Integração de Novos Anos do ENADE

Este guia ensina a **"Fórmula"** exata para estruturar, limpar e integrar a base de dados de um novo ano do ENADE (ex: 2023, 2024, etc.) dentro do Painel Enade IFES.

Nós automatizamos 95% do trabalho pesado. Você só precisará baixar a planilha bruta do Inep, rodar um script que criamos para você, e adicionar 6 linhas de código no seu aplicativo para ver a mágica acontecer.

---

## 🛠️ Passo 1: Obter o Arquivo Bruto do INEP
1. Faça o download da planilha oficial de microdados do ENADE do ano desejado no portal do INEP.
2. O arquivo geralmente vem com um nome como `Enade 2023.xlsm` ou `Enade 2024.xlsx` e é bem pesado (500MB+).
3. Coloque este arquivo bruto na mesma pasta raiz do projeto (`Painel Enade IFES - IC`).

---

## ⚙️ Passo 2: Rodar o Script Mestre de Extração (ETL)

Nós desenvolvemos o script `processar_novo_enade.py`. Ele detém toda a lógica de inteligência de dados: ele varre o arquivo gigantesco, filtra estritamente alunos do IFES, limpa lixos de formatação, gera a aba secreta de questões específicas (`Arq_3B`) e cria o arquivo consolidado final.

Abra o seu terminal (CMD ou PowerShell) na pasta do projeto e digite o seguinte comando:

```bash
python processar_novo_enade.py [ANO] "[NOME_DO_ARQUIVO_BRUTO]"
```

**Exemplo prático (se você baixou o Enade 2023):**
```bash
python processar_novo_enade.py 2023 "Enade 2023.xlsm"
```

### O que o script faz sozinho por você?
- Verifica quais cursos pertencem ao IFES (usando sua base validada do EMEC).
- Deleta os milhões de registros do resto do Brasil, economizando 99% do espaço em disco.
- Renomeia as abas confusas do INEP (`microdados2017_arq5`) para o nosso padrão (`Arq_5`).
- Desmembra a complexa string de respostas do Componente Específico em colunas tratáveis (`CE1` até `CE27`).
- Salva um arquivo levinho (ex: `Enade_2023_Ifes.xlsx`).
- **Gera automaticamente a tela gráfica do painel** (ele cria o arquivo `views/visao_2023.py` clonando perfeitamente a nossa melhor tecnologia visual).

---

## 🚀 Passo 3: Ativar o Novo Ano no Aplicativo (`app.py`)

Com o arquivo Excel tratado (`Enade_2023_Ifes.xlsx`) e a tela gráfica (`visao_2023.py`) criados, falta apenas "plugar o fio na tomada". 

Abra o arquivo `app.py` no seu editor de código e faça 3 pequenas adições:

### 3.1 Informar ao Streamlit para carregar o novo arquivo de Notas
Procure a função `load_data()`. Na linha que tem a variável `files`, adicione o seu novo arquivo no final da lista.
```python
# ANTES:
files = ['Enade_2017_Ifes.xlsx', 'Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']

# DEPOIS:
files = ['Enade_2017_Ifes.xlsx', 'Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx', 'Enade_2023_Ifes.xlsx']
```

### 3.2 Informar para carregar os Microdados (Questionários)
Procure a função `load_microdata()`. Faça a exata mesma coisa na variável `files` que está lá dentro:
```python
files = ['Enade_2017_Ifes.xlsx', 'Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx', 'Enade_2023_Ifes.xlsx']
```

### 3.3 Adicionar o Roteamento da Tela
Vá até o **final do arquivo `app.py`** onde os anos são roteados (`if st.session_state.page == ...`). Adicione um bloco `elif` para o seu ano novo. O código do dashboard é modular e puxará a sua tela recém-criada.

```python
# Adicione este bloco no final da cadeia de if/elif
elif st.session_state.page == 'visao_2023':
    from views.visao_2023 import render_visao_2023
    render_visao_2023(data, microdados, render_filters, render_page_header)
```

**Pronto!** Limpe o cache do Streamlit e o ano novo aparecerá magicamente integrado em todos os painéis, menus, métricas e análises profundas.

---

## 🤖 Passo Alternativo: Delegar o Trabalho para a Inteligência Artificial

Se você não quiser abrir o terminal nem digitar código nenhum, você pode simplesmente colocar a planilha do INEP na pasta do projeto e copiar e colar o **"Comando Mágico"** abaixo no chat da Inteligência Artificial (trocando apenas o ano `2024` pelo ano real que você estiver fazendo):

> *"Antigravity, acabei de colocar a planilha bruta do INEP chamada `Enade 2024.xlsm` na raiz do projeto. Por favor, execute o nosso pipeline automatizado usando o script `processar_novo_enade.py` para processar o ano de 2024. Em seguida, atualize automaticamente o arquivo `app.py` adicionando o novo ano nas funções `load_data` e `load_microdata`, e crie a rota da página lá no final do código."*

Ao enviar isso, a IA fará 100% do trabalho (Passos 2 e 3 descritos acima) de forma totalmente autônoma para você!

### Opção B: Comando para Microdados em arquivo TXT / CSV

Se a base de dados do Inep estiver no formato de texto gigante (`.txt` ou `.csv`), a IA utilizará o script tradutor especializado para texto. Basta usar o seguinte comando:

> *"Antigravity, acabei de colocar o arquivo de texto bruto do INEP chamado `MICRODADOS_ENADE_2024.txt` na raiz do projeto. Por favor, execute o nosso pipeline tradutor automatizado usando o script `processar_novo_enade_txt.py` para processar o ano de 2024. Em seguida, atualize automaticamente o arquivo `app.py` para integrar o arquivo gerado e crie a rota da visualização."*
