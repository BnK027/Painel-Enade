import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from app import load_data
data = load_data()
for year in data['ANO'].dropna().unique():
    courses = data[data['ANO'] == year]['NOME DO CURSO'].dropna().unique()
    print(f"Year {year} courses: {', '.join(courses[:3])}...")
