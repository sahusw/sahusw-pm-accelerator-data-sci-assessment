# ============================================================================
# SECTION 1: IMPORT LIBRARIES
# ============================================================================

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


# ============================================================================
# SECTION 2: LOAD DATA FROM CSV FILES
# ============================================================================

def load_analysis_results():
    #load model results
    model_df = pd.read_csv('model_results_summary.csv')
    
    #load descriptive statistics
    stats_df = pd.read_csv('descriptive_statistics.csv', index_col=0)
    
    #extract key values from model results
    best_model_idx = model_df['RMSE'].idxmin()
    best_model_name = model_df.loc[best_model_idx, 'Model']
    best_rmse = model_df.loc[best_model_idx, 'RMSE']
    best_r2 = model_df.loc[best_model_idx, 'R2_Score']
    
    #extract key values from descriptive statistics
    temp_mean = stats_df.loc['mean', 'temperature_celsius']
    temp_min = stats_df.loc['min', 'temperature_celsius']
    temp_max = stats_df.loc['max', 'temperature_celsius']
    temp_std = stats_df.loc['std', 'temperature_celsius']
    humidity_mean = stats_df.loc['mean', 'humidity']
    wind_mean = stats_df.loc['mean', 'wind_kph']
    total_rows = int(stats_df.loc['count', 'temperature_celsius'])
    
    return {
        'model_df': model_df,
        'stats_df': stats_df,
        'best_model_name': best_model_name,
        'best_rmse': best_rmse,
        'best_r2': best_r2,
        'temp_mean': temp_mean,
        'temp_min': temp_min,
        'temp_max': temp_max,
        'temp_std': temp_std,
        'humidity_mean': humidity_mean,
        'wind_mean': wind_mean,
        'total_rows': total_rows
    }


# ============================================================================
# SECTION 3: CREATE PDF REPORT
# ============================================================================

