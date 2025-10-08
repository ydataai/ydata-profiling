"""
Complete workflow example for custom translations in ydata-profiling
演示如何使用 ydata-profiling 的自定义翻译功能的完整工作流程
"""
import pandas as pd
import json
import tempfile
import shutil
from pathlib import Path
from ydata_profiling import ProfileReport
from ydata_profiling.i18n import (
    export_translation_template,
    load_translation_file,
    add_translation_directory,
    set_locale,
    get_available_locales,
    get_locale
)
from ydata_profiling.i18n import _


def create_sample_data():
    """创建示例数据"""
    print("📊 Creating sample dataset...")

    data = {
        'product_name': ['iPhone 14', 'Samsung Galaxy', 'Google Pixel', 'iPhone 14', 'OnePlus 10'],
        'price': [999, 899, 799, 999, 649],
        'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
        'rating': [4.5, 4.2, 4.0, 4.5, 3.8],
        'in_stock': [True, True, False, True, True],
        'release_date': ['2022-09-16', '2022-02-25', '2022-10-13', '2022-09-16', '2022-01-11']
    }

    df = pd.DataFrame(data)
    print(f"✅ Sample dataset created with {len(df)} rows and {len(df.columns)} columns")
    return df


def step1_export_template():
    """步骤1: 导出翻译模板"""
    print("\n🔧 Step 1: Exporting translation template...")

    # 导出英文模板作为翻译基础
    template_file = "en_translation_template.json"
    export_translation_template('en', template_file)

    print(f"✅ Translation template exported to: {template_file}")

    # 显示模板内容预览
    with open(template_file, 'r', encoding='utf-8') as f:
        template_data = json.load(f)

    print("📋 Template preview (first few keys):")
    print(json.dumps({k: v for k, v in list(template_data.items())[:2]}, indent=2))

    return template_file


