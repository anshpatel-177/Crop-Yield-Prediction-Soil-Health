# Crop Yield Prediction & Soil Health Analysis

## Project Overview

Crop Yield Prediction & Soil Health Analysis is a machine learning-based web application designed to predict crop yield and analyze soil health using agricultural and environmental parameters.

The project uses machine learning regression models to estimate crop yield and a rule-based scoring method to classify soil health as Good, Moderate, or Poor. It also integrates the OpenWeatherMap API to fetch current weather information.

## Key Features

- **Crop Yield Prediction:** Predicts estimated crop yield in tonnes per hectare.
- **Soil Health Analysis:** Evaluates soil parameters such as pH, Nitrogen, Phosphorus, Potassium, and Organic Matter.
- **Weather Integration:** Fetches current temperature and humidity using the OpenWeatherMap API.
- **Soil Improvement Suggestions:** Displays project-based suggestions according to entered soil values.
- **Model Performance Dashboard:** Compares machine learning models using MAE, RMSE, and R² Score.
- **Prediction Report:** Allows users to download crop prediction results in CSV format.
- **Interactive Dashboard:** Provides a user-friendly interface built with Streamlit.

## Technologies Used

- Python
- Pandas and NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Joblib
- Requests
- OpenWeatherMap API
- Jupyter Notebook

## Machine Learning Models

The following regression algorithms are used for comparison:

1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor

Model evaluation metrics:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

The best-performing model is selected based on the evaluation results.

## Dataset Information

The project uses a structured synthetic agricultural dataset containing 12,000 records representing agricultural conditions across selected districts of Uttar Pradesh.

The dataset includes:
- District and crop information
- Year and cropping season
- Farm area
- Soil pH and nutrient values
- Temperature, rainfall, and humidity
- Soil moisture
- Irrigation and fertilizer information
- Soil health score and crop yield

**Note:** The dataset is synthetic and is intended for academic project development and demonstration. It should not be treated as official government or field-survey data.

## Project Structure

```text
Crop Yield Prediction/
│
├── data/
│   ├── UP_Crop_Yield_Cleaned.csv
│   └── prediction_results.csv
│
├── models/
│   ├── best_crop_yield_model.pkl
│   ├── preprocessor.pkl
│   └── model_performance.csv
│
├── notebooks/
│   └── model_training.ipynb
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd "Crop Yield Prediction"
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure OpenWeatherMap API

Create a file named `secrets.toml` inside the `.streamlit` folder.

Add your API key:

```toml
OPENWEATHER_API_KEY = "YOUR_API_KEY"
```

Keep this file private. Never upload your actual API key to GitHub.

### 7. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## Project Limitations

- The dataset is synthetic and may not represent actual field conditions.
- Predictions depend on the quality and range of the training data.
- Weather information requires an active internet connection and a valid API key.
- Rainfall and soil moisture are entered manually.
- Soil health classification uses project-specific scoring rules and is not an official soil-health assessment.
- The system is an academic decision-support prototype, not a substitute for professional agricultural advice.

## Future Scope

- Integration of real agricultural field datasets.
- Support for additional crops and geographical regions.
- Integration of IoT-based soil sensors.
- Satellite imagery and remote sensing integration.
- Advanced machine learning and deep learning techniques.
- Mobile application development.

## Project Domain

Agri-Tech | Machine Learning | Data Science

## Academic Project

B.Tech – Computer Science and Engineering (Data Science & AI)

Shri Ramswaroop Memorial University

Academic Session: 2026–27