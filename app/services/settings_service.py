from app.models import SystemSetting,db


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


def save_settings(settings):
    try:
        for key, value in settings.items():
            setting = SystemSetting.query.filter_by(
                setting_key=key
            ).first()

            if setting is None:
                setting = SystemSetting(
                    setting_key=key,
                    setting_value=str(value)
                )
                db.session.add(setting)
            else:
                setting.setting_value = str(value)

        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        raise
