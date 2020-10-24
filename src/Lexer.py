status = {
    'OK': '200 OK',
    'BAD': '400 BAD'
}

command_argument_syntaxis = {
    'QUIT': 1,
    'LIST_BKT': 1,
    'CREATE_BKT': 1,
    'OPEN_BKT': 2,
    'DELETE_BKT': 2,
    'UPLOAD_FL': 3,
    'DOWNLOAD_FL': 3,
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