import app
print(app.data.head())
print("Data shape:", app.data.shape)
print("Unique Years:", app.data['ANO'].unique())