def step2_create_custom_translations(template_file):
    """步骤2: 基于模板创建自定义翻译"""
    print(f"\n🌍 Step 2: Creating custom translations based on {template_file}...")

    # 读取模板
    with open(template_file, 'r', encoding='utf-8') as f:
        template = json.load(f)

    # 创建法语翻译
    french_translation = {
        "report": {
            "title": "Rapport de profilage YData",
            "overview": "Aperçu",
            "variables": "Variables",
            "interactions": "Interactions",
            "correlations": "Corrélations",
            "missing_values": "Valeurs manquantes",
            "sample": "Échantillon",
            "duplicates": "Lignes dupliquées",
            "footer_text": "Rapport généré par <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=pandasprofiling&utm_campaign=report\">YData</a>.",
            "most_frequently_occurring": "Les plus fréquemment observés",
            "columns": "Colonnes",
            "more_details": "Plus de détails"
        },
        "overview": {
            "dataset_info": "Informations sur l'ensemble de données",
            "variable_types": "Types de variables",
            "dataset_statistics": "Statistiques de l'ensemble de données",
            "number_of_variables": "Nombre de variables",
            "number_of_observations": "Nombre d'observations",
            "missing_cells": "Cellules manquantes",
            "missing_cells_percentage": "Cellules manquantes (%)",
            "duplicate_rows": "Lignes dupliquées",
            "duplicate_rows_percentage": "Lignes dupliquées (%)",
            "average_record_size": "Taille moyenne d'un enregistrement en mémoire"
        },
        "variables": {
            "numeric": "Numérique",
            "categorical": "Catégorique",
            "boolean": "Booléen",
            "date": "Date",
            "text": "Texte",
            "url": "URL",
            "path": "Chemin",
            "image": "Image",
            "distinct": "Distinct",
            "distinct_percentage": "Distinct (%)",
            "missing": "Manquant",
            "missing_percentage": "Manquant (%)",
            "statistics": "Statistiques",
            "quantile_statistics": "Statistiques de quantiles",
            "common_values": "Valeurs courantes",
            "histogram": "Histogramme",
            "mode": "Mode",
            "standard_deviation": "Écart-type",
            "sum": "Somme",
            "mad": "Déviation absolue médiane (DAM)",
            "coefficient_of_variation": "Coefficient de variation (CV)",
            "kurtosis": "Kurtosis",
            "skewness": "Asymétrie",
            "range": "Étendue",
            "interquartile_range": "Écart interquartile (IQR)",
            "length": "Longueur",
            "sample": "Échantillon"
        },
        "correlations": {
            "pearson": "Corrélation de Pearson (r)",
            "spearman": "Corrélation de Spearman (ρ)",
            "kendall": "Corrélation de Kendall (τ)",
            "phi_k": "Phik (φk)",
            "cramers": "V de Cramér (φc)",
            "auto": "Automatique"
        },
        "interactions": {
            "scatter_plot": "Nuage de points",
            "variable": "Variable"
        },
        "missing_values": {
            "matrix": "Matrice",
            "bar_chart": "Graphique à barres",
            "heatmap": "Carte thermique",
            "dendrogram": "Dendrogramme"
        },
        "alerts": {
            "high_correlation": "Corrélation élevée",
            "high_cardinality": "Cardinalité élevée",
            "constant": "Constante",
            "zeros": "Zéros",
            "missing": "Manquant",
            "skewed": "Asymétrique",
            "type_date": "Date",
            "uniform": "Uniforme",
            "unique": "Unique",
            "constant_length": "Longueur constante",
            "duplicates": "Duplicatas",
            "empty": "Vide",
            "imbalance": "Déséquilibre",
            "near_duplicates": "Quasi-duplicatas",
            "non_stationary": "Non stationnaire",
            "seasonal": "Saisonnier",
            "truncated": "Tronqué",
            "unsupported": "Non supporté",
            "dirty_category": "Catégorie non propre"
        },
        "formatting": {
            "bytes": "{value} octets",
            "kb": "{value} Ko",
            "mb": "{value} Mo",
            "gb": "{value} Go",
            "percentage": "{value} %"
        },
        "rendering": {
            "generate_structure": "Générer la structure du rapport",
            "html_progress": "Rendu HTML",
            "json_progress": "Rendu JSON",
            "widgets_progress": "Rendu des widgets",
            "other_values_count": "Autres valeurs ({other_count})",
            "missing": "(Manquant)"
        },
        "core": {
            "unknown": "inconnu",
            "alerts": "Alertes",
            "collapse": "Réduire",
            "container": "Conteneur",
            "correlationTable": "Tableau de corrélation",
            "dropdown": "Menu déroulant",
            "duplicate": "Duplicata",
            "frequencyTable": "Tableau de fréquence",
            "frequencyTableSmall": "Tableau de fréquence réduit",
            "html": "HTML",
            "image": "Image",
            "sample": "Échantillon",
            "scores": "Scores",
            "table": "Tableau",
            "toggle_button": "Bouton de bascule",
            "variable": "Variable",
            "variable_info": "Informations sur la variable",
            "model": {
                "bar_count": "Compte",
                "bar_caption": "Une visualisation simple des valeurs nulles par colonne.",
                "matrix": "Matrice",
                "matrix_caption": "La matrice de nullité est une représentation dense des données qui permet de repérer rapidement visuellement les modèles de complétude des données.",
                "heatmap": "Carte thermique",
                "heatmap_caption": "La carte thermique de corrélation mesure la corrélation de nullité : à quel point la présence ou l'absence d'une variable affecte la présence d'une autre.",
                "first_rows": "Premières lignes",
                "last_rows": "Dernières lignes",
                "random_sample": "Échantillon aléatoire"
            },
            "structure": {
                "correlations": "Corrélations",
                "heatmap": "Carte thermique",
                "table": "Tableau",
                "overview": {
                    "values": "valeurs",
                    "number_variables": "Nombre de variables",
                    "number_observations": "Nombre d'observations",
                    "missing_cells": "Cellules manquantes",
                    "missing_cells_percentage": "Cellules manquantes (%)",
                    "duplicate_rows": "Lignes dupliquées",
                    "duplicate_rows_percentage": "Lignes dupliquées (%)",
                    "total_size_memory": "Taille totale en mémoire",
                    "average_record_memory": "Taille moyenne d'un enregistrement en mémoire",
                    "dataset_statistics": "Statistiques de l'ensemble de données",
                    "variable_types": "Types de variables",
                    "overview": "Aperçu",
                    "url": "URL",
                    "copyright": "Droits d'auteur",
                    "dataset": "Ensemble de données",
                    "analysis_started": "Analyse commencée",
                    "analysis_finished": "Analyse terminée",
                    "duration": "Durée",
                    "software_version": "Version du logiciel",
                    "download_configuration": "Télécharger la configuration",
                    "reproduction": "Reproduction",
                    "variable_descriptions": "Descriptions des variables",
                    "variables": "Variables",
                    "alerts_count": "Alertes ({count})",
                    "number_of_series": "Nombre de séries",
                    "timeseries_length": "Longueur de la série temporelle",
                    "starting_point": "Point de départ",
                    "ending_point": "Point de fin",
                    "period": "Période",
                    "timeseries_statistics": "Statistiques des séries temporelles",
                    "original": "Original",
                    "scaled": "Échelonné",
                    "time_series": "Séries temporelles",
                    "interactions": "Interactions",
                    "distinct": "Distinct",
                    "distinct_percentage": "Distinct (%)",
                    "missing": "Manquant",
                    "missing_percentage": "Manquant (%)",
                    "memory_size": "Taille en mémoire",
                    "file": "Fichier",
                    "size": "Taille",
                    "file_size": "Taille du fichier",
                    "file_size_caption": "Histogramme avec des intervalles fixes de tailles de fichiers (en octets)",
                    "unique": "Unique",
                    "unique_help": "Le nombre de valeurs uniques (toutes les valeurs qui n'apparaissent qu'une seule fois dans l'ensemble de données).",
                    "unique_percentage": "Unique (%)",
                    "max_length": "Longueur maximale",
                    "median_length": "Longueur médiane",
                    "mean_length": "Longueur moyenne",
                    "min_length": "Longueur minimale",
                    "length": "Longueur",
                    "length_histogram": "Histogramme de longueur",
                    "histogram_lengths_category": "Histogramme des longueurs de la catégorie",
                    "most_occurring_categories": "Catégories les plus fréquentes",
                    "most_frequent_character_per_category": "Caractère le plus fréquent par catégorie",
                    "most_occurring_scripts": "Scripts les plus fréquents",
                    "most_frequent_character_per_script": "Caractère le plus fréquent par script",
                    "most_occurring_blocks": "Blocs les plus fréquents",
                    "most_frequent_character_per_block": "Caractère le plus fréquent par bloc",
                    "total_characters": "Nombre total de caractères",
                    "distinct_characters": "Caractères distincts",
                    "distinct_categories": "Catégories distinctes",
                    "unicode_categories": "Catégories Unicode (cliquez pour plus d'informations)",
                    "distinct_scripts": "Scripts distincts",
                    "unicode_scripts": "Scripts Unicode (cliquez pour plus d'informations)",
                    "distinct_blocks": "Blocs distincts",
                    "unicode_blocks": "Blocs Unicode (cliquez pour plus d'informations)",
                    "characters_unicode": "Caractères et Unicode",
                    "characters_unicode_caption": "La norme Unicode attribue des propriétés à chaque point de code, qui peuvent être utilisées pour analyser des variables textuelles.",
                    "most_occurring_characters": "Caractères les plus fréquents",
                    "characters": "Caractères",
                    "categories": "Catégories",
                    "scripts": "Scripts",
                    "blocks": "Blocs",
                    "unicode": "Unicode",
                    "common_values": "Valeurs courantes",
                    "common_values_table": "Valeurs courantes (Tableau)",
                    "1st_row": "1ère ligne",
                    "2nd_row": "2ème ligne",
                    "3rd_row": "3ème ligne",
                    "4th_row": "4ème ligne",
                    "5th_row": "5ème ligne",
                    "categories_passes_threshold": "Nombre de catégories de variables dépassant le seuil (<code>config.plot.cat_freq.max_unique</code>)",
                    "common_values_plot": "Valeurs courantes (Graphique)",
                    "common_words": "Mots courants",
                    "wordcloud": "Nuage de mots",
                    "words": "Mots",
                    "mean": "Moyenne",
                    "min": "Minimum",
                    "max": "Maximum",
                    "zeros": "Zéros",
                    "zeros_percentage": "Zéros (%)",
                    "scatter": "Nuage",
                    "scatterplot": "Nuage de points",
                    "scatterplot_caption": "Nuage de points dans le plan complexe",
                    "mini_histogram": "Mini-histogramme",
                    "histogram": "Histogramme",
                    "histogram_caption": "Histogramme avec des intervalles fixes",
                    "extreme_values": "Valeurs extrêmes",
                    "histogram_s": "Histogramme(s)",
                    "invalid_dates": "Dates invalides",
                    "invalid_dates_percentage": "Dates invalides (%)",
                    "created": "Créé",
                    "accessed": "Accédé",
                    "modified": "Modifié",
                    "min_width": "Largeur minimale",
                    "median_width": "Largeur médiane",
                    "max_width": "Largeur maximale",
                    "min_height": "Hauteur minimale",
                    "median_height": "Hauteur médiane",
                    "max_height": "Hauteur maximale",
                    "min_area": "Surface minimale",
                    "median_area": "Surface médiane",
                    "max_area": "Surface maximale",
                    "scatter_plot_image_sizes": "Nuage de points des tailles d'image",
                    "scatter_plot": "Nuage de points",
                    "dimensions": "Dimensions",
                    "exif_keys": "Clés EXIF",
                    "exif_data": "Données EXIF",
                    "image": "Image",
                    "common_prefix": "Préfixe commun",
                    "unique_stems": "Racines uniques",
                    "unique_names": "Noms uniques",
                    "unique_extensions": "Extensions uniques",
                    "unique_directories": "Répertoires uniques",
                    "unique_anchors": "Ancres uniques",
                    "full": "Complet",
                    "stem": "Racine",
                    "name": "Nom",
                    "extension": "Extension",
                    "parent": "Parent",
                    "anchor": "Ancre",
                    "path": "Chemin",
                    "infinite": "Infini",
                    "infinite_percentage": "Infini (%)",
                    "Negative": "Négatif",
                    "Negative_percentage": "Négatif (%)",
                    "5_th_percentile": "5e centile",
                    "q1": "Q1",
                    "median": "Médiane",
                    "q3": "Q3",
                    "95_th_percentile": "95e centile",
                    "range": "Étendue",
                    "iqr": "Écart interquartile (IQR)",
                    "quantile_statistics": "Statistiques de quantiles",
                    "standard_deviation": "Écart-type",
                    "cv": "Coefficient de variation (CV)",
                    "kurtosis": "Kurtosis",
                    "mad": "Déviation absolue médiane (DAM)",
                    "skewness": "Asymétrie",
                    "sum": "Somme",
                    "variance": "Variance",
                    "monotonicity": "Monotonie",
                    "descriptive_statistics": "Statistiques descriptives",
                    "statistics": "Statistiques",
                    "augmented_dickey_fuller_test_value": "Valeur p du test de Dickey-Fuller augmenté",
                    "autocorrelation": "Autocorrélation",
                    "autocorrelation_caption": "ACF et PACF",
                    "timeseries": "Série temporelle",
                    "timeseries_plot": "Graphique de série temporelle",
                    "scheme": "Schéma",
                    "netloc": "Emplacement réseau",
                    "query": "Requête",
                    "fragment": "Fragment",
                    "heatmap": "Carte thermique"
                }
            }
        },
        "html": {
            "alerts": {
                "title": "Alertes",
                "not_present": "Aucune alerte présente dans cet ensemble de données",
                "has_constant_value": "a une valeur constante",
                "has_constant_length": "a une longueur constante",
                "has_dirty_categories": "a des catégories non propres",
                "has_high_cardinality": "a une cardinalité élevée",
                "distinct_values": "valeurs distinctes",
                "dataset_has": "L'ensemble de données a",
                "duplicate_rows": "lignes dupliquées",
                "dataset_is_empty": "L'ensemble de données est vide",
                "is_highly": "est fortement",
                "correlated_with": "corrélé avec",
                "and": "et",
                "other_fields": "autres champs",
                "highly_imbalanced": "est fortement déséquilibré",
                "has": "a",
                "infinite_values": "valeurs infinies",
                "missing_values": "valeurs manquantes",
                "near_duplicate_rows": "lignes quasi-dupliquées",
                "non_stationary": "est non stationnaire",
                "seasonal": "est saisonnier",
                "highly_skewed": "est fortement asymétrique",
                "truncated_files": "fichiers tronqués",
                "alert_type_date": "contient uniquement des valeurs datetime, mais est catégorique. Envisagez d'appliquer",
                "uniformly_distributed": "est uniformément distribué",
                "unique_values": "a des valeurs uniques",
                "alert_unsupported": "est un type non supporté, vérifiez s'il nécessite un nettoyage ou une analyse supplémentaire",
                "zeros": "zéros"
            },
            "sequence": {
                "overview_tabs": {
                    "brought_to_you_by": "Présenté par <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=ydataprofiling&utm_campaign=report\">YData</a>"
                }
            },
            "dropdown": "Sélectionner les colonnes",
            "frequency_table": {
                "value": "Valeur",
                "count": "Compte",
                "frequency_percentage": "Fréquence (%)",
                "redacted_value": "Valeur masquée",
                "no_values_found": "Aucune valeur trouvée"
            },
            "scores": {
                "overall_data_quality": "Score global de la qualité des données"
            },
            "variable_info": {
                "no_alerts": "Aucune alerte"
            }
        }
    }

    # 创建西班牙语翻译
    spanish_translation = {
        "report": {
            "title": "Informe de Perfilado de YData",
            "overview": "Resumen",
            "variables": "Variables",
            "interactions": "Interacciones",
            "correlations": "Correlaciones",
            "missing_values": "Valores faltantes",
            "sample": "Muestra",
            "duplicates": "Filas duplicadas",
            "footer_text": "Informe generado por <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=pandasprofiling&utm_campaign=report\">YData</a>.",
            "most_frequently_occurring": "Los más frecuentes",
            "columns": "Columnas",
            "more_details": "Más detalles"
          },
        "overview": {
            "dataset_info": "Información del conjunto de datos",
            "variable_types": "Tipos de variables",
            "dataset_statistics": "Estadísticas del conjunto de datos",
            "number_of_variables": "Número de variables",
            "number_of_observations": "Número de observaciones",
            "missing_cells": "Celdas faltantes",
            "missing_cells_percentage": "Celdas faltantes (%)",
            "duplicate_rows": "Filas duplicadas",
            "duplicate_rows_percentage": "Filas duplicadas (%)",
            "average_record_size": "Tamaño promedio de registro en memoria"
          },
        "variables": {
            "numeric": "Numérico",
            "categorical": "Categórico",
            "boolean": "Booleano",
            "date": "Fecha",
            "text": "Texto",
            "url": "URL",
            "path": "Ruta",
            "image": "Imagen",
            "distinct": "Distinto",
            "distinct_percentage": "Distinto (%)",
            "missing": "Faltante",
            "missing_percentage": "Faltante (%)",
            "statistics": "Estadísticas",
            "quantile_statistics": "Estadísticas de cuantiles",
            "common_values": "Valores comunes",
            "histogram": "Histograma",
            "mode": "Moda",
            "standard_deviation": "Desviación estándar",
            "sum": "Suma",
            "mad": "Desviación absoluta mediana (DAM)",
            "coefficient_of_variation": "Coeficiente de variación (CV)",
            "kurtosis": "Curtosis",
            "skewness": "Asimetría",
            "range": "Rango",
            "interquartile_range": "Rango intercuartílico (IQR)",
            "length": "Longitud",
            "sample": "Muestra"
          },
        "correlations": {
            "pearson": "Correlación de Pearson (r)",
            "spearman": "Correlación de Spearman (ρ)",
            "kendall": "Correlación de Kendall (τ)",
            "phi_k": "Phik (φk)",
            "cramers": "V de Cramér (φc)",
            "auto": "Automático"
          },
        "interactions": {
            "scatter_plot": "Gráfico de dispersión",
            "variable": "Variable"
          },
        "missing_values": {
            "matrix": "Matriz",
            "bar_chart": "Gráfico de barras",
            "heatmap": "Mapa de calor",
            "dendrogram": "Dendrograma"
          },
        "alerts": {
            "high_correlation": "Correlación alta",
            "high_cardinality": "Alta cardinalidad",
            "constant": "Constante",
            "zeros": "Ceros",
            "missing": "Faltante",
            "skewed": "Asimétrico",
            "type_date": "Fecha",
            "uniform": "Uniforme",
            "unique": "Único",
            "constant_length": "Longitud constante",
            "duplicates": "Duplicados",
            "empty": "Vacío",
            "imbalance": "Desequilibrio",
            "near_duplicates": "Casi duplicados",
            "non_stationary": "No estacionario",
            "seasonal": "Estacional",
            "truncated": "Truncado",
            "unsupported": "No soportado",
            "dirty_category": "Categoría sucia"
          },
        "formatting": {
            "bytes": "{value} bytes",
            "kb": "{value} KB",
            "mb": "{value} MB",
            "gb": "{value} GB",
            "percentage": "{value}%"
          },
        "rendering": {
            "generate_structure": "Generar estructura del informe",
            "html_progress": "Renderizar HTML",
            "json_progress": "Renderizar JSON",
            "widgets_progress": "Renderizar widgets",
            "other_values_count": "Otros valores ({other_count})",
            "missing": "(Faltante)"
          },
        "core": {
            "unknown": "desconocido",
            "alerts": "Alertas",
            "collapse": "Colapsar",
            "container": "Contenedor",
            "correlationTable": "Tabla de correlación",
            "dropdown": "Menú desplegable",
            "duplicate": "Duplicado",
            "frequencyTable": "Tabla de frecuencia",
            "frequencyTableSmall": "Tabla de frecuencia pequeña",
            "html": "HTML",
            "image": "Imagen",
            "sample": "Muestra",
            "scores": "Puntuaciones",
            "table": "Tabla",
            "toggle_button": "Botón de alternancia",
            "variable": "Variable",
            "variable_info": "Información de la variable",
            "model": {
                "bar_count": "Conteo",
                "bar_caption": "Una visualización simple de la nulidad por columna.",
                "matrix": "Matriz",
                "matrix_caption": "La matriz de nulidad es una representación densa de datos que permite identificar rápidamente patrones visuales en la completitud de los datos.",
                "heatmap": "Mapa de calor",
                "heatmap_caption": "El mapa de calor de correlación mide la correlación de nulidad: cómo la presencia o ausencia de una variable afecta la presencia de otra.",
                "first_rows": "Primeras filas",
                "last_rows": "Últimas filas",
                "random_sample": "Muestra aleatoria"
            },
            "structure": {
                "correlations": "Correlaciones",
                "heatmap": "Mapa de calor",
                "table": "Tabla",
                "overview": {
                    "values": "valores",
                    "number_variables": "Número de variables",
                    "number_observations": "Número de observaciones",
                    "missing_cells": "Celdas faltantes",
                    "missing_cells_percentage": "Celdas faltantes (%)",
                    "duplicate_rows": "Filas duplicadas",
                    "duplicate_rows_percentage": "Filas duplicadas (%)",
                    "total_size_memory": "Tamaño total en memoria",
                    "average_record_memory": "Tamaño promedio de registro en memoria",
                    "dataset_statistics": "Estadísticas del conjunto de datos",
                    "variable_types": "Tipos de variables",
                    "overview": "Resumen",
                    "url": "URL",
                    "copyright": "Derechos de autor",
                    "dataset": "Conjunto de datos",
                    "analysis_started": "Análisis iniciado",
                    "analysis_finished": "Análisis finalizado",
                    "duration": "Duración",
                    "software_version": "Versión del software",
                    "download_configuration": "Descargar configuración",
                    "reproduction": "Reproducción",
                    "variable_descriptions": "Descripciones de variables",
                    "variables": "Variables",
                    "alerts_count": "Alertas ({count})",
                    "number_of_series": "Número de series",
                    "timeseries_length": "Longitud de la serie temporal",
                    "starting_point": "Punto de inicio",
                    "ending_point": "Punto final",
                    "period": "Período",
                    "timeseries_statistics": "Estadísticas de series temporales",
                    "original": "Original",
                    "scaled": "Escalado",
                    "time_series": "Series temporales",
                    "interactions": "Interacciones",
                    "distinct": "Distinto",
                    "distinct_percentage": "Distinto (%)",
                    "missing": "Faltante",
                    "missing_percentage": "Faltante (%)",
                    "memory_size": "Tamaño en memoria",
                    "file": "Archivo",
                    "size": "Tamaño",
                    "file_size": "Tamaño del archivo",
                    "file_size_caption": "Histograma con intervalos fijos de tamaños de archivo (en bytes)",
                    "unique": "Único",
                    "unique_help": "El número de valores únicos (todos los valores que aparecen exactamente una vez en el conjunto de datos).",
                    "unique_percentage": "Único (%)",
                    "max_length": "Longitud máxima",
                    "median_length": "Longitud mediana",
                    "mean_length": "Longitud media",
                    "min_length": "Longitud mínima",
                    "length": "Longitud",
                    "length_histogram": "Histograma de longitud",
                    "histogram_lengths_category": "Histograma de longitudes de la categoría",
                    "most_occurring_categories": "Categorías más frecuentes",
                    "most_frequent_character_per_category": "Carácter más frecuente por categoría",
                    "most_occurring_scripts": "Scripts más frecuentes",
                    "most_frequent_character_per_script": "Carácter más frecuente por script",
                    "most_occurring_blocks": "Bloques más frecuentes",
                    "most_frequent_character_per_block": "Carácter más frecuente por bloque",
                    "total_characters": "Total de caracteres",
                    "distinct_characters": "Caracteres distintos",
                    "distinct_categories": "Categorías distintas",
                    "unicode_categories": "Categorías Unicode (haga clic para más información)",
                    "distinct_scripts": "Scripts distintos",
                    "unicode_scripts": "Scripts Unicode (haga clic para más información)",
                    "distinct_blocks": "Bloques distintos",
                    "unicode_blocks": "Bloques Unicode (haga clic para más información)",
                    "characters_unicode": "Caracteres y Unicode",
                    "characters_unicode_caption": "El estándar Unicode asigna propiedades a cada punto de código, que pueden usarse para analizar variables textuales.",
                    "most_occurring_characters": "Caracteres más frecuentes",
                    "characters": "Caracteres",
                    "categories": "Categorías",
                    "scripts": "Scripts",
                    "blocks": "Bloques",
                    "unicode": "Unicode",
                    "common_values": "Valores comunes",
                    "common_values_table": "Valores comunes (Tabla)",
                    "1st_row": "1ª fila",
                    "2nd_row": "2ª fila",
                    "3rd_row": "3ª fila",
                    "4th_row": "4ª fila",
                    "5th_row": "5ª fila",
                    "categories_passes_threshold": "Número de categorías de variables que superan el umbral (<code>config.plot.cat_freq.max_unique</code>)",
                    "common_values_plot": "Valores comunes (Gráfico)",
                    "common_words": "Palabras comunes",
                    "wordcloud": "Nube de palabras",
                    "words": "Palabras",
                    "mean": "Media",
                    "min": "Mínimo",
                    "max": "Máximo",
                    "zeros": "Ceros",
                    "zeros_percentage": "Ceros (%)",
                    "scatter": "Dispersión",
                    "scatterplot": "Gráfico de dispersión",
                    "scatterplot_caption": "Gráfico de dispersión en el plano complejo",
                    "mini_histogram": "Mini-histograma",
                    "histogram": "Histograma",
                    "histogram_caption": "Histograma con intervalos fijos",
                    "extreme_values": "Valores extremos",
                    "histogram_s": "Histograma(s)",
                    "invalid_dates": "Fechas inválidas",
                    "invalid_dates_percentage": "Fechas inválidas (%)",
                    "created": "Creado",
                    "accessed": "Accedido",
                    "modified": "Modificado",
                    "min_width": "Ancho mínimo",
                    "median_width": "Ancho mediano",
                    "max_width": "Ancho máximo",
                    "min_height": "Altura mínima",
                    "median_height": "Altura mediana",
                    "max_height": "Altura máxima",
                    "min_area": "Área mínima",
                    "median_area": "Área mediana",
                    "max_area": "Área máxima",
                    "scatter_plot_image_sizes": "Gráfico de dispersión de tamaños de imagen",
                    "scatter_plot": "Gráfico de dispersión",
                    "dimensions": "Dimensiones",
                    "exif_keys": "Claves EXIF",
                    "exif_data": "Datos EXIF",
                    "image": "Imagen",
                    "common_prefix": "Prefijo común",
                    "unique_stems": "Raíces únicas",
                    "unique_names": "Nombres únicos",
                    "unique_extensions": "Extensiones únicas",
                    "unique_directories": "Directorios únicos",
                    "unique_anchors": "Anclas únicas",
                    "full": "Completo",
                    "stem": "Raíz",
                    "name": "Nombre",
                    "extension": "Extensión",
                    "parent": "Padre",
                    "anchor": "Ancla",
                    "path": "Ruta",
                    "infinite": "Infinito",
                    "infinite_percentage": "Infinito (%)",
                    "Negative": "Negativo",
                    "Negative_percentage": "Negativo (%)",
                    "5_th_percentile": "Percentil 5",
                    "q1": "Q1",
                    "median": "Mediana",
                    "q3": "Q3",
                    "95_th_percentile": "Percentil 95",
                    "range": "Rango",
                    "iqr": "Rango intercuartílico (IQR)",
                    "quantile_statistics": "Estadísticas de cuantiles",
                    "standard_deviation": "Desviación estándar",
                    "cv": "Coeficiente de variación (CV)",
                    "kurtosis": "Curtosis",
                    "mad": "Desviación absoluta mediana (DAM)",
                    "skewness": "Asimetría",
                    "sum": "Suma",
                    "variance": "Varianza",
                    "monotonicity": "Monotonía",
                    "descriptive_statistics": "Estadísticas descriptivas",
                    "statistics": "Estadísticas",
                    "augmented_dickey_fuller_test_value": "Valor p del test de Dickey-Fuller aumentado",
                    "autocorrelation": "Autocorrelación",
                    "autocorrelation_caption": "ACF y PACF",
                    "timeseries": "Serie temporal",
                    "timeseries_plot": "Gráfico de serie temporal",
                    "scheme": "Esquema",
                    "netloc": "Ubicación de red",
                    "query": "Consulta",
                    "fragment": "Fragmento",
                    "heatmap": "Mapa de calor"
                }
            }
        },
        "html": {
            "alerts": {
                "title": "Alertas",
                "not_present": "No hay alertas presentes en este conjunto de datos",
                "has_constant_value": "tiene un valor constante",
                "has_constant_length": "tiene una longitud constante",
                "has_dirty_categories": "tiene categorías sucias",
                "has_high_cardinality": "tiene una alta cardinalidad",
                "distinct_values": "valores distintos",
                "dataset_has": "El conjunto de datos tiene",
                "duplicate_rows": "filas duplicadas",
                "dataset_is_empty": "El conjunto de datos está vacío",
                "is_highly": "está altamente",
                "correlated_with": "correlacionado con",
                "and": "y",
                "other_fields": "otros campos",
                "highly_imbalanced": "está altamente desequilibrado",
                "has": "tiene",
                "infinite_values": "valores infinitos",
                "missing_values": "valores faltantes",
                "near_duplicate_rows": "filas casi duplicadas",
                "non_stationary": "es no estacionario",
                "seasonal": "es estacional",
                "highly_skewed": "es altamente asimétrico",
                "truncated_files": "archivos truncados",
                "alert_type_date": "solo contiene valores de fecha y hora, pero es categórico. Considere aplicar",
                "uniformly_distributed": "está uniformemente distribuido",
                "unique_values": "tiene valores únicos",
                "alert_unsupported": "es un tipo no soportado, verifique si necesita limpieza o análisis adicional",
                "zeros": "ceros"
            },
            "sequence": {
                "overview_tabs": {
                    "brought_to_you_by": "Presentado por <a href=\"https://ydata.ai/?utm_source=opensource&utm_medium=ydataprofiling&utm_campaign=report\">YData</a>"
                }
            },
            "dropdown": "Seleccionar columnas",
            "frequency_table": {
                "value": "Valor",
                "count": "Conteo",
                "frequency_percentage": "Frecuencia (%)",
                "redacted_value": "Valor redactado",
                "no_values_found": "No se encontraron valores"
            },
            "scores": {
                "overall_data_quality": "Puntuación general de calidad de datos"
            },
            "variable_info": {
                "no_alerts": "Sin alertas"
            }
        }
    }

    # 保存翻译文件
    french_file = "french_translation.json"
    spanish_file = "spanish_translation.json"

    with open(french_file, 'w', encoding='utf-8') as f:
        json.dump(french_translation, f, indent=2, ensure_ascii=False)

    with open(spanish_file, 'w', encoding='utf-8') as f:
        json.dump(spanish_translation, f, indent=2, ensure_ascii=False)

    print(f"✅ French translation saved to: {french_file}")
    print(f"✅ Spanish translation saved to: {spanish_file}")

    return french_file, spanish_file


