#!/usr/bin/env python3
"""
Test script to identify Flask app startup issues
"""
import sys
import traceback

def test_imports():
    """Test if all imports work"""
    print("Testing imports...")
    try:
        from app import create_app
        print("✓ create_app imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """Test if app can be created"""
    print("\nTesting app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✓ App created successfully")
        return app
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        traceback.print_exc()
        return None

def test_database_connection(app):
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        with app.app_context():
            from app.database import db
            print("✓ App context created")
            
            # Test if we can connect to the database
            connection = db.engine.connect()
            print("✓ Database connection successful")
            connection.close()
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        traceback.print_exc()
        return False

def test_route_registration(app):
    """Test if routes can be registered"""
    print("\nTesting route registration...")
    try:
        # Check if blueprints are registered
        blueprints = list(app.blueprints.keys())
        print(f"✓ Blueprints registered: {blueprints}")
        
        # Test if we can access a route
        with app.test_client() as client:
            response = client.get('/health')
            print(f"✓ Health endpoint responds: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Route registration failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=== Flask App Startup Test ===\n")
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Import test failed. Cannot proceed.")
        return
    
    # Test 2: App creation
    app = test_app_creation()
    if not app:
        print("\n❌ App creation failed. Cannot proceed.")
        return
    
    # Test 3: Database connection
    if not test_database_connection(app):
        print("\n❌ Database connection failed.")
        return
    
    # Test 4: Route registration
    if not test_route_registration(app):
        print("\n❌ Route registration failed.")
        return
    
    print("\n✅ All tests passed! The app should work.")
    print("\nTrying to start Flask server...")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"\n❌ Flask server failed to start: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()
