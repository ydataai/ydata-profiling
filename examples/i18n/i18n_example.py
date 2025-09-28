"""
Example of using ydata-profiling with internationalization
"""
import pandas as pd
from ydata_profiling import ProfileReport
from ydata_profiling.i18n import set_locale
from ydata_profiling.utils.locale_utils import auto_set_locale

# Create sample data
df = pd.DataFrame({
    'numeric_column': [1, 2, 3, 4, 5],
    'categorical_column': ['A', 'B', 'A', 'C', 'B'],
    'text_column': ['Hello', 'World', 'Test', 'Data', 'Science']
})

# Use the default report generation method
print("Default report generation report...")
profile_default = ProfileReport(df, title="Default Data Profiling Report")
profile_default.to_file("default_report.html")

# Auto-detect and set language
print("Auto-detect generation report...")
auto_set_locale()
profile_zh = ProfileReport(df, title="Auto Detect Data Profiling Report")
profile_zh.to_file("auto_report_chinese.html")

# Generate a report in English
print("Generating English report...")
set_locale('en')
profile_en = ProfileReport(df, title="English Data Profiling Report")
profile_en.to_file("report_english.html")

# Generate a report in Chinese
print("Generating Chinese report...")
set_locale('zh')
profile_zh = ProfileReport(df, title="中文数据分析报告")
profile_zh.to_file("report_chinese.html")

# Specify the language during initialization
print("Generating report with locale parameter...")
profile_locale = ProfileReport(df, title="报告标题", locale='zh')
profile_locale.to_file("report_with_locale.html")