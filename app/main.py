import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
# Load your dataset
@st.cache_data
def load_data():
    data = pd.read_csv('C:/Users/zelalem.wubet/projects/personal/ten-academy/Solar-Radiation-Measurement/data/benin-malanville.csv')
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])  # Ensure Timestamp is in datetime format
    data.set_index('Timestamp', inplace=True)  # Set Timestamp as the index
    return data

data = load_data()

# Dashboard title
st.title("MoonLight Energy Solutions - Solar Data Visualization")

# Visualizing Outliers
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

# Resampling Data
monthly_data = data.resample('M').mean()  # Monthly average
daily_data = data.resample('D').mean()    # Daily average
hourly_data = data.resample('H').mean()   # Hourly average

# Plotting Monthly Data
st.header('Monthly Averages of GHI, DNI, DHI, and Tamb')
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
st.header('Daily Averages of GHI, DNI, DHI, and Tamb')
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
st.header('Monthly Area Plot of GHI, DNI, DHI, and Tamb')
fig, ax = plt.subplots(figsize=(14, 7))
monthly_data[['GHI', 'DNI', 'DHI', 'Tamb']].plot.area(ax=ax, alpha=0.4)
ax.set_title('Monthly Area Plot of GHI, DNI, DHI, and Tamb')
ax.set_xlabel('Date')
ax.set_ylabel('Values')
st.pyplot(fig)

# Correlation Analysis
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

# Wind Analysis 
st.header('Wind Analysis')
# Convert the wind direction (WD) from degrees to radians since polar plots in Matplotlib require angles in radians.
data['WD_radians'] = np.deg2rad(data['WD'])

#Create a Polar Plot for Wind Speed and Direction
plt.figure(figsize=(8, 8))
plt.subplot(projection='polar')
plt.scatter(data['WD_radians'], data['WS'], c=data['WS'], cmap='viridis', alpha=0.75)
plt.colorbar(label='Wind Speed (m/s)')
plt.title('Wind Speed and Direction Distribution')
st.pyplot(plt)


# Plot Wind Gusts
plt.figure(figsize=(8, 8))
plt.subplot(projection='polar')
plt.scatter(data['WD_radians'], data['WSgust'], c=data['WSgust'], cmap='plasma', alpha=0.75)
plt.colorbar(label='Wind Gust Speed (m/s)')
plt.title('Wind Gust Speed and Direction Distribution')
st.pyplot(plt)

#Analyze Wind Direction Variability
plt.figure(figsize=(8, 8))
plt.subplot(projection='polar')
plt.scatter(data['WD_radians'], data['WDstdev'], c=data['WDstdev'], cmap='coolwarm', alpha=0.75)
plt.colorbar(label='Wind Direction Variability (°)')
plt.title('Wind Direction Variability Distribution')
st.pyplot(plt)



# Temperature Analysis 
st.header('Temperature Analysis')

#Scatter Plots
# RH vs. Ambient Temperature (Tamb)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='RH', y='Tamb', data=data, alpha=0.5)
plt.title('Relative Humidity vs. Ambient Temperature')
plt.xlabel('Relative Humidity (%)')
plt.ylabel('Ambient Temperature (°C)')
st.pyplot(plt)

# RH vs. Global Horizontal Irradiance (GHI)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='RH', y='GHI', data=data, alpha=0.5)
plt.title('Relative Humidity vs. Global Horizontal Irradiance')
plt.xlabel('Relative Humidity (%)')
plt.ylabel('GHI (W/m²)')
st.pyplot(plt)

# RH vs. Direct Normal Irradiance (DNI)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='RH', y='DNI', data=data, alpha=0.5)
plt.title('Relative Humidity vs. Direct Normal Irradiance')
plt.xlabel('Relative Humidity (%)')
plt.ylabel('DNI (W/m²)')
st.pyplot(plt)

# RH vs. Diffuse Horizontal Irradiance (DHI)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='RH', y='DHI', data=data, alpha=0.5)
plt.title('Relative Humidity vs. Diffuse Horizontal Irradiance')
plt.xlabel('Relative Humidity (%)')
plt.ylabel('DHI (W/m²)')
st.pyplot(plt)