def step3_single_file_loading(df, french_file):
    """步骤3: 单个翻译文件加载示例"""
    print(f"\n📁 Step 3: Loading single translation file - {french_file}")

    # 加载法语翻译
    load_translation_file(french_file, 'fr')

    print(f"📋 Available locales after loading: {get_available_locales()}")

    # 设置为法语并生成报告
    set_locale('fr')
    print(f"🌍 Current locale set to: {get_locale()}")

    profile = ProfileReport(df, title="Rapport d'Analyse des Produits")
    output_file = "product_analysis_french.html"

    # 强制覆盖生成报告
    try:
        profile.to_file(output_file)
        print(f"✅ French report generated: {output_file}")
    except Exception as e:
        print(f"⚠️ Warning generating French report: {e}")
        # 如果报告生成失败，删除已存在的文件再重试
        if Path(output_file).exists():
            Path(output_file).unlink()
        profile.to_file(output_file)
        print(f"✅ French report generated (after cleanup): {output_file}")

    return output_file


def step4_directory_loading(df, french_file, spanish_file):
    """步骤4: 翻译目录加载示例"""
    print(f"\n📂 Step 4: Loading translation directory")

    # 创建翻译目录
    translations_dir = Path("custom_translations")
    translations_dir.mkdir(exist_ok=True)

    # 移动翻译文件到目录
    french_target = translations_dir / "fr.json"
    spanish_target = translations_dir / "es.json"

    # 复制文件而不是移动，避免文件已存在的错误
    try:
        shutil.copy2(french_file, french_target)
        print(f"📄 Copied {french_file} to {french_target}")
    except Exception as e:
        print(f"⚠️ Warning copying French file: {e}")
        # 如果复制失败，直接覆盖
        shutil.copyfile(french_file, french_target)

    try:
        shutil.copy2(spanish_file, spanish_target)
        print(f"📄 Copied {spanish_file} to {spanish_target}")
    except Exception as e:
        print(f"⚠️ Warning copying Spanish file: {e}")
        # 如果复制失败，直接覆盖
        shutil.copyfile(spanish_file, spanish_target)

    print(f"📁 Created translation directory: {translations_dir}")
    print(f"📄 Files in directory: {list(translations_dir.glob('*.json'))}")

    # 加载整个翻译目录
    add_translation_directory(translations_dir)

    print(f"📋 Available locales after directory loading: {get_available_locales()}")

    # 生成西班牙语报告
    set_locale('es')
    print(f"🌍 Current locale set to: {get_locale()}")

    profile = ProfileReport(df, title="Informe de Análisis de Productos")
    output_file = "product_analysis_spanish.html"

    # 强制覆盖生成报告
    try:
        profile.to_file(output_file)
        print(f"✅ Spanish report generated: {output_file}")
    except Exception as e:
        print(f"⚠️ Warning generating Spanish report: {e}")
        # 如果报告生成失败，删除已存在的文件再重试
        if Path(output_file).exists():
            Path(output_file).unlink()
        profile.to_file(output_file)
        print(f"✅ Spanish report generated (after cleanup): {output_file}")

    return output_file, translations_dir


