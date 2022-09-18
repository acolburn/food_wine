# Original pairing chart at https://tinyurl.com/ydx4twpy
# data.query() info at https://www.geeksforgeeks.org/python-filtering-data-with-pandas-query-method/

# how to select first 3 rows
# out = data.head(3)

# filtering with query method
# if user selects pairing with meat:
# out = data.loc[data['category'] == 'meat']

# user selects pairing with red meat
# filtered_data = data.loc[data['name'] == 'red meat']

# how to select rows that contain value 2 in any column
# out = out[out.isin([2]).any(axis=1)]

# display only name and examples columns
# print(out[['name', 'examples']])

# importing pandas package
import pandas as pd

# output will display all the rows and cols in the dataframe/spreadsheet
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)

# making data frame from csv file
data = pd.read_csv("food_wine_pairing.csv", encoding='unicode_escape')
# replacing blank spaces with '_'
data.columns = [column.replace(" ", "_") for column in data.columns]

# Introduction text
print("Let's pair! Follow the prompts to find wines to pair with your meal.\n")


def input_choices(prompt, category):
    # global selected_data
    print(prompt)
    _choices = data.loc[data['category'] == category]
    _choices_list = _choices.name.to_list()
    _examples_list = _choices.examples.to_list()
    for item in _choices_list:
        # print(f"{choices_list.index(item)}\t{item}")
        s = str(_choices_list.index(item)) + '\t' + item
        t = _examples_list[_choices_list.index(item)]
        # if there's an example, print it, otherwise ... don't
        # below is the preferred way to do what you want to do
        # cells without values still evaluated as NaN (like null),
        # also, there's the issue of cells that are blank but still have a space, tab, or other invisible character
        if pd.isnull(t) or t.isspace():
            print(s)
        else:
            print(s + f' (e.g., {t})')
    print(f"{len(_choices_list)}\tnone of the above/skip this category")
    i = input("Your selection: ")
    if int(i) < len(_choices_list):
        _new_data = data.loc[data['name'] == _choices_list[int(i)]]
        print(f"You selected: {_new_data.name}")
        try:
            _selected_data = pd.concat([selected_data, _new_data])
        except NameError:  # Get this error if there's nothing in the global selected_data
            _selected_data = _new_data
    else:
        print('OK, moving on.\n')
        try:
            _selected_data = selected_data
        except NameError:  # Get this error if selected_data is undefined, i.e., choose 'none' for first category
            return None
    print("\n---------------------------------------------------------\n")
    return _selected_data


# Ask about meats
selected_data = input_choices("Which, if any, of these meats are part of your meal?", 'meat')

# Ask about preparation
selected_data = input_choices(
    "Now let's consider how the meat, or main dish in the meal, will be prepared.\nWhich, if any of these preparation methods, are important to your meal:",
    "preparation")

# Ask about dairy
selected_data = input_choices("Will your meal include dairy products?", 'dairy')

# Ask about vegetables
selected_data = input_choices("Now let us consider those healthy vegetables!", 'vegetable')

# Ask about seasoning
selected_data = input_choices("Seasoning is important for wine pairing. Are any of these part of your meal?",
                              'seasoning')

# Ask about starch
selected_data = input_choices("Are starches playing a role in your meal?", 'starch')

# Ask about sweets
selected_data = input_choices("Finally, sweets:", 'sweets')

print("Here is what you selected:")
# print(selected_data['name']) //this line includes type and int64 info that's unneeded
sel = selected_data['name'].values
for item in sel:
    print(item)

print("\n---------------------------------------------------------\n")

# Let's start parsing the selected_data dataframe:
# select cols that contain 2's everywhere
# these are columns for wines that not only pair with everything, but pair really well
# (note: the list(set()) code converts the data to a list, and also assures there are no duplicate items
out2 = list(set(selected_data.columns[selected_data.eq(2).all()]))

# select cols that contain value 1
cols_with_1 = selected_data.columns[selected_data.eq(1).any()]
# select cols that contain value 2
cols_with_2 = selected_data.columns[selected_data.eq(2).any()]

# combine cols_with_1 and cols_with_2 for everything with a 1 or 2
# these are columns for wines that pair with everything
# (note: the list(set()) code converts the data to a list, and also assures there are no duplicate items
out = list(set(cols_with_2.append(cols_with_1)))

# select cols that contain 0's everywhere
# these are columns for wines that don't pair with anything in the meal
# (note: the list(set()) code converts the data to a list, and also assures there are no duplicate items
out0 = list(set(selected_data.columns[selected_data.eq(0).all()]))

if len(out2) > 0:
    print("This is the best pairing for your meal:")
    for item in out2:
        item = item.replace("_", ' ')
        print(item)
    print("\nHere is the full list of pairings to consider:")
elif len(out) > 0:
    print("Here are some pairing suggestions for your meal (ranked from best to worst):")
else:
    print("Unfortunately, I did not find great pairings for your meal.")

# for item in out:
#     item = item.replace("_", ' ')
#     print(item)

# replace _ with spaces before displaying
selected_data.columns = [column.replace("_", " ") for column in selected_data.columns]
# .sum() adds the values in each column
# .sort_values(ascending=False) sorts the values (duh) and displays from highest to lowest
display = selected_data.sum(numeric_only=True).sort_values(ascending=False)
# without .to_string() the info is displayed with an added Type:int64 attribute at the end
# see https://stackoverflow.com/questions/53025207/how-do-i-remove-name-and-dtype-from-pandas-output
print(display.to_string())

if len(out0) > 0:
    print("\nIn other words, for this meal, stay away from these wines:")
    for item in out0:
        item = item.replace("_", ' ')
        print(item)

print("\nDONE!")