#Heatmap for Correlation Analysis
correlation_matrix = data[['RH', 'Tamb', 'GHI', 'DNI', 'DHI']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap: RH, Temperature, and Solar Radiation')
st.pyplot(plt)

# Joint Plots
# RH vs. Tamb
sns.jointplot(x='RH', y='Tamb', data=data, kind='scatter', alpha=0.5)
plt.suptitle('Joint Plot: Relative Humidity vs. Ambient Temperature', y=1.02)
st.pyplot(plt)

# RH vs. GHI
sns.jointplot(x='RH', y='GHI', data=data, kind='scatter', alpha=0.5)
plt.suptitle('Joint Plot: Relative Humidity vs. Global Horizontal Irradiance', y=1.02)
st.pyplot(plt)

# RH vs. DNI
sns.jointplot(x='RH', y='DNI', data=data, kind='scatter', alpha=0.5)
plt.suptitle('Joint Plot: Relative Humidity vs. Direct Normal Irradiance', y=1.02)
st.pyplot(plt)

# RH vs. DHI
sns.jointplot(x='RH', y='DHI', data=data, kind='scatter', alpha=0.5)
plt.suptitle('Joint Plot: Relative Humidity vs. Diffuse Horizontal Irradiance', y=1.02)
st.pyplot(plt)


# Histograms
st.header('Histograms')
#  Set up the figure and axes
plt.figure(figsize=(14, 10))

# Histogram for Global Horizontal Irradiance (GHI)
plt.subplot(3, 2, 1)
sns.histplot(data['GHI'], bins=50, kde=True, color='skyblue')
plt.title('Histogram of Global Horizontal Irradiance (GHI)')
plt.xlabel('GHI (W/m²)')
plt.ylabel('Frequency')

# Histogram for Direct Normal Irradiance (DNI)
plt.subplot(3, 2, 2)
sns.histplot(data['DNI'], bins=50, kde=True, color='lightgreen')
plt.title('Histogram of Direct Normal Irradiance (DNI)')
plt.xlabel('DNI (W/m²)')
plt.ylabel('Frequency')

# Histogram for Diffuse Horizontal Irradiance (DHI)
plt.subplot(3, 2, 3)
sns.histplot(data['DHI'], bins=50, kde=True, color='salmon')
plt.title('Histogram of Diffuse Horizontal Irradiance (DHI)')
plt.xlabel('DHI (W/m²)')
plt.ylabel('Frequency')

# Histogram for Wind Speed (WS)
plt.subplot(3, 2, 4)
sns.histplot(data['WS'], bins=50, kde=True, color='orange')
plt.title('Histogram of Wind Speed (WS)')
plt.xlabel('WS (m/s)')
plt.ylabel('Frequency')

# Histogram for Ambient Temperature (Tamb)
plt.subplot(3, 2, 5)
sns.histplot(data['Tamb'], bins=50, kde=True, color='blue')
plt.title('Histogram of Ambient Temperature (Tamb)')
plt.xlabel('Tamb (°C)')
plt.ylabel('Frequency')

# Histogram for Module A Temperature (TModA)
plt.subplot(3, 2, 6)
sns.histplot(data['TModA'], bins=50, kde=True, color='purple')
plt.title('Histogram of Module A Temperature (TModA)')
plt.xlabel('TModA (°C)')
plt.ylabel('Frequency')

# Adjust layout
plt.tight_layout()
st.pyplot(plt)

# Z-Score Analysis
st.header('Z-Score Analysis')
# Calculate Z-scores for all numeric columns
z_scores = pd.DataFrame(stats.zscore(data.select_dtypes(include=[np.number])), columns=data.select_dtypes(include=[np.number]).columns)

# Define the threshold for identifying outliers
threshold = 3

# Identify outliers
outliers = (np.abs(z_scores) > threshold).astype(int)

# Add Z-scores and outliers to the original dataframe
df_z_scores = data.copy()
df_z_scores[z_scores.columns] = z_scores
df_z_scores[outliers.columns] = outliers

# Determine the number of columns to plot
num_columns = len(z_scores.columns)

# Calculate the number of rows and columns for the subplot grid
num_rows = int(np.ceil(num_columns / 4))  # 4 columns per row

# Plot histograms of Z-scores
plt.figure(figsize=(14, 10))

for i, column in enumerate(z_scores.columns):
    plt.subplot(num_rows, 4, i + 1)  # Adjust the grid size dynamically
    sns.histplot(z_scores[column], bins=50, kde=True, color='skyblue')
    plt.title(f'Z-Scores for {column}')
    plt.xlabel('Z-Score')
    plt.ylabel('Frequency')

plt.tight_layout()
st.pyplot(plt)

# Bubble Charts

# Extract relevant columns
data = data[['GHI', 'Tamb', 'WS', 'RH', 'BP']]


# Plotting
plt.figure(figsize=(12, 8))

# Create bubble chart
plt.scatter(
    data['GHI'],         # X-axis
    data['Tamb'],        # Y-axis
    s=data['RH'] * 10,   # Bubble size (scaled for better visibility)
    c=data['BP'],        # Bubble color (optional, can represent another variable)
    cmap='viridis',      # Color map
    alpha=0.6,           # Transparency
    edgecolors='w',      # Edge color
    linewidth=0.5       # Edge width
)

# Add labels and title
plt.xlabel('Global Horizontal Irradiance (GHI)')
plt.ylabel('Ambient Temperature (Tamb)')
plt.title('Bubble Chart of GHI vs. Tamb vs. WS with Bubble Size Representing RH')
plt.colorbar(label='Barometric Pressure (BP)')  # Color bar for bubble color if used
plt.grid(True)

# Show plot
st.pyplot(plt)