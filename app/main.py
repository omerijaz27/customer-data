import csv
import json
from datetime import datetime


def remove_card(row: dict):
    try:
        f_start_date = datetime.strptime(row.get('credit_card').get('start_date'), "%m/%y")
        f_expiry_date = datetime.strptime(row.get('credit_card').get('expiry_date'), "%m/%y")

        time_difference = int((f_expiry_date - f_start_date).days / 365)
        if time_difference > 10:
            print(f"Row adding to remove_ccard.json\n{row}")
            return True

    except Exception as ex:
        raise Exception(f"{ex}")


def main():
    try:
        # Task 1
        # Read in the provided ACW Data using the CSV library.

        processed_data = []
        problematic_rows = []
        with open('data/read/acw_user_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            # Task 2
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    struct_data = {
                        "first_name": row[11],
                        "last_name": row[13],
                        "age": row[3],
                        "sex": row[18],
                        "retired": row[16],
                        "marital_status": row[14],
                        "dependants": row[10] if row[10] not in ["", " "] else "-",
                        "salary": row[17],
                        "pension": row[15],
                        "company": row[5],
                        "commute_distance": row[4],
                        "vehicle": {
                            "make": row[19],
                            "model": row[20],
                            "Year": row[21],
                            "Type": row[22]
                        },
                        "credit_card": {
                            "start_date": row[6],
                            "expiry_date": row[7],
                            "number": row[8],
                            "cvv": row[9],
                            "iban": row[12],
                        },
                        "address": {
                            "street": row[0],
                            "city": row[1],
                            "postcode": row[2],
                        }
                    }
                    line_count += 1

                    # Task 3
                    if struct_data.get('dependants') == "-":
                        problematic_rows.append(line_count)

                    processed_data.append(struct_data)

        # Task 3 Print list of problematic rows
        print(f'Problematic rows are: {problematic_rows}')

        # Task 4
        with open('data/output/processed.json', 'w') as f:
            json.dump(processed_data, f)

        # Task 5
        with open('data/output/retired.json', 'w') as f:
            for data in processed_data:
                if data.get('retired') == 'True':
                    json.dump(data, f)

        with open('data/output/employed.json', 'w') as f:
            for data in processed_data:
                if data.get('retired') != 'True':
                    json.dump(data, f)

        # Task 6
        remove_card_data = []
        for row in processed_data:
            r_card = remove_card(row)
            if r_card:
                remove_card_data.append(row)
        with open('data/output/remove_ccard.json', 'w') as f:
            json.dump(remove_card_data, f)

        # Task 7
        commute_data = []
        with open('data/output/processed.json') as processed:
            data = processed.read()

        obj = json.loads(data)

        for o in obj:
            commute_distance = float(o.get('commute_distance'))
            salary = float(o.get('salary'))

            if commute_distance > 1:
                o["salary-commute"] = str(salary * commute_distance)

            else:
                o["salary-commute"] = str(salary)

            commute_data.append(o)
        sorted_data = (sorted(commute_data, key=lambda x: x['salary-commute']))
        with open('data/output/commute.json', 'w') as f:
            json.dump(sorted_data, f)

    except Exception as ex:
        print(f"{ex}")


if __name__ == "__main__":
    main()
