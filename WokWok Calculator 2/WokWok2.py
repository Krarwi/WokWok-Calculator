import tkinter as tk
import pandas as pd
from tkinter import messagebox, filedialog, ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

root = tk.Tk()
root.attributes('-fullscreen',True)
root.title("WokWok Sales Calculator")
root.configure(background="azure2")

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, 'WokWok.png')
if os.path.exists(icon_path):
    root.iconphoto(False, tk.PhotoImage(file=icon_path))
else:
    print("Icon file not found")

sales_inputs = {}
sale_rates = {"20%": 0.80, "25%": 0.75, "30%": 0.70, "Buying": None}
all_sales_data = {}

store_options = [
    "Alepa Tripla", "KM Pohjoinen Rautatiekatu", "KM Lönnriotinkatu", "KM Freda",
    "KM Eerikinkatu", "KM Lönkan Herkku", "KM Albertin Herkku",
    "KM Erottaja", "KM Espa",
    "S Kasarmitori", "KM Liisankatu",
    "KSM Munkki", "Alepa Munkki",
    "KM Otaniemi", "S Pohjois-Tapiola",
    "KSM Masi", "KM Roihuvuori",
    "S Pakila", "S Pukinmäki", "Prisma Malmi", "S Jakomäki", "S Lähdenranta",
    "Alepa Viherlaakso", "KSM Malminmäki", "S Nöykkiö", "S Kivenlahdentie",
    "K Matinkylä", "S Tuusula", "S Korso", "Prisma Tikkurila", "KM Suutarila",
    "KM Töyrynummi", "S Kaivoksela", "Alepa Airport", "KSM Vihti",
    "KSM Lempola", "KM Mansku", "Alepa Kisahalli", "KM Pikku-Huopalahti",
    "KM Ruskeasuo", "KM Krunikka", "KM Katajanokka", "KSM Kaisaniemi",
    "KM Hakaniemen Herkku", "KM Lyyra", "KM Kallio", "KM Sörkka",
    "KM Amerinkulma", "KM Masurkka", "KM Pasaati", "KM Museokatu",
    "KM Meclu", "KM Kotikontu", "Alepa Kamppi", "KM Jätkäsaari",
    "KSM Westbest", "KSM Vattuniemi", "KM Kasinonranta", "KM Maarinsolmu",
    "KM Ravioli", "S Grani", "KM Kivenlahti", "KM Sorsakivi",
    "Alepa Westend", "KSM Pohjois-Haaga", "KSM Haaga", "KSM Kontumarket",
    "S Itäkeskus", "KSM Basilika", "S Maunula", "KM Kivistö",
    "Alepa Kivistö", "KSM Martsari", "Prisma Myyrmäki", "KM Kannelmäki",
    "KSM Nikinmäki", "S Porttipuisto", "KM Hämeentie 42", "KM Töölöntori",
    "KM Masala", "KM Kalasatama", "KSM Torpparinmäki", "KM Heikinlaakso",
    "KSM Söderkulla", "KSM Korso", "KM Öster", "KM Tapuli",
    "KSM Arabia", "KM Roba", "KM Munkki", "KSM Lähde", "KSM Nurmijärvi"
]

food_options = [
    "Lohi sushi lajitelma", "Tonnikala mix", "Sushi mix", "Lohi nigiri",
    "Kungpo kana nuudeliwokki", "Mustapippurinauta", "Thai katkarapu nuudeliwokki",
    "Hapan makea kananuudeli wokki", "Tokyo BBQ nauta nuudeliwokki",
    "Bulgogi kana nuudeliwokki", "Thai curry kana nuudeliwokki",
    "Teriyaki kana nuudeliwokki", "Kasvis kevätkääryleet",
    "Korealainen makean tulinen kana riisillä", "Teriyaki kana riisillä",
    "Shanghai riisinuudeliwokki", "Paistettu riisi kanalla",
    "Vege mix", "Lohi unelma"
]

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

sushi = ["Lohi sushi lajitelma", "Tonnikala mix", "Sushi mix", "Lohi nigiri", "Lohi unelma", "Vege mix"]

