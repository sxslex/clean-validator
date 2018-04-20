# -*- coding: utf-8 -*-
"""Used to validate objects cleanly and simply."""

__version__ = '0.0.3'


TypeNone = type(None)
TypeFunction = type(lambda a: a)

MISSING_MSG = 'missing fields %s'
EXTRAS_MSG = 'returned extra fields %s'


def pprint_object_type(obj):
    """Pprint_object_type."""
    print(pformat_object_type(obj))


def pformat_object_type(obj, level=1):
    """Pformat_object_type."""
    tab_level = '\t' * level
    if isinstance(obj, dict):
        return (
            '{\n' +
            ''.join([
                "%s'%s': %s,\n" % (
                    tab_level,
                    key,
                    pformat_object_type(obj[key], level + 1)
                ) for key in sorted(obj)
            ]) +
            ('\t' * (level - 1)) +
            '}'
        )
    if isinstance(obj, list):
        return (
            '[\n' +
            ''.join([
                "%s%s,\n" % (
                    tab_level,
                    pformat_object_type(item, level + 1)

                ) for item in obj
            ]) +
            ('\t' * (level - 1)) +
            ']'
        )
    else:
        return '%s' % (
            type(obj).__name__ if obj is not None else 'TypeNone'
        )


class OR(list):
    """OR List Comparations."""

    def __init__(self, *kargs):
        """OR List Comparations."""
        list.__init__(self, kargs)


class AND(list):
    """AND List Comparations."""

    def __init__(self, *kargs):
        """AND List Comparations."""
        list.__init__(self, kargs)


def or_(*kargs):
    """OR List Comparations."""
    return OR(*kargs)


def and_(*kargs):
    """AND List Comparations."""
    return AND(*kargs)


def valid_object(
    obs,
    types,
    name=None,
    missing_msg=MISSING_MSG,
    extras_msg=EXTRAS_MSG,
):
    """Valid_object."""
    name = name or []
    erros = []
    if isinstance(types, (type, )):
        if not isinstance(obs, types):
            erros.append(
                'type invalid field %s:%s != %s' % (
                    '.'.join(name), type(obs), types
                )
            )
        return erros
    if isinstance(types, TypeFunction):
        resp = types(obs)
        msg = ''
        if isinstance(resp, (tuple, list, )):
            resp, msg = resp
        if not resp:
            if msg:
                erros.append(msg)
            else:
                erros.append(
                    (
                        'invalid field %s:%s' % ('.'.join(name), obs, )
                    ).strip()
                )
        return erros
    if isinstance(types, (tuple, OR)):
        is_erro = True
        resps = []
        for o in types:
            resp = valid_object(
                obs=obs,
                types=o,
                name=name,
                missing_msg=missing_msg,
                extras_msg=extras_msg,
            )
            if not resp:
                is_erro = False
                break
            else:
                resps.extend(resp)
        if is_erro:
            erros.extend(resps)
        return erros
    if isinstance(types, (AND, )):
        for o in types:
            erros.extend(valid_object(
                obs=obs,
                types=o,
                name=name,
                missing_msg=missing_msg,
                extras_msg=extras_msg,
            ))
        return erros
    if isinstance(types, list) and obs:
        new_name = list(name)
        if new_name:
            new_name[-1] += '[]'
        if len(types) == 1:
            for ob in obs:
                aux = valid_object(
                    obs=ob,
                    types=types[0],
                    name=new_name,
                    missing_msg=missing_msg,
                    extras_msg=extras_msg,
                )
                erros.extend(aux)
        else:
            aux = None
            for ob, ty in zip(obs, types):
                aux = valid_object(
                    obs=ob,
                    types=ty,
                    name=new_name,
                    missing_msg=missing_msg,
                    extras_msg=extras_msg,
                )
            if aux:
                erros.extend(aux)
        return erros
    if isinstance(types, dict):
        extras = set(obs) - set(types)
        missing = set(types) - set(obs)
        num_none = len([
            t
            for t in types
            if (isinstance(types[t], (tuple, OR,)) and TypeNone in types[t]) or
            isinstance(types[t], TypeNone)
        ])
        if extras_msg and len(extras):
            s_extras = extras_msg
            if '%s' in s_extras:
                s_extras = s_extras % ', '.join(extras)
            erros.append(s_extras)
        if missing_msg and len(missing) > num_none:
            s_missing = extras_msg
            if '%s' in s_missing:
                s_missing = s_missing % ', '.join(missing)
            erros.append(s_missing)
        for type_name in types:
            new_name = list(name)
            new_name.append(type_name)
            erros.extend(
                valid_object(
                    obs=obs.get(type_name),
                    types=types[type_name],
                    name=new_name,
                    missing_msg=missing_msg,
                    extras_msg=extras_msg,
                )
            )
        return erros
    if isinstance(types, (int, str, bool)):
        if obs != types:
            erros.append(
                'value invalid field %s:%s != %s' % (
                    '.'.join(name), obs, types
                )
            )
        return erros
    raise Exception(
        'type invalid: %s:%s' % (
            '.'.join(name), types
        )
    )


def assert_valid_object(
    obs, types,
    missing_msg=MISSING_MSG,
    extras_msg=EXTRAS_MSG,
):
    """Assert_valid_object."""
    erros = valid_object(
        obs=obs,
        types=types,
        missing_msg=missing_msg,
        extras_msg=extras_msg,
    )
    if erros:
        raise Exception(
            '\n'.join('\t' + e for e in erros)
        )