def step5_using_locale_parameter(df):
    """步骤5: 使用ProfileReport的locale参数"""
    print(f"\n⚙️ Step 5: Using ProfileReport locale parameter")

    # 直接在ProfileReport中指定语言
    print("🔄 Generating report with locale='zh' parameter...")
    profile_zh = ProfileReport(df, title="产品分析报告", locale='zh')
    output_file = "product_analysis_chinese.html"

    # 强制覆盖生成报告
    try:
        profile_zh.to_file(output_file)
        print(f"✅ Chinese report generated: {output_file}")
    except Exception as e:
        print(f"⚠️ Warning generating Chinese report: {e}")
        # 如果报告生成失败，删除已存在的文件再重试
        if Path(output_file).exists():
            Path(output_file).unlink()
        profile_zh.to_file(output_file)
        print(f"✅ Chinese report generated (after cleanup): {output_file}")

    print(f"🌍 Current global locale remains: {get_locale()}")

    return output_file


def cleanup_files(files_to_clean):
    """清理生成的文件"""
    print(f"\n🧹 Cleaning up generated files...")

    for file_path in files_to_clean:
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)

            if file_path.exists():
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                print(f"🗑️ Removed: {file_path}")
        except Exception as e:
            print(f"⚠️ Could not remove {file_path}: {e}")