chinese_food = ["Teriyaki kana riisillä", "Bulgogi kana nuudeliwokki", "Tokyo BBQ nauta nuudeliwokki", "Hapan makea kananuudeli wokki", "Thai katkarapu nuudeliwokki",
                "Mustapippurinauta", "Thai curry kana nuudeliwokki", "Teriyaki kana nuudeliwokki", "Kasvis kevätkääryleet", "Korealainen makean tulinen kana riisillä",
                "Shanghai riisinuudeliwokki", "Paistettu riisi kanalla"]

round_store_mapping = {
    "Round 1": ["Alepa Tripla", "KM Pasaati", "KM Amerinkulma", "KM Marsukka", "KSM Arabia", "KM Kalasatama", "KM Liisankatu", "KM Krunika", 
                "KM Katajanokka", "S Kasarmitori", "KM Roba", "KM Erottaja", "KM Espa", "KSM Kaisaniemi", "KM Hakan Herkku", "KM Lyyra", 
                "KM Kallio", "KM Sorkka", "KM Hämeentie 42"],
    "Round 2": ["KM Mansku", "Alepa Kisahalli", "KM Töölöntori", "KM Museokatu", "KM Meclu", "KM Pohjoinen Rautatiekatu", 
                "KM Kotikontu", "KM Freda", "Alepa Kamppi", "KM Eerikinkatu", "KM Lönkan Herkku", "KM Albertin Herkku",
                "KSM Westbest", "KSM Vattuniemi", "KM Kasinonranta", ],
    "Round 3": ["S Pohjois-Tapiola", "KM Maarinsolmu", "KM Otaniemi", "S Lähdenranta", "Alepa Viherlaakso", "KM Ravioli", 
                "S Grani", "KSM Malminmäki", "S Nöykkiö", "S Kivenlahdentie", "KM Kivenlahti", "KM Sorsakivi", "Alepa Westend", "KSM Lempola"],
    "Round 4": ["KSM Pohjois-Haaga", "KSM Haaga", "KSM Munkki", "Alepa Munkki"],
    "Round 5": ["KM Kannelmäki", "S Maunula", "S Pakila", "KSM Torpparinmäki", "KM Pukin", "S Pukinmäki", "Prisma Malmi", "KM Töyrynummi", 
                "KM Suutarila", "KM Tapuli", "KM Heikinlaakso", "S Jakomäki", "KSM Masi", "KSM Kontumarket", "S Itäkeskus", "KM Roihuvuori", "KM Öster",
                "KSM Söderkulla", "KSM Basilika"],
    "Round 6": ["KSM Torpparinmäki", "KSM Nurmijärvi", "KSM Lähde", "S Tuusula", "S Korso", "KSM Korso", "KSM Nikinmäki", "S Porttipuisto", "Prisma Tikkurila"],
    "Round 7": ["S Kaivoksela", "Prisma Myyrmäki", "KSM Martsari", "KM Kivistö", "Alepa Kivistö", "Alepa Airport"],
    "Round 8": [""],
    "Overall": store_options
}

delivery_drivers = 8
chefs = 4
delivery_hourly_salary = 11 * 1.4
chef_hourly_salary = 12 * 1.4
delivery_hours = 8
chef_hours = 8

round_distances = {
    "Round 1": 28.5,
    "Round 2": 18.6,
    "Round 3": 100.1,
    "Round 4": 6.4,
    "Round 5": 78.1,
    "Round 6": 94.3,
    "Round 7": 23,
    "Round 8": 0,
    "Overall": 376
}

def update_store_options(*args):
    round_selected = selected_route_var.get()
    store_menu['menu'].delete(0, 'end')
    for store in round_store_mapping[round_selected]:
        store_menu['menu'].add_command(label=store, command=tk._setit(store_var, store))

food_entries = {}

