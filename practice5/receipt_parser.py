import re
with open("raw.txt", "r") as file:
    text = file.read()

#task 1 / price
price_pat = r"\d{1,3}(?:\s\d{3})*,\d{2}"
price = re.findall(price_pat, text)

prices = []
for i in price:
    cp = i.replace(" ", "").replace(",", ".")
    prices.append(float(cp))

#task 2 / product
product_pat = r"\d+\.\s*\n(.+?)\n\d{1,3}(?:\s\d{3})*,\d{2}"
product = re.findall(product_pat, text)

products = [p.strip().replace("\n", " ") for p in product]

#task 3 / total
total = re.search(r"ИТОГО:\s*\n?(\d{1,3}(?:\s\d{3})*,\d{2})", text)
if total:
    total = float(total.group(1).replace(" ", "").replace(",", "."))
else:
    total = sum(prices)

#task 4 / date and time
time_and_date = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})", text)

date = time_and_date.group(1) if time_and_date else None
time = time_and_date.group(2) if time_and_date else None

#task 5 / payment type
payment_type = re.search(r"(Банковская карта|Наличные|Карта)", text)
payment = payment_type.group(1) if payment_type else None

#task 6 / result
result = {
    "prices": prices,
    "products": products,
    "total_amount": total,
    "date": date,
    "time": time,
    "payment_method": payment
}
print("                                 ")
print("                                 ")
print("------ RECEIPT PARSED DATA ------")
print("                                 ")
print(f"DATE: {date}")
print(f"TIME: {time}")
print(f"PAYMENT METHOD: {payment}")
print(f"TOTAL AMOUNT: {total}")
print("                                 ")
print("---------------------------------")
print("\nPRODUCTS:")
print("                                 ")
for product, price in zip(products, prices):
    print(f"{product} : {price} KZT")
print("                                 ")
print("---------------------------------")
print("                                 ")
print("                                 ")