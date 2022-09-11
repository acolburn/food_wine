# Original pairing chart at https://tinyurl.com/ydx4twpy
# data.query() info at https://www.geeksforgeeks.org/python-filtering-data-with-pandas-query-method/

# importing pandas package
import pandas as pd

# output will display all the rows and cols in the dataframe/spreadsheet
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# making data frame from csv file
data = pd.read_csv("food_wine_pairing.csv", encoding='unicode_escape')
# replacing blank spaces with '_'
data.columns = [column.replace(" ", "_") for column in data.columns]

# select first 3 rows
# out = data.head(3)

# filtering with query method
# if user selects pairing with meat:
# out = data.loc[data['category'] == 'meat']

# user selects pairing with red meat
filtered_data = data.loc[data['name'] == 'red meat']
# then user also selects pairing with grilled
filtered_data2 = data.loc[data['name'] == 'grilled']
combined_data = pd.concat([filtered_data, filtered_data2])
# this also works:
# combined_data = pd.concat([filtered_data, data.loc[data['name'] == 'grilled']])
# let's also add in green vegetables
filtered_data3 = data.loc[data['name'] == 'green vegetables']
combined_data = pd.concat([combined_data, filtered_data3])


# select rows that contain value 2 in any column
# out = out[out.isin([2]).any(axis=1)]

# out = out.loc[data['bold_red'] >= 1]

# select cols that contain value 2
cols_with_2 = combined_data.columns[combined_data.eq(2).any()]

# select cols that contain value 1
cols_with_1 = combined_data.columns[combined_data.eq(1).any()]

# combine out1 and out2 for everything with a 1 or 2
# these are columns for wines that pair with everything
out = cols_with_2.append(cols_with_1)
# select cols that contain 2's everywhere
# these are columns for wines that not only pair with everything, but pair really well
out2 = combined_data.columns[combined_data.eq(2).all()]
# select cols that contain 0's everywhere
# these are columns for wines that don't pair with anything in the meal
out0 = combined_data.columns[combined_data.eq(0).all()]

# display only name and examples columns
# print(out[['name', 'examples']])

if out2.size > 0:
    print("This is the best pairing for your meal:")
    for item in out2:
        item = item.replace("_", ' ')
        print(item)
    print("\nHere is the full list of pairings to consider:")
elif out.size > 0:
    print("Here are some pairing suggestions for your meal:")
else:
    print("Unfortunately, I did not find great pairings for your meal.")

for item in out:
    item = item.replace("_", ' ')
    print(item)

if out0.size > 0:
    print("\nFor this meal, stay away from these wines:")
    for item in out0:
        item=item.replace("_", ' ')
        print(item)


