status = {
    'OK': '200 OK',
    'BAD': '400 BAD'
}

rule_argument_syntaxis = {
    'quit': 1,
    'ls_bkt': 1,
    'create_bkt': 1,
    'open_bkt': 2,
    'rm_bkt': 2,
    'rm_file': 3,
    'upload': 3,
    'download': 3,
}

def check_sintaxis(rule):
    if rule.split(' ')[0] in rule_argument_syntaxis:
        parameters = rule.split(' ')
        raw_rule = parameters[0]
        quantity_parameters = len(parameters)

        correct = rule_argument_syntaxis[raw_rule] == quantity_parameters
        if correct:
            return status['OK']
    else:
        return status['BAD']