import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Load your dataset
@st.cache_data
def load_data():
    data = pd.read_csv('../data/benin-malanville.csv')
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Ensure Timestamp is in datetime format
    data.set_index('Timestamp', inplace=True)  # Set Timestamp as the index
    return data

data = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a section:", [
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
    st.write("This dashboard provides insights into solar radiation, temperature, and wind conditions. Use the sidebar to navigate through various analyses and visualizations.")

elif page == "Visualize Outliers":
    st.header('Visualize Outliers')
    
    # Boxplot for ModA
    st.subheader('Boxplot of ModA')
    fig, ax = plt.subplots()
    sns.boxplot(x=data['ModA'], ax=ax)
    ax.set_title('Boxplot of ModA')
    st.pyplot(fig)

    # Boxplot for Wind Speed (WS)
    st.subheader('Boxplot of Wind Speed (WS)')
    fig, ax = plt.subplots()
    sns.boxplot(x=data['WS'], ax=ax)
    ax.set_title('Boxplot of Wind Speed (WS)')
    st.pyplot(fig)

elif page == "Monthly & Daily Averages":
    st.header('Monthly & Daily Averages of GHI, DNI, DHI, and Tamb')

    # Resampling Data
    monthly_data = data.resample('M').mean()  # Monthly average
    daily_data = data.resample('D').mean()    # Daily average

    # Plotting Monthly Data
    st.subheader('Monthly Averages')
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(monthly_data.index, monthly_data['GHI'], label='GHI', color='orange')
    ax.plot(monthly_data.index, monthly_data['DNI'], label='DNI', color='red')
    ax.plot(monthly_data.index, monthly_data['DHI'], label='DHI', color='blue')
    ax.plot(monthly_data.index, monthly_data['Tamb'], label='Tamb', color='green')
    ax.set_title('Monthly Averages of GHI, DNI, DHI, and Tamb')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.legend()
    st.pyplot(fig)

    # Plotting Daily Data
    st.subheader('Daily Averages')
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(daily_data.index, daily_data['GHI'], label='GHI', color='orange')
    ax.plot(daily_data.index, daily_data['DNI'], label='DNI', color='red')
    ax.plot(daily_data.index, daily_data['DHI'], label='DHI', color='blue')
    ax.plot(daily_data.index, daily_data['Tamb'], label='Tamb', color='green')
    ax.set_title('Daily Averages of GHI, DNI, DHI, and Tamb')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.legend()
    st.pyplot(fig)

    # Area Plot for Monthly Data
    st.subheader('Monthly Area Plot')
    fig, ax = plt.subplots(figsize=(14, 7))
    monthly_data[['GHI', 'DNI', 'DHI', 'Tamb']].plot.area(ax=ax, alpha=0.4)
    ax.set_title('Monthly Area Plot of GHI, DNI, DHI, and Tamb')
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    st.pyplot(fig)

elif page == "Correlation Analysis":
    st.header('Correlation Analysis')

    # Compute Correlation Matrix
    st.subheader('Correlation Matrix')
    correlation_matrix = data[['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD']].corr()
    st.write(correlation_matrix)

    # Plotting Correlation Heatmap
    st.subheader('Correlation Heatmap')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Heatmap of Solar Radiation, Temperature, and Wind Conditions')
    st.pyplot(fig)

    # Pair Plots
    st.subheader('Pair Plot')
    sns.pairplot(data[['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD']])
    plt.suptitle('Pair Plot of Solar Radiation, Temperature, and Wind Conditions', y=1.02)
    st.pyplot(plt)

elif page == "Wind Analysis":
    st.header('Wind Analysis')
    
    # Convert the wind direction (WD) from degrees to radians since polar plots in Matplotlib require angles in radians.
    data['WD_radians'] = np.deg2rad(data['WD'])

    # Create a Polar Plot for Wind Speed and Direction
    st.subheader('Wind Speed and Direction Distribution')
    plt.figure(figsize=(8, 8))
    plt.subplot(projection='polar')
    plt.scatter(data['WD_radians'], data['WS'], c=data['WS'], cmap='viridis', alpha=0.75)
    plt.colorbar(label='Wind Speed (m/s)')
    plt.title('Wind Speed and Direction Distribution')
    st.pyplot(plt)

    # Plot Wind Gusts
    st.subheader('Wind Gust Speed and Direction Distribution')
    plt.figure(figsize=(8, 8))
    plt.subplot(projection='polar')
    plt.scatter(data['WD_radians'], data['WSgust'], c=data['WSgust'], cmap='plasma', alpha=0.75)
    plt.colorbar(label='Wind Gust Speed (m/s)')
    plt.title('Wind Gust Speed and Direction Distribution')
    st.pyplot(plt)

    # Analyze Wind Direction Variability
    st.subheader('Wind Direction Variability Distribution')
    plt.figure(figsize=(8, 8))
    plt.subplot(projection='polar')
    plt.scatter(data['WD_radians'], data['WDstdev'], c=data['WDstdev'], cmap='coolwarm', alpha=0.75)
    plt.colorbar(label='Wind Direction Variability (°)')
    plt.title('Wind Direction Variability Distribution')
    st.pyplot(plt)

