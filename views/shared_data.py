
# Dictionary to store data from each page
page_data = {
    "Cashflow": {
        "Total Inflows": 0, 
        "Total Outflows": 0,
        "Net Gain/Loss": 0},
    "Portfolio": {"value": 0, "returns": 0},
    "Networth": {"assets": 0, "liabilities": 0},
}

def get_page_data():
    return page_data

def update_cashflow_data(inflows, outflows, net_gain_loss):
    page_data["Cashflow"]["Total Inflows"] = inflows
    page_data["Cashflow"]["Total Outflows"] = outflows
    page_data["Cashflow"]["Net Gain/Loss"] = net_gain_loss
