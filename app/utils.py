import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from scipy.stats import zscore 

def load_data(country):
    """Load the data for a specific country."""
    if country == 'Benin':
        return pd.read_csv('./data/benin-malanville.csv')
    elif country == 'Sierra Leone':
        return pd.read_csv('./data/sierraleone-bumbuna.csv')
    elif country == 'Togo':
        return pd.read_csv('./data/togo-dapaong_qc.csv')

def perform_eda(df, country_name):
    """Perform exploratory data analysis (EDA) on the given dataframe."""
    st.header(f"Exploratory Data Analysis for {country_name}")

    # Display basic statistics
    st.subheader('Summary Statistics')
    st.write(df.describe())

    # Data Quality Check
    st.subheader('Data Quality Check')
    st.write('Checking for missing values and data types:')
    st.write(df.info())

    # Missing Values
    st.write('Missing values per column:')
    st.write(df.isnull().sum())

    # Time Series Analysis
    st.subheader('Time Series Analysis')
    st.line_chart(df[['GHI', 'DNI', 'DHI', 'Tamb']])

    # Correlation Analysis
    st.subheader('Correlation Analysis')
    numeric_df = df.select_dtypes(include=[float, int])
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    st.pyplot(plt.gcf())

    # Wind Analysis
    st.subheader('Wind Analysis')
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='WS', y='GHI', data=df)
    st.pyplot(plt.gcf())

    # Wind Direction Analysis
    st.subheader('Wind Direction Analysis')
    df['WD_radians'] = np.radians(df['WD'])  # Use numpy's radians function
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    ax.scatter(df['WD_radians'], df['WS'], alpha=0.75)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title(f'Wind Speed and Direction in {country_name}')
    st.pyplot(fig)

    # Temperature Analysis
    st.subheader('Temperature Analysis')
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Tamb', y='GHI', data=df)
    st.pyplot(plt.gcf())

    # Histograms
    st.subheader('Histograms')
    df[['GHI', 'DNI', 'DHI', 'Tamb']].hist(bins=20, alpha=0.7, figsize=(12, 8))
    st.pyplot(plt.gcf())

    # Z-Score Analysis
    st.subheader('Z-Score Analysis')
    z_scores = zscore(df[['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD']])
    z_scores_df = pd.DataFrame(z_scores, columns=['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust', 'WD'], index=df.index)
    fig, ax = plt.subplots(figsize=(14, 7))
    z_scores_df.plot(ax=ax)
    ax.set_title(f'Z-Score Analysis of Solar Radiation, Temperature, and Wind Conditions in {country_name}')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Z-Score')
    st.pyplot(fig)

    # Bubble Charts
    st.subheader('Bubble Charts')
    fig, ax = plt.subplots(figsize=(10, 6))
    bubble = ax.scatter(x=df['DNI'], y=df['GHI'], s=df['WS']*10, alpha=0.5)
    ax.set_title(f'Bubble Chart of DNI vs. GHI with Wind Speed in {country_name}')
    ax.set_xlabel('DNI (W/m²)')
    ax.set_ylabel('GHI (W/m²)')
    st.pyplot(fig)