import unittest
import pandas as pd
import streamlit as st
from app.utils import load_data, perform_eda
from unittest.mock import patch, MagicMock
# from scripts.main import main  # Assuming your main script is named main.py

class TestLoadData(unittest.TestCase):
    def test_load_data_benin(self):
        """Test loading data for Benin."""
        df = load_data('Benin')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)  # Ensure the DataFrame is not empty

    def test_load_data_sierra_leone(self):
        """Test loading data for Sierra Leone."""
        df = load_data('Sierra Leone')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

    def test_load_data_togo(self):
        """Test loading data for Togo."""
        df = load_data('Togo')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)


class TestPerformEDA(unittest.TestCase):
    @patch('app.utils.st')
    def test_perform_eda(self, mock_st):
        """Test the perform_eda function."""
        # Create a sample DataFrame similar to what your data might look like
        df = pd.DataFrame({
            'GHI': [100, 200, 150],
            'DNI': [300, 250, 350],
            'DHI': [400, 300, 200],
            'Tamb': [20, 21, 19],
            'TModA': [15, 16, 15],
            'TModB': [14, 15, 16],
            'WS': [5, 7, 9],
            'WSgust': [10, 12, 11],
            'WD': [120, 130, 140]
        })
        
        # Mock the Streamlit methods
        mock_st.header = MagicMock()
        mock_st.subheader = MagicMock()
        mock_st.write = MagicMock()
        mock_st.pyplot = MagicMock()
        mock_st.line_chart = MagicMock()

        # Call perform_eda with the sample data
        perform_eda(df, 'Test Country')

        # Check if the mocked Streamlit methods were called
        mock_st.header.assert_called()
        mock_st.subheader.assert_called()
        mock_st.write.assert_called()
        mock_st.pyplot.assert_called()
        mock_st.line_chart.assert_called()

if __name__ == '__main__':
    unittest.main()