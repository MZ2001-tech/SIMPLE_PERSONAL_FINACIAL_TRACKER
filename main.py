import pandas as pd
import csv
import datetime as datetime

class CSV:
    CSV_FILE = "finace_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def iniatialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COlUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

        
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry ={
            "date": date,
            "amount": amount,
            "category": category,            "description": description
            }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer= csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)            
            writer.writerow(new_entry)
            print("Entry added sucessfully")

CSV.iniatialize_csv()
CSV.add_entry("20-07-2025",125.90, "Income", "Salary")




