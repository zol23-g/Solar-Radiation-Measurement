import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Load datasets from multiple countries
countries = ['benin-malanville', 'sierraleone-bumbuna', 'togo-dapaong_qc']

@st.cache_data
def load_data():
    dfs = []
    for country in countries:
        data = pd.read_csv(f'./data/{country}.csv')
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Ensure Timestamp is in datetime format
        data.set_index('Timestamp', inplace=True)  # Set Timestamp as the index
        data['Country'] = country  # Add a column to distinguish the data
        dfs.append(data)
    return pd.concat(dfs)

data = load_data()

# Custom CSS for the sidebar and hamburger menu (same as before)
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f4f4f4;
        padding: 20px;
    }
    .hamburger {
        display: none;
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1000;
    }
    .hamburger:hover {
        background-color: #45a049;
    }
    @media (max-width: 768px) {
        .hamburger {
            display: block;
        }
        .sidebar .sidebar-content {
            display: none;
        }
        .sidebar.active .sidebar-content {
            display: block;
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 250px;
            z-index: 1000;
            background-color: #333;
            color: white;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar toggle button (Hamburger menu)
st.markdown("""
    <button class="hamburger" onclick="toggleSidebar()">☰ Menu</button>
    <script>
    function toggleSidebar() {
        var sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('active');
    }
    </script>
""", unsafe_allow_html=True)

# Sidebar for navigation (dropdown)
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a section:", [
    "Introduction",
    "Visualize Outliers",
    "Monthly & Daily Averages",
    "Correlation Analysis",
    "Wind Analysis",
    "Temperature Analysis",
    "Histograms",
    "Z-Score Analysis",
    "Bubble Charts"
])

# Dashboard title
st.title("MoonLight Energy Solutions - Solar Data Visualization")

if page == "Introduction":
    st.header("Introduction")
    st.write("This dashboard provides insights into solar radiation, temperature, and wind conditions across multiple countries. Use the sidebar to navigate through various analyses and visualizations.")

elif page == "Visualize Outliers":
    st.header('Visualize Outliers')
    
    # Boxplot for ModA
    st.subheader('Boxplot of ModA')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='Country', y='ModA', data=data, ax=ax)
    ax.set_title('Boxplot of ModA by Country')
    st.pyplot(fig)

    # Boxplot for Wind Speed (WS)
    st.subheader('Boxplot of Wind Speed (WS)')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='Country', y='WS', data=data, ax=ax)
    ax.set_title('Boxplot of Wind Speed (WS) by Country')
    st.pyplot(fig)

