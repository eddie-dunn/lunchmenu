#!/usr/bin/env python
"""Example restaurant plugin

The requirements for a restaurant fetch is that it can

1. Be executed without arguments
2. Returns a json object in the format suggested by MENU below, where keys are
   required attributes, and values are whatever you deem appropriate.
"""
import json

MENU_SAMPLE = {
    'restaurant': 'Example Restaurant',
    'courses': [
        {
            'name': 'Course 1',
            'description': 'Alla bäckar äro brännvin',
        },
        {
            'name': 'Course 2',
            'description': 'Stadsparksdammen full af Bayerskt öl',
        },
        {
            'name': 'Course 3',
            'description': 'Cognac i varenda rännsten',
        },
        {
            'name': 'Course 4',
            'description': 'Punch i varendaste pöl',
        },
    ],
}


def main():
    """Main"""
    return MENU_SAMPLE


if __name__ == "__main__":
    print(json.dumps(main()))
