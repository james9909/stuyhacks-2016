from werkzeug.security import check_password_hash, generate_password_hash

def hash(string):
    return generate_password_hash(string)

def check_hash(actual, candidate):
    return check_password_hash(actual, candidate)
