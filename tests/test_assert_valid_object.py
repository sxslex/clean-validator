# -*- coding: utf-8 -*-
"""Test's."""

import clean_validator


def test_dict_str():
    """Test dict str."""
    clean_validator.assert_valid_object({"name": "SleX"}, {"name": str})


def test_complex_struct():
    """Test complex struct."""
    clean_validator.assert_valid_object(
        [
            {"email": "sx.slex@gmail.com", "name": "SleX", "idade": 37},
            {"email": "slex@slex.com.br", "name": "Alexandre"},
        ],
        [{
            "email": lambda e: '@' in e and '.' in e,
            "name": str,
            "idade": (int, clean_validator.TypeNone,),
        }]
    )


def test_list_diff():
    """Test list diff."""
    clean_validator.assert_valid_object(
        [1, 'slex'],
        [int, str]
    )
