#!/usr/bin/env python
"""Test restaurant"""
import json

def main():
    other_menu = {
        'restaurant': 'Test Restaurant',
        'courses': [
            {
                'name': 'Local',
                'descr': 'Öl och viltfärs med palsternacka',
            },
            {
                'name': 'World Wide',
                'descr': '비빔밥 (Bibimbap)',
            },
        ],
    }
    return other_menu


if __name__ == "__main__":
    print(json.dumps(main()))
    # print(main())
