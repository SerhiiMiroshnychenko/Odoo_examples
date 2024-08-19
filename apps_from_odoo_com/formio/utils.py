# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import ast
import json


def json_loads(data):
    """ Due to possible legacy data (Python literals) in some records.

    json.loads(data) refuses identifies with single quotes.
    Use ast.literal_eval() instead.
    """
    try:
        res = json.loads(data)
    except Exception:
        res = ast.literal_eval(data)
    return res


def get_field_selection_label(model_obj, field, print_label=False):
    field_def = model_obj.fields_get([field], ['selection', 'string'])[field]

    for r in field_def['selection']:
        if r[0] == getattr(model_obj, field):
            if print_label:
                return '%s: %s' % (field_def['string'], r[1])
            else:
                return '%s' % r[1]
