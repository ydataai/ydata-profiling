# 自定义翻译
 
ydata-profiling 支持用户自定义翻译文件，让您可以添加新的语言支持或修改现有翻译。
 
## 快速开始
### 1. 安装 ydata-profiling
```bash
pip install ydata-profiling
```

### 2. 导出翻译模板
#### 方法A：使用命令行工具生成模板
```python
ydata-profiling-translate create-template -l en -o ./
这会生成 en_template.json 文件
```
#### 方法B：使用Python代码生成模板
```python
from ydata_profiling.i18n import export_translation_template
 
# 导出英文模板作为翻译基础
export_translation_template('en', 'translation_template.json')
```

### 3.编辑翻译文件
#### 将模板文件重命名并翻译，例如创建 french.json：
```json
{
  "report": {
    "title": "Rapport d'Analyse YData",
    "overview": "Aperçu"
  }
}
```

### 4. 在您的项目代码中使用
```python
# 您的项目文件，例如 data_analysis.py
import pandas as pd
from ydata_profiling import ProfileReport
from ydata_profiling.i18n import load_translation_file, set_locale
 
# 加载您创建的翻译文件
load_translation_file('./french.json', 'fr')
 
# 设置语言并生成报告
set_locale('fr')
df = pd.read_csv('your_data.csv')
profile = ProfileReport(df, title="Mon Analyse de Données")
profile.to_file("rapport_francais.html")
```

### 项目结构示例
#### 您的项目结构可能如下：
```bash
my_data_project/
├── data/
│   └── dataset.csv
├── translations/          # 您的翻译文件目录
│   ├── zh.json
│   ├── french.json
│   └── german.json
├── analysis.py           # 您的分析脚本
└── requirements.txt
```
#### 在 analysis.py 中：
```python
from ydata_profiling.i18n import add_translation_directory
 
# 加载整个翻译目录
add_translation_directory('./translations/')
 
# 现在可以使用任何语言
set_locale('zh')  # 使用法语
```