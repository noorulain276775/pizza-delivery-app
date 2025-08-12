"""
AI Chatbot Service using Hugging Face Transformers
Handles customer interactions with intelligent responses
"""

import logging
from typing import Dict, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import re
import json
import os
from flask import current_app

logger = logging.getLogger(__name__)

class PizzaAIService:
    """
    AI-powered chatbot service for pizza delivery customer support
    Uses Hugging Face transformers for natural language understanding
    """
    
    def __init__(self, config=None):
        """Initialize the AI service with configuration"""
        # Use provided config or get from Flask app context
        if config is None:
            try:
                config = current_app.config
                logger.info("Using Flask app config")
            except RuntimeError:
                # Fallback to environment variables if not in Flask context
                logger.info("Using environment variables as fallback")
                config = type('Config', (), {
                    'AI_MODEL_NAME': os.environ.get('AI_MODEL_NAME', 'microsoft/DialoGPT-medium'),
                    'AI_MAX_LENGTH': int(os.environ.get('AI_MAX_LENGTH', '100')),
                    'AI_TEMPERATURE': float(os.environ.get('AI_TEMPERATURE', '0.7'))
                })()
        
        # Debug logging
        logger.info(f"Config object type: {type(config)}")
        logger.info(f"Config attributes: {dir(config)}")
        logger.info(f"AI_MODEL_NAME from config: {getattr(config, 'AI_MODEL_NAME', 'NOT_FOUND')}")
        logger.info(f"AI_MAX_LENGTH from config: {getattr(config, 'AI_MAX_LENGTH', 'NOT_FOUND')}")
        logger.info(f"AI_TEMPERATURE from config: {getattr(config, 'AI_TEMPERATURE', 'NOT_FOUND')}")
        
        self.model_name = getattr(config, 'AI_MODEL_NAME', 'microsoft/DialoGPT-medium')
        self.max_length = getattr(config, 'AI_MAX_LENGTH', 100)
        self.temperature = getattr(config, 'AI_TEMPERATURE', 0.7)
        
        self.tokenizer = None
        self.model = None
        self.conversation_pipeline = None
        self.conversation_history: Dict[str, List[Dict]] = {}
        
        # Pizza domain knowledge - Move to database or config file in production
        self.pizza_knowledge = {
            "menu": [
                "Margherita Pizza - Classic tomato and mozzarella",
                "Pepperoni Pizza - Spicy pepperoni with cheese",
                "Vegetarian Pizza - Fresh vegetables and cheese"
            ],
            "prices": [
                "Margherita: $12.99",
                "Pepperoni: $14.99", 
                "Vegetarian: $13.99"
            ],
            "delivery": [
                "Standard delivery: 30-45 minutes",
                "Express delivery: 20-30 minutes (additional $3)",
                "Free delivery on orders over $25"
            ],
            "payment": [
                "Cash on delivery",
                "Credit card",
                "Digital wallets accepted"
            ]
        }
        
        # Initialize models in background to avoid blocking server startup
        self._initialize_models_async()
    
    def _initialize_models_async(self):
        """Initialize models asynchronously to avoid blocking server startup"""
        import threading
        
        def init_models():
            try:
                logger.info("Starting AI model initialization in background...")
                self._load_models()
            except Exception as e:
                logger.error(f"Failed to initialize AI models: {e}")
                logger.info("Setting up fallback mode...")
                self._setup_fallback()
        
        try:
            # Start initialization in background thread
            thread = threading.Thread(target=init_models, daemon=True)
            thread.start()
            logger.info("AI model initialization started in background thread")
        except Exception as e:
            logger.error(f"Failed to start AI initialization thread: {e}")
            self._setup_fallback()
        
        # Set a flag to indicate initialization is in progress
        self._initializing = True
    
    def _load_models(self):
        """Load Hugging Face models and tokenizer"""
        try:
            logger.info(f"Loading AI models: {self.model_name}")
            
            # Set Hugging Face environment variables if available
            hf_token = os.environ.get('HUGGING_FACE_HUB_TOKEN')
            if hf_token:
                logger.info("Using Hugging Face token for authentication")
                os.environ['HF_TOKEN'] = hf_token
            
            # Set cache directory if specified
            cache_dir = os.environ.get('HUGGING_FACE_HUB_CACHE_DIR')
            if cache_dir:
                logger.info(f"Using custom cache directory: {cache_dir}")
                os.environ['HF_HOME'] = cache_dir
            
            logger.info("Importing transformers and torch...")
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            
            logger.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=hf_token,
                cache_dir=cache_dir
            )
            logger.info("Tokenizer loaded successfully")
            
            logger.info("Loading model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=hf_token,
                cache_dir=cache_dir
            )
            logger.info("Model loaded successfully")
            
            logger.info("Creating conversation pipeline...")
            # Create conversation pipeline
            self.conversation_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=self.max_length,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            logger.info("AI models loaded successfully")
            self._initializing = False
            
        except ImportError as e:
            logger.error(f"Import error loading AI models: {e}")
            logger.warning("Transformers or torch not available, falling back to rule-based responses")
            self._setup_fallback()
        except Exception as e:
            logger.error(f"Error loading AI models: {e}")
            logger.warning("Falling back to rule-based responses")
            # Fallback to rule-based responses
            self._setup_fallback()
            self._initializing = False
    
    def _setup_fallback(self):
        """Setup fallback rule-based system if AI models fail"""
        logger.warning("Setting up fallback rule-based system - AI models unavailable")
        self.conversation_pipeline = None
        self.model = None
        self.tokenizer = None
        self._initializing = False
    
    def is_ai_available(self):
        """Check if AI models are available"""
        return self.conversation_pipeline is not None and self.model is not None
    
    def is_initializing(self):
        """Check if AI models are still initializing"""
        return getattr(self, '_initializing', False)
    
    def get_status(self):
        """Get AI service status"""
        return {
            'available': self.is_ai_available(),
            'initializing': self.is_initializing(),
            'model_name': self.model_name,
            'fallback_mode': self.conversation_pipeline is None
        }
    
    def generate_response(self, user_message: str, session_id: str = "default") -> str:
        """
        Generate AI-powered response to user message
        
        Args:
            user_message: User's input message
            session_id: Unique session identifier for conversation history
            
        Returns:
            AI-generated response string
        """
        try:
            # Store user message in conversation history
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            self.conversation_history[session_id].append({
                "role": "user",
                "content": user_message,
                "timestamp": self._get_timestamp()
            })
            
            # Generate AI response
            if self.conversation_pipeline:
                response = self._generate_ai_response(user_message, session_id)
            else:
                response = self._generate_rule_based_response(user_message)
            
            # Store AI response in conversation history
            self.conversation_history[session_id].append({
                "role": "assistant",
                "content": response,
                "timestamp": self._get_timestamp()
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_error_response()
    
    def _generate_ai_response(self, user_message: str, session_id: str) -> str:
        """Generate response using Hugging Face transformers"""
        try:
            # Prepare conversation context
            context = self._prepare_conversation_context(session_id)
            
            # Combine context with user message
            full_input = context + " " + user_message if context else user_message
            
            # Generate response using the pipeline
            generated = self.conversation_pipeline(
                full_input,
                max_length=len(full_input.split()) + 50,
                num_return_sequences=1
            )
            
            # Extract and clean the response
            response = generated[0]['generated_text']
            response = self._clean_ai_response(response, full_input)
            
            # Enhance with pizza domain knowledge
            enhanced_response = self._enhance_with_domain_knowledge(user_message, response)
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return self._generate_rule_based_response(user_message)
    
    def _prepare_conversation_context(self, session_id: str) -> str:
        """Prepare conversation context from history"""
        if session_id not in self.conversation_history:
            return ""
        
        # Get last 3 exchanges for context
        recent_messages = self.conversation_history[session_id][-6:]
        context_parts = []
        
        for msg in recent_messages:
            if msg["role"] == "user":
                context_parts.append(f"User: {msg['content']}")
            else:
                context_parts.append(f"Assistant: {msg['content']}")
        
        return " ".join(context_parts)
    
    def _clean_ai_response(self, response: str, input_text: str) -> str:
        """Clean and format AI-generated response"""
        # Remove input text from response
        if input_text in response:
            response = response.replace(input_text, "").strip()
        
        # Clean up common artifacts
        response = re.sub(r'<\|endoftext\|>', '', response)
        response = re.sub(r'Assistant:', '', response)
        response = re.sub(r'User:', '', response)
        
        # Limit response length
        if len(response) > 200:
            response = response[:200] + "..."
        
        return response.strip()
    
    def _enhance_with_domain_knowledge(self, user_message: str, ai_response: str) -> str:
        """Enhance AI response with pizza domain knowledge"""
        user_message_lower = user_message.lower()
        
        # Check for specific pizza-related queries
        if any(word in user_message_lower for word in ["menu", "pizza", "available"]):
            menu_info = "\n\nAvailable pizzas:\n" + "\n".join(self.pizza_knowledge["menu"])
            return ai_response + menu_info
        
        elif any(word in user_message_lower for word in ["price", "cost", "how much"]):
            price_info = "\n\nPricing:\n" + "\n".join(self.pizza_knowledge["prices"])
            return ai_response + price_info
        
        elif any(word in user_message_lower for word in ["delivery", "time", "how long"]):
            delivery_info = "\n\nDelivery options:\n" + "\n".join(self.pizza_knowledge["delivery"])
            return ai_response + delivery_info
        
        elif any(word in user_message_lower for word in ["payment", "pay", "cash", "card"]):
            payment_info = "\n\nPayment methods:\n" + "\n".join(self.pizza_knowledge["payment"])
            return ai_response + payment_info
        
        return ai_response
    
    def _generate_rule_based_response(self, user_message: str) -> str:
        """Generate rule-based response as fallback"""
        user_message_lower = user_message.lower()
        
        # Greeting patterns
        if any(word in user_message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "Hello! Welcome to Pizza Delivery! How can I help you today? I can assist with menu information, pricing, delivery options, and placing orders."
        
        # Menu queries
        elif any(word in user_message_lower for word in ["menu", "what", "available", "pizza"]):
            return "Here's our delicious menu:\n" + "\n".join(self.pizza_knowledge["menu"]) + "\n\nWould you like to know more about any specific pizza?"
        
        # Price queries
        elif any(word in user_message_lower for word in ["price", "cost", "how much", "expensive"]):
            return "Our pricing is very competitive:\n" + "\n".join(self.pizza_knowledge["prices"]) + "\n\nWe also offer free delivery on orders over $25!"
        
        # Delivery queries
        elif any(word in user_message_lower for word in ["delivery", "time", "how long", "fast"]):
            return "We offer fast delivery:\n" + "\n".join(self.pizza_knowledge["delivery"]) + "\n\nWhere would you like your pizza delivered?"
        
        # Order queries
        elif any(word in user_message_lower for word in ["order", "buy", "purchase", "get"]):
            return "Great! To place an order, you can use our website or mobile app. You can select your pizzas, add toppings, and choose delivery options. What would you like to order?"
        
        # Payment queries
        elif any(word in user_message_lower for word in ["payment", "pay", "cash", "card", "credit"]):
            return "We accept multiple payment methods:\n" + "\n".join(self.pizza_knowledge["payment"]) + "\n\nWhat's your preferred payment method?"
        
        # Thank you
        elif any(word in user_message_lower for word in ["thank", "thanks", "appreciate"]):
            return "You're welcome! Is there anything else I can help you with today?"
        
        # Default response
        else:
            return "I'm here to help with your pizza delivery needs! You can ask me about our menu, prices, delivery options, or how to place an order. What would you like to know?"
    
    def _get_error_response(self) -> str:
        """Return error response when AI generation fails"""
        return "I'm experiencing some technical difficulties right now, but I can still help you with basic information about our pizzas, prices, and delivery options. What would you like to know?"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for conversation history"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        return self.conversation_history.get(session_id, [])
    
    def clear_conversation_history(self, session_id: str):
        """Clear conversation history for a session"""
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
    
    def get_system_stats(self) -> Dict:
        """Get system statistics and health information"""
        return {
            "ai_model_loaded": self.conversation_pipeline is not None,
            "model_name": self.model_name,
            "active_sessions": len(self.conversation_history),
            "total_conversations": sum(len(conv) for conv in self.conversation_history.values()),
            "fallback_mode": self.conversation_pipeline is None
        }
