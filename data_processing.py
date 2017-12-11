import os
import sys
import pandas as pd

# retrieve and format the training data for use by the SVM
def build_training_set():
    path = os.path.join(sys.path[0], "training_data.csv")
    training_data_df = pd.read_csv(path);

    X = training_data_df[['Return on Equity',
                          'Return on Equity Change',
                          'Working Capital Ratio',
                          'Working Capital Change',
                          'Debt to Equity',
                          'Debt to Equity Change',
                          'Comprehensive Free Cash Flow',
                          'Free Cash Flow Change',
                          'Earnings Growth']].values.tolist()

    y = [classify_stock(value) for value in training_data_df['Performance'].values.tolist()]

    return X, y


# classify a stock based on its performance relative to the S&P 500
def classify_stock(performance):
    # if the stock beats the S&P 500 by 5% or more, it is a strong performer ("Buy")
    if performance >= .05:
        return 1
    # above -5%, the stock is a "Hold"; not bad enough to sell, but there are better options to buy
    elif performance > -.05:
        return 0
    # below -5%, the stock will underperform enough to warrant a "Sell"
    else:
        return -1