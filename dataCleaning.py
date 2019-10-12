import dataHandler

last_date = dataHandler.my_data['InvoiceDate'].sort_values(ascending=False)[0]
print(last_date)