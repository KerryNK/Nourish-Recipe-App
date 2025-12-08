#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    # Compatibility shim: older Django (2.1) calls gettext.translation with
    # a `codeset` kwarg. Newer Python's gettext may not accept it. Wrap and
    # replace gettext.translation to safely ignore `codeset` when present.
    try:
        import gettext as _gettext
        import inspect
        _orig_translation = getattr(_gettext, 'translation', None)
        if _orig_translation is not None:
            try:
                sig = inspect.signature(_orig_translation)
                if 'codeset' not in sig.parameters:
                    def _translation(domain, localedir=None, languages=None, class_=None, fallback=False, codeset=None):
                        return _orig_translation(domain, localedir, languages, class_, fallback)
                    _gettext.translation = _translation
            except Exception:
                pass
    except Exception:
        pass

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
