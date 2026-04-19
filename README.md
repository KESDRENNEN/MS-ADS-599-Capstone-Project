# Predicting Next-Day Flight Delay and Cancellation Risk Using Pre-Departure Operational Data, Weather Signals, and Temporal Feature Engineering

This project is a part of the ADS-599 course in the Applied Data Science Program at the University of San Diego.

## Installation
### 1. To use this project, first clone the repositry using the command below
   
    git clone https://github.com/KESDRENNEN/MS-ADS-599-Capstone-Project.git
   
    cd MS-ADS-599-Capstone-Project/CapstoneProjectContent
   
### 2. Create and Activate Environment (Conda)
   
    conda create -n capstone python=3.10 -y
    conda activate capstone
   
### 3. Install dependencies
   
    pip install -r requirements.txt
   
### 4. Run the dashboard
   
    pip install -r requirements.txt
   
### 5. Run Notebook (Optional)

    streamlit run app.py

## Project Introduction/Objective

  The main purpose of this project is to develop a predictive system that estimates the risk of next-day flight delays (15+ minutes) and cancellations using only pre-departure information. The goal is to shift from reactive to proactive decision-making by identifying disruption risk before flights occur.

  This project supports operational planning for airlines and airports by enabling better resource allocation and scheduling decisions. By combining historical operational patterns with weather signals, the model provides actionable insights that can improve efficiency and reduce passenger disruption.

## Partners

Akshat Patni

Kirsten Drennen

# Methods Used

• Predictive Modeling

• Machine Learning (Classification)

• Data Engineering

• Data Cleaning and Transformation

• Feature Engineering (Lagged, Rolling, Aggregated Features)

• Time-Based Cross-Validation

• Exploratory Data Analysis (EDA)

• Data Visualization

# Technologies

• Python

• Pandas, NumPy

• Scikit-learn

• Matplotlib, Seaborn, Plotly

• Streamlit (Dashboard Deployment)

• Jupyter Notebook

• Parquet (Data Storage)

## Project Description

This project uses two primary datasets:

  • Flight Data: U.S. Bureau of Transportation Statistics (BTS) On-Time Performance dataset
  
  • Weather Data: Open-Meteo Historical Weather API

  The dataset consists of hundreds of thousands of flight records with features including origin, destination, carrier, flight date, weather conditions, and engineered historical delay patterns.

  A key component of this project is feature engineering, where lagged and rolling delay rates were created across multiple levels (route, carrier-route, origin) to capture temporal and network-level patterns in delay behavior. These features were designed to reflect only pre-departure information to avoid data leakage and ensure real-world applicability.

  The modeling approach frames the problem as a binary classification task, predicting whether a flight will experience a delay of 15 minutes or more. Multiple models were evaluated, including Logistic Regression, Random Forest, and HistGradientBoosting, using time-based cross-validation. Model performance was evaluated using ROC-AUC, PR-AUC, and F1 score.

  A key outcome of the project is an interactive Streamlit dashboard, which allows users to explore predicted delay risk across flights, routes, and time periods. The dashboard integrates model outputs with historical baseline rates to support both high-level monitoring and detailed analysis.

###  Challenges
  • Preventing data leakage from post-event variables
  
  • Handling large datasets efficiently
  
  • Capturing temporal dependencies in delay behavior
  
  • Balancing model performance with interpretability

## Live Application

The deployed dashboard can be accessed here:  
https://ms-ads-599-capstone-project.streamlit.app

## License

This project is licensed under the MIT License.

## Acknowledgments

• U.S. Bureau of Transportation Statistics (BTS) for flight data  

• Open-Meteo for historical weather data  

• University of San Diego Applied Data Science Program faculty and instructors for guidance  

• OpenAI ChatGPT for assistance with code troubleshooting, documentation, and drafting support  
     - All modeling decisions, data processing, analysis, and interpretations were developed and validated by the authors

