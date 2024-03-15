import csv
import json

from openpyxl import Workbook


def list_of_dicts_to_csv(data, csv_file):
    if not data:
        print("Data is empty.")
        return

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='') as f:
        # Create a CSV writer object
        csv_writer = csv.writer(f)

        # Write the header based on the keys of the first dictionary in the list
        csv_writer.writerow(data[0].keys())

        # Write each row of data to the CSV file
        for item in data:
            csv_writer.writerow(item.values())


def list_of_dicts_to_json(data, json_file):
    if not data:
        print("Data is empty.")
        return

    # Open the JSON file in write mode
    with open(json_file, 'w') as f:
        # Write the data to the JSON file
        json.dump(data, f, indent=4)


def list_of_dicts_to_xlsx(data, xlsx_file):
    if not data:
        print("Data is empty.")
        return

    # Create a new Workbook object
    wb = Workbook()

    # Create a new worksheet
    ws = wb.active

    # Write the header row based on the keys of the first dictionary in the list
    header = list(data[0].keys())
    ws.append(header)

    # Write each row of data to the worksheet
    for item in data:
        ws.append(list(item.values()))

    # Save the workbook to the XLSX file
    wb.save(xlsx_file)
