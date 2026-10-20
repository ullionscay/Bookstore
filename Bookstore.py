#Contributers: Ciaran Scullion, Matthew Kerr, Luke Mcmorrow
import pandas as pd
import matplotlib.pyplot as plt 

def display_menu():
    print("\nBOOK STOCK MENU")
    print("1. List all book titles and details")
    print("2. Show summary report")
    print("3. Show number of titles in each genre")
    print("4. Add a new book item")
    print("5. Query/update stock level for a book")
    print("6. List books alphabetically by author")
    print("7. Plot genre bar chart")
    print("8. Exit")

def book_titles(): #1

    df = pd.read_csv("Books data.csv")
    print(df.to_string(index=False))

def show_summary(): #2
    df = pd.read_csv("Books data.csv")
    total_titles= df["Title"].nunique()
    total_value= (df['Cost'] * df['Stock']).sum()
    avg_price= df['Cost'].mean()
    print(f"""

     BOOK SUMMARY REPORT
   
    Total number of titles : {total_titles}
    Total stock value      : £{total_value:.2f}
    Average book price     : £{avg_price:.2f}
    
   """)

def titles_genre(): #3
    df = pd.read_csv("Books data.csv")
    genre_counts= df['Genre'].value_counts()
    total_count= genre_counts.sum()
    print("Titles per Genre")
    print(genre_counts)
    print("Total number of titles" , total_count)

def add_new_book(): #4
    df = pd.read_csv("Books data.csv")
    before= df['Title'].nunique() #count before

    new_book= {
        "Author": input("Enter Author: "),
        "Title": input("Enter Title: "),
        "Format": input("Enter Format: pb/hb "),
        "Publisher": input("Enter Publisher: "),
        "Cost": float(input("Enter Cost: ")),
        "Stock": int(input("Enter Stock: ")),
        "Genre": input("Enter Genre: "),
    }
    df= pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    after= df['Title'].nunique() #count after
    increase= after - before # counting increase in books

    df.to_csv("Books data.csv", index=False)

    print("Book added successfully!")

    print(f'\n Titles before: {before}')
    print(f'\n Titles after: {after}')
    print(f'\n Increase: {increase}')



def stock_menu(): #5
        df = pd.read_csv("Books data.csv")
        book_name = input("Enter book title: ")
        match = df["Title"].str.lower().str.contains(book_name.lower())
        book_match = df[match]

        if book_match.empty:
            print("Book not found.")
            return

        index= book_match.index[0]
        stock = int(df.loc[index, "Stock"])
        title= df.loc[index, "Title"]

        print(f'\nTitle: {title}')
        print(f'Current stock: {stock}')

        print('\n Stock Options')
        print('1. Increase Stock')
        print('2. Decrease Stock due to a sale')

        choice= input("Enter your choice: ")

        if choice == "1":
            try:
                amount= int(input("Enter amount: "))
            except ValueError:
                print('Invalid Input. Please enter a number.')
                return

            if amount <= 0:
                print("Invalid amount: Amount must be greater than 0")
                return

            df.loc[index, "Stock"] = stock + amount
            print(f'Stock Increased. New stock: {stock + amount}')

        elif choice == "2":
            try:
                amount= int(input("Enter amount sold: "))
            except ValueError:
                print('Please enter a number.')
                return

            if amount <= 0:
                print("Invalid amount: Amount must be greater than 0")
                return

            if amount > stock:
                print('Not enough stock available.')
                return

            new_stock= stock - amount
            df.loc[index, "Stock"] = new_stock
            print(f'Stock Decreased. New stock: {new_stock}')

            if new_stock == 0:
                print("Out of stock")

        else:
            print('Invalid choice.')
            return

        df.to_csv("Books data.csv", index=False)
        print("Stock updated successfully.")


def sort_alphabetically(): #6
    df= pd.read_csv("Books data.csv")
    df_sorted= df.sort_values(by='Author', ascending=True)
    print(df_sorted.to_string(index=False))


def plot_genre(): #7
    df = pd.read_csv("Books data.csv")

    genre_counts = df["Genre"].value_counts()

    genre_counts.plot(kind="bar", rot= 45)

    plt.xlabel("Genre")
    plt.ylabel("Number of Books")
    plt.title("Number of Books in Each Genre")
    plt.tight_layout()
    plt.show()


def main():
    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Outputting list of book titles and details...")
            book_titles()

        elif choice == "2":
            print("Displaying summary report...")
            show_summary()

        elif choice == "3":
            print("Displaying number of titles in each genre...")
            titles_genre()

        elif choice == "4":
            print("Adding a new book item...")
            add_new_book()

        elif choice == "5":
            print("Querying book availability...")
            stock_menu()

        elif choice == "6":
            print("Listing books alphabetically by author...")
            sort_alphabetically()

        elif choice == "7":
            print("Plotting genre bar chart...")
            plot_genre()

        elif choice == "8":
            print("Exiting program...")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 8.")


main()