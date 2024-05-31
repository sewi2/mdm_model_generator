# TODO: make tests for each function


def is_fk_field(prop_definition):
    return (
        prop_definition['type'] == 'object'
        and prop_definition.get('properties'))


def is_text_field(prop_definition):
    return (
        prop_definition['type'] == 'string'
        and not prop_definition.get('format'))


def is_dated_string(prop_definition):
    return (
        prop_definition['type'] == 'string'
        and prop_definition.get('format', '') in ('date', 'date-time'))


def is_number_field(prop_definition):
    return prop_definition['type'] in ('integer', 'number')
