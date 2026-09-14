from app.models import SystemSetting


def get_setting(key, default=None):
    setting = SystemSetting.query.filter_by(setting_key=key).first()

    if setting is None:
        return default

    return setting.setting_value


def get_int_setting(key, default=0):

    try:
        return int(get_setting(key, default))
    except (TypeError, ValueError):
        return default
