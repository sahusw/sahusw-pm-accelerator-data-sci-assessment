##############################################################
# SECTION 1: IMPORT LIBRARIES
##############################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#machine learning libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, IsolationForest, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

#set style for all plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


##############################################################
# SECTION 2: DATA LOADING AND CLEANING
##############################################################

def load_and_clean_data(filepath):
    #read the csv file
    df = pd.read_csv(filepath)
    
    #convert last_updated to datetime
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
    
    #extract useful time features from the date
    df['date'] = df['last_updated'].dt.date
    df['hour'] = df['last_updated'].dt.hour
    df['day_of_week'] = df['last_updated'].dt.dayofweek
    df['month'] = df['last_updated'].dt.month
    df['day_of_year'] = df['last_updated'].dt.dayofyear
    
    #handle missing values with median imputation
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    return df


##############################################################
# SECTION 3: ANOMALY DETECTION
##############################################################

def detect_anomalies(df):
    #select features for anomaly detection
    features_for_anomaly = ['temperature_celsius', 'humidity', 'wind_kph', 
                            'pressure_mb', 'precip_mm', 'uv_index']
    
    #only use rows where all features exist
    df_anomaly = df[features_for_anomaly].dropna()
    
    #create and train isolation forest model
    iso_forest = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
    
    #fit and predict anomalies
    anomaly_labels = iso_forest.fit_predict(df_anomaly)
    
    #add anomaly labels to dataframe
    df.loc[df_anomaly.index, 'is_anomaly'] = anomaly_labels
    
    return df


##############################################################
# SECTION 4: DATA VISUALIZATION
##############################################################