elif page == "Temperature Analysis":
    st.header('Temperature Analysis')

    # Scatter Plots
    st.subheader('Relative Humidity vs. Ambient Temperature')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='RH', y='Tamb', data=data, alpha=0.5)
    plt.title('Relative Humidity vs. Ambient Temperature')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('Ambient Temperature (°C)')
    st.pyplot(plt)

    st.subheader('Relative Humidity vs. Global Horizontal Irradiance')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='RH', y='GHI', data=data, alpha=0.5)
    plt.title('Relative Humidity vs. Global Horizontal Irradiance')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('GHI (W/m²)')
    st.pyplot(plt)

    st.subheader('Relative Humidity vs. Direct Normal Irradiance')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='RH', y='DNI', data=data, alpha=0.5)
    plt.title('Relative Humidity vs. Direct Normal Irradiance')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('DNI (W/m²)')
    st.pyplot(plt)

    st.subheader('Relative Humidity vs. Diffuse Horizontal Irradiance')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='RH', y='DHI', data=data, alpha=0.5)
    plt.title('Relative Humidity vs. Diffuse Horizontal Irradiance')
    plt.xlabel('Relative Humidity (%)')
    plt.ylabel('DHI (W/m²)')
    st.pyplot(plt)

    # Heatmap for Correlation Analysis
    st.subheader('Correlation Heatmap: RH, Temperature, and Solar Radiation')
    correlation_matrix = data[['RH', 'Tamb', 'GHI', 'DNI', 'DHI']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap: RH, Temperature, and Solar Radiation')
    st.pyplot(plt)

    # Joint Plots
    st.subheader('Joint Plots')
    sns.jointplot(x='RH', y='Tamb', data=data, kind='scatter', alpha=0.5)
    plt.suptitle('Joint Plot: Relative Humidity vs. Ambient Temperature')
    st.pyplot(plt)

elif page == "Histograms":
    st.header('Histograms')

    # Histograms for GHI, DNI, DHI
    st.subheader('Histograms for GHI, DNI, DHI')
    fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

    axs[0].hist(data['GHI'].dropna(), bins=30, color='orange')
    axs[0].set_title('Histogram of GHI')
    axs[0].set_xlabel('GHI (W/m²)')
    axs[0].set_ylabel('Frequency')

    axs[1].hist(data['DNI'].dropna(), bins=30, color='red')
    axs[1].set_title('Histogram of DNI')
    axs[1].set_xlabel('DNI (W/m²)')

    axs[2].hist(data['DHI'].dropna(), bins=30, color='blue')
    axs[2].set_title('Histogram of DHI')
    axs[2].set_xlabel('DHI (W/m²)')

    plt.suptitle('Histograms of Solar Radiation Variables')
    st.pyplot(fig)

elif page == "Z-Score Analysis":
    st.header('Z-Score Analysis')
    
    # Calculate Z-Scores
    data_z_scores = data[['GHI', 'DNI', 'DHI']].apply(lambda x: stats.zscore(x.dropna()), axis=0)
    data_z_scores['Timestamp'] = data.index

    # Plot Z-Scores
    st.subheader('Z-Scores of Solar Radiation Variables')
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(data_z_scores['Timestamp'], data_z_scores['GHI'], label='GHI Z-Score', color='orange')
    ax.plot(data_z_scores['Timestamp'], data_z_scores['DNI'], label='DNI Z-Score', color='red')
    ax.plot(data_z_scores['Timestamp'], data_z_scores['DHI'], label='DHI Z-Score', color='blue')
    ax.set_title('Z-Scores of Solar Radiation Variables')
    ax.set_xlabel('Date')
    ax.set_ylabel('Z-Score')
    ax.legend()
    st.pyplot(fig)

elif page == "Bubble Charts":
    st.header('Bubble Charts')

    # Bubble Chart for GHI, DNI, and DHI
    st.subheader('Bubble Chart: GHI, DNI, and DHI')
    plt.figure(figsize=(10, 8))
    plt.scatter(data['GHI'], data['DNI'], s=data['DHI'], alpha=0.5, c=data['GHI'], cmap='viridis')
    plt.colorbar(label='GHI (W/m²)')
    plt.title('Bubble Chart of GHI, DNI, and DHI')
    plt.xlabel('GHI (W/m²)')
    plt.ylabel('DNI (W/m²)')
    plt.xscale('log')
    plt.yscale('log')
    st.pyplot(plt)

    # Bubble Chart for Temperature and Wind Speed
    st.subheader('Bubble Chart: Temperature and Wind Speed')
    plt.figure(figsize=(10, 8))
    plt.scatter(data['Tamb'], data['WS'], s=data['GHI'], alpha=0.5, c=data['Tamb'], cmap='plasma')
    plt.colorbar(label='Temperature (°C)')
    plt.title('Bubble Chart of Temperature and Wind Speed')
    plt.xlabel('Ambient Temperature (°C)')
    plt.ylabel('Wind Speed (m/s)')
    plt.xscale('log')
    plt.yscale('log')
    st.pyplot(plt)

else:
    st.write("Please select a section from the sidebar to view the analysis.")
