import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_amount, get_category, get_date, get_description

class CSV:
    #Declare CSV Variables
    CSV_FILE = "finace_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def iniatialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE) #Open CSV file 
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COlUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
    
    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format= CSV.FORMAT) 
        start_date = datetime.strptime(start_date, CSV.FORMAT) # Select Starting Date row
        end_date = datetime.strptime(end_date, CSV.FORMAT) # Select End Date Row

        mask = (df["date"] >= start_date) & (df["date"] <= end_date) # if the range date is correct
        filtered_df = df.loc[mask] #Acess data frame
        #Conditions
        if filtered_df.empty: 
            print('No transaction found in the given date range.')
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}" #print date range strftime -> print dates into strings
                
            )

            print(
                filtered_df.to_string(
                    index = False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}  #converted it to a readable output.
                    )
            )
            #output 
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_exspense = filtered_df[filtered_df["category"] == "Exspense"]["amount"].sum()
            print("\n")
            print(f"Total Income: RM{total_income:.2f}")
            print(f"Total Exspense: RM{total_exspense:.2f}")
            print(f"Net savings: RM{(total_income)-(total_exspense):.2f}")

            return filtered_df

        
    @classmethod#Input dictionary 
    def add_entry(cls, date, amount, category, description):
        new_entry ={
            "date": date,
            "amount": amount,
            "category": category,            
            "description": description
            }
        #Open CSV for data input
        with open(cls.CSV_FILE, "a", newline="") as csvfile: 
            writer= csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)            
            writer.writerow(new_entry)
            print("Entry added sucessfully")

def add():
    #Format for data input
    CSV.iniatialize_csv()
    #get data
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category =get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)
    
#plot function
def plot_transaction(df):
    df.set_index('date', inplace=True)

    income_df = (df[df["category"] == "Income"]
                 .resample("D") # resample data frame by day
                 .sum()
                 .reindex(df.index, fill_value = 0)
                 )
    
    exspense_df = (df[df["category"] == "Exspense"]
                 .resample("D") # resample data frame by day
                 .sum()
                 .reindex(df.index, fill_value = 0)
                 )
    #plot figure 
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label = "Income", color = "g")
    plt.plot(exspense_df.index, exspense_df["amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount") 
    plt.title('Income and Expense Over Time ')
    plt.legend()
    plt.grid(True)
    plt.show(block = True )

    

def main():
    while True:
        print("\n1. Add new transaction")
        print("2. View transaction and sumarry within a date range")
        print("3. exit")
        choice = input("Enter your Input (1-3): ")

        

        if choice == "1":
            add()
        elif  choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df =CSV.get_transaction(start_date, end_date)
            if input("Do you want to see the graph ? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            print("exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    main()



