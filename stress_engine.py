import pandas as pd

def compute_stress(df):

    # -----------------------------------------
    # STEP 1: Proper month ordering
    # -----------------------------------------
    # Alphabetical sorting is wrong for months
    # So we manually define month sequence

    month_order = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    # Create numerical month column
    df['MonthOrder'] = df['Month'].map(month_order)

    # Sort properly by customer and month
    df = df.sort_values(by=['CustomerID', 'MonthOrder'])

    # -----------------------------------------
    # STEP 2: Income change calculation
    # -----------------------------------------
    # pct_change() compares current value
    # with previous month value

    df['delta_income'] = (
        df.groupby('CustomerID')['Income']
        .pct_change()
    )

    # -----------------------------------------
    # STEP 3: Handle NaN values
    # -----------------------------------------
    # First month has no previous month
    # So replace NaN with 0

    df['delta_income'] = df['delta_income'].fillna(0)

    # -----------------------------------------
    # STEP 4: Income stress
    # -----------------------------------------
    # Income drop => higher stress
    # Example:
    # -10% income drop => stress increase

    df['S_income'] = (
        -df['delta_income'] / 0.3
    ).clip(0, 1)

    # -----------------------------------------
    # STEP 5: EMI burden stress
    # -----------------------------------------
    # High EMI compared to income
    # means repayment pressure

    df['emi_ratio'] = df['EMI'] / df['Income']

    df['S_emi'] = (
        df['emi_ratio'] / 0.5
    ).clip(0, 1)

    # -----------------------------------------
    # STEP 6: Credit utilization stress
    # -----------------------------------------
    # More credit usage => more stress

    df['S_util'] = df['Utilization'].clip(0, 1)

    # -----------------------------------------
    # STEP 7: Late payment stress
    # -----------------------------------------
    # More late payments => risky customer

    df['S_late'] = (
        df['LatePayments'] / 3
    ).clip(0, 1)

    # -----------------------------------------
    # STEP 8: Final EW-CSI
    # -----------------------------------------
    # Weighted average stress index

    df['EW_CSI'] = (
        0.25 * df['S_income'] +
        0.25 * df['S_emi'] +
        0.25 * df['S_util'] +
        0.25 * df['S_late']
    )

    return df