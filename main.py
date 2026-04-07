import pandas as pd
from score_engine import compute_credit_score

def main():

    print("=== BANK CREDIT RISK ENGINE ===\n")

    df = pd.read_csv("data/retail.csv")

    print("Input Data:\n")
    print(df)

    df = compute_credit_score(df)

    print("\n--- CREDIT SCORES ---\n")

    for index, row in df.iterrows():
        print(f"Customer {row['CustomerID']} -> Score: {row['CreditScore']}")

    print("\n=== PROCESS COMPLETE ===")

if __name__ == "__main__":
    main()