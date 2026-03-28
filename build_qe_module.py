import json

with open('extracted_missing_qe.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Take 2021 since it has the most questions (including Covid-specific ones)
base_dict = data['Enade_2021_Ifes.xlsx']

# Write python module
with open('qe_dictionary.py', 'w', encoding='utf-8') as f:
    f.write('qe_dict = {\n')
    for k, v in sorted(base_dict.items(), key=lambda x: int(x[0].split('I')[1])):
        safe_v = v.replace('"', '\\"').replace('\n', ' ')
        f.write(f'    "{k}": "{safe_v}",\n')
    f.write('}\n')

print("Created qe_dictionary.py successfully.")
