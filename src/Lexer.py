keywords = {
'QUIT': 'BYE BYE',
'HELLO': 'WELCOME TO THE SERVER!',
'DATA_SEND': 'ACCEPTED',
'INVALID': 'RULE DOES NOT EXIST',
'DATA_RECEIVED': 'DATA RECEIVED'
}

def find_rule(token):
    if token in keywords:
        return keywords[token]
    else:
        return keywords['INVALID']
