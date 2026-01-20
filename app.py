import streamlit as st
import datetime
from datetime import date
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Numerology Calculator", layout="wide")
st.title("🔮 Vedic Numerology Calculator")

# --- Logic Preservation ---
# We keep the core mathematical logic exactly as provided in the original script.
# Minor adjustments were made only to return data for display instead of printing to console.


def dnumber(n):
    sum_val = 0
    while n > 0 or sum_val > 9:
        if n == 0:
            n = sum_val
            sum_val = 0
        sum_val += n % 10
        n //= 10
    return sum_val

# Duplicate functions preserved to maintain original logic flow


def bumber(bno):
    return dnumber(bno)


def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - \
        ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age


def get_matrix(bno, bm_str, by_str, destiny_num):
    # Logic to build the Lo Shu Grid matrix
    birth_num_val = dnumber(bno)

    # Constructing the string of all numbers
    a = str(bno) + str(bm_str) + str(by_str) + \
        str(destiny_num) + str(birth_num_val)

    one = a.count("1")
    two = a.count("2")
    three = a.count("3")
    four = a.count("4")
    five = a.count("5")
    six = a.count("6")
    seven = a.count("7")
    eight = a.count("8")
    nine = a.count("9")

    # Creating the grid exactly as logic dictated
    # Using ' ' instead of empty strings for better visual table alignment if count is 0
    r1 = ["3" * three if three else "-", "1" *
          one if one else "-", "9" * nine if nine else "-"]
    r2 = ["6" * six if six else "-", "7" *
          seven if seven else "-", "5" * five if five else "-"]
    r3 = ["2" * two if two else "-", "8" *
          eight if eight else "-", "4" * four if four else "-"]

    return [r1, r2, r3]


# --- Sidebar Input ---
st.sidebar.header("User Details")
dob_input = st.sidebar.date_input(
    "Enter Birth Date",
    value=date(2000, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date(2100, 12, 31)
)

# --- Processing Inputs (Global variables simulation) ---
bno = dob_input.day
bmonth = dob_input.month
byear = dob_input.year

# Recreating original derived variables
x = dob_input
n_val = bno + bmonth + byear
bd_str = x.strftime("%d")
bm_str = x.strftime("%m")
by_str = x.strftime("%y")

# Destiny Number Calculation
destiny_val = dnumber(n_val)
birth_val = dnumber(bno)

# --- Application Layout (Replacing the Menu) ---

# We use Tabs to replace the "Menu" logic
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔢 Matrix (Lo Shu)",
    "📅 Dasha/Antardasha",
    "⏳ Pariyantardasha",
    "📆 Daily Dasha"
])

# --- TAB 1: Overview (Birth & Destiny) ---
with tab1:
    st.subheader("Basic Numerology Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Birth Number", birth_val)
    with col2:
        st.metric("Destiny Number", destiny_val)
    with col3:
        st.metric("Current Age", f"{calculateAge(dob_input)} years")

# --- TAB 2: Matrix ---
with tab2:
    st.subheader("Numerology Grid")
    grid_data = get_matrix(bno, bm_str, by_str, destiny_val)

    # transforming to dataframe for clean display
    df_grid = pd.DataFrame(grid_data)

    # Custom CSS to make it look like a grid
    st.markdown("""
    <style>
    div[data-testid="stDataFrame"] table {
        width: 100%;
        text-align: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.table(df_grid)

# --- TAB 3: Dasha and Antardasha ---
with tab3:
    st.subheader("Dasha & Antardasha (Up to 2040)")

    # Logic extracted from 'dasha(n)' function
    data_list = []
    i = byear
    b = birth_val  # Using variable 'b' logic from script

    # Caching the dashas logic for later use in Pariyantar
    dashas_map = {}
    antardasha_map = {}

    while i < 2040:
        if b > 9:
            b = 1

        # Inner loop logic preserved
        j = 0
        while j < b and i < 2040:
            # Recreating the datetime object as per logic
            y = datetime.datetime(i, bmonth, bno)
            ye = int(y.strftime("%y"))
            y_1 = int(y.strftime("%w"))

            dlord = 0
            # Logic mapping days to lord
            if (y_1 == 0):
                dlord = 1
            if (y_1 == 1):
                dlord = 2
            if (y_1 == 2):
                dlord = 9
            if (y_1 == 3):
                dlord = 5
            if (y_1 == 4):
                dlord = 3
            if (y_1 == 5):
                dlord = 6
            if (y_1 == 6):
                dlord = 8

            ada = bno + bmonth + ye + dlord
            ans = dnumber(ada)

            data_list.append({
                "Year": i,
                "Dasha (Maha)": b,
                "Antardasha": ans
            })

            # Save for Pariyantar usage
            dashas_map[i] = b
            antardasha_map[i] = ans

            i += 1
            j += 1
        b += 1

    st.dataframe(pd.DataFrame(data_list), use_container_width=True)

# --- TAB 4: Pariyantardasha ---
with tab4:
    st.subheader("Pariyantardasha Calculator")

    # Replacing 'input("Enter start year")'
    ye2 = st.number_input("Enter Start Year", min_value=byear,
                          max_value=2040, value=date.today().year)

    if st.button("Calculate Pariyantar"):
        ye1 = ye2 + 1

        # Check if year exists in our pre-calculated maps
        das = dashas_map.get(ye2, 0)
        wass = antardasha_map.get(ye2, 0)

        if das == 0:
            st.warning("Year out of range for current logic.")
        else:
            pariyantar_data = []

            # Date Logic
            date1 = datetime.date(ye2, bmonth, bno)
            date2 = datetime.date(ye1, bmonth, bno)

            # Lord Logic (Preserved)
            y_1 = int(date1.strftime("%w"))
            dlord = 0
            if (y_1 == 0):
                dlord = 1
            if (y_1 == 1):
                dlord = 2
            if (y_1 == 2):
                dlord = 9
            if (y_1 == 3):
                dlord = 5
            if (y_1 == 4):
                dlord = 3
            if (y_1 == 5):
                dlord = 6
            if (y_1 == 6):
                dlord = 8

            bd_val = int(date1.strftime("%d"))
            bm_val = int(date1.strftime("%m"))
            ye_val = int(date1.strftime("%y"))

            adaa = bd_val + bm_val + ye_val + dlord
            ada = dnumber(adaa)

            st.write(f"**Dasha:** {das} | **Antardasha:** {wass}")

            # Loop Logic
            while date1 < date2:
                if ada > 9:
                    ada = 1

                d1 = 0
                if (ada == 1):
                    d1 = 8
                if (ada == 2):
                    d1 = 16
                if (ada == 3):
                    d1 = 24
                if (ada == 4):
                    d1 = 32
                if (ada == 5):
                    d1 = 41
                if (ada == 6):
                    d1 = 49
                if (ada == 7):
                    d1 = 57
                if (ada == 8):
                    d1 = 65
                if (ada == 9):
                    d1 = 73

                date3 = date1 + datetime.timedelta(days=d1)

                pariyantar_data.append({
                    "Start Date": date1,
                    "End Date": date3,
                    "Pariyantar Value": ada
                })

                date1 = date3
                ada += 1

            st.table(pd.DataFrame(pariyantar_data))

# --- TAB 5: Daily Dasha ---
with tab5:
    st.subheader("Daily Dasha")

    # Replacing 'input("Enter start Month")'
    bmo_input = st.number_input(
        "Enter Start Month (1-12)", min_value=1, max_value=12, value=date.today().month)

    if st.button("Calculate Daily"):
        daily_list = []
        bye_daily = int(date.today().year)

        try:
            date1 = datetime.date(bye_daily, bmo_input, 1)
        except ValueError:
            # Handle leap year or invalid date issues simply
            date1 = datetime.date(bye_daily, bmo_input, 1)

        date2 = date1 + datetime.timedelta(days=31)

        # Helper function needed inside this scope (yantar logic)
        def get_yantar_val(target_date, bye_param):
            y_date = datetime.date(bye_param, bmonth, bno)
            p_date = datetime.date(bye_param - 1, bmonth, bno)

            if target_date <= y_date:
                calc_date = p_date
            else:
                calc_date = y_date

            y_w = int(calc_date.strftime("%w"))
            dlord_y = 0
            if (y_w == 0):
                dlord_y = 1
            if (y_w == 1):
                dlord_y = 2
            if (y_w == 2):
                dlord_y = 9
            if (y_w == 3):
                dlord_y = 5
            if (y_w == 4):
                dlord_y = 3
            if (y_w == 5):
                dlord_y = 6
            if (y_w == 6):
                dlord_y = 8

            bd_d = int(calc_date.strftime("%d"))
            bm_d = int(calc_date.strftime("%m"))
            ye_d = int(calc_date.strftime("%y"))

            adaa_d = bd_d + bm_d + ye_d + dlord_y
            ada_d = dnumber(adaa_d)

            temp_date = calc_date

            while temp_date <= target_date:
                if ada_d > 9:
                    ada_d = 1

                d1_d = 0
                if (ada_d == 1):
                    d1_d = 8
                if (ada_d == 2):
                    d1_d = 16
                if (ada_d == 3):
                    d1_d = 24
                if (ada_d == 4):
                    d1_d = 32
                if (ada_d == 5):
                    d1_d = 41
                if (ada_d == 6):
                    d1_d = 49
                if (ada_d == 7):
                    d1_d = 57
                if (ada_d == 8):
                    d1_d = 65
                if (ada_d == 9):
                    d1_d = 73

                temp_date = temp_date + datetime.timedelta(days=d1_d)

                if temp_date > target_date:
                    break
                ada_d += 1
            return ada_d

        # Main Daily Loop
        while date1 < date2:
            # Stop if we jumped to next month
            if date1.month != bmo_input:
                break

            y_ = int(date1.strftime("%w"))
            dlord = 0
            if (y_ == 0):
                dlord = 1
            if (y_ == 1):
                dlord = 2
            if (y_ == 2):
                dlord = 9
            if (y_ == 3):
                dlord = 5
            if (y_ == 4):
                dlord = 3
            if (y_ == 5):
                dlord = 6
            if (y_ == 6):
                dlord = 8

            pd_val = get_yantar_val(date1, bye_daily)
            dd = dlord + pd_val
            ddd = int(dnumber(dd))

            daily_list.append({
                "Date": date1,
                "Day": date1.strftime("%A"),
                "Daily Value": ddd
            })

            date1 = date1 + datetime.timedelta(days=1)

        st.dataframe(pd.DataFrame(daily_list), use_container_width=True)
