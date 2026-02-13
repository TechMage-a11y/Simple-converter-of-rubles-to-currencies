import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

CURRENCY = {
    "USD": 77.1880, "EUR": 91.7113, "CNY": 11.1582, "GBP": 105.2304,
    "CHF": 100.4790, "JPY": 0.5042, "KZT": 0.1573, "AED": 21.0178
}

def convert():
    try:
        amt = float(entry.get())
        if amt <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть больше 0!")
            return
        curr = combo.get()
        if not curr:
            messagebox.showerror("Ошибка", "Выберите валюту!")
            return
        res = amt / CURRENCY[curr]
        text = f"{int(res)} {curr}" if curr == "JPY" else f"{res:.2f} {curr}"
        result_label.config(text=f"{amt:.2f} RUB → {text}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число!")
    except KeyError:
        messagebox.showerror("Ошибка", "Неизвестная валюта!")

def process_file():
    path = filedialog.askopenfilename(
        title="Выбрать файл",
        filetypes=[("Текстовые файлы", "*.txt"), ("CSV-файлы", "*.csv"), ("Все файлы", "*.*")]
    )
    if not path:
        return

    results = []
    try:
        if path.endswith(".txt"):
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    parts = line.strip().split()
                    if len(parts) != 2:
                        continue

                    try:
                        amt = float(parts[0])
                        curr = parts[1].upper()

                        if curr not in CURRENCY and curr != "RUB":
                            continue

                        if curr != "RUB":
                            amt_rub = amt * CURRENCY[curr]
                        else:
                            amt_rub = amt

                        res_line = f"{amt:.2f} {curr} → "
                        res_line += ", ".join(
                            f"{int(amt_rub / r)} {c}" if c == "JPY" else f"{amt_rub / r:.2f} {c}"
                            for c, r in CURRENCY.items()
                        )
                        results.append(res_line)

                    except ValueError:
                        continue

        elif path.endswith(".csv"):
            with open(path, mode="r", encoding="utf-8", newline="") as f:
                first_line = f.readline().strip()
                has_header = first_line.count(",") >= 1 and any(
                    h.lower() in ["amount", "currency"] for h in first_line.split(",")
                )
                f.seek(0)

                if has_header:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            amt = float(row["amount"])
                            curr = row["currency"].upper()
                            if curr != "RUB" or amt <= 0:
                                continue
                            res_line = f"{amt:.2f} RUB → "
                            res_line += ", ".join(
                                f"{int(amt / r)} {c}" if c == "JPY" else f"{amt / r:.2f} {c}"
                                for c, r in CURRENCY.items()
                            )
                            results.append(res_line)
                        except (ValueError, KeyError):
                            continue
                else:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) < 2:
                            continue
                        try:
                            amt = float(row[0])
                            curr = row[1].upper()
                            if curr != "RUB" or amt <= 0:
                                continue
                            res_line = f"{amt:.2f} RUB → "
                            res_line += ", ".join(
                                f"{int(amt / r)} {c}" if c == "JPY" else f"{amt / r:.2f} {c}"
                                for c, r in CURRENCY.items()
                            )
                            results.append(res_line)
                        except ValueError:
                            continue

        if results:
            display_text = "\n".join(results[:30])
            if len(results) > 30:
                display_text += "\n... и др."
            result_label.config(text=display_text, justify="left")
        else:
            result_label.config(text="Нет данных для отображения.", justify="left")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при обработке файла:\n{e}")

root = tk.Tk()
root.title("Конвертер валют")
root.geometry("600x400")

tk.Label(root, text="Сумма (RUB):").pack(pady=5)
entry = tk.Entry(root, width=20)
entry.pack()

tk.Label(root, text="В валюту:").pack(pady=5)
combo = ttk.Combobox(root, values=list(CURRENCY.keys()), state="readonly", width=18)
combo.set("USD")
combo.pack()

tk.Button(root, text="Конвертировать", command=convert, bg="green").pack(pady=10)
tk.Button(root, text="Из файла", command=process_file, bg="blue", fg="white").pack()

result_label = tk.Label(root, text="", justify="left", anchor="w")
result_label.pack(pady=10, padx=10, fill="both")

root.mainloop()