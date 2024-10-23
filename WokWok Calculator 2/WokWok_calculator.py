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

selected_day = "Monday"

food_prices = {
    "Lohi sushi lajitelma": 11.95,
    "Tonnikala mix": 10.95,
    "Sushi mix": 11.95,
    "Lohi nigiri": 11.95,
    "Kungpo kana nuudeliwokki": 5.99,
    "Mustapippurinauta": 5.99,
    "Thai katkarapu nuudeliwokki": 5.99,
    "Hapan makea kananuudeli wokki": 5.99,
    "Tokyo BBQ nauta nuudeliwokki": 5.99,
    "Bulgogi kana nuudeliwokki": 5.99,
    "Thai curry kana nuudeliwokki": 5.99,
    "Teriyaki kana nuudeliwokki": 5.99,
    "Kasvis kevätkääryleet": 5.99,
    "Korealainen makean tulinen kana riisillä": 5.99,
    "Teriyaki kana riisillä": 5.99,
    "Shanghai riisinuudeliwokki": 5.99,
    "Paistettu riisi kanalla": 5.99,
    "Vege mix": 11.95,
    "Lohi unelma": 11.95,
    
}

sales_inputs = {}

sale_rates = {"20%": 0.80, "25%": 0.75, "30%": 0.70, "Buying": None}

def set_food_price(choice):
    if choice not in sales_inputs:
        sales_inputs[choice] = {"amount": 0, "sale_rate": "20%"}
        
        row = len(sales_inputs) + 3  
        tk.Label(root, text=choice, name=f"label_{choice}").grid(row=row, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=tk.StringVar(value="0"), name=f"entry_{choice}_amount").grid(row=row, column=1, padx=10, pady=5)

        sale_rate_var = tk.StringVar(value="20%")
        
        sale_rate_menu = tk.OptionMenu(root, sale_rate_var, *sale_rates.keys(), command=lambda rate, food=choice: set_sale_rate(food, rate))
        sale_rate_menu.grid(row=row, column=2, padx=10, pady=5)
        sales_inputs[choice]["sale_rate_menu"] = sale_rate_menu
        
        sales_inputs[choice]["sale_rate_var"] = sale_rate_var

        tk.Button(root, text="Remove", command=lambda food=choice: remove_food_item(food), name=f"button_{choice}_remove").grid(row=row, column=3, padx=10, pady=5)

def remove_food_item(food):
    if f"label_{food}" in root.children:
        root.nametowidget(f"label_{food}").grid_remove()
    
    if f"entry_{food}_amount" in root.children:
        root.nametowidget(f"entry_{food}_amount").grid_remove()
    
    if f"button_{food}_remove" in root.children:
        root.nametowidget(f"button_{food}_remove").grid_remove()
    
    if "sale_rate_menu" in sales_inputs[food]:
        sales_inputs[food]["sale_rate_menu"].grid_remove()

    if food in sales_inputs:
        del sales_inputs[food]

def set_sale_rate(food, rate):
    sales_inputs[food]["sale_rate"] = rate

def calculate_sales():
    total_sales = 0
    total_sales_data = []
    food_items = []
    
    current_day = selected_day_var.get()  
    
    for food_item, info in sales_inputs.items():
        amount_widget = root.nametowidget(f"entry_{food_item}_amount")
        try:
            amount = int(amount_widget.get())
        except ValueError:
            messagebox.showerror("Input Error", f"Please enter a valid number for {food_item}.")
            return
        
        sale_rate = sale_rates[info["sale_rate"]]
        if sale_rate is None:
            price = 8.45
        else:
            price = food_prices[food_item] * sale_rate
        
        total_sale = price * amount
        total_sales += total_sale
        total_sales_data.append(total_sale)
        food_items.append(food_item)
    
    messagebox.showinfo("Total Sales", f"The total sale amount is: {total_sales:.2f}€")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(food_items, total_sales_data)
    
    ax.set_ylabel('Total Sales (€)')
    ax.set_title(f'Total Sales for Selected Items on {current_day}')
    ax.text(1.05, 0.80, f'Total Sales: {total_sales:.2f}€', transform=ax.transAxes, verticalalignment='top')
    
    plt.xticks(rotation=45, ha="right")  
    plt.tight_layout()
    plt.show()

def export_data():
    data = {food: {"amount": root.nametowidget(f"entry_{food}_amount").get(), "sale_rate": info["sale_rate"]} for food, info in sales_inputs.items()}
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")], title="Save Sales Data")
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

def import_data():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Open Sales Data")
    if file_path:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        sales_inputs.clear()
        for row, (food_item, info) in enumerate(data.items(), start=4):
            set_food_price(food_item)
            root.nametowidget(f"entry_{food_item}_amount").delete(0, tk.END)
            root.nametowidget(f"entry_{food_item}_amount").insert(0, info["amount"])
            sales_inputs[food_item]["sale_rate_var"].set(info["sale_rate"])

food_options = ["Lohi sushi lajitelma", "Tonnikala mix", "Sushi mix", "Lohi nigiri", "Kungpo kana nuudeliwokki", "Mustapippurinauta", "Thai katkarapu nuudeliwokki", "Hapan makea kananuudeli wokki", "Tokyo BBQ nauta nuudeliwokki", "Bulgogi kana nuudeliwokki", "Thai curry kana nuudeliwokki", "Teriyaki kana nuudeliwokki", "Kasvis kevätkääryleet", "Korealainen makean tulinen kana riisillä", "Teriyaki kana riisillä", "Shanghai riisinuudeliwokki", "Paistettu riisi kanalla", "Vege mix", "Lohi unelma"]
selected_food_var = tk.StringVar(root)
selected_food_var.set(food_options[0])

label_food = tk.Label(root, text="Select Food Type:")
label_food.grid(row=0, column=0, padx=10, pady=10)
dropdown_food = tk.OptionMenu(root, selected_food_var, *food_options, command=set_food_price)
dropdown_food.grid(row=0, column=1, padx=10, pady=10)

label_day = tk.Label(root, text="Select Day:")
label_day.grid(row=1, column=0, padx=10, pady=10)
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
selected_day_var = tk.StringVar(root)
selected_day_var.set(days_of_week[0])
dropdown_day = tk.OptionMenu(root, selected_day_var, *days_of_week, command=selected_day_var)
dropdown_day.grid(row=1, column=1, padx=10, pady=10)

btn_calculate = tk.Button(root, text="Calculate Total Sales", command=calculate_sales)
btn_calculate.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

btn_export = tk.Button(root, text="Export Data", command=export_data)
btn_export.grid(row=3, column=0, padx=10, pady=10)

btn_import = tk.Button(root, text="Import Data", command=import_data)
btn_import.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()