def update_food_entries():
    global first_entry
    first_entry = None
    try:
        if first_entry and first_entry.winfo_exists():
            first_entry.focus_set()
        else:
            print("First entry does not exist.")
    except Exception as e:
        print(f"Error in update_food_entries: {e}")

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget.winfo_name().startswith("food_row_"):
            widget.destroy()

    selected_chinese_foods = [chinese_food_listbox.get(i) for i in chinese_food_listbox.curselection()]
    selected_sushi_foods = [sushi_listbox.get(i) for i in sushi_listbox.curselection()]

    selected_foods = set(selected_chinese_foods + selected_sushi_foods)

    row_frame = None
    item_count = 0

    def enter_remove_focus(event):
        entry.insert(0, "")
        root.focus_set()

    for food in selected_foods:
        if item_count % 4 == 0:
            row_frame = tk.Frame(root, name=f"food_row_{item_count // 4}", background="azure2")
            row_frame.pack(pady=5, padx=5, anchor="center")

        label = tk.Label(row_frame, text=f"{food} (Quantity): ", background="azure2")
        label.pack(side="left", padx=(0, 5))

        entry = tk.Entry(row_frame, name=f"entry_{food}_amount")
        entry.insert(0, "")
        entry.pack(side="left", padx=(0, 15))

        entry.bind("<Return>", enter_remove_focus)

        food_entries[food] = (label, entry)

        item_count += 1

    if food_entries:
        first_entry = list(food_entries.values())[0][1]
        first_entry.focus_set()

def load_sales_data():
    global all_sales_data
    file_path = 'allsales_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            all_sales_data = json.load(file)

def save_sales_data():
    with open('sales_data.json', 'w') as file:
        json.dump(all_sales_data, file, indent=4)

def calculate_sales():
    global all_sales_data
    total_sales = 0
    other_expenses = 0

    selected_route = selected_route_var.get()
    selected_store = store_var.get()

    for food_item, (label, entry) in food_entries.items():
        if entry.winfo_exists():
            try:
                quantity = int(entry.get())
            except ValueError:
                quantity = 0
        else:
            quantity = 0

        sale_rate_key = "default_rate"
        sale_rate = sale_rates.get(sale_rate_key, 1)

        if sale_rate is None and food_item in ["Lohi nigiri", "Lohi sushi lajitelma", "Lohi unelma", "Sushi mix", "Vege mix", "Tonnikala mix"]:
            price = 8.45
        elif sale_rate is None and food_item in ["Kungpo kana nuudeliwokki", "Mustapippurinauta", "Thai katkarapu nuudeliwokki", "Hapan makea kananuudeli wokki"]:
            price = 3.45
        else:
            price = food_prices.get(food_item, 0) * sale_rate

        total_sale = price * quantity
        total_sales += total_sale

        if food_item not in all_sales_data:
            all_sales_data[food_item] = {"stores": [], "totals": []}
        all_sales_data[food_item]["stores"].append(selected_store)
        all_sales_data[food_item]["totals"].append(total_sale)

    delivery_driver_salary = delivery_drivers * delivery_hours * delivery_hourly_salary
    chef_salary = chefs * chef_hours * chef_hourly_salary
    distance = round_distances.get(selected_route, 0)

    distance_cost = round_distances.get(selected_route, 0) * 0.30
    total_cost = distance_cost + delivery_driver_salary + chef_salary + other_expenses

    try:
        other_expenses = float(other_expenses_entry.get())
    except ValueError:
        other_expenses = 0 

    save_sales_data()
    messagebox.showinfo("Total Sales", f"The total sale amount is: {total_sales:.2f}€\nTotal Cost: {total_cost:.2f}€")
    plot_sales(selected_route, distance_cost)
    print("Sales data: ", all_sales_data)

def reset_sales_data():
    global all_sales_data
    all_sales_data.clear()
    save_sales_data()
    messagebox.showinfo("Reset Successful", "All sales data has been reset.")
    for food in sales_inputs.keys():
        root.nametowidget(f"entry_{food}_amount").delete(0, tk.END)
        root.nametowidget(f"entry_{food}_amount").insert(0, "0")
        sales_inputs[food]["sale_rate_var"].set("20%")

def exit():
    root.quit()

