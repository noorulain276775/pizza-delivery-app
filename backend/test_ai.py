#!/usr/bin/env python3
"""
Simple test script to check AI service initialization
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ai_service():
    """Test AI service initialization"""
    try:
        print("Testing AI service import...")
        from app.services.ai_service import PizzaAIService
        print("AI service import successful")
        
        print("Testing AI service initialization...")
        ai_service = PizzaAIService()
        print("AI service initialization successful")
        
        print("Testing AI service availability...")
        if ai_service.is_ai_available():
            print("AI models loaded successfully")
        else:
            print("AI models not available, using fallback mode")
        
        print("Testing response generation...")
        response = ai_service.generate_response("Hello", "test")
        print(f"Response generated: {response[:100]}...")
        
        print("\n All tests passed! AI service is working correctly.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ai_service()
    sys.exit(0 if success else 1)
