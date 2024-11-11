from blueprints.user.model import UserModel,UserRole

def get_all_users_by_filter(page,perPage,name,role):
    users = UserModel.find_all_by_filter(page = page, perPage = perPage, name = name,role = role)
    result = []

    for user in users:
        result.append(user.convert_json())

    return result

def get_all_roles():
    roles = [role.value for role in UserRole]

    return roles

def get_user_by_id(id):
    return UserModel.find_by_id(id = id)