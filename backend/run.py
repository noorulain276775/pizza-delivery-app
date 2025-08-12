"""
Main application entry point for the Pizza Delivery API
"""
import os
import sys
from dotenv import load_dotenv
from app import create_app

def validate_environment():
    """Validate required environment variables"""
    required_vars = []
    
    # Check if we're in production
    if os.environ.get('FLASK_ENV') == 'production':
        required_vars = ['DATABASE_URL', 'SECRET_KEY']
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running in production mode.")
        sys.exit(1)

def main():
    """Main application entry point"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Validate environment
        validate_environment()
        
        # Get configuration from environment
        config_name = os.environ.get('FLASK_ENV', 'development')
        host = os.environ.get('FLASK_HOST', '127.0.0.1')
        port = int(os.environ.get('FLASK_PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        
        # Security check for production
        if config_name == 'production' and debug:
            print("Warning: Debug mode is enabled in production!")
            debug = False
        
        # Validate host binding
        if host == '0.0.0.0' and config_name == 'production':
            print("Warning: Binding to 0.0.0.0 in production may expose the service!")
        
        print(f"Starting Pizza Delivery API on {host}:{port}")
        print(f"Environment: {config_name}")
        print(f"Debug mode: {debug}")
        
        # Create application instance
        app = create_app(config_name)
        
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
