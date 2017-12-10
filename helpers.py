import requests
import re
from bs4 import BeautifulSoup

def get_financials(symbol):
    print('Gathering data for: {}'.format(symbol))

    balance_sheet = BeautifulSoup(requests.get('https://finance.yahoo.com/quote/{}/balance-sheet'.format(symbol)).content, 'html.parser')
    balance_nodes = [node.get_text() for node in balance_sheet.find(id='Col1-3-Financials-Proxy').tbody.find_all('td')]
    cash_flow = BeautifulSoup(requests.get('https://finance.yahoo.com/quote/{}/cash-flow'.format(symbol)).content, 'html.parser')
    cash_nodes = [node.get_text() for node in cash_flow.find(id='Col1-3-Financials-Proxy').tbody.find_all('td')]

    # convert '-' characters into zeroes, strip commas from numbers and cast everything but dates to integers
    date_pattern = re.compile('\d*/\d*/\d*')
    for i in range(len(balance_nodes)):
        if balance_nodes[i] == '-':
            balance_nodes[i] = 0
        elif not balance_nodes[i][0].isalpha() and not date_pattern.match(balance_nodes[i]):
            balance_nodes[i] = int(balance_nodes[i].replace(',', ''))

    for i in range(len(cash_nodes)):
        if cash_nodes[i] == '-':
            cash_nodes[i] = 0
        elif not cash_nodes[i][0].isalpha() and not date_pattern.match(cash_nodes[i]):
            cash_nodes[i] = int(cash_nodes[i].replace(',', ''))

    # retrieve necessary data from the scraped webpages
    index = balance_nodes.index('Total Current Assets') + 1
    current_assets = balance_nodes[index:index + 3]
    index = balance_nodes.index('Total Current Liabilities') + 1
    current_liabilities = balance_nodes[index:index + 3]
    index = balance_nodes.index('Total Stockholder Equity') + 1
    total_equity = balance_nodes[index:index + 3]
    index = balance_nodes.index('Total Liabilities') + 1
    total_liabilities = balance_nodes[index:index + 3]

    index = cash_nodes.index('Net Income') + 1
    net_income = cash_nodes[index:index + 3]
    index = cash_nodes.index('Total Cash Flow From Operating Activities') + 1
    cash_flow_operations = cash_nodes[index:index + 3]
    index = cash_nodes.index('Capital Expenditures') + 1
    capital_expenditures = cash_nodes[index:index + 3]
    index = cash_nodes.index('Dividends Paid') + 1
    dividends_paid = cash_nodes[index:index + 3]

    ''' Calculated Values '''

    # various fundamental parameters
    working_capital_ratio = current_assets[0] / current_liabilities[0]
    working_capital_change = ((current_assets[0] - current_liabilities[0]) - (current_assets[1] - current_liabilities[1])) / (current_assets[1] - current_liabilities[1])
    return_on_equity = net_income[0] / total_equity[0]
    return_on_equity_change = ((net_income[0] / total_equity[0]) - (net_income[1] / total_equity[1])) / (net_income[1] / total_equity[1])
    debt_to_equity = total_liabilities[0] / total_equity[0]
    debt_to_equity_change = ((total_liabilities[0] / total_equity[0]) - (total_liabilities[1] / total_equity[1])) / (total_liabilities[1] / total_equity[1])
    comprehensive_free_cash_flow = (cash_flow_operations[0] + capital_expenditures[0] - dividends_paid[0]) / cash_flow_operations[0]
    free_cash_flow_change = ((cash_flow_operations[0] + capital_expenditures[0] - dividends_paid[0]) - (cash_flow_operations[1] + capital_expenditures[1] - dividends_paid[1])) / (cash_flow_operations[1] + capital_expenditures[1] - dividends_paid[1])
    earnings_growth = (net_income[0] - net_income[1]) / net_income[1]

    #append this stock's data to the dataframe
    financial_data = {
        'Return on Equity': return_on_equity,
        'Return on Equity Change': return_on_equity_change,
        'Working Capital Ratio': working_capital_ratio,
        'Working Capital Change': working_capital_change,
        'Debt to Equity': debt_to_equity,
        'Debt to Equity Change': debt_to_equity_change,
        'Comprehensive Free Cash Flow': comprehensive_free_cash_flow,
        'Free Cash Flow Change': free_cash_flow_change,
        'Earnings Growth': earnings_growth
    }

    return financial_data