"""
Tests for internationalization functionality
"""
import pytest
from ydata_profiling.i18n import set_locale, get_locale, _, t, TranslationManager

def test_translation_manager():
    """Test translation manager"""
    tm = TranslationManager()
    assert tm is not None

def test_locale_setting():
    """Test locale setting and getting"""
    set_locale('zh')
    assert get_locale() == 'zh'

    set_locale('en')
    assert get_locale() == 'en'

def test_translation_function():
    """Test translation functions"""
    set_locale('en')
    assert _('report.title') == 'YData Profiling Report'
    assert t('report.overview') == 'Overview'

    set_locale('zh')
    assert _('report.title') == 'YData 数据分析报告'
    assert t('report.overview') == '概览'

def test_fallback_translation():
    """Test fallback behavior"""
    set_locale('unknown_locale')
    # Should fall back to key if no translation exists
    result = _('nonexistent.key')
    assert result == 'nonexistent.key'

def test_parameterized_translation():
    """Test translations with parameters"""
    set_locale('en')
    result = _('formatting.percentage', value='85.5')
    assert '85.5%' in result