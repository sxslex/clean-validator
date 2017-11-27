# -*- coding: utf-8 -*-

__version__ = '1.0.0'


TypeNone = type(None)
TypeFunction = type(lambda a: a)


def pprint_object_type(obj):
    print(pformat_object_type(obj))


def pformat_object_type(obj, level=1):
    tab_level = '\t' * level
    if isinstance(obj, dict):
        return (
            '{\n' +
            ''.join([
                "{}'{}': {},\n".format(
                    tab_level,
                    key,
                    pformat_object_type(obj[key], level + 1)
                ) for key in obj
            ]) +
            ('\t' * (level - 1)) +
            '}'
        )
    if isinstance(obj, list):
        return (
            '[\n' +
            ''.join([
                "{}{},\n".format(
                    tab_level,
                    pformat_object_type(item, level + 1)

                ) for item in obj
            ]) +
            ('\t' * (level - 1)) +
            ']'
        )
    else:
        return '{}'.format(
            type(obj).__name__ if obj is not None else 'TypeNone'
        )


class OR(list):
    def __init__(self, *kargs):
        list.__init__(self, kargs)


class AND(list):
    def __init__(self, *kargs):
        list.__init__(self, kargs)


def valid_object(obs, types, name=None, ignore_missing=False):
    name = name or []
    erros = []
    if isinstance(types, (type, )):
        if not isinstance(obs, types):
            erros.append(
                'type invalid field {}:{} != {}'.format(
                    '.'.join(name), type(obs), types
                )
            )
    elif isinstance(types, TypeFunction):
        resp = types(obs)
        msg = ''
        if isinstance(resp, (tuple, list, )):
            resp, msg = resp
        if not resp:
            erros.append(
                'invalid field {}:{} {}'.format(
                    '.'.join(name), obs, msg
                ).strip()
            )
    elif isinstance(types, (tuple, OR)):
        is_erro = True
        resps = []
        for o in types:
            resp = valid_object(
                obs=obs,
                types=o,
                name=name,
                ignore_missing=ignore_missing
            )
            if not resp:
                is_erro = False
                break
            else:
                resps.extend(resp)
        if is_erro:
            erros.extend(resps)
    elif isinstance(types, (AND, )):
        for o in types:
            erros.extend(valid_object(
                obs=obs,
                types=o,
                name=name,
                ignore_missing=ignore_missing
            ))
    elif isinstance(types, list) and obs:
        # TODO: testar em todos os itens mas agrupar o erro
        new_name = list(name)
        if new_name:
            new_name[-1] += '[]'
        aux = valid_object(
            obs=obs[0],
            types=types[0],
            name=new_name,
            ignore_missing=ignore_missing
        )
        erros.extend(aux)
    elif isinstance(types, dict):
        try:
            extras = set(obs) - set(types)
            missing = set(types) - set(obs)
        except:
            extras = 0
            missing = 0
            pass
        num_none = len([
            t
            for t in types
            if (isinstance(types[t], (tuple, OR,)) and TypeNone in types[t]) or
            isinstance(types[t], TypeNone)
        ])
        if len(extras):
            erros.append('Retornado campos extras {}'.format(extras))
        if len(missing) > num_none and not ignore_missing:
            erros.append('Faltando campos {}'.format(missing))
        for nname in types:
            new_name = list(name)
            new_name.append(nname)
            erros.extend(
                valid_object(
                    obs=obs.get(nname),
                    types=types[nname],
                    name=new_name,
                    ignore_missing=ignore_missing
                )
            )
    else:
        raise Exception(
            'type invalid: {}:{}'.format(
                '.'.join(name), types
            )
        )
    return erros


def assert_valid_object(obs, types, ignore_missing=False):
    erros = valid_object(
        obs=obs,
        types=types,
        ignore_missing=ignore_missing
    )
    if erros:
        raise Exception(
            '\n'.join('\t' + e for e in erros)
        )


# print(pformat_object_type({"nome": "slex", "idade": 38}))
# print(pformat_object_type({
#     "nome": "slex",
#     "idade": 38,
#     "filhos": [
#         {
#             "nome": "Icaro",
#         },
#         {
#             "nome": "Gabriel",
#         }
#     ]
# }))
