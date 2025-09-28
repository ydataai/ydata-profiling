"""
Internationalization module for ydata-profiling
"""
import os
import json
from pathlib import Path
from typing import Dict, Optional
import threading


class TranslationManager:
    """Manages translations for ydata-profiling"""

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
            self.initialized = True
            self._load_translations()

    def _load_translations(self):
        """Load all translation files"""
        translations_dir = Path(__file__).parent / 'locales'
        if not translations_dir.exists():
            return

        for locale_file in translations_dir.glob('*.json'):
            locale = locale_file.stem
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    self.translations[locale] = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load translation file {locale_file}: {e}")

    def set_locale(self, locale: str):
        """Set the current locale"""
        if locale in self.translations or locale == self.fallback_locale:
            self.current_locale = locale
        else:
            print(f"Warning: Locale '{locale}' not found, using fallback '{self.fallback_locale}'")

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


# Global translation manager instance
_translation_manager = TranslationManager()


def set_locale(locale: str):
    """Set the global locale"""
    _translation_manager.set_locale(locale)


def get_locale() -> str:
    """Get the current locale"""
    return _translation_manager.current_locale


def _(key: str, **kwargs) -> str:
    """Translation function - shorthand for get_translation"""
    return _translation_manager.get_translation(key, **kwargs)


def t(key: str, **kwargs) -> str:
    """Translation function - alias for _()"""
    return _(key, **kwargs)


# Export main functions
__all__ = ['set_locale', 'get_locale', '_', 't', 'TranslationManager']