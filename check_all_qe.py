import pandas as pd
import shutil
import os
import re

files = ['Enade_2018_Ifes.xlsx', 'Enade_2019_Ifes.xlsx', 'Enade_2021_Ifes.xlsx', 'Enade_2022_Ifes.xlsx']
all_dicts = {}

for f in files:
    try:
        tmp_name = f"temp_{f}"
        shutil.copy2(f, tmp_name)
        
        xls = pd.ExcelFile(tmp_name)
        dic_sheet = [s for s in xls.sheet_names if 'DICION' in s.upper()][0]
        df = pd.read_excel(xls, sheet_name=dic_sheet, header=None)
        
        qe_dict = {}
        for idx, row in df.iterrows():
            row_str = " | ".join([str(x) for x in row if pd.notna(x)])
            
            # Find QE_Ixx
            match_var = re.search(r'QE_I(\d{2})', row_str)

            if match_var:
                code = match_var.group(1)
                
                # The text is typically in the second cell
                # row looks like: [ 'microdados2018_arq26', 'Edição... QE20: Text', 'NU_ANO...QE_I20' ]
                vals = [str(x) for x in row if pd.notna(x)]
                if len(vals) >= 2:
                    text_candidate = vals[1]
                    # extract what comes after 'QE\d+:'
                    text_match = re.search(r'QE\s*\d+:(.*)', text_candidate)
                    if text_match:
                        desc = text_match.group(1).strip()
                    else:
                        # fallback, maybe it was in a different column
                        desc = text_candidate
                else:
                    desc = vals[0]
                    
                qe_dict[f"QE_I{code}"] = desc
                
        all_dicts[f] = qe_dict
        xls.close()
        os.remove(tmp_name)

    except Exception as e:
        pass

base_file = files[0]
base_dict = all_dicts.get(base_file, {})

print("\n--- COMPARISON OF COMMON QUESTIONS ---")
common_keys = set(base_dict.keys())
for f in files[1:]:
    common_keys = common_keys.intersection(all_dicts.get(f, {}).keys())

diffs_found = False
for k in sorted(common_keys):
    base_text = all_dicts[base_file][k]
    for f in files[1:]:
        curr_text = all_dicts[f][k]
        # Ignore minor punctuation/space differences
        norm_b = re.sub(r'\W+', '', base_text.lower())
        norm_c = re.sub(r'\W+', '', curr_text.lower())
        if norm_b != norm_c:
            print(f"Diff on {k} between 2018 and {f[6:10]}:")
            print(f"  2018: {base_text}")
            print(f"  {f[6:10]}: {curr_text}")
            diffs_found = True

if not diffs_found:
    print("All common questions are exactly identical in text across all years!")

print("\n--- EXTRA OR MISSING QUESTIONS ---")
for f in files:
    keys = set(all_dicts[f].keys())
    extra = sorted(keys - common_keys)
    if extra:
        print(f"[{f}] has extra questions not common to all: {extra}")

