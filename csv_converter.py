
import pandas as pd


read_data = pd.read_csv('dados.txt')
read_data.to_csv('dados_convertidos.csv')
print(read_data)