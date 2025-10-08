"""
Internationalization module for ydata-profiling
"""
import os
import json
from pathlib import Path
from typing import Dict, Optional, List, Union
import threading

class TranslationManager:
    """Manages translations for ydata-profiling with support for external translation files"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.translations: Dict[str, Dict[str, str]] = {}
            self.current_locale = 'en'
            self.fallback_locale = 'en'
            self.external_translation_dirs: List[Path] = []
            self.initialized = True
            self._load_translations()

    def add_translation_directory(self, directory: Union[str, Path]):
        """Add external translation directory

        Args:
            directory: Path to directory containing translation JSON files
        """
        dir_path = Path(directory)
        if dir_path.exists() and dir_path.is_dir():
            if dir_path not in self.external_translation_dirs:
                self.external_translation_dirs.append(dir_path)
                self._load_external_translations(dir_path)
        else:
            print(f"Warning: Translation directory {directory} does not exist")

    def load_translation_file(self, file_path: Union[str, Path], locale: Optional[str] = None):
        """Load a specific translation file

        Args:
            file_path: Path to the translation JSON file
            locale: Locale code. If None, will be inferred from filename
        """
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: Translation file {file_path} does not exist")
            return

        if locale is None:
            locale = file_path.stem

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                external_translations = json.load(f)

            # Merge with existing translations
            if locale in self.translations:
                self.translations[locale] = self._merge_translations(
                    self.translations[locale],
                    external_translations
                )
            else:
                self.translations[locale] = external_translations

            print(f"Successfully loaded translation file for locale '{locale}' from {file_path}")
        except Exception as e:
            print(f"Warning: Failed to load translation file {file_path}: {e}")

    def _merge_translations(self, base: dict, override: dict) -> dict:
        """Recursively merge translation dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_translations(result[key], value)
            else:
                result[key] = value
        return result

    def _load_translations(self):
        """Load built-in translation files"""
        translations_dir = Path(__file__).parent / 'locales'
        if translations_dir.exists():
            self._load_translations_from_directory(translations_dir)

    def _load_external_translations(self, directory: Path):
        """Load translations from external directory"""
        self._load_translations_from_directory(directory)

    def _load_translations_from_directory(self, directory: Path):
        """Load all translation files from a directory"""
        for locale_file in directory.glob('*.json'):
            locale = locale_file.stem
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)

                if locale in self.translations:
                    # Merge with existing translations
                    self.translations[locale] = self._merge_translations(
                        self.translations[locale],
                        translations
                    )
                else:
                    self.translations[locale] = translations

            except Exception as e:
                print(f"Warning: Failed to load translation file {locale_file}: {e}")

    def get_available_locales(self) -> List[str]:
        """Get list of available locales"""
        return list(self.translations.keys())

    def set_locale(self, locale: str):
        """Set the current locale"""
        if locale in self.translations or locale == self.fallback_locale:
            self.current_locale = locale
        else:
            print(f"Warning: Locale '{locale}' not found, using fallback '{self.fallback_locale}'")
            print(f"Available locales: {self.get_available_locales()}")

    def get_translation(self, key: str, locale: Optional[str] = None, **kwargs) -> str:
        """Get translation for a key"""
        target_locale = locale or self.current_locale

        # Try current locale
        if target_locale in self.translations:
            translation = self._get_nested_value(self.translations[target_locale], key)
            if translation:
                return self._format_translation(translation, **kwargs)

        # Try fallback locale
        if target_locale != self.fallback_locale and self.fallback_locale in self.translations:
            translation = self._get_nested_value(self.translations[self.fallback_locale], key)
            if translation:
                return self._format_translation(translation, **kwargs)

        # Return key if no translation found
        return key

    def _get_nested_value(self, data: dict, key: str) -> Optional[str]:
        """Get nested value from dictionary using dot notation"""
        keys = key.split('.')
        current = data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
        return current if isinstance(current, str) else None

    def _format_translation(self, translation: str, **kwargs) -> str:
        """Format translation with parameters"""
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation

    def export_template(self, locale: str, output_file: Union[str, Path]):
        """Export translation template for a specific locale

        Args:
            locale: Source locale to export (usually 'en')
            output_file: Output file path
        """
        if locale not in self.translations:
            print(f"Warning: Locale '{locale}' not found")
            return

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.translations[locale], f, indent=2, ensure_ascii=False)

        print(f"Translation template exported to {output_path}")

# Global translation manager instance
_translation_manager = TranslationManager()

def set_locale(locale: str):
    """Set the global locale"""
    _translation_manager.set_locale(locale)

def get_locale() -> str:
    """Get the current locale"""
    return _translation_manager.current_locale

def add_translation_directory(directory: Union[str, Path]):
    """Add external translation directory"""
    _translation_manager.add_translation_directory(directory)

def load_translation_file(file_path: Union[str, Path], locale: Optional[str] = None):
    """Load a specific translation file"""
    _translation_manager.load_translation_file(file_path, locale)

def get_available_locales() -> List[str]:
    """Get list of available locales"""
    return _translation_manager.get_available_locales()

def export_translation_template(locale: str = 'en', output_file: Union[str, Path] = 'translation_template.json'):
    """Export translation template for customization"""
    _translation_manager.export_template(locale, output_file)

def _(key: str, default: Optional[str] = None, **kwargs) -> str:
    """Translation function with optional default fallback

    Args:
        key: Translation key in dot notation (e.g., 'report.title')
        default: Default value to return if translation is not found
        **kwargs: Parameters for string formatting

    Returns:
        Translated string, default value, or the key itself if no translation found
    """
    translation = _translation_manager.get_translation(key, **kwargs)

    # If the translation key is not found and a default value is provided, use the default value
    if translation == key and default is not None:
        return default

    return translation

def t(key: str, **kwargs) -> str:
    """Translation function - alias for _()

    Args:
        key: Translation key in dot notation
        **kwargs: Parameters for string formatting

    Returns:
        Translated string
    """
    return _(key, **kwargs)

# Export main functions
__all__ = [
    'set_locale', 'get_locale', '_', 't', 'TranslationManager',
    'add_translation_directory', 'load_translation_file',
    'get_available_locales', 'export_translation_template'
]