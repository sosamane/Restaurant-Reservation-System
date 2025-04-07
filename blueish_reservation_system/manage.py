#!/usr/bin/env python
"""Django's CLI utility for admin tasks"""

#imports OS & sys
import os #handles various OS utilities
import sys #supports all built-in functions

#main func
def main():
    #runs admin tasks
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blueish_reservation_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


#if function to check if name is equal to __main__
if __name__ == '__main__':
    main() #runs main method
