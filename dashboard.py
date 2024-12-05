import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from database import engine, User, Vehicle, Rental, RentalSummary
from etl_process import run_etl
import matplotlib.pyplot as plt

# Database session setup
Session = sessionmaker(bind=engine)
session = Session()

st.title("Vehicle Rental System Dashboard")
st.sidebar.header("Insights Menu")

# Function to display ETL status
def display_etl_status():
    try:
        # Fetch the ETL status
        summary_records = session.query(RentalSummary).all()
        total_records = len(summary_records)
        last_updated = (
            max(record.last_updated for record in summary_records)
            if total_records > 0
            else None
        )

        st.subheader("ETL Monitoring Page")
        st.write(f"**Total Records:** {total_records}")
        st.write(f"**Last Updated:** {last_updated if last_updated else 'No updates yet'}")

        # Button to trigger ETL process
        if st.button("Run ETL Process"):
            run_etl()
            st.success("ETL process completed successfully!")
    except Exception as e:
        st.error(f"Error fetching or running ETL: {e}")

# Function to plot top vehicles by rental frequency
def plot_top_vehicles():
    query = session.query(Vehicle.make, Vehicle.model, Rental.vehicle_id).join(Rental, Vehicle.vehicle_id == Rental.vehicle_id).all()
    data = pd.DataFrame(query, columns=['Make', 'Model', 'Vehicle_ID'])
    vehicle_rentals = data.groupby(['Make', 'Model']).size().reset_index(name='Rental_Count')
    top_vehicles = vehicle_rentals.sort_values(by='Rental_Count', ascending=False).head(10)
    
    st.subheader("Top 10 Vehicles by Rental Frequency")
    fig, ax = plt.subplots()
    top_vehicles.plot(kind='bar', x='Model', y='Rental_Count', legend=False, color='skyblue', ax=ax)
    ax.set_title('Top 10 Vehicles by Rental Frequency')
    ax.set_ylabel('Number of Rentals')
    ax.set_xlabel('Vehicle Model')
    st.pyplot(fig)

# Function to plot monthly revenue trends
def plot_revenue_trends():
    query = session.query(Rental.pickup_date, Rental.total_cost).all()
    data = pd.DataFrame(query, columns=['Pickup_Date', 'Revenue'])
    
    if data.empty:
        st.warning("No data available for Monthly Revenue Trends.")
        return
    
    data['Revenue'] = pd.to_numeric(data['Revenue'], errors='coerce')  # Ensure numeric
    data['Month'] = data['Pickup_Date'].apply(lambda x: x.strftime('%Y-%m'))
    monthly_revenue = data.groupby('Month')['Revenue'].sum().reset_index()
    
    st.subheader("Monthly Revenue Trends")
    fig, ax = plt.subplots()
    monthly_revenue.plot(kind='line', x='Month', y='Revenue', legend=False, color='orange', ax=ax)
    ax.set_title('Monthly Revenue Trends')
    ax.set_ylabel('Revenue ($)')
    ax.set_xlabel('Month')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Function to plot vehicle category usage
def plot_vehicle_category_usage():
    query = session.query(Vehicle.type, Rental.vehicle_id).join(Rental, Vehicle.vehicle_id == Rental.vehicle_id).all()
    data = pd.DataFrame(query, columns=['Vehicle_Type', 'Vehicle_ID'])
    vehicle_usage = data['Vehicle_Type'].value_counts().reset_index(name='Count').rename(columns={'index': 'Vehicle_Type'})
    
    if vehicle_usage.empty:
        st.warning("No data available for Vehicle Category Usage.")
        return
    
    st.subheader("Vehicle Category Usage")
    fig, ax = plt.subplots()
    vehicle_usage.plot(kind='pie', y='Count', labels=vehicle_usage['Vehicle_Type'], autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title('Vehicle Category Usage')
    st.pyplot(fig)

# Function to plot user age distribution
def plot_user_age_distribution():
    query = session.query(User.age).all()
    data = pd.DataFrame(query, columns=['Age'])
    data['Age_Group'] = pd.cut(data['Age'], bins=[0, 20, 30, 40, 50, 60, 70, 80], labels=['10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80'])
    age_groups = data['Age_Group'].value_counts().reset_index(name='Count')
    
    st.subheader("User Age Distribution")
    fig, ax = plt.subplots()
    age_groups.plot(kind='bar', x='Age_Group', y='Count', legend=False, color='purple', ax=ax)
    ax.set_title('User Age Distribution')
    ax.set_ylabel('Number of Users')
    ax.set_xlabel('Age Group')
    st.pyplot(fig)

# Function to plot city-wise rental frequency
def plot_city_rental_frequency():
    query = session.query(User.city, Rental.user_id).join(User, Rental.user_id == User.user_id).all()
    data = pd.DataFrame(query, columns=['City', 'User_ID'])
    city_rentals = data['City'].value_counts().reset_index(name='Rental_Count')
    city_rentals.rename(columns={'index': 'City'}, inplace=True)  # Ensure the column is renamed correctly

    if city_rentals.empty:
        st.warning("No data available for City-Wise Rental Frequency.")
        return

    st.subheader("Top 10 Cities by Rental Frequency")
    city_rentals = city_rentals.head(10)  # Only top 10
    fig, ax = plt.subplots()
    city_rentals.plot(kind='bar', x='City', y='Rental_Count', legend=False, color='green', ax=ax)
    ax.set_title('Top 10 Cities by Rental Frequency')
    ax.set_ylabel('Number of Rentals')
    ax.set_xlabel('City')
    st.pyplot(fig)

# Sidebar menu
option = st.sidebar.selectbox(
    "Choose Insight",
    ("ETL Status", "Top Vehicles by Rental Frequency", "Monthly Revenue Trends", "Vehicle Category Usage", "User Age Distribution", "City-Wise Rental Frequency",
     )
)

# Display selected visualization
if option == "ETL Status":
    display_etl_status()
if option == "Top Vehicles by Rental Frequency":
    plot_top_vehicles()
elif option == "Monthly Revenue Trends":
    plot_revenue_trends()
elif option == "Vehicle Category Usage":
    plot_vehicle_category_usage()
elif option == "User Age Distribution":
    plot_user_age_distribution()
elif option == "City-Wise Rental Frequency":
    plot_city_rental_frequency()


