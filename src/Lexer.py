status = {
    'OK': '200 OK',
    'BAD': '400 BAD'
}

command_argument_syntaxis = {
    'quit': 1,
    'ls_bkt': 1,
    'create_bkt': 1,
    'open_bkt': 2,
    'rm_bkt': 2,
    'upload': 3,
    'download': 3,
}

def check_sintaxis(command):
    if command.split(' ')[0] in command_argument_syntaxis:
        arguments = command.split(' ')
        raw_command = arguments[0]
        quantity_arguments = len(arguments)

        correct = command_argument_syntaxis[raw_command] == quantity_arguments
        if correct:
            return status['OK']
    else:
        return status['BAD']