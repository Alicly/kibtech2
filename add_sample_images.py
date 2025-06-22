#!/usr/bin/env python3
"""
Script to add sample images to courses for testing purposes.
This script will update existing courses with sample image URLs.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.course import Course

def add_sample_images():
    """Add sample images to courses that don't have images."""
    
    app = create_app()
    
    with app.app_context():
        # Sample image URLs (you can replace these with actual uploaded images)
        sample_images = [
            "agriculture_course.jpg",
            "electrical_course.jpg", 
            "mechanical_course.jpg",
            "computer_course.jpg",
            "fashion_course.jpg",
            "hospitality_course.jpg",
            "business_course.jpg",
            "construction_course.jpg"
        ]
        
        # Get all courses without images
        courses_without_images = Course.query.filter(
            (Course.image_url.is_(None)) | (Course.image_url == '')
        ).all()
        
        print(f"Found {len(courses_without_images)} courses without images")
        
        for i, course in enumerate(courses_without_images):
            # Use a sample image based on course category or index
            if course.category:
                category_lower = course.category.lower()
                if 'agriculture' in category_lower:
                    image_name = "agriculture_course.jpg"
                elif 'electrical' in category_lower:
                    image_name = "electrical_course.jpg"
                elif 'mechanical' in category_lower:
                    image_name = "mechanical_course.jpg"
                elif 'computer' in category_lower or 'ict' in category_lower:
                    image_name = "computer_course.jpg"
                elif 'fashion' in category_lower:
                    image_name = "fashion_course.jpg"
                elif 'hospitality' in category_lower:
                    image_name = "hospitality_course.jpg"
                elif 'business' in category_lower:
                    image_name = "business_course.jpg"
                elif 'construction' in category_lower or 'civil' in category_lower:
                    image_name = "construction_course.jpg"
                else:
                    # Use a default image
                    image_name = sample_images[i % len(sample_images)]
            else:
                # Use a default image
                image_name = sample_images[i % len(sample_images)]
            
            course.image_url = image_name
            print(f"Added image '{image_name}' to course: {course.name}")
        
        # Commit changes
        db.session.commit()
        print(f"\nSuccessfully updated {len(courses_without_images)} courses with sample images")
        
        # Show instructions
        print("\n" + "="*60)
        print("IMPORTANT: To make images appear, you need to:")
        print("1. Place actual image files in: app/static/uploads/")
        print("2. Use these exact filenames:")
        for img in sample_images:
            print(f"   - {img}")
        print("\nOr upload images through the admin panel:")
        print("1. Go to Admin Panel > Courses")
        print("2. Edit any course")
        print("3. Upload an image file")
        print("4. Save the course")
        print("="*60)

if __name__ == "__main__":
    add_sample_images() 