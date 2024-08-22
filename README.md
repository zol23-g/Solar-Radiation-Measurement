# Solar-Radiation-Measurement

===========================================================================
## Overview
Welcome to the Solar Farm Data Analysis Dashboard project! This project aims to provide a comprehensive and interactive web application for performing exploratory data analysis (EDA) on solar farm data from various countries. Built using Streamlit, a powerful and user-friendly framework for creating data apps in Python, this dashboard allows users to gain insights into solar farm performance and related environmental factors.

## Features
This dashboard offers a range of features to help you analyze and visualize solar farm data effectively:

- Summary Statistics: Get a quick overview of key metrics such as mean, median, standard deviation, and more.
- Data Quality Checks: Identify and handle missing values, duplicates, and other data quality issues.
- Time Series Analysis: Explore trends and patterns over time with interactive time series plots.
- Correlation Analysis: Understand relationships between different variables using correlation matrices and scatter plots.
- Wind Analysis: Analyze the impact of wind speed and direction on solar farm performance.
- Temperature Analysis: Examine how temperature variations affect solar energy production.
- Visualizations: Generate histograms, box plots, scatter plots, and more to visualize data distributions and relationships.

## Installation
To get started with the Solar RadiationMeasurement Dashboard, follow these steps:

1. Clone the Repository: Clone this repository to your local machine using the following command:

   git clone https://github.com/zol23-g/Solar-Radiation-Measurement.git
   

2. Navigate to the Project Directory: Change to the project directory:
   
   cd Solar-Radiation-Measurement
   

3. Install Dependencies: Install the required Python packages using pip:
   
   pip install -r requirements.txt
   

4. Run the Streamlit App: Launch the Streamlit application:
   
   streamlit run app/main.py
   

## Usage
Once the Streamlit app is running, open your web browser and navigate to the local URL displayed in your terminal (usually `http://localhost:8501`). Use the sidebar to select a country from the available options. The dashboard will then display the corresponding EDA results, allowing you to interact with various visualizations and analyses.

## Data
The data used in this project is stored in CSV files located in the `data` directory. Each file contains solar farm data for a specific country, including information on solar energy production, weather conditions, and other relevant variables.

## Contributing
I welcome contributions to enhance the functionality and usability of this dashboard. If you have any suggestions or improvements, please feel free to open an issue or submit a pull request. For major changes, it's best to discuss your ideas first by opening an issue to ensure alignment with the project's goals.

Thank you for your interest in the Solar Radiation Measurement Analysis Dashboard! I hope you find it useful and informative.