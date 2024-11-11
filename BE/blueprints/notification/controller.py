from blueprints.notification.model import NotificationModel

def get_all_notification():
    notifications = NotificationModel.get_all_records()
    result = []

    for notification in notifications:
        result.append(notification.convert_json())

    return result


def get_all_notification_by_filter(page,perPage,admin,user_id,class_id):
    notifications = NotificationModel.find_all_by_filter(page = page, perPage = perPage, admin = admin, user_id = user_id,class_id = class_id)
    result = []

    for notification in notifications:
        result.append(notification.convert_json())

    return result