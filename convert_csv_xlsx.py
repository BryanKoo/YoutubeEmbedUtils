'''
convert tsv/csv to excel
'''
import pandas as pd
import sys

input_file = sys.argv[1]
output_file = input_file[:-3] + "xlsx"
df = pd.read_csv(input_file, sep='\t')
df.to_excel(output_file, header=False)
