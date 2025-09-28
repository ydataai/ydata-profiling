"""
Locale utilities for ydata-profiling
"""
import locale
import os
from typing import Optional
from ydata_profiling.i18n import set_locale, get_locale


def detect_system_locale() -> str:
    """Detect system locale"""
    try:
        # Attempt to retrieve the system's locale settings
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            # 转换为简化的语言代码
            lang_code = system_locale.split('_')[0].lower()
            return lang_code
    except:
        pass

    # Check environment variables
    for env_var in ['LANG', 'LANGUAGE', 'LC_ALL']:
        env_locale = os.environ.get(env_var)
        if env_locale:
            lang_code = env_locale.split('_')[0].lower()
            return lang_code

    return 'en'  # Default return English


def auto_set_locale():
    """Automatically set locale based on system settings"""
    detected_locale = detect_system_locale()
    set_locale(detected_locale)
    return detected_locale


def get_available_locales() -> list:
    """Get list of available locales"""
    from pathlib import Path
    locales_dir = Path(__file__).parent.parent / 'i18n' / 'locales'
    if locales_dir.exists():
        return [f.stem for f in locales_dir.glob('*.json')]
    return ['en']