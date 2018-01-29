# -*- coding: utf-8 -*-
"""Test's."""
# update pypi:
# python setup.py sdist upload -r pypi

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


def test_valid_retorn_msg_custom():
    resp = clean_validator.valid_object(
        dict(email="teste@teste.com.br"),
        {
            'password': lambda c: (
                isinstance(c, str) and bool(len(c) > 3),
                'Senha obrigatorio com mais de 3 caracteres'
            ),
            'email': lambda c: (
                isinstance(c, str) and bool(c.strip()),
                'Email obrigadorio'
            ),
            'name': lambda c: (
                isinstance(c, str) and bool(c.strip()),
                'Nome obrigadorio'
            ),
        },
        missing_msg=None,
        extras_msg=None,
    )
    assert len(resp) == 2
    assert 'Senha obrigatorio com mais de 3 caracteres' in resp
    assert 'Nome obrigadorio' in resp


def test_pformat_object_type():
    resp = clean_validator.pformat_object_type(
        dict(
            email="teste@teste.com.br",
            filhos=[
                dict(nome='Icaro', idade=18),
                dict(nome='Gabriel', idade=3),
            ]
        )
    )
    assert resp == (
        "{\n"
        "\t'email': str,\n"
        "\t'filhos': [\n"
        '\t\t{\n'
        "\t\t\t'idade': int,\n"
        "\t\t\t'nome': str,\n"
        "\t\t},\n"
        "\t\t{\n"
        "\t\t\t'idade': int,\n"
        "\t\t\t'nome': str,\n"
        "\t\t},\n"
        "\t],\n"
        "}"
    )


def test_assert_expecific_value():
    resp = clean_validator.valid_object(
        dict(
            email="teste@teste.com.br",
            filhos=[
                dict(nome='Icaro', idade=18)
            ]
        ),
        {
            'email': 'teste@teste.com.br.',
            'filhos': [
                {
                    'idade': 18,
                    'nome': 'Icaro',
                },
            ],
        }
    )
    assert len(resp) == 1
    assert (
        'value invalid field email:teste@teste.com.br != teste@teste.com.br.'
    ) in resp
