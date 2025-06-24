from app import create_app, db
from app.models.system_setting import SystemSetting

def check_and_enable_registration():
    app = create_app()
    with app.app_context():
        # Check current setting
        setting = SystemSetting.query.filter_by(setting_key='registration_lecturer').first()
        
        if setting:
            print(f"Current lecturer registration setting: {setting.setting_value}")
            if setting.setting_value != 'enabled':
                setting.setting_value = 'enabled'
                db.session.commit()
                print("Lecturer registration has been enabled.")
        else:
            # Create the setting if it doesn't exist
            new_setting = SystemSetting(
                setting_key='registration_lecturer',
                setting_value='enabled',
                setting_type='text',
                description='Controls whether lecturer registration is enabled'
            )
            db.session.add(new_setting)
            db.session.commit()
            print("Created and enabled lecturer registration setting.")

if __name__ == '__main__':
    check_and_enable_registration() 