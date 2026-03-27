#import required libraries
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, 
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_pdf_report():
    """
    Creates a PDF report summarizing the weather analysis.
    This function builds the report page by page using reportlab.
    """
    
    #create the PDF
    #letter = 8.5 x 11 inches (standard US paper size)
    doc = SimpleDocTemplate(
        "Global_Weather_Analysis_Report.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    #get default styles and create custom ones
    styles = getSampleStyleSheet()
    
    #custom styles for our report
    #title style - big and centered
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=HexColor('#4a4a4a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    #heading style - section headers
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#667eea'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    #subheading style
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#4a4a4a'),
        spaceBefore=15,
        spaceAfter=8
    )
    
    #body text style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14  #line spacing
    )
    
    #mission statement style - italic
    mission_style = ParagraphStyle(
        'Mission',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#11998e'),
        fontName='Helvetica-Oblique',
        spaceAfter=15,
        alignment=TA_CENTER,
        leading=14
    )
    #this list will hold all the content for our PDF
    #reportlab builds the PDF from this list
    story = []
    
    #########################################################################
    # PAGE 1: TITLE PAGE
    #########################################################################
    
    story.append(Spacer(1, 1.5*inch))
    
    #main title
    story.append(Paragraph(
        "Global Weather Analysis Report",
        title_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    #subtitle
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "A Comprehensive Data Science Analysis",
        subtitle_style
    ))
    
    story.append(Spacer(1, 0.5*inch))
    
    #PM Accelerator Mission box
    story.append(Paragraph(
        "<b>PM Accelerator Mission</b>",
        ParagraphStyle('MissionTitle', parent=styles['Normal'], 
                      fontSize=14, alignment=TA_CENTER, textColor=HexColor('#11998e'))
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        '"Our mission is to break down financial barriers and achieve educational fairness. '
        'With the goal of establishing 200 schools worldwide over the next 20 years, we aim to '
        'empower more kids for a better future in their life and career, simultaneously fostering '
        'a diverse landscape in the tech industry."',
        mission_style
    ))
    
    story.append(Spacer(1, 1*inch))
    
    #proj info
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("Dataset: Kaggle Global Weather Repository", info_style))
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 2: EXECUTIVE SUMMARY
    #########################################################################
    
    story.append(Paragraph("1. Executive Summary", heading_style))
    
    story.append(Paragraph(
        "This report presents a comprehensive analysis of the Global Weather Repository dataset, "
        "containing weather observations from around the world. The analysis demonstrates both "
        "basic and advanced data science techniques including anomaly detection, multiple forecasting "
        "models, and geographical pattern analysis.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    #key statistics table
    story.append(Paragraph("Key Statistics", subheading_style))
    
    stats_data = [
        ['Metric', 'Value'],
        ['Total Observations', '130,978'],
        ['Countries Covered', '211'],
        ['Features Analyzed', '41'],
        ['Anomalies Detected', '6,549 (5.0%)'],
        ['Best Model RMSE', '2.67 degrees C'],
        ['Best Model R-squared', '0.924 (92.4%)'],
    ]
    
    #create table with styling
    stats_table = Table(stats_data, colWidths=[3*inch, 25*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 1), (-1, -1), black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(stats_table)
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 3: DATA OVERVIEW
    #########################################################################
    
    story.append(Paragraph("2. Data Overview and Cleaning", heading_style))
    
    story.append(Paragraph("Dataset Features", subheading_style))
    story.append(Paragraph(
        "The dataset includes 41 features covering geographic data, temperature measurements, "
        "atmospheric conditions, wind data, air quality metrics, and astronomical data.",
        body_style
    ))
    
    story.append(Paragraph("Data Cleaning Steps Performed:", subheading_style))
    
    cleaning_steps = [
        "Converted datetime columns for proper date handling",
        "Extracted time features (hour, day, month, day_of_week)",
        "Handled missing values using median imputation",
        "Identified and flagged anomalous records using Isolation Forest"
    ]
    
    for step in cleaning_steps:
        story.append(Paragraph(f"* {step}", body_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Temperature Statistics", subheading_style))
    
    temp_data = [
        ['Statistic', 'Value'],
        ['Minimum', '-29.8 degrees C'],
        ['Maximum', '49.2 degrees C'],
        ['Mean', '21.4 degrees C'],
        ['Standard Deviation', '9.7 degrees C'],
    ]
    
    temp_table = Table(temp_data, colWidths=[3*inch, 2.5*inch])
    temp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#11998e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(temp_table)
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 4: ANOMALY DETECTION
    #########################################################################
    
    story.append(Paragraph("3. Advanced EDA: Anomaly Detection", heading_style))
    
    story.append(Paragraph(
        "Isolation Forest algorithm was used to detect anomalies in the weather data. "
        "This algorithm identifies unusual data points by 'isolating' them - anomalies require "
        "fewer splits to isolate, making them easy to detect.",
        body_style
    ))
    
    story.append(Paragraph("Anomaly Characteristics", subheading_style))
    
    anomaly_data = [
        ['Feature', 'Anomaly Mean', 'Normal Mean', 'Difference'],
        ['Wind Speed (km/h)', '17.32', '12.71', '+36.3%'],
        ['Precipitation (mm)', '1.19', '0.08', '+1406.6%'],
        ['UV Index', '5.53', '3.26', '+69.9%'],
        ['Humidity (%)', '63.08', '66.64', '-5.3%'],
        ['Temperature (C)', '21.96', '21.34', '+2.9%'],
    ]
    
    anomaly_table = Table(anomaly_data, colWidths=[1.8*inch, 1.4*inch, 1.4*inch, 1.2*inch])
    anomaly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#ff6b6b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(anomaly_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "<b>Key Insight:</b> Anomalies are characterized by extreme precipitation (1406% higher), "
        "higher wind speeds (36% higher), and elevated UV index values - often indicating severe weather events.",
        body_style
    ))
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 5: FORECASTING MODELS
    #########################################################################
    
    story.append(Paragraph("4. Forecasting Models", heading_style))
    
    story.append(Paragraph(
        "Five different machine learning models were built and compared to predict temperature "
        "based on other weather features. The models range from simple linear regression to "
        "advanced ensemble methods.",
        body_style
    ))
    
    story.append(Paragraph("Model Performance Comparison", subheading_style))
    
    model_data = [
        ['Model', 'RMSE (C)', 'MAE (C)', 'R-squared'],
        ['Linear Regression', '7.75', '5.59', '0.359'],
        ['Ridge Regression', '7.75', '5.59', '0.359'],
        ['Random Forest (BEST)', '2.67', '1.82', '0.924'],
        ['Gradient Boosting', '3.15', '2.24', '0.895'],
        ['Ensemble (Average)', '4.68', '3.40', '0.767'],
    ]
    
    model_table = Table(model_data, colWidths=[2.2*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    model_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        #highlight best model row
        ('BACKGROUND', (0, 3), (-1, 3), HexColor('#d4edda')),
    ]))
    story.append(model_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "<b>Best Model:</b> Random Forest achieved the lowest RMSE (2.67 C) and highest "
        "R-squared score (0.924), explaining 92.4% of temperature variance!",
        body_style
    ))
    
    story.append(Paragraph("What do these metrics mean?", subheading_style))
    story.append(Paragraph(
        "<b>RMSE (Root Mean Square Error):</b> Measures average prediction error in degrees Celsius. "
        "Lower is better. Our best model predicts temperature within about 2.67 C on average.",
        body_style
    ))
    story.append(Paragraph(
        "<b>R-squared:</b> Shows how much variance is explained by the model. "
        "R-squared = 1.0 means perfect predictions, 0.0 means no better than guessing the mean. "
        "Our 0.924 score is excellent!",
        body_style
    ))
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 6: FEATURE IMPORTANCE
    #########################################################################
    
    story.append(Paragraph("5. Feature Importance Analysis", heading_style))
    
    story.append(Paragraph(
        "Feature importance tells us which weather variables are most useful for predicting temperature. "
        "This was extracted from the Random Forest model.",
        body_style
    ))
    
    importance_data = [
        ['Rank', 'Feature', 'Importance', 'Explanation'],
        ['1', 'Latitude', '37.3%', 'Distance from equator'],
        ['2', 'UV Index', '32.6%', 'Sun intensity'],
        ['3', 'Pressure', '13.4%', 'Atmospheric pressure'],
        ['4', 'Longitude', '7.4%', 'East-west position'],
        ['5', 'Humidity', '4.4%', 'Moisture in air'],
        ['6', 'Hour', '2.6%', 'Time of day'],
        ['7', 'Wind Speed', '1.1%', 'Air movement'],
        ['8', 'Cloud Cover', '0.8%', 'Sky coverage'],
        ['9', 'Visibility', '0.4%', 'How far you can see'],
    ]
    
    importance_table = Table(importance_data, colWidths=[0.6*inch, 1.4*inch, 1.2*inch, 2.5*inch])
    importance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#764ba2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(importance_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "<b>Key Insight:</b> Geographic location (latitude) is the most important factor in predicting "
        "temperature, followed by UV index intensity. This makes sense as regions closer to the equator "
        "receive more direct sunlight and are therefore warmer.",
        body_style
    ))
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 7: CLIMATE ANALYSIS
    #########################################################################
    
    story.append(Paragraph("6. Climate Analysis by Region", heading_style))
    
    story.append(Paragraph("Climate Zones", subheading_style))
    
    climate_data = [
        ['Climate Zone', 'Avg Temp (C)', 'Humidity (%)', 'Precip (mm)', 'UV Index'],
        ['Tropical (near equator)', '25.5', '72.2', '0.19', '3.4'],
        ['Temperate (mid-latitude)', '17.3', '60.8', '0.08', '3.4'],
    ]
    
    climate_table = Table(climate_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1*inch, 1*inch])
    climate_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#38ef7d')),
        ('TEXTCOLOR', (0, 0), (-1, 0), black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(climate_table)
    
    story.append(Paragraph("Extreme Weather Locations", subheading_style))
    
    story.append(Paragraph("<b>Hottest Locations (Average):</b>", body_style))
    story.append(Paragraph("1. Ar Riyadh, Saudi Arabia: 45.0 C", body_style))
    story.append(Paragraph("2. Kuwait, Kuwait: 44.4 C", body_style))
    story.append(Paragraph("3. Morocco City, Morocco: 40.3 C", body_style))
    
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>Coldest Locations (Average):</b>", body_style))
    story.append(Paragraph("1. Chi-Chi-Erh, Russia: -17.1 C", body_style))
    story.append(Paragraph("2. S-Chanf, Switzerland: 1.0 C", body_style))
    story.append(Paragraph("3. Ulaanbaatar, Mongolia: 3.4 C", body_style))
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 8: AIR QUALITY
    #########################################################################
    
    story.append(Paragraph("7. Environmental Impact: Air Quality", heading_style))
    
    story.append(Paragraph(
        "This analysis examines how air quality metrics correlate with weather parameters.",
        body_style
    ))
    
    story.append(Paragraph("Correlation with Weather Parameters", subheading_style))
    
    aq_data = [
        ['Air Quality Metric', 'vs Temperature', 'vs Humidity', 'vs Wind'],
        ['PM2.5', '+0.051', '-0.211', '-0.041'],
        ['PM10', '+0.106', '-0.238', '+0.055'],
        ['Ozone', '+0.264', '-0.410', '+0.111'],
        ['Nitrogen Dioxide', '-0.146', '-0.098', '-0.120'],
    ]
    
    aq_table = Table(aq_data, colWidths=[1.8*inch, 1.4*inch, 1.4*inch, 1.2*inch])
    aq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#17a2b8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(aq_table)
    
    story.append(Paragraph("Cities with Highest PM2.5 (Worst Air Quality)", subheading_style))
    story.append(Paragraph("1. Kuwait, Kuwait: 176.7 micrograms/cubic meter", body_style))
    story.append(Paragraph("2. Santiago, Chile: 154.2 micrograms/cubic meter", body_style))
    story.append(Paragraph("3. Jakarta, Indonesia: 146.9 micrograms/cubic meter", body_style))
    story.append(Paragraph("4. Riyadh, Saudi Arabia: 138.1 micrograms/cubic meter", body_style))
    story.append(Paragraph("5. Beijing, China: 135.7 micrograms/cubic meter", body_style))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "<b>Key Finding:</b> Higher humidity is associated with LOWER particulate matter (PM2.5, PM10), "
        "likely because moisture causes particles to settle. Temperature positively correlates with "
        "ozone formation (warmer weather = more ozone).",
        body_style
    ))
    
    story.append(PageBreak())
    
    #########################################################################
    # PAGE 9: CONCLUSIONS
    #########################################################################
    
    story.append(Paragraph("8. Conclusions and Recommendations", heading_style))
    
    story.append(Paragraph("Key Takeaways", subheading_style))
    
    conclusions = [
        "Random Forest is the best model for temperature prediction (RMSE: 2.67 C, R-squared: 0.924)",
        "Geographic location (latitude) is the most important predictor of temperature",
        "5% of weather observations are anomalous, often indicating severe weather events",
        "Tropical regions average 8 C warmer than temperate zones",
        "Higher humidity correlates with better air quality (lower PM2.5 levels)",
        "Wind helps disperse air pollutants, improving air quality"
    ]
    
    for conclusion in conclusions:
        story.append(Paragraph(f"* {conclusion}", body_style))
    
    story.append(Paragraph("Future Improvements", subheading_style))
    
    improvements = [
        "Add time series forecasting models (ARIMA, Prophet)",
        "Implement cross-validation for more robust model evaluation",
        "Create interactive dashboards with Plotly or Streamlit",
        "Add real-time data streaming capabilities",
        "Include more advanced ensemble methods (XGBoost, LightGBM)"
    ]
    
    for improvement in improvements:
        story.append(Paragraph(f"* {improvement}", body_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    #final note
    story.append(Paragraph("Files Generated", subheading_style))
    
    files_data = [
        ['File Name', 'Description'],
        ['weather_forecast_analysis.py', 'Main Python analysis script'],
        ['generate_pdf_report.py', 'This PDF generator script'],
        ['visualizations.png', '12-plot EDA visualization'],
        ['model_comparison.png', 'Model performance charts'],
        ['model_results_summary.csv', 'Model metrics in CSV format'],
        ['descriptive_statistics.csv', 'Data summary statistics'],
        ['README.md', 'Project documentation'],
        ['requirements.txt', 'Python dependencies'],
    ]
    
    files_table = Table(files_data, colWidths=[2.8*inch, 3*inch])
    files_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#6c757d')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(files_table)
    
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#888888'),
        alignment=TA_CENTER
    )
    
    #########################################################################
    # BUILD THE PDF
    #########################################################################
    
    #reportlab builds the PDF from story
    doc.build(story)


# Run the function when script is executed
if __name__ == "__main__":
    create_pdf_report()
