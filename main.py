import pandas as pd
from score_engine import compute_credit_score
from stress_engine import compute_stress


def main():

    print("\n=== BANK CREDIT RISK ENGINE ===\n")

    # -----------------------------------------
    # STEP 1: Load dataset
    # -----------------------------------------

    df = pd.read_csv("data/retail.csv")

    print("INPUT DATA:\n")
    print(df)

    # -----------------------------------------
    # STEP 2: Compute stress index
    # -----------------------------------------

    df = compute_stress(df)

    # -----------------------------------------
    # STEP 3: Compute base credit score
    # -----------------------------------------

    df = compute_credit_score(df)

    # -----------------------------------------
    # STEP 4: Stress Adjusted Credit Score
    # -----------------------------------------
    # Higher stress => lower final score

    df['SACS'] = (
        df['CreditScore'] *
        (1 - df['EW_CSI'])
    )

    # -----------------------------------------
    # STEP 5: Display results
    # -----------------------------------------

    print("\n=== RESULTS ===\n")

    for index, row in df.iterrows():

        print(f"Customer ID : {row['CustomerID']}")
        print(f"Month        : {row['Month']}")

        print(f"Base Score   : {row['CreditScore']}")

        print(
            f"Stress Index : {round(row['EW_CSI'], 2)}"
        )

        print(
            f"Adjusted Score : {int(row['SACS'])}"
        )

        print("-" * 40)

    print("\n=== PROCESS COMPLETE ===")


if __name__ == "__main__":
    main()