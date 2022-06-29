from ..database import saveAUser, consultFirstUserByName



def validateRegisterForm(user):
    query = consultFirstUserByName(user)
    return query


def registerUser(user):
    register = saveAUser(user)
    return register


def registerVectors(userVectors):
    vectors = validateVectors(userVectors)


'''
layer controller from users
'''
