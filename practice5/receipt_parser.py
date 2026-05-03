import re

# Открываем файл из правильного пути
with open("/Users/bekzatmarat/Desktop/Study/PP2/practices/practice5/raw.txt", "r") as file:
    text = file.read()

# task 1 / price
price_pat = r"\d{1,3}(?:\s\d{3})*,\d{2}"
price_matches = re.findall(price_pat, text)

prices = [float(p.replace(" ", "").replace(",", ".")) for p in price_matches]

# task 2 / product
product_pat = r"\d+\.\s*\n(.+?)\n\d{1,3}(?:\s\d{3})*,\d{2}"
product_matches = re.findall(product_pat, text)

products = [p.strip().replace("\n", " ") for p in product_matches]

# task 3 / total
total_match = re.search(r"ИТОГО:\s*\n?(\d{1,3}(?:\s\d{3})*,\d{2})", text)
if total_match:
    total = float(total_match.group(1).replace(" ", "").replace(",", "."))
else:
    total = sum(prices)

# task 4 / date and time
time_and_date = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})", text)
date = time_and_date.group(1) if time_and_date else None
time = time_and_date.group(2) if time_and_date else None

# task 5 / payment type
payment_match = re.search(r"(Банковская карта|Наличные|Карта)", text)
payment = payment_match.group(1) if payment_match else None

# task 6 / result
result = {
    "prices": prices,
    "products": products,
    "total_amount": total,
    "date": date,
    "time": time,
    "payment_method": payment
}

# Вывод данных
print("\n------ RECEIPT PARSED DATA ------\n")
print(f"DATE: {date}")
print(f"TIME: {time}")
print(f"PAYMENT METHOD: {payment}")
print(f"TOTAL AMOUNT: {total}")
print("\n---------------------------------")
print("\nPRODUCTS:\n")
for product, price in zip(products, prices):
    print(f"{product} : {price} KZT")
print("\n---------------------------------\n")