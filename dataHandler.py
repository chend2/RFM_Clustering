import pandas as pd

my_data = pd.read_excel("./data/OnlineRetail.xlsx")
# remove rows where there is no customer ID and quantity is negative
my_data = my_data[pd.notnull(my_data['CustomerID'])]
my_data = my_data[my_data.Quantity >= 0]

#RFM scoring -> Recency, Frequency, Monetary Value
#group by customer ID
# frequency can be counted

my_data['InvoiceDate'] = pd.to_datetime(my_data['InvoiceDate'])

last_date = my_data['InvoiceDate'].sort_values(ascending=False).reset_index(drop=True)[0]
my_data['recency'] = my_data['InvoiceDate'] - last_date
my_data['TotalPrice'] = my_data['Quantity']*my_data['UnitPrice']

rdm_table = my_data.groupby('CustomerID').agg({
    'recency': lambda x: abs((x.max()).days),
    'InvoiceNo': lambda x: len(x),
    'TotalPrice': lambda x: x.sum()
})

rdm_scores = rdm_table.copy()

def intervalGenerator(x):
    total = (x.max() // 5) + 1
    intervals = [total*i for i in range(1, 5)]
    return intervals

def rdm_scorer(x, y):
    # x is a series such as rdm_table['regency']
    intervals_list = intervalGenerator(y)
    if intervals_list[0] <= x <intervals_list[1]:
        return 1
    if intervals_list[1] <= x < intervals_list[2]:
        return 2
    if intervals_list[2] <= x < intervals_list[3]:
        return 3
    if intervals_list[3] <= x < intervals_list[4]:
        return 4
    if intervals_list[4] <= x:
        return 5

rdm_scores['recency'] = rdm_scores.apply(lambda x: rdm_scorer(x, rdm_table['recency'] ))

# rdm_table['recency'].max() = 374
# round to nearest 5 and find intervals -> 75
# 0-75, 76-150, 151-225, 226-300, 300-375

#rdm_table['InvoiceNo'].max() = 7847
# round up to 7850/5 -> 1570
# 0-1570, 1571

# rdm_scores['recency'] = my_data['recency'].apply(lambda x: rdm_scorer(x))