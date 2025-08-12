#!/usr/bin/env python3
"""
Minimal test script to check Flask app creation and route registration
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_creation():
    """Test Flask app creation and route registration"""
    try:
        print("Testing Flask app creation...")
        from app import create_app
        
        print("Creating app...")
        app = create_app('development')
        print("App created successfully")
        
        print("Checking registered routes...")
        with app.app_context():
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append(f"{rule.methods} {rule.rule}")
            
            print(f" Found {len(routes)} routes:")
            for route in routes[:10]:  # Show first 10 routes
                print(f"  {route}")
            
            # Check if chat routes are registered
            chat_routes = [r for r in routes if '/api/chat' in r]
            if chat_routes:
                print(f"Chat routes found: {len(chat_routes)}")
                for route in chat_routes:
                    print(f"  {route}")
            else:
                print("No chat routes found!")
        
        print("\n App creation and route registration successful!")
        return True
        
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_creation()
    sys.exit(0 if success else 1)
