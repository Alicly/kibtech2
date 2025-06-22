#!/usr/bin/env python3
"""
Test script to debug route registration issues
"""

from app import create_app

def test_routes():
    app = create_app()
    
    print("Testing route registration...")
    
    # Check if lecturer blueprint is registered
    if 'lecturer' in app.blueprints:
        print("✅ Lecturer blueprint is registered")
    else:
        print("❌ Lecturer blueprint is NOT registered")
        return
    
    # List all lecturer routes
    lecturer_routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('lecturer.'):
            lecturer_routes.append((rule.rule, rule.endpoint))
    
    print(f"\n📋 Found {len(lecturer_routes)} lecturer routes:")
    for rule, endpoint in sorted(lecturer_routes):
        print(f"  {rule} -> {endpoint}")
    
    # Check specifically for grading routes
    grading_routes = [route for route in lecturer_routes if 'grading' in route[1]]
    print(f"\n🎯 Found {len(grading_routes)} grading routes:")
    for rule, endpoint in grading_routes:
        print(f"  {rule} -> {endpoint}")
    
    # Test URL generation
    print("\n🔗 Testing URL generation:")
    with app.app_context():
        try:
            from flask import url_for
            grading_url = url_for('lecturer.grading')
            print(f"✅ lecturer.grading -> {grading_url}")
        except Exception as e:
            print(f"❌ Error generating lecturer.grading URL: {e}")
        
        try:
            course_grading_url = url_for('lecturer.course_grading', course_id=1)
            print(f"✅ lecturer.course_grading -> {course_grading_url}")
        except Exception as e:
            print(f"❌ Error generating lecturer.course_grading URL: {e}")

if __name__ == "__main__":
    test_routes() 