def export_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("Excel files", "*.xlsx")], title="Save Sales Data")
    if file_path:
        if file_path.endswith(".json"):
            with open(file_path, 'w') as file:
                json.dump(all_sales_data, file, indent=4)
            messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

        elif file_path.endswith(".xlsx"):
            try:
                with pd.ExcelWriter(file_path) as writer:
                    rows = []

                    for food_item, data in all_sales_data.items():
                        for store, total in zip(data["stores"], data["totals"]):
                            rows.append({
                                "Food Item": food_item,
                                "Store": store,
                                "Total": total
                            })

                    df = pd.DataFrame(rows)

                    df.to_excel(writer, index=False, sheet_name="Sales Data")
                messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred while exporting: {e}")


def import_data():
    global all_sales_data
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("Excel files", "*.xlsx")], 
        title="Import Sales Data"
    )
    if file_path:
        if file_path.endswith(".json"):
            try:
                with open(file_path, 'r') as file:
                    all_sales_data = json.load(file)
                messagebox.showinfo("Import Successful", f"Data imported successfully from {file_path}")
            except json.JSONDecodeError:
                messagebox.showerror("Import Error", "Failed to import JSON data")
        elif file_path.endswith(".xlsx"):
            try:
                excel_data = pd.ExcelFile(file_path)
                new_sales_data = {}
                for sheet_name in excel_data.sheet_names:
                    df = excel_data.parse(sheet_name)
                    food_items = df['Food Item'].tolist()
                    stores = df['Store'].tolist()
                    totals = df['Total'].tolist()
                    for food_item, store, total in zip(food_items, stores, totals):
                        if food_item not in new_sales_data:
                            new_sales_data[food_item] = {"stores": [], "totals": []}
                        new_sales_data[food_item]["stores"].append(store)
                        new_sales_data[food_item]["totals"].append(total)
                all_sales_data.update(new_sales_data)
                messagebox.showinfo("Import Successful", f"Data imported successfully from {file_path}")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import Excel data Error: {e}")
        save_sales_data()

def plot_sales(selected_route, distance_cost):
    fig, ax = plt.subplots(figsize=(14, 8))

    store_names = round_store_mapping[selected_route]
    store_sales = {store: {"all": 0, "sushi": 0, "chinese": 0} for store in store_names}

    round_distances = {
        "Round 1": 28.5,
        "Round 2": 18.6,
        "Round 3": 100.1,
        "Round 4": 6.4,
        "Round 5": 78.1,
        "Round 6": 94.3,
        "Round 7": 23,
        "Round 8": 0,
        "Overall": 376
    }
    delivery_driver_salary = delivery_drivers * delivery_hours * delivery_hourly_salary
    chef_salary = chefs * chef_hours * chef_hourly_salary

    distance = round_distances.get(selected_route, 0)
    total_cost = distance * 0.30 + delivery_driver_salary + chef_salary

    total_sales = 0
    for food_item, data in all_sales_data.items():
        for store, total_sale in zip(data["stores"], data["totals"]):
            if store in store_sales:
                store_sales[store]["all"] += total_sale
                if food_item in sushi:
                    store_sales[store]["sushi"] += total_sale
                elif food_item in chinese_food:
                    store_sales[store]["chinese"] += total_sale
            total_sales += total_sale

    x_positions = list(range(len(store_names)))
    width = 0.25 

    total_sales_values = [store_sales[store]["all"] for store in store_names]
    sushi_sales_values = [store_sales[store]["sushi"] for store in store_names]
    chinese_sales_values = [store_sales[store]["chinese"] for store in store_names]

    ax.bar(x_positions, total_sales_values, width=width, color="skyblue", label="Total Sales (€)")
    ax.bar([x + width for x in x_positions], sushi_sales_values, width=width, color="salmon", label="Sushi Sales (€)")
    ax.bar([x + 2 * width for x in x_positions], chinese_sales_values, width=width, color="lightgreen", label="Chinese Food Sales (€)")

    ax.bar(len(store_names) + 1, total_sales, width=width * 1.5, color="blue", label="Overall Total Sales (€)")
    ax.bar(len(store_names) + 2.5, total_cost, width=width * 1.5, color="grey", label="Total Costs (€)")

    ax.set_xticks([x + width for x in x_positions] + [len(store_names) + 1, len(store_names) + 2.5])
    ax.set_xticklabels(store_names + ["Total Sales", "Total Costs"], rotation=45, ha="right")

    ax.set_xlabel('Store')
    ax.set_ylabel('Revenue (€)')
    ax.set_title(f'Total Sales and Costs for {selected_route}')
    ax.legend()
    plt.tight_layout()
    plt.show()

