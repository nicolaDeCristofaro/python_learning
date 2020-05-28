import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Automation report of multiple excel sheets

excel_file_1 = "shift-data.xlsx"
excel_file_2 = "third-shift-data.xlsx"

df_first_shift = pd.read_excel(excel_file_1, sheet_name="first")
df_second_shift = pd.read_excel(excel_file_1, sheet_name="second")
df_third_shift = pd.read_excel(excel_file_2)

print(df_first_shift)  # print the whole first shift from excel
print(df_first_shift["Product"])  # print one column

# Combining Data: combining data from different sheets in one
df_all = pd.concat([df_first_shift, df_second_shift, df_third_shift])
print(df_all)

# calculations: (in our example) which shift is more productive in create the products
pivot = df_all.groupby(["Shift"]).mean()
shift_productivity = pivot.loc[:, "Production Run Time (Min)":"Products Produced (Units)"]

print(shift_productivity)

# Show data on graph
shift_productivity.plot(kind="bar")
plt.show()

# Output these data to a new excel sheet
df_all.to_excel("output.xlsx")