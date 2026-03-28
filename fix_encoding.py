import re

with open("app.py", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

pattern = r"'QE_I39':.*?\]\n\s+qe_cols\.sort\(\)"

replacement = """'QE_I39': 'Os professores demonstraram domínio dos conteúdos abordados nas disciplinas.',
        'QE_I41': "Os professores utilizaram tecnologias da informação e comunicação (TIC's) como estratégia de ensino..."
    }

    # Discover all QE_I columns available in Arq_4 (Likert scale 1-6)
    qe_cols = [str(c) for c in df_arq4.columns if str(c).startswith('QE_I')]
    qe_cols.sort()"""

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Fixed app.py syntax and encoding.")