elif page == "Monthly & Daily Averages":
    st.header('Monthly & Daily Averages of GHI, DNI, DHI, and Tamb')

    # Resampling Data by Country
    monthly_data = data.groupby('Country').resample('M').mean().reset_index()  # Monthly average by country
    daily_data = data.groupby('Country').resample('D').mean().reset_index()    # Daily average by country

    # Plotting Monthly Data for All Countries Together
    st.subheader('Monthly Averages (Combined)')
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(x='Timestamp', y='GHI', hue='Country', data=monthly_data, ax=ax)
    sns.lineplot(x='Timestamp', y='DNI', hue='Country', data=monthly_data, ax=ax, linestyle="--")
    sns.lineplot(x='Timestamp', y='DHI', hue='Country', data=monthly_data, ax=ax, linestyle=":")
    sns.lineplot(x='Timestamp', y='Tamb', hue='Country', data=monthly_data, ax=ax, linestyle="-.")
    ax.set_title('Monthly Averages of GHI, DNI, DHI, and Tamb by Country')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.legend()
    st.pyplot(fig)

    # Plotting Daily Data for All Countries Together
    st.subheader('Daily Averages (Combined)')
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(x='Timestamp', y='GHI', hue='Country', data=daily_data, ax=ax)
    sns.lineplot(x='Timestamp', y='DNI', hue='Country', data=daily_data, ax=ax, linestyle="--")
    sns.lineplot(x='Timestamp', y='DHI', hue='Country', data=daily_data, ax=ax, linestyle=":")
    sns.lineplot(x='Timestamp', y='Tamb', hue='Country', data=daily_data, ax=ax, linestyle="-.")
    ax.set_title('Daily Averages of GHI, DNI, DHI, and Tamb by Country')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.legend()
    st.pyplot(fig)

    # Plotting Monthly Data for Each Country Separately
    st.subheader('Monthly Averages (Separate)')
    for country in countries:
        st.write(f"**{country.capitalize()}**")
        country_monthly_data = monthly_data[monthly_data['Country'] == country]
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(country_monthly_data['Timestamp'], country_monthly_data['GHI'], label='GHI', color='orange')
        ax.plot(country_monthly_data['Timestamp'], country_monthly_data['DNI'], label='DNI', color='red')
        ax.plot(country_monthly_data['Timestamp'], country_monthly_data['DHI'], label='DHI', color='blue')
        ax.plot(country_monthly_data['Timestamp'], country_monthly_data['Tamb'], label='Tamb', color='green')
        ax.set_title(f'Monthly Averages of GHI, DNI, DHI, and Tamb in {country.capitalize()}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Values')
        ax.legend()
        st.pyplot(fig)

    # Plotting Daily Data for Each Country Separately
    st.subheader('Daily Averages (Separate)')
    for country in countries:
        st.write(f"**{country.capitalize()}**")
        country_daily_data = daily_data[daily_data['Country'] == country]
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(country_daily_data['Timestamp'], country_daily_data['GHI'], label='GHI', color='orange')
        ax.plot(country_daily_data['Timestamp'], country_daily_data['DNI'], label='DNI', color='red')
        ax.plot(country_daily_data['Timestamp'], country_daily_data['DHI'], label='DHI', color='blue')
        ax.plot(country_daily_data['Timestamp'], country_daily_data['Tamb'], label='Tamb', color='green')
        ax.set_title(f'Daily Averages of GHI, DNI, DHI, and Tamb in {country.capitalize()}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Values')
        ax.legend()
        st.pyplot(fig)

elif page == "Correlation Analysis":
    st.header('Correlation Analysis')

    # Compute Correlation Matrix for each country
    st.subheader('Correlation Matrix by Country')
    for country in countries:
        st.write(f"**{country.capitalize()}**")
        country_data = data[data['Country'] == country]
        correlation_matrix = country_data[['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD']].corr()
        st.write(correlation_matrix)
        
        # Plotting Correlation Heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
        ax.set_title(f'Correlation Heatmap of Solar Radiation, Temperature, and Wind Conditions in {country.capitalize()}')
        st.pyplot(fig)

elif page == "Wind Analysis":
    st.header('Wind Analysis')
    
    # Convert the wind direction (WD) from degrees to radians since polar plots in Matplotlib require angles in radians.
    data['WD_radians'] = np.deg2rad(data['WD'])

    # Create a Polar Plot for Wind Speed and Direction by Country
    st.subheader('Wind Speed and Direction Distribution by Country')
    for country in countries:
        st.write(f"**{country.capitalize()}**")
        country_data = data[data['Country'] == country]
        plt.figure(figsize=(8, 8))
        plt.subplot(projection='polar')
        plt.scatter(country_data['WD_radians'], country_data['WS'], c=country_data['WS'], cmap='viridis', alpha=0.75)
        plt.colorbar(label='Wind Speed (m/s)')
        plt.title(f'Wind Speed and Direction Distribution in {country.capitalize()}')
        st.pyplot(plt)

elif page == "Temperature Analysis":
    st.header('Temperature Analysis')

    # Scatter Plots for Temperature Analysis by Country
    st.subheader('Relative Humidity vs. Ambient Temperature by Country')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='RH', y='Tamb', hue='Country', data=data, alpha=0.5, ax=ax)
    plt.title('Relative Humidity vs. Ambient Temperature by Country')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Ambient Temperature (°C)')
    st.pyplot(fig)

    # You can add similar comparisons for other temperature-related analyses

