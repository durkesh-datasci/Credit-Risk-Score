import pandas as pd

def compute_credit_score(df):

    scores = []

    for index, row in df.iterrows():

        income = row['Income']
        emi = row['EMI']
        util = row['Utilization']
        late = row['LatePayments']

        emi_ratio = emi / income

        score = 900

        # Payment behavior
        score -= late * 50

        # Utilization penalty
        if util > 0.7:
            score -= 100
        elif util > 0.5:
            score -= 60
        elif util > 0.3:
            score -= 30

        # EMI burden
        if emi_ratio > 0.5:
            score -= 100
        elif emi_ratio > 0.4:
            score -= 60
        elif emi_ratio > 0.3:
            score -= 30

        # Income bonus
        if income > 70000:
            score += 20

        score = max(300, min(900, score))

        scores.append(score)

    df['CreditScore'] = scores

    return df