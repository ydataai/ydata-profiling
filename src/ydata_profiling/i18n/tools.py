"""
Translation tools for ydata-profiling
"""
import json
from pathlib import Path
from typing import Dict, Any, Union
import click


def create_translation_template(locale: str = 'en', output_dir: Union[str, Path] = '.'):
    """Create a translation template file for customization

    Args:
        locale: Source locale to use as template
        output_dir: Output directory
    """
    from ydata_profiling.i18n import export_translation_template

    output_path = Path(output_dir) / f"{locale}_template.json"
    export_translation_template(locale, output_path)
    return output_path


def validate_translation_file(file_path: Union[str, Path], reference_locale: str = 'en') -> Dict[str, Any]:
    """Validate a translation file against reference

    Args:
        file_path: Path to translation file to validate
        reference_locale: Reference locale to compare against

    Returns:
        Validation result dictionary
    """
    from ydata_profiling.i18n import _translation_manager

    file_path = Path(file_path)
    if not file_path.exists():
        return {"valid": False, "error": f"File {file_path} does not exist"}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
    except Exception as e:
        return {"valid": False, "error": f"Invalid JSON: {e}"}

    # Get reference translations
    if reference_locale not in _translation_manager.translations:
        return {"valid": False, "error": f"Reference locale '{reference_locale}' not found"}

    reference = _translation_manager.translations[reference_locale]

    # Check for missing and extra keys
    missing_keys = []
    extra_keys = []

    def check_keys(ref_dict: dict, trans_dict: dict, prefix: str = ""):
        for key, value in ref_dict.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if key not in trans_dict:
                missing_keys.append(full_key)
            elif isinstance(value, dict) and isinstance(trans_dict[key], dict):
                check_keys(value, trans_dict[key], full_key)

        for key in trans_dict:
            full_key = f"{prefix}.{key}" if prefix else key
            if key not in ref_dict:
                extra_keys.append(full_key)

    check_keys(reference, translations)

    result = {
        "valid": len(missing_keys) == 0,
        "missing_keys": missing_keys,
        "extra_keys": extra_keys,
        "total_keys": len(missing_keys) + len(extra_keys)
    }

    return result


@click.group()
def cli():
    """YData Profiling Translation Tools"""
    pass


@cli.command()
@click.option('--locale', '-l', default='en', help='Source locale for template')
@click.option('--output', '-o', default='.', help='Output directory')
def create_template(locale: str, output: str):
    """Create a translation template file"""
    output_path = create_translation_template(locale, output)
    click.echo(f"Translation template created: {output_path}")


@cli.command()
@click.argument('file_path')
@click.option('--reference', '-r', default='en', help='Reference locale')
def validate(file_path: str, reference: str):
    """Validate a translation file"""
    result = validate_translation_file(file_path, reference)

    if result["valid"]:
        click.echo(click.style("✓ Translation file is valid!", fg='green'))
    else:
        click.echo(click.style("✗ Translation file has issues:", fg='red'))

        if 'error' in result:
            click.echo(f"Error: {result['error']}")
        else:
            if result['missing_keys']:
                click.echo(f"\nMissing keys ({len(result['missing_keys'])}):")
                for key in result['missing_keys']:
                    click.echo(f"  - {key}")

            if result['extra_keys']:
                click.echo(f"\nExtra keys ({len(result['extra_keys'])}):")
                for key in result['extra_keys']:
                    click.echo(f"  + {key}")