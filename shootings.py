import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data_path = "https://github.com/Adzic/NYPD-Shootings-Data-Explorer/blob/main/NYPD_Shooting_Incident_Data__Year_To_Date__20231125.csv"
df = pd.read_csv(data_path)

# Function to preprocess data
def preprocess_data(df):
    # Convert OCCUR_DATE to datetime format
    if 'OCCUR_DATE' in df.columns:
        df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
    
    return df

# Preprocess the data
df = preprocess_data(df)

# Streamlit app
def main():
    st.title("NYPD Shootings Data Explorer")
    st.markdown("This is a Streamlit app used to analyze the NYPD shootings data.")

    # Sidebar for user inputs
    st.sidebar.header("Filter Data")

    # Date range filter
    date_range = st.sidebar.date_input("Select Date Range", [df['OCCUR_DATE'].min(), df['OCCUR_DATE'].max()])

    # Convert date_range to datetime64[ns]
    date_range = pd.to_datetime(date_range)


    # Location filter
    selected_borough = st.sidebar.selectbox("Select Borough", ["All"] + df['BORO'].unique().tolist(), index=0)
    if selected_borough != "All":
        df_filtered = df[df['BORO'] == selected_borough]
    else:
        df_filtered = df

    # Display filtered data
    st.subheader("Filtered Data")
    # Convert date_range[0] and date_range[1] to datetime64[ns]
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    st.write(df_filtered[(df_filtered['OCCUR_DATE'] >= start_date) & (df_filtered['OCCUR_DATE'] <= end_date)])

    # Statistics
    st.subheader("Statistics")
    st.write(f"Total Incidents: {len(df_filtered)}")

    # Plot incidents over time
    st.subheader("Incidents Over Time")
    incidents_over_time = df_filtered.groupby(df_filtered['OCCUR_DATE'].dt.to_period("M")).size()
    st.line_chart(incidents_over_time)

    # Plot incidents by borough
    st.subheader("Incidents by Borough")

    # Create a DataFrame for incidents by borough and race
    incidents_by_borough_race = df_filtered.groupby(['BORO', 'PERP_RACE']).size().reset_index(name='Count')

    # Create a pivot table for better display
    pivot_table = incidents_by_borough_race.pivot_table(index='BORO', columns='PERP_RACE', values='Count', fill_value=0)

    # Display the table
    st.table(pivot_table)

    # Table showing count of PERP_RACE
    st.subheader("Count by Race")
    perp_race_count = df_filtered['PERP_RACE'].value_counts().reset_index()
    perp_race_count.columns = ['PERP_RACE', 'Count']
    st.table(perp_race_count)

 

if __name__ == "__main__":
    main()
