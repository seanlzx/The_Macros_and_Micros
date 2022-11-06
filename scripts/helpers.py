from flask import request


def getFormListValues(list):
    dict = {}
    for str in list:
        value = request.form.get(str)
        if value:
            dict[str] = value
            
    return dict

