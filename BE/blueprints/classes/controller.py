from blueprints.classes.model import ClassModel

def get_all_classes():
    classes = ClassModel.get_all_records()
    result = []

    for clas in classes:
        result.append(clas.convert_json())

    return result


def get_all_classes_by_filter(page,perPage,class_name):
    classes = ClassModel.find_all_by_filter(page = page, perPage = perPage, class_name = class_name)
    result = []

    for clas in classes:
        result.append(clas.convert_json())

    return result

def get_by_id(id):
    class_object = ClassModel.find_by_id(id)
    return class_object.convert_json()
