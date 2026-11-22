
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ==========================================
# 1. PATIENT INFORMATION
# ==========================================

patient_name = "Patient X"


# ==========================================
# 2. DATA INPUT
# ==========================================

data = {
    "Test": [
        "Hemoglobin",
        "Platelets",
        "WBC",
        "Creatinine",
        "Urine ACR",
        "Fasting Glucose",
        "PP Glucose",
        "Uric Acid"
    ],

    "Patient_Value": [
        12.0,
        200000,
        6000,
        1.0,
        20,
        95,
        130,
        5.0
    ],

    "Normal_Low": [
        13,
        140000,
        4000,
        0.6,
        0,
        60,
        0,
        3.0
    ],

    "Normal_High": [
        18,
        440000,
        11000,
        1.3,
        30,
        110,
        145,
        7.0
    ],

    "Unit": [
        "g/dL",
        "/Cumm",
        "/Cumm",
        "mg/dL",
        "mg/g",
        "mg/dL",
        "mg/dL",
        "mg/dL"
    ]
}


# ==========================================
# 3. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(data)

print("\nPATIENT LABORATORY DATA")
print("=" * 80)

print(df)


# ==========================================
# 4. STATUS CALCULATION
# ==========================================

def calculate_status(row):

    value = row["Patient_Value"]
    low = row["Normal_Low"]
    high = row["Normal_High"]

    if value < low:

        difference = low - value
        percentage = (difference / low) * 100

        return pd.Series([
            "LOW",
            difference,
            percentage,
            "Below normal"
        ])

    elif value > high:

        difference = value - high
        percentage = (difference / high) * 100

        return pd.Series([
            "HIGH",
            difference,
            percentage,
            "Above normal"
        ])

    else:

        return pd.Series([
            "NORMAL",
            0,
            0,
            "Within normal range"
        ])


# ==========================================
# 5. APPLY FUNCTION TO EVERY ROW
# ==========================================

df[
    ["Status", "Difference", "Difference_%", "Meaning"]
] = df.apply(calculate_status, axis=1)


# ==========================================
# 6. DISPLAY DATA ANALYSIS
# ==========================================

print("\nDATA ANALYSIS")
print("=" * 100)

print(
    df[
        [
            "Test",
            "Patient_Value",
            "Normal_Low",
            "Normal_High",
            "Unit",
            "Status",
            "Difference",
            "Difference_%"
        ]
    ]
)


# ==========================================
# 7. GRAPH FUNCTION
# ==========================================

def plot_test(row):

    test = row["Test"]
    value = row["Patient_Value"]
    low = row["Normal_Low"]
    high = row["Normal_High"]
    unit = row["Unit"]
    status = row["Status"]
    difference = row["Difference"]
    percentage = row["Difference_%"]

    normal_range = high - low

    if normal_range == 0:
        normal_range = max(abs(high), 1)

    padding = normal_range * 0.30

    graph_low = min(low - padding, value - padding)
    graph_high = max(high + padding, value + padding)

    fig, ax = plt.subplots(figsize=(10, 5))


    # ======================================
    # 8. NORMAL RANGE SHADING
    # ======================================

    ax.axhspan(
        graph_low,
        low,
        color="red",
        alpha=0.20,
        label="Below normal"
    )

    ax.axhspan(
        low,
        high,
        color="green",
        alpha=0.20,
        label="Normal range"
    )

    ax.axhspan(
        high,
        graph_high,
        color="red",
        alpha=0.20,
        label="Above normal"
    )


    # ======================================
    # 9. NORMAL RANGE LINES
    # ======================================

    ax.axhline(
        low,
        color="green",
        linestyle="--",
        linewidth=2
    )

    ax.axhline(
        high,
        color="green",
        linestyle="--",
        linewidth=2
    )


    # ======================================
    # 10. PATIENT SCATTER POINT
    # ======================================

    if status == "NORMAL":
        patient_color = "green"
    else:
        patient_color = "red"

    ax.scatter(
        0,
        value,
        color=patient_color,
        s=250,
        zorder=5,
        edgecolor="black",
        linewidth=1.5,
        label=f"{patient_name}: {value} {unit}"
    )


    # ======================================
    # 11. ANNOTATION
    # ======================================

    ax.annotate(
        f"{patient_name}\n{value} {unit}",
        xy=(0, value),
        xytext=(0.15, value),
        fontsize=12,
        fontweight="bold",
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.5
        )
    )


    # ======================================
    # 12. NORMAL RANGE LABEL
    # ======================================

    ax.text(
        0.50,
        (low + high) / 2,
        f"NORMAL\n{low} - {high} {unit}",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="darkgreen"
    )


    # ======================================
    # 13. STATUS MESSAGE
    # ======================================

    if status == "LOW":

        message = (
            f"LOW\n"
            f"{difference:.2f} {unit} below lower limit\n"
            f"{percentage:.1f}% below normal"
        )

        message_color = "red"

    elif status == "HIGH":

        message = (
            f"HIGH\n"
            f"{difference:.2f} {unit} above upper limit\n"
            f"{percentage:.1f}% above normal"
        )

        message_color = "red"

    else:

        message = (
            "NORMAL\n"
            "Within reference range"
        )

        message_color = "green"


    ax.text(
        0.98,
        0.05,
        message,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color=message_color,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            edgecolor=message_color,
            linewidth=2
        )
    )


    # ======================================
    # 14. GRAPH SETTINGS
    # ======================================

    ax.set_title(
        f"{patient_name}'s {test} - Patient vs Normal",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_ylabel(unit, fontsize=12)

    ax.set_xticks([0])

    ax.set_xticklabels(
        [patient_name],
        fontsize=12
    )

    ax.set_ylim(
        graph_low,
        graph_high
    )

    ax.grid(
        axis="y",
        linestyle=":",
        alpha=0.5
    )

    ax.legend(loc="upper left")

    plt.tight_layout()

    plt.show()


# ==========================================
# 15. CREATE GRAPHS FOR ALL TESTS
# ==========================================

for index, row in df.iterrows():

    plot_test(row)


# ==========================================
# 16. FINAL COMPARISON
# ==========================================

print("\nFINAL COMPARISON")
print("=" * 100)

for index, row in df.iterrows():

    print(
        f"{row['Test']:20} | "
        f"Patient X = {row['Patient_Value']} "
        f"{row['Unit']:7} | "
        f"Normal = {row['Normal_Low']} - "
        f"{row['Normal_High']} | "
        f"{row['Status']:6} | "
        f"Difference = {row['Difference']:.2f} "
        f"({row['Difference_%']:.1f}%)"
    )
