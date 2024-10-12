import pymupdf4llm
import datetime
import calendar
import re
import pathlib


def is_leap_year(year):
    return calendar.isleap(year)


# Custom function to correctly translate the current date to the correct page in the pdf
def get_page_number(date):
    day_of_year = date.timetuple().tm_yday  # Gets the current day of the year

    # Initial page number calculation
    page_number = 14 + (day_of_year - 1) + (date.month - 1)

    # Extra checks to avoid title pages
    if 5 <= date.month <= 8:
        page_number += 1
    elif date.month > 8:
        page_number += 2

    if not is_leap_year(date.year) and date.month > 2:
        page_number += 1

    return page_number


# Get today's date
t_date = datetime.datetime.now()
# test_date = datetime.date(2024, 3, 1)
# print(get_page_number(test_date))

reader = pymupdf4llm.to_markdown(r"C:\Users\scale\PycharmProjects\Extract_text_from_PDF\The Daily Stoic.pdf", pages=[get_page_number(t_date)], show_progress=False)
pathlib.Path("output.md").write_bytes(reader.encode())

tokens = re.findall(r'\S+|\s+', reader)
letter = ""
counter = 1
first_area = tokens[1:].index("######")

for token in tokens[1:]:
    if token == "#":
        letter = tokens[counter+2]
        tokens[counter-1:counter+3] = ""
    elif token == "######" and counter - 1 != first_area:
        tokens[counter - 5:counter - 3] = ""
    counter += 1

counter = 1
for token in tokens[1:]:
    if token == "######":
        tokens[counter:counter + 1] = ""
        tokens[counter + 1] = letter + tokens[counter + 1]
    counter += 1

reconstructed_text = ''.join(tokens)
print(reconstructed_text)
pathlib.Path("output.md").write_bytes(reconstructed_text.encode())
with open(r"C:\Users\scale\OneDrive\Desktop\Stoic.txt", "w") as file:
    file.write(reconstructed_text)