load_sales_data()

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

frame_sales = tk.Frame(notebook, background="azure2")
frame_costs = tk.Frame(notebook, background="azure2")

notebook.add(frame_sales, text="Calculate Total Sales")
notebook.add(frame_costs, text="Calculate Total Costs")

round_label = tk.Label(frame_sales, text="Select Round:", background="azure2", font=("Helvetica", 12, "bold"))
round_label.pack(pady=10)

selected_route_var = tk.StringVar(root)
selected_route_var.set("Round 1")
round_menu = tk.OptionMenu(frame_sales, selected_route_var, *round_store_mapping.keys())
round_menu.pack(pady=10)

store_label = tk.Label(frame_sales, text="Select Store:", background="azure2", font=("Helvetica", 12, "bold"))
store_label.pack(pady=10)

store_var = tk.StringVar(root)
store_var.set(round_store_mapping["Round 1"][0])
store_menu = tk.OptionMenu(frame_sales, store_var, *round_store_mapping["Round 1"])
store_menu.pack(pady=10)

selected_route_var.trace("w", update_store_options)

food_label = tk.Label(frame_sales, text="Select Food Items and Quantity:", background="azure2", font=("Helvetica", 12, "bold"))
food_label.pack(pady=10)

chinese_food_listbox = tk.Listbox(frame_sales, selectmode=tk.MULTIPLE, height=10, exportselection=False)
for food in chinese_food:
    chinese_food_listbox.insert(tk.END, food)
chinese_food_listbox.pack(pady=10)
chinese_food_listbox.bind('<<ListboxSelect>>', lambda e: update_food_entries())

sushi_listbox = tk.Listbox(frame_sales, selectmode=tk.MULTIPLE, height=10, exportselection=False)
for food in sushi:
    sushi_listbox.insert(tk.END, food)
sushi_listbox.pack(pady=10)
sushi_listbox.bind('<<ListboxSelect>>', lambda e: update_food_entries())

select_button = tk.Button(frame_sales, text="Calculate Sales", command=calculate_sales)
select_button.pack(pady=10)

btn_reset = tk.Button(frame_sales, text="Reset Sales Data", command=reset_sales_data)
btn_reset.pack(pady=10)

btn_export = tk.Button(frame_sales, text="Export Sales Data", command=export_data)
btn_export.pack(pady=10)

btn_import = tk.Button(frame_sales, text="Import Sales Data", command=import_data)
btn_import.pack(pady=10)

btn_exit = tk.Button(frame_sales, text="Exit", command=exit)
btn_exit.pack(pady=10)

salary_label = tk.Label(frame_costs, text="Select Salaries:", background="azure2", font=("Helvetica", 12, "bold"))
salary_label.pack(pady=10)

#chef_hours_label = tk.Label(frame_costs, text="Chef Hours:", background="azure2")
#chef_hours_label.pack(pady=10)
#chef_hours_entry = tk.Entry(frame_costs, name=f"entry_chef_hours_amount")
#chef_hours_entry.insert(0, "")
#chef_hours_entry.pack(pady=0)

#driver_hours_label = tk.Label(frame_costs, text="Driver Hours:", background="azure2")
#driver_hours_label.pack(pady=10)
#driver_hours_entry = tk.Entry(frame_costs, name=f"entry_driver_hours_amount")
#driver_hours_entry.insert(0, "")
#driver_hours_entry.pack(pady=0)

other_expenses_label = tk.Label(frame_costs, text="Other Expenses:", background="azure2")
other_expenses_label.pack(pady=10)
other_expenses_entry = tk.Entry(frame_costs, name=f"entry_other_expenses_amount")
other_expenses_entry.insert(0, "")
other_expenses_entry.pack(pady=0)

root.mainloop()