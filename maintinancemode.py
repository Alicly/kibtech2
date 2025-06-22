print("Script started")
try:
    from app import create_app, db
    print("Imported app and db")
    from app.models.system_setting import SystemSetting
    print("Imported SystemSetting")
except Exception as import_error:
    print(f"❌ Import error: {import_error}")
    import sys
    sys.exit(1)

try:
    app = create_app()
    print("App created")
    with app.app_context():
        print("In app context")
        setting = SystemSetting.query.get('maintenance_mode')
        print(f"Setting fetched: {setting}")
        if setting:
            setting.value = 'off'
            db.session.commit()
            print("✅ Maintenance mode disabled.")
        else:
            print("⚠️ 'maintenance_mode' setting not found.")
except Exception as e:
    print(f"❌ Error: {e}")