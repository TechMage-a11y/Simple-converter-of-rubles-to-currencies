import tkinter as tk
from tkinter import ttk, messagebox

CURRENCY = {
    "USD": 77.1880,
    "EUR": 91.7113,
    "CNY": 11.1582,
    "GBP": 105.2304,
    "CHF": 100.4790,
    "JPY": 0.5042,
    "KZT": 0.1573,
    "AED": 21.0178
}

def convert():
    try:
        amount = float(entry.get())
        if amount <= 0:
            messagebox.showerror("Ошибка", "Сумма > 0!")
            return
        curr = combo.get()
        rate = CURRENCY[curr]
        result = amount / rate
        res_text = f"{int(result)} {curr}" if curr == 'JPY' else f"{result:.2f} {curr}"
        result_label.config(text=f"{amount:.2f} RUB -> {res_text}")
    except:
        messagebox.showerror("Ошибка", "Вводите цифры!")

root = tk.Tk()
root.title("Конвертация RUB в другую валюту")
root.geometry("400x300")

tk.Label(root, text="Рубли:", font=("Monaspace", 10)).pack(pady=10)
entry = tk.Entry(root, width=20, font=("Monaspace", 11))
entry.pack(pady=2)

tk.Label(root, text="Валюта:", font=("Monaspace", 10)).pack(pady=10)
combo = ttk.Combobox(root, values=list(CURRENCY.keys()), state="readonly", width=18)
combo.set("USD")
combo.pack(pady=2)

tk.Button(root, text="Вычислить", command=convert, bg="green", font=("Monaspace", 10)).pack(pady=15)
result_label = tk.Label(root, text="", fg="green", font=("Monaspace", 10),)
result_label.pack(pady=5)

root.mainloop()