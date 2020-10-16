keywords = {
'QUIT': 'BYE BYE',
'HELLO': 'WELCOME TO THE SERVER!',
'DATA_SEND': 'ACCEPTED',
'DATA_RECEIVED': 'DATA RECEIVED',
'INVALID': 'RULE DOES NOT EXIST',
'CREATE_BUCKET': 'BUCKET CREATED',
'LIST_BKTS': 'BUCKETS LISTED',
'DELETE_BUCKET': 'BUCKET DELETED',
'CREATE_OBJ': '',
'LIST_OBJ': '',
'DELETE_OBJ': '',
}

def find_rule(token):
    print(token)
    if token in keywords:
        return keywords[token]
    else:
        return keywords['INVALID']
