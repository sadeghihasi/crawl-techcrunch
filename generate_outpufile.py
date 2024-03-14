import csv


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
