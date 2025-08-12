"""
AI Chatbot API Routes
Handles customer interactions with the AI-powered chatbot
"""
from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import uuid
import logging
from ..services.ai_service import PizzaAIService

chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

def get_ai_service():
    """Get AI service instance with proper configuration"""
    try:
        logger.info("Initializing AI service...")
        ai_service = PizzaAIService(current_app.config)
        logger.info("AI service initialized successfully")
        return ai_service
    except Exception as e:
        logger.error(f"Failed to initialize AI service: {e}")
        logger.warning("Chat endpoints will return service unavailable errors")
        return None

@chat_bp.route('/', methods=['POST'])
def chat():
    """
    Main chat endpoint for AI chatbot interactions
    
    Expected JSON payload:
    {
        "message": "User message",
        "session_id": "unique_session_id"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get AI service
        ai_service = get_ai_service()
        if not ai_service:
            return jsonify({'error': 'AI service unavailable'}), 503
        
        # Generate AI response
        response = ai_service.generate_response(message, session_id)
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': ai_service._get_timestamp()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get chat history for a specific session"""
    try:
        ai_service = get_ai_service()
        if not ai_service:
            return jsonify({'error': 'AI service unavailable'}), 503
        
        history = ai_service.get_conversation_history(session_id)
        return jsonify({
            'session_id': session_id,
            'history': history,
            'timestamp': ai_service._get_timestamp()
        })
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve chat history'}), 500

@chat_bp.route('/clear/<session_id>', methods=['DELETE'])
def clear_chat_history(session_id):
    """Clear chat history for a specific session"""
    try:
        ai_service = get_ai_service()
        if not ai_service:
            return jsonify({'error': 'AI service unavailable'}), 503
        
        ai_service.clear_conversation_history(session_id)
        return jsonify({
            'message': 'Chat history cleared successfully',
            'session_id': session_id,
            'timestamp': ai_service._get_timestamp()
        })
    except Exception as e:
        logger.error(f"Clear history error: {str(e)}")
        return jsonify({'error': 'Failed to clear chat history'}), 500

@chat_bp.route('/stats', methods=['GET'])
def get_chat_stats():
    """Get chatbot usage statistics"""
    try:
        ai_service = get_ai_service()
        if not ai_service:
            return jsonify({'error': 'AI service unavailable'}), 503
        
        stats = ai_service.get_system_stats()
        return jsonify({
            'stats': stats,
            'timestamp': ai_service._get_timestamp()
        })
    except Exception as e:
        logger.error(f"Stats retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@chat_bp.route('/health', methods=['GET'])
def chat_health():
    """Check if AI chatbot is working"""
    try:
        # Check if AI service is working
        ai_service = get_ai_service()
        if not ai_service:
            return jsonify({'error': 'AI service unavailable'}), 503

        test_response = ai_service.generate_response("Hello", "health_check")
        
        return jsonify({
            'status': 'healthy',
            'model': ai_service.model_name,
            'timestamp': ai_service._get_timestamp(),
            'test_response': test_response[:50] + "..." if len(test_response) > 50 else test_response
        })
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': ai_service._get_timestamp() if 'ai_service' in locals() else 'N/A'
        }), 503

@chat_bp.route('/help', methods=['GET'])
def chat_help():
    """Get API documentation and usage information"""
    return jsonify({
        'endpoints': {
            'POST /': 'Send a message to the AI chatbot',
            'GET /history/<session_id>': 'Get chat history for a session',
            'DELETE /clear/<session_id>': 'Clear chat history for a session',
            'GET /stats': 'Get chatbot usage statistics',
            'GET /health': 'Check chatbot health status',
            'GET /help': 'This help information'
        },
        'rate_limits': {
            'chat': '20 per minute',
            'history': '30 per minute',
            'clear': '10 per minute',
            'stats': '5 per minute'
        },
        'example_request': {
            'method': 'POST',
            'endpoint': '/',
            'body': {
                'message': 'What pizzas do you have?',
                'session_id': 'optional_session_id'
            }
        }
    })
