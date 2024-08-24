import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
 # Import zscore from scipy.stats
from utils import load_data,perform_eda


def main():
    st.title('Solar Radiation Measurement Analysis Dashboard')

    # Option to select the type of analysis
    analysis_type = st.sidebar.selectbox(
        'Choose Analysis Type',
        ['Combined Analysis', 'Benin Analysis', 'Sierra Leone Analysis', 'Togo Analysis']
    )

    # Perform analysis based on user selection
    if analysis_type == 'Combined Analysis':
        st.header('Combined Analysis for Benin, Sierra Leone, and Togo')
        
        # Load data for all countries
        df_benin = load_data('Benin')
        df_sierra_leone = load_data('Sierra Leone')
        df_togo = load_data('Togo')

        # Perform combined analysis (for demonstration, showing only summary statistics)
        st.subheader('Summary Statistics for Benin')
        st.write(df_benin.describe())
        st.subheader('Summary Statistics for Sierra Leone')
        st.write(df_sierra_leone.describe())
        st.subheader('Summary Statistics for Togo')
        st.write(df_togo.describe())

    elif analysis_type == 'Benin Analysis':
        df_benin = load_data('Benin')
        perform_eda(df_benin, 'Benin')

    elif analysis_type == 'Sierra Leone Analysis':
        df_sierra_leone = load_data('Sierra Leone')
        perform_eda(df_sierra_leone, 'Sierra Leone')

    elif analysis_type == 'Togo Analysis':
        df_togo = load_data('Togo')
        perform_eda(df_togo, 'Togo')

if __name__ == '__main__':
    main()
