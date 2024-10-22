import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import json
import os

root = tk.Tk()
root.title("WokWok Sales Calculator")

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, 'WokWok.png')
root.iconphoto(False, tk.PhotoImage(file=icon_path))

salesinput1 = 0
salesinput2 = 0
salesinput3 = 0
foodint = 3
selected_food_item = "Lohi sushi lajitelma"
selected_day = "Monday"
selected_sell = "20%"

def set_food_price(choice):
    global foodint, selected_food_item
    selected_food_item = choice
    if choice == "Lohi sushi lajitelma":
        foodint = 11.95
    elif choice == "Tonnikala mix":
        foodint = 10.95
    elif choice == "Sushi mix":
        foodint = 11.95
    elif choice == "Lohi nigiri":
        foodint = 11.95
    elif choice == "Lohi unelma":
        foodint = 11.95
    elif choice == "Vege mix":
        foodint = 11.95
    else:
        foodint = 0

def calculate_sales():
    global salesinput1, salesinput2, salesinput3, foodint
    
    try:
        salesinput1 = int(entry_kmarket1.get())
        salesinput2 = int(entry_kmarket2.get())
        salesinput3 = int(entry_kmarket3.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for sales.")
        return

    totalsalesamount = salesinput1 + salesinput2 + salesinput3
    
    if selected_sell == "20%":
        totalsales = foodint * totalsalesamount * 0.80
    elif selected_sell == "25%":
        totalsales = foodint * totalsalesamount * 0.75
    elif selected_sell == "28%":
        totalsales = foodint * totalsalesamount * 0.72
    elif selected_sell == "Buying":
        totalsales = 8.45 * totalsalesamount

    messagebox.showinfo("Total Sales", f"The total sale amount is: {totalsales:.2f}€")

    categories = ['K-market Lähde', 'K-market Ryhimäkki', 'K-market Kalasatama']
    sales_data = [salesinput1, salesinput2, salesinput3]
    
    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    ax.bar(categories, sales_data)
    
    ax.set_ylabel('Units Sold')
    ax.set_title('Sales per Store')

    ax.text(1.05, 0.95, f'Date: {selected_day}', transform=ax.transAxes, verticalalignment='top')
    ax.text(1.05, 0.90, f'Total Sales: {totalsales:.2f}€', transform=ax.transAxes, verticalalignment='top')

    plt.show()

def export_data():
    global salesinput1, salesinput2, salesinput3, selected_food_item, selected_day
    
    data = {
        "Food Type": selected_food_item,
        "Day": selected_day,
        "Sales": {
            "K-market Lähde": salesinput1,
            "K-market Ryhimäkki": salesinput2,
            "K-market Kalasatama": salesinput3
        },
        "Total Sales": foodint * (salesinput1 + salesinput2 + salesinput3)
    }

    file_path = filedialog.asksaveasfilename(defaultextension=".json", 
                                             filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")],
                                             title="Save Sales Data")

    if file_path:
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting data: {e}")

def import_data():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")],
                                            title="Open Sales Data")

    if file_path:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            global salesinput1, salesinput2, salesinput3
            salesinput1 = data["Sales"]["K-market Lähde"]
            salesinput2 = data["Sales"]["K-market Ryhimäkki"]
            salesinput3 = data["Sales"]["K-market Kalasatama"]
            total_sales = data["Total Sales"]
            food_type = data["Food Type"]
            day = data["Day"]

            categories = ['K-market Lähde', 'K-market Ryhimäkki', 'K-market Kalasatama']
            sales_data = [salesinput1, salesinput2, salesinput3]

            fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
            ax.bar(categories, sales_data)
            ax.set_ylabel('Units Sold')
            ax.set_title(f'Sales per Store for {food_type} on {day}')

            ax.text(1.05, 0.95, f'Total Sales: {total_sales:.2f}€', transform=ax.transAxes, verticalalignment='top')

            plt.show()

        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred while importing data: {e}")

food_options = ["Lohi sushi lajitelma", "Tonnikala mix", "Sushi Mix", "Lohi nigiri", "Lohi unelma", "Vege mix"]
selected_food = tk.StringVar(root)
selected_food.set(food_options[0])

label_food = tk.Label(root, text="Select Food Type:")
label_food.grid(row=0, column=0, padx=10, pady=10)

dropdown_food = tk.OptionMenu(root, selected_food, *food_options, command=set_food_price)
dropdown_food.grid(row=0, column=1, padx=10, pady=10)

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
selected_day_var = tk.StringVar(root)
selected_day_var.set(days_of_week[0])

def set_day(choice):
    global selected_day
    selected_day = choice

label_day = tk.Label(root, text="Select Day:")
label_day.grid(row=1, column=0, padx=10, pady=10)

dropdown_day = tk.OptionMenu(root, selected_day_var, *days_of_week, command=set_day)
dropdown_day.grid(row=1, column=1, padx=10, pady=10)

selling_options = ["20%", "25%", "28%", "Buying"]
selected_sell_var = tk.StringVar(root)
selected_sell_var.set(selling_options[0])

def set_sell(choice):
    global selected_sell
    selected_sell = choice

label_sell = tk.Label(root, text="Select Type of alv:")
label_sell.grid(row=2, column=0, padx=10, pady=10)

dropdown_sell = tk.OptionMenu(root, selected_sell_var, *selling_options, command=set_sell)
dropdown_sell.grid(row=2, column=1, padx=10, pady=10)

label_kmarket1 = tk.Label(root, text="K-market Lähde Sales:")
label_kmarket1.grid(row=3, column=0, padx=10, pady=10)
entry_kmarket1 = tk.Entry(root)
entry_kmarket1.grid(row=3, column=1, padx=10, pady=10)

label_kmarket2 = tk.Label(root, text="K-market Ryhimäkki Sales:")
label_kmarket2.grid(row=4, column=0, padx=10, pady=10)
entry_kmarket2 = tk.Entry(root)
entry_kmarket2.grid(row=4, column=1, padx=10, pady=10)

label_kmarket3 = tk.Label(root, text="K-market Kalasatama Sales:")
label_kmarket3.grid(row=5, column=0, padx=10, pady=10)
entry_kmarket3 = tk.Entry(root)
entry_kmarket3.grid(row=5, column=1, padx=10, pady=10)

btn_calculate = tk.Button(root, text="Calculate Total Sales", command=calculate_sales)
btn_calculate.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

btn_export = tk.Button(root, text="Export Data", command=export_data)
btn_export.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

btn_import = tk.Button(root, text="Import Data", command=import_data)
btn_import.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