elif page == "Histograms":
    st.header('Histograms')

    # Histograms for GHI, DNI, DHI by Country
    st.subheader('Histograms for GHI, DNI, DHI by Country')
    fig, axs = plt.subplots(3, len(countries), figsize=(18, 15), sharey=True)
    for i, country in enumerate(countries):
        country_data = data[data['Country'] == country]
        axs[0, i].hist(country_data['GHI'].dropna(), bins=30, color='orange')
        axs[0, i].set_title(f'Histogram of GHI in {country.capitalize()}')
        axs[0, i].set_xlabel('GHI (W/m²)')
        axs[0, i].set_ylabel('Frequency')

        axs[1, i].hist(country_data['DNI'].dropna(), bins=30, color='red')
        axs[1, i].set_title(f'Histogram of DNI in {country.capitalize()}')
        axs[1, i].set_xlabel('DNI (W/m²)')

        axs[2, i].hist(country_data['DHI'].dropna(), bins=30, color='blue')
        axs[2, i].set_title(f'Histogram of DHI in {country.capitalize()}')
        axs[2, i].set_xlabel('DHI (W/m²)')
    
    plt.suptitle('Histograms of Solar Radiation Variables by Country')
    st.pyplot(fig)

elif page == "Z-Score Analysis":
    st.header('Z-Score Analysis')
    
    # Calculate Z-Scores for each country
    z_score_data = []
    for country in countries:
        country_data = data[data['Country'] == country]
        z_scores = country_data[['GHI', 'DNI', 'DHI']].apply(lambda x: stats.zscore(x.dropna()), axis=0)
        z_scores['Timestamp'] = country_data.index
        z_scores['Country'] = country
        z_score_data.append(z_scores)
    z_score_data = pd.concat(z_score_data)

    # Plot Z-Scores for All Countries Together
    st.subheader('Z-Scores of Solar Radiation Variables (Combined)')
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(x='Timestamp', y='GHI', hue='Country', data=z_score_data, ax=ax)
    sns.lineplot(x='Timestamp', y='DNI', hue='Country', data=z_score_data, ax=ax, linestyle="--")
    sns.lineplot(x='Timestamp', y='DHI', hue='Country', data=z_score_data, ax=ax, linestyle=":")
    ax.set_title('Z-Scores of Solar Radiation Variables by Country')
    ax.set_xlabel('Date')
    ax.set_ylabel('Z-Score')
    ax.legend()
    st.pyplot(fig)

    # Plot Z-Scores for Each Country Separately
    st.subheader('Z-Scores of Solar Radiation Variables (Separate)')
    for country in countries:
        st.write(f"**{country.capitalize()}**")
        country_z_scores = z_score_data[z_score_data['Country'] == country]
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(country_z_scores['Timestamp'], country_z_scores['GHI'], label='GHI Z-Score', color='orange')
        ax.plot(country_z_scores['Timestamp'], country_z_scores['DNI'], label='DNI Z-Score', color='red')
        ax.plot(country_z_scores['Timestamp'], country_z_scores['DHI'], label='DHI Z-Score', color='blue')
        ax.set_title(f'Z-Scores of Solar Radiation Variables in {country.capitalize()}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Z-Score')
        ax.legend()
        st.pyplot(fig)

elif page == "Bubble Charts":
    st.header('Bubble Charts')

    # Bubble Chart for GHI, DNI, and DHI by Country
    st.subheader('Bubble Chart: GHI, DNI, and DHI by Country')
    for country in countries:
        st.write(f"**{country.capitalize()}**")
        country_data = data[data['Country'] == country]
        plt.figure(figsize=(10, 8))
        plt.scatter(country_data['GHI'], country_data['DNI'], s=country_data['DHI'], alpha=0.5, c=country_data['GHI'], cmap='viridis')
        plt.colorbar(label='GHI (W/m²)')
        plt.title(f'Bubble Chart of GHI, DNI, and DHI in {country.capitalize()}')
        plt.xlabel('GHI (W/m²)')
        plt.ylabel('DNI (W/m²)')
        plt.xscale('log')
        plt.yscale('log')
        st.pyplot(plt)

else:
    st.write("Please select a section from the sidebar to view the analysis.")