def safe_file_operation(operation_func, *args, **kwargs):
    """安全执行文件操作，包含重试逻辑"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}. Retrying...")
                import time
                time.sleep(0.5)  # 短暂等待
            else:
                print(f"❌ All attempts failed: {e}")
                raise


def main():
    """主函数 - 演示完整的翻译工作流程"""
    print("🚀 YData Profiling Custom Translation Workflow Example")
    print("=" * 60)

    # 记录要清理的文件
    files_to_clean = []

    try:
        # 创建示例数据
        df = create_sample_data()

        # 步骤1: 导出模板
        template_file = step1_export_template()
        files_to_clean.append(template_file)

        # 步骤2: 创建自定义翻译
        french_file, spanish_file = step2_create_custom_translations(template_file)
        files_to_clean.extend([french_file, spanish_file])

        # 步骤3: 单文件加载
        french_report = safe_file_operation(step3_single_file_loading, df, french_file)
        files_to_clean.append(french_report)

        # 步骤4: 目录加载
        spanish_report, translations_dir = safe_file_operation(step4_directory_loading, df, french_file, spanish_file)
        files_to_clean.extend([spanish_report, translations_dir])

        # 步骤5: 使用locale参数
        chinese_report = safe_file_operation(step5_using_locale_parameter, df)
        files_to_clean.append(chinese_report)

        print(f"\n🎉 All steps completed successfully!")
        print(f"📊 Generated reports:")
        print(f"   - {french_report} (French)")
        print(f"   - {spanish_report} (Spanish)")
        print(f"   - {chinese_report} (Chinese)")
        print(f"\n💡 You can open these HTML files in your browser to see the translated reports.")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # 询问是否清理文件
        try:
            response = input(f"\n🤔 Do you want to clean up generated files? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                cleanup_files(files_to_clean)
            else:
                print("📁 Files kept for your review.")
                print("💡 Tip: You can run this script multiple times to see the overwrites working.")
        except KeyboardInterrupt:
            print(f"\n📁 Files kept for your review.")


if __name__ == "__main__":
    main()