def create_pdf_report():
    #load data from csv files
    data = load_analysis_results()
    
    #create the pdf document
    doc = SimpleDocTemplate(
        "Global_Weather_Analysis_Report.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    #get default styles
    styles = getSampleStyleSheet()
    
    #custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=HexColor('#4a4a4a'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#667eea'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#4a4a4a'),
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
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
    
    #list to hold all content
    story = []
    
    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Global Weather Analysis Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=HexColor('#666666'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("A Comprehensive Data Science Analysis", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("<b>PM Accelerator Mission</b>",
        ParagraphStyle('MissionTitle', parent=styles['Normal'], 
                      fontSize=14, alignment=TA_CENTER, textColor=HexColor('#11998e'))))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        '"Our mission is to break down financial barriers and achieve educational fairness. '
        'With the goal of establishing 200 schools worldwide over the next 20 years, we aim to '
        'empower more kids for a better future in their life and career, simultaneously fostering '
        'a diverse landscape in the tech industry."',
        mission_style))
    
    story.append(Spacer(1, 1*inch))
    
    info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=12,
                                textColor=HexColor('#666666'), alignment=TA_CENTER)
    story.append(Paragraph("Data Science Project | 2024", info_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY
    # =========================================================================
    
    story.append(Paragraph("1. Executive Summary", heading_style))
    story.append(Paragraph(
        "This report presents a comprehensive analysis of the Global Weather Repository dataset. "
        "The analysis demonstrates both basic and advanced data science techniques including "
        "anomaly detection, multiple forecasting models, and geographical pattern analysis.",
        body_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Key Statistics", subheading_style))
    
    #build stats table using actual data
    stats_data = [
        ['Metric', 'Value'],
        ['Total Observations', f'{data["total_rows"]:,}'],
        ['Best Model', data['best_model_name']],
        ['Best Model RMSE', f'{data["best_rmse"]:.2f} degrees C'],
        ['Best Model R-squared', f'{data["best_r2"]:.4f} ({data["best_r2"]*100:.1f}%)'],
        ['Average Temperature', f'{data["temp_mean"]:.1f} degrees C'],
        ['Average Humidity', f'{data["humidity_mean"]:.1f}%'],
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(stats_table)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: DATA OVERVIEW
    # =========================================================================
    
    story.append(Paragraph("2. Data Overview", heading_style))
    story.append(Paragraph("Temperature Statistics", subheading_style))
    
    temp_data = [
        ['Statistic', 'Value'],
        ['Minimum', f'{data["temp_min"]:.1f} degrees C'],
        ['Maximum', f'{data["temp_max"]:.1f} degrees C'],
        ['Mean', f'{data["temp_mean"]:.1f} degrees C'],
        ['Standard Deviation', f'{data["temp_std"]:.1f} degrees C'],
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
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Other Weather Statistics", subheading_style))
    
    other_data = [
        ['Metric', 'Average Value'],
        ['Humidity', f'{data["humidity_mean"]:.1f}%'],
        ['Wind Speed', f'{data["wind_mean"]:.1f} km/h'],
    ]
    
    other_table = Table(other_data, colWidths=[3*inch, 2.5*inch])
    other_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#17a2b8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(other_table)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 4: MODEL COMPARISON
    # =========================================================================
    
    story.append(Paragraph("3. Forecasting Models", heading_style))
    story.append(Paragraph(
        "Five different machine learning models were built and compared to predict temperature. "
        "The table below shows the performance metrics for each model.",
        body_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Model Performance Comparison", subheading_style))
    
    #build model table from actual data
    model_table_data = [['Model', 'RMSE (C)', 'MAE (C)', 'R-squared']]
    for _, row in data['model_df'].iterrows():
        model_table_data.append([
            row['Model'],
            f'{row["RMSE"]:.2f}',
            f'{row["MAE"]:.2f}',
            f'{row["R2_Score"]:.4f}'
        ])
    
    model_table = Table(model_table_data, colWidths=[2.2*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    
    #find best model row index for highlighting
    best_row_idx = data['model_df']['RMSE'].idxmin() + 1
    
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#dddddd')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, best_row_idx), (-1, best_row_idx), HexColor('#d4edda')),
    ]
    model_table.setStyle(TableStyle(table_style))
    story.append(model_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        f"<b>Best Model:</b> {data['best_model_name']} achieved the lowest RMSE "
        f"({data['best_rmse']:.2f} C) and highest R-squared score ({data['best_r2']:.4f}), "
        f"explaining {data['best_r2']*100:.1f}% of temperature variance.",
        body_style))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 5: METHODOLOGY
    # =========================================================================
    
    story.append(Paragraph("4. Methodology", heading_style))
    
    story.append(Paragraph("Data Cleaning", subheading_style))
    story.append(Paragraph("* Converted datetime columns for proper date handling", body_style))
    story.append(Paragraph("* Extracted time features (hour, day, month)", body_style))
    story.append(Paragraph("* Handled missing values using median imputation", body_style))
    story.append(Paragraph("* Identified anomalies using Isolation Forest algorithm", body_style))
    
    story.append(Paragraph("Anomaly Detection", subheading_style))
    story.append(Paragraph(
        "Isolation Forest algorithm was used to detect anomalies in the weather data. "
        "This algorithm identifies unusual data points by isolating them. Anomalies require "
        "fewer splits to isolate, making them easy to detect. The contamination rate was "
        "set to 5%.",
        body_style))
    
    story.append(Paragraph("Machine Learning Models", subheading_style))
    story.append(Paragraph("* Linear Regression - simple baseline model", body_style))
    story.append(Paragraph("* Ridge Regression - linear model with regularization", body_style))
    story.append(Paragraph("* Random Forest - ensemble of decision trees", body_style))
    story.append(Paragraph("* Gradient Boosting - sequential ensemble method", body_style))
    story.append(Paragraph("* Ensemble Average - combination of all models", body_style))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 6: CONCLUSIONS
    # =========================================================================
    
    story.append(Paragraph("5. Conclusions", heading_style))
    
    story.append(Paragraph("Key Findings", subheading_style))
    story.append(Paragraph(
        f"* {data['best_model_name']} is the best model for temperature prediction "
        f"(RMSE: {data['best_rmse']:.2f} C)",
        body_style))
    story.append(Paragraph(
        f"* The model explains {data['best_r2']*100:.1f}% of temperature variance",
        body_style))
    story.append(Paragraph(
        f"* Average global temperature in the dataset: {data['temp_mean']:.1f} C",
        body_style))
    story.append(Paragraph(
        f"* Temperature range: {data['temp_min']:.1f} C to {data['temp_max']:.1f} C",
        body_style))
    
    story.append(Paragraph("Output Files Generated", subheading_style))
    
    files_data = [
        ['File Name', 'Description'],
        ['weather_forecast_analysis.py', 'Main analysis script'],
        ['generate_pdf_report.py', 'PDF generator script'],
        ['visualizations.png', 'EDA visualizations'],
        ['model_comparison.png', 'Model performance charts'],
        ['model_results_summary.csv', 'Model metrics'],
        ['descriptive_statistics.csv', 'Data statistics'],
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
    
    #footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10,
                                  textColor=HexColor('#888888'), alignment=TA_CENTER)
    story.append(Paragraph("---", footer_style))
    story.append(Paragraph("Global Weather Analysis Report", footer_style))
    story.append(Paragraph("PM Accelerator Data Science Assessment", footer_style))
    
    #build the pdf
    doc.build(story)


# ============================================================================
# SECTION 4: MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    create_pdf_report()