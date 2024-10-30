import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

root = tk.Tk()
root.title("WokWok Sales Calculator")

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, 'WokWok.png')
root.iconphoto(False, tk.PhotoImage(file=icon_path))

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

        row = len(sales_inputs) + 4  
        tk.Label(root, text=choice, name=f"label_{choice}").grid(row=row, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=tk.StringVar(value="0"), name=f"entry_{choice}_amount").grid(row=row, column=1, padx=10, pady=5)

        sale_rate_var = tk.StringVar(value="20%")

        sale_rate_menu = tk.OptionMenu(root, sale_rate_var, *sale_rates.keys(), command=lambda rate, food=choice: set_sale_rate(food, rate))
        sale_rate_menu.grid(row=row, column=2, padx=10, pady=5)
        sales_inputs[choice]["sale_rate_menu"] = sale_rate_menu
        sales_inputs[choice]["sale_rate_var"] = sale_rate_var

        tk.Button(root, text="Remove", command=lambda food=choice: remove_food_item(food), name=f"button_{choice}_remove").grid(row=row, column=3, padx=10, pady=5)

def set_store_price(choice):
    if choice not in sales_inputs:
        sales_inputs[choice] = {"amount": 0, "sale_rate": "20%"}
        row = len(sales_inputs) + 4
        tk.Label(root, text=choice, name=f"label_{choice}").grid(row=row, column=0, padx=15, pady=5)
        tk.Entry(root, textvariable=tk.StringVar(value="0"), name=f"entry_{choice}_amount").grid(row=row, column=1, padx=10, pady=5)
        
        sale_rate_var = tk.StringVar(value="20%")

        sale_rate_menu = tk.OptionMenu(root, sale_rate_var, *sale_rates.keys(), command=lambda rate, food=choice: set_sale_rate(food, rate))
        sale_rate_menu.grid(row=row, column=2, padx=15, pady=5)
        sales_inputs[choice]["sale_rate_menu"] = sale_rate_menu
        sales_inputs[choice]["sale_rate_var"] = sale_rate_var

        tk.Button(root, text="Remove", command=lambda store=choice: remove_store_item(store), name=f"button_{choice}_remove").grid(row=row, column=3, padx=15, pady=5)

def remove_store_item(store):
    if f"label_{store}" in root.children:
        root.nametowidget(f"label_{store}").grid_remove()

    if f"entry_{store}_amount" in root.children:
        root.nametowidget(f"entry_{store}_amount").grid_remove()

    if f"button_{store}_remove" in root.children:
        root.nametowidget(f"button_{store}_remove").grid_remove()

    if "sale_rate_menu" in sales_inputs[store]:
        sales_inputs[store]["sale_rate_menu"].grid_remove()

    if store in sales_inputs:
        del sales_inputs[store]

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

all_sales_data = {}
 
def load_sales_data():
    global all_sales_data
    file_path = 'sales_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            all_sales_data = json.load(file)

def save_sales_data():
    with open('sales_data.json', 'w') as file:
        json.dump(all_sales_data, file, indent=4)

def calculate_sales():
    global all_sales_data
    total_sales = 0

    selected_date = date_entry.get_date().strftime('%Y-%m-%d')
    selected_route = selected_route_var.get()

    for food_item, info in sales_inputs.items():
        amount_widget = root.nametowidget(f"entry_{food_item}_amount")
        try:
            amount = int(amount_widget.get())
        except ValueError:
            messagebox.showerror("Input Error", f"Please enter a valid number for {food_item}.")
            return

        sale_rate = sale_rates[info["sale_rate"]]
        if sale_rate is None and food_item in ["Lohi nigiri", "Lohi sushi lajitelma", "Lohi unelma", "Sushi mix", "Vege mix", "Tonnikala mix"]:
            price = 8.45
        elif sale_rate is None and food_item in ["Kungpo kana nuudeliwokki", "Mustapippurinauta", "Thai katkarapu nuudeliwokki", "Hapan makea kananuudeli wokki", "Tokyo BBQ nauta nuudeliwokki", "Bulgogi kana nuudeliwokki", "Thai curry kana nuudeliwokki", "Teriyaki kana nuudeliwokki", "Kasvis kevätkääryleet", "Korealainen makean tulinen kana riisillä", "Teriyaki kana riisillä", "Shanghai riisinuudeliwokki", "Paistettu riisi kanalla"]:
            price = 3.45
        elif food_item in ["Alepa Tripla", "KM Pohjoinen Rautatiekatu", "KM Lönnriotinkatu", "KM Freda",
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
                            "S itäkeskus", "KSM Basilika", "S Maunula", "KM Kivistö",
                            "Alepa Kivistö", "KSM Martsari", "Prisma Myyrmäki", "KM Kannelmäki",
                            "KSM Nikinmäki", "S Porttipuisto", "KM Hämeentie 42", "KM Töölöntori",
                            "KM Masala", "KM Kalasatama", "KSM Torpparinmäki", "KM Heikinlaakso",
                            "KSM Söderkulla", "KSM Korso", "KM Öster", "KM Tapuli",
                            "KSM Arabia", "KM Roba", "KM Munkki", "KSM Lähde", "KSM Nurmijärvi"
                            ]:
            price = 1
        else:
            price = food_prices[food_item] * sale_rate

        total_sale = price * amount
        total_sales += total_sale

        if food_item not in all_sales_data:
            all_sales_data[food_item] = {"dates": [], "totals": []}
        all_sales_data[food_item]["dates"].append(selected_date)
        all_sales_data[food_item]["totals"].append(total_sale)

    save_sales_data()
    messagebox.showinfo("Total Sales", f"The total sale amount is: {total_sales:.2f}€")

    plot_sales(selected_route)

def plot_sales(selected_route):
    fig, ax = plt.subplots(figsize=(10, 5))

    for food_item, data in all_sales_data.items():
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in data["dates"]]
        ax.plot(dates, data["totals"], label=food_item, marker='o', linestyle='-', linewidth=1)

        for i, txt in enumerate(data["dates"]):
            ax.annotate(txt, (dates[i], data["totals"][i]), textcoords="offset points", xytext=(5,5), ha='center', fontsize=8)

    ax.set_xlabel('Date')
    ax.set_ylabel('Total Revenue (€)')
    ax.set_title(f'Total Sales for {selected_route}')
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8)

    plt.tight_layout()
    plt.show()

load_sales_data()

def export_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")], title="Save Sales Data")
    if file_path:
        with open(file_path, 'w') as file:
            json.dump(all_sales_data, file, indent=4)
        messagebox.showinfo("Export Successful", f"Data exported successfully to {file_path}")

def import_data():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Open Sales Data")
    if file_path:
        with open(file_path, 'r') as file:
            all_sales_data = json.load(file)

        sales_inputs.clear()
        for row, (food_item, info) in enumerate(all_sales_data.items(), start=5):
            set_food_price(food_item)
            root.nametowidget(f"entry_{food_item}_amount").delete(0, tk.END)
            root.nametowidget(f"entry_{food_item}_amount").insert(0, info["amount"])
            sales_inputs[food_item]["sale_rate_var"].set(info["sale_rate"])

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
    "S itäkeskus", "KSM Basilika", "S Maunula", "KM Kivistö",
    "Alepa Kivistö", "KSM Martsari", "Prisma Myyrmäki", "KM Kannelmäki",
    "KSM Nikinmäki", "S Porttipuisto", "KM Hämeentie 42", "KM Töölöntori",
    "KM Masala", "KM Kalasatama", "KSM Torpparinmäki", "KM Heikinlaakso",
    "KSM Söderkulla", "KSM Korso", "KM Öster", "KM Tapuli",
    "KSM Arabia", "KM Roba", "KM Munkki", "KSM Lähde", "KSM Nurmijärvi"
]

selected_food_var = tk.StringVar(root)
selected_food_var.set(food_options[0])
selected_store_var = tk.StringVar(root)
selected_store_var.set(store_options[0])

label_food = tk.Label(root, text="Select Food Type:")
label_food.grid(row=0, column=0, padx=10, pady=10)
dropdown_food = tk.OptionMenu(root, selected_food_var, *food_options, command=set_food_price)
dropdown_food.grid(row=0, column=1, padx=10, pady=10)

label_store = tk.Label(root, text="Select Store:")
label_store.grid(row=1, column=0, padx=15, pady=10)
dropdown_store = tk.OptionMenu(root, selected_store_var, *store_options, command=set_store_price)
dropdown_store.grid(row=1, column=1, padx=15, pady=10)

label_date = tk.Label(root, text="Select Date:")
label_date.grid(row=2, column=0, padx=10, pady=10)
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=2, column=1, padx=10, pady=10)

label_route = tk.Label(root, text="Select Round:")
label_route.grid(row=3, column=0, padx=10, pady=10)
routes = ["Round 1", "Round 2", "Round 3", "Round 4", "Round 5", "Round 6", "Round 7", "Round 8", "Tuesday", "Vantaa", "Tampere", "Espoo", "Järvenpää East Vantaa", "Wednesday Kacper", "Grani only wed", "Torppa Nurmi"]
selected_route_var = tk.StringVar(root)
selected_route_var.set(routes[0])
dropdown_route = tk.OptionMenu(root, selected_route_var, *routes)
dropdown_route.grid(row=3, column=1, padx=10, pady=10)

btn_calculate = tk.Button(root, text="Calculate Total Sales", command=calculate_sales)
btn_calculate.grid(row=4, column=0, padx=10, pady=10)

btn_export = tk.Button(root, text="Export Sales Data", command=export_data)
btn_export.grid(row=4, column=1, padx=10, pady=10)

btn_import = tk.Button(root, text="Import Sales Data", command=import_data)
btn_import.grid(row=4, column=2, padx=10, pady=10)

root.mainloop()