def create_visualizations(df):
    #create figure with multiple subplots
    fig = plt.figure(figsize=(20, 24))
    
    #plot 1: temperature distribution
    ax1 = fig.add_subplot(4, 3, 1)
    df['temperature_celsius'].hist(bins=50, ax=ax1, color='coral', edgecolor='white')
    ax1.set_xlabel('Temperature (C)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Global Temperature Distribution', fontsize=12, fontweight='bold')
    ax1.axvline(df['temperature_celsius'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df["temperature_celsius"].mean():.1f}C')
    ax1.legend()
    
    #plot 2: temperature by country
    ax2 = fig.add_subplot(4, 3, 2)
    top_countries = df['country'].value_counts().head(10).index
    temp_by_country = df[df['country'].isin(top_countries)].groupby('country')['temperature_celsius'].mean().sort_values(ascending=True)
    temp_by_country.plot(kind='barh', ax=ax2, color=sns.color_palette("coolwarm", len(temp_by_country)))
    ax2.set_xlabel('Average Temperature (C)')
    ax2.set_title('Avg Temperature by Country (Top 10)', fontsize=12, fontweight='bold')
    
    #plot 3: temperature vs humidity scatter
    ax3 = fig.add_subplot(4, 3, 3)
    sample = df.sample(min(5000, len(df)), random_state=42)
    scatter = ax3.scatter(sample['temperature_celsius'], sample['humidity'], 
                         c=sample['uv_index'], cmap='viridis', alpha=0.5, s=10)
    ax3.set_xlabel('Temperature (C)')
    ax3.set_ylabel('Humidity (%)')
    ax3.set_title('Temperature vs Humidity', fontsize=12, fontweight='bold')
    plt.colorbar(scatter, ax=ax3, label='UV Index')
    
    #plot 4: wind speed distribution
    ax4 = fig.add_subplot(4, 3, 4)
    df['wind_kph'].hist(bins=50, ax=ax4, color='skyblue', edgecolor='white')
    ax4.set_xlabel('Wind Speed (km/h)')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Wind Speed Distribution', fontsize=12, fontweight='bold')
    
    #plot 5: weather conditions
    ax5 = fig.add_subplot(4, 3, 5)
    condition_counts = df['condition_text'].value_counts().head(10)
    condition_counts.plot(kind='barh', ax=ax5, color=sns.color_palette("Set2", len(condition_counts)))
    ax5.set_xlabel('Count')
    ax5.set_title('Top 10 Weather Conditions', fontsize=12, fontweight='bold')
    
    #plot 6: air quality pm2.5 distribution
    ax6 = fig.add_subplot(4, 3, 6)
    pm25_data = df['air_quality_PM2.5'].dropna()
    pm25_filtered = pm25_data[pm25_data < pm25_data.quantile(0.99)]
    pm25_filtered.hist(bins=50, ax=ax6, color='mediumpurple', edgecolor='white')
    ax6.set_xlabel('PM2.5 (ug/m3)')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Air Quality PM2.5 Distribution', fontsize=12, fontweight='bold')
    
    #plot 7: anomaly visualization
    ax7 = fig.add_subplot(4, 3, 7)
    if 'is_anomaly' in df.columns:
        anomaly_sample = df.dropna(subset=['is_anomaly']).sample(min(3000, len(df)), random_state=42)
        colors = ['red' if x == -1 else 'blue' for x in anomaly_sample['is_anomaly']]
        ax7.scatter(anomaly_sample['temperature_celsius'], anomaly_sample['wind_kph'], 
                   c=colors, alpha=0.5, s=10)
        ax7.set_xlabel('Temperature (C)')
        ax7.set_ylabel('Wind Speed (km/h)')
        ax7.set_title('Anomalies (Red) vs Normal (Blue)', fontsize=12, fontweight='bold')
    
    #plot 8: correlation heatmap
    ax8 = fig.add_subplot(4, 3, 8)
    corr_cols = ['temperature_celsius', 'humidity', 'wind_kph', 'pressure_mb', 
                 'precip_mm', 'uv_index', 'visibility_km', 'cloud']
    corr_matrix = df[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax8,
                center=0, square=True, cbar_kws={'shrink': 0.8})
    ax8.set_title('Feature Correlations', fontsize=12, fontweight='bold')
    
    #plot 9: geographic distribution
    ax9 = fig.add_subplot(4, 3, 9)
    sample_geo = df.sample(min(5000, len(df)), random_state=42)
    scatter2 = ax9.scatter(sample_geo['longitude'], sample_geo['latitude'],
                          c=sample_geo['temperature_celsius'], cmap='RdYlBu_r', 
                          alpha=0.6, s=5)
    ax9.set_xlabel('Longitude')
    ax9.set_ylabel('Latitude')
    ax9.set_title('Geographic Temperature Map', fontsize=12, fontweight='bold')
    plt.colorbar(scatter2, ax=ax9, label='Temperature (C)')
    
    #plot 10: air quality comparison
    ax10 = fig.add_subplot(4, 3, 10)
    aq_cols = ['air_quality_PM2.5', 'air_quality_PM10', 'air_quality_Ozone']
    aq_means = df[aq_cols].mean()
    ax10.bar(range(len(aq_means)), aq_means.values, color=['purple', 'orange', 'green'])
    ax10.set_xticks(range(len(aq_means)))
    ax10.set_xticklabels(['PM2.5', 'PM10', 'Ozone'], rotation=45)
    ax10.set_ylabel('Average Level')
    ax10.set_title('Average Air Quality Levels', fontsize=12, fontweight='bold')
    
    #plot 11: temperature by hour
    ax11 = fig.add_subplot(4, 3, 11)
    hourly_temp = df.groupby('hour')['temperature_celsius'].mean()
    ax11.plot(hourly_temp.index, hourly_temp.values, marker='o', color='coral', linewidth=2)
    ax11.fill_between(hourly_temp.index, hourly_temp.values, alpha=0.3, color='coral')
    ax11.set_xlabel('Hour of Day')
    ax11.set_ylabel('Average Temperature (C)')
    ax11.set_title('Temperature by Hour of Day', fontsize=12, fontweight='bold')
    ax11.set_xticks(range(0, 24, 3))
    
    #plot 12: uv index by location
    ax12 = fig.add_subplot(4, 3, 12)
    uv_by_country = df.groupby('country')['uv_index'].mean().sort_values(ascending=False).head(15)
    uv_by_country.plot(kind='bar', ax=ax12, color=sns.color_palette("YlOrRd", len(uv_by_country)))
    ax12.set_xlabel('Country')
    ax12.set_ylabel('Average UV Index')
    ax12.set_title('Top 15 Countries by UV Index', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('visualizations.png', dpi=150, bbox_inches='tight')
    plt.close()


##############################################################
# SECTION 5: FORECASTING MODELS
##############################################################

def build_forecasting_models(df):
    #prepare features for modeling
    feature_cols = ['humidity', 'wind_kph', 'pressure_mb', 'cloud', 
                    'uv_index', 'visibility_km', 'latitude', 'longitude', 'hour']
    target_col = 'temperature_celsius'
    
    #remove rows with missing values
    model_df = df[feature_cols + [target_col]].dropna()
    
    #split data into features and target
    X = model_df[feature_cols]
    y = model_df[target_col]
    
    #split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    #scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    #dictionary to store results
    results = {}
    
    #model 1: linear regression
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    lr_pred = lr_model.predict(X_test_scaled)
    results['Linear Regression'] = {
        'predictions': lr_pred,
        'rmse': np.sqrt(mean_squared_error(y_test, lr_pred)),
        'mae': mean_absolute_error(y_test, lr_pred),
        'r2': r2_score(y_test, lr_pred)
    }
    
    #model 2: ridge regression
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train_scaled, y_train)
    ridge_pred = ridge_model.predict(X_test_scaled)
    results['Ridge Regression'] = {
        'predictions': ridge_pred,
        'rmse': np.sqrt(mean_squared_error(y_test, ridge_pred)),
        'mae': mean_absolute_error(y_test, ridge_pred),
        'r2': r2_score(y_test, ridge_pred)
    }
    
    #model 3: random forest
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    results['Random Forest'] = {
        'predictions': rf_pred,
        'rmse': np.sqrt(mean_squared_error(y_test, rf_pred)),
        'mae': mean_absolute_error(y_test, rf_pred),
        'r2': r2_score(y_test, rf_pred),
        'feature_importance': dict(zip(feature_cols, rf_model.feature_importances_))
    }
    
    #model 4: gradient boosting
    gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    gb_model.fit(X_train, y_train)
    gb_pred = gb_model.predict(X_test)
    results['Gradient Boosting'] = {
        'predictions': gb_pred,
        'rmse': np.sqrt(mean_squared_error(y_test, gb_pred)),
        'mae': mean_absolute_error(y_test, gb_pred),
        'r2': r2_score(y_test, gb_pred),
        'feature_importance': dict(zip(feature_cols, gb_model.feature_importances_))
    }
    
    #ensemble model - average of all predictions
    ensemble_pred = (lr_pred + ridge_pred + rf_pred + gb_pred) / 4
    results['Ensemble (Average)'] = {
        'predictions': ensemble_pred,
        'rmse': np.sqrt(mean_squared_error(y_test, ensemble_pred)),
        'mae': mean_absolute_error(y_test, ensemble_pred),
        'r2': r2_score(y_test, ensemble_pred)
    }
    
    return results, y_test


##############################################################
# SECTION 6: CLIMATE ANALYSIS
##############################################################

def climate_analysis(df):
    #define climate zones based on latitude
    def classify_climate_zone(lat):
        lat = abs(lat)
        if lat < 23.5:
            return 'Tropical'
        elif lat < 66.5:
            return 'Temperate'
        else:
            return 'Polar'
    
    df['climate_zone'] = df['latitude'].apply(classify_climate_zone)
    
    return df


##############################################################
# SECTION 7: GEOGRAPHICAL PATTERN ANALYSIS
##############################################################

def geographical_analysis(df):
    #analyze by hemisphere
    df['hemisphere'] = df['latitude'].apply(lambda x: 'Northern' if x >= 0 else 'Southern')
    
    #continental analysis based on coordinates
    def classify_continent(row):
        lat, lon = row['latitude'], row['longitude']
        if -30 < lat < 70 and -30 < lon < 60:
            return 'Europe/Africa'
        elif -60 < lat < 80 and 60 < lon < 180:
            return 'Asia/Oceania'
        elif -60 < lat < 80 and -180 < lon < -30:
            return 'Americas'
        else:
            return 'Other'
    
    df['continent_region'] = df.apply(classify_continent, axis=1)
    
    return df


##############################################################
# SECTION 8: CREATE MODEL COMPARISON VISUALIZATION
##############################################################

def create_model_plots(model_results, y_test):
    fig = plt.figure(figsize=(16, 12))
    
    #plot 1: model performance comparison (rmse)
    ax1 = fig.add_subplot(2, 2, 1)
    models = list(model_results.keys())
    rmse_values = [model_results[m]['rmse'] for m in models]
    colors = sns.color_palette("husl", len(models))
    bars = ax1.bar(range(len(models)), rmse_values, color=colors)
    ax1.set_xticks(range(len(models)))
    ax1.set_xticklabels(models, rotation=45, ha='right')
    ax1.set_ylabel('RMSE (C)')
    ax1.set_title('Model Performance Comparison (RMSE)', fontsize=12, fontweight='bold')
    
    #add value labels on bars
    for bar, val in zip(bars, rmse_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=10)
    
    #plot 2: r2 score comparison
    ax2 = fig.add_subplot(2, 2, 2)
    r2_values = [model_results[m]['r2'] for m in models]
    bars2 = ax2.bar(range(len(models)), r2_values, color=colors)
    ax2.set_xticks(range(len(models)))
    ax2.set_xticklabels(models, rotation=45, ha='right')
    ax2.set_ylabel('R2 Score')
    ax2.set_title('Model R2 Score Comparison', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 1)
    
    for bar, val in zip(bars2, r2_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.3f}', ha='center', va='bottom', fontsize=10)
    
    #plot 3: actual vs predicted for best model
    ax3 = fig.add_subplot(2, 2, 3)
    best_model_name = min(model_results.items(), key=lambda x: x[1]['rmse'])[0]
    best_pred = model_results[best_model_name]['predictions']
    
    #sample for visualization
    sample_idx = np.random.choice(len(y_test), min(1000, len(y_test)), replace=False)
    y_test_sample = y_test.iloc[sample_idx]
    pred_sample = best_pred[sample_idx]
    
    ax3.scatter(y_test_sample, pred_sample, alpha=0.5, s=10)
    ax3.plot([y_test_sample.min(), y_test_sample.max()], 
             [y_test_sample.min(), y_test_sample.max()], 'r--', linewidth=2)
    ax3.set_xlabel('Actual Temperature (C)')
    ax3.set_ylabel('Predicted Temperature (C)')
    ax3.set_title(f'Actual vs Predicted ({best_model_name})', fontsize=12, fontweight='bold')
    
    #plot 4: feature importance from random forest
    ax4 = fig.add_subplot(2, 2, 4)
    if 'Random Forest' in model_results and 'feature_importance' in model_results['Random Forest']:
        importance = model_results['Random Forest']['feature_importance']
        sorted_imp = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        features = [x[0] for x in sorted_imp]
        importances = [x[1] for x in sorted_imp]
        
        y_pos = range(len(features))
        ax4.barh(y_pos, importances, color=sns.color_palette("viridis", len(features)))
        ax4.set_yticks(y_pos)
        ax4.set_yticklabels(features)
        ax4.set_xlabel('Importance')
        ax4.set_title('Feature Importance (Random Forest)', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()


##############################################################
# SECTION 9: SAVE RESULTS
##############################################################

def save_results(model_results, df):
    #save model results to csv
    summary_data = []
    for model_name, results in model_results.items():
        summary_data.append({
            'Model': model_name,
            'RMSE': round(results['rmse'], 3),
            'MAE': round(results['mae'], 3),
            'R2_Score': round(results['r2'], 4)
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('model_results_summary.csv', index=False)
    
    #save descriptive statistics
    df.describe().to_csv('descriptive_statistics.csv')


##############################################################
# SECTION 10: MAIN EXECUTION
##############################################################

def main():
    #load and clean data
    df = load_and_clean_data('GlobalWeatherRepository.csv')
    
    #detect anomalies
    df = detect_anomalies(df)
    
    #create visualizations
    create_visualizations(df)
    
    #build forecasting models
    model_results, y_test = build_forecasting_models(df)
    
    #perform climate analysis
    df = climate_analysis(df)
    
    #perform geographical analysis
    df = geographical_analysis(df)
    
    #create model comparison plots
    create_model_plots(model_results, y_test)
    
    #save results
    save_results(model_results, df)


#run the main function when script is executed
if __name__ == "__main__":
    main()