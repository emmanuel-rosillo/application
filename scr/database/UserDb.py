from ..models import db, User, Face


# filter by name
def consultFirstUserByName(user):
    try:

        consultOne = User.query.filter(User.name == user.name).filter(User.firstName == user.firstName).filter(
            User.lastName == user.lastName).first()

    except Exception as e:
        print(e)
        consultOne = False
    finally:
        if consultOne is not None:
            return consultOne
        else:
            return None


# save user in db
def saveAUser(user):
    try:
        db.session.add(user)
        db.session.commit()
        success = True
    except Exception as e:
        print(e)
        success = False
    finally:
        return success


async def validateVectors(userVectors):
    query = Face.query.filter(Face.vectorEyes == userVectors.vectorEyes).filter(
        Face.vectorEars == userVectors.vectorEars).filter(Face.vectorLips == userVectors.vectorLips).all()
    if query is None:
        return True
    for results in query:
        pic = results[0]
        user = query[1]


'''
broker between controller and db
'''
