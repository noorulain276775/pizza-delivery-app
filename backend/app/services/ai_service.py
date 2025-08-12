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
        
        # Initialize enhanced knowledge immediately
        self._setup_enhanced_knowledge()
        
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
                # Add a small delay to ensure the thread starts properly
                import time
                time.sleep(1)
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
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info("Tokenizer loaded successfully")
            
            logger.info("Loading model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=hf_token,
                cache_dir=cache_dir
            )
            logger.info("Model loaded successfully")
            
            logger.info("Creating conversation pipeline...")
            # Create conversation pipeline with proper configuration
            self.conversation_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=self.max_length,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                top_p=0.9,
                top_k=50
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
        """Setup intelligent fallback system if AI models fail"""
        logger.warning("Setting up intelligent fallback system - AI models unavailable")
        self.conversation_pipeline = None
        self.model = None
        self.tokenizer = None
        self._initializing = False
        
        # Initialize enhanced pizza knowledge for better responses
        self._setup_enhanced_knowledge()
    
    def _setup_enhanced_knowledge(self):
        """Setup enhanced knowledge base for more intelligent responses"""
        self.enhanced_knowledge = {
            "pepperoni": {
                "description": "Spicy pepperoni slices with melted mozzarella cheese on our signature crust",
                "price": "14.99",
                "toppings": "Pepperoni, mozzarella cheese",
                "popularity": "Our most popular pizza",
                "spice_level": "Medium spicy",
                "cooking_time": "12-15 minutes"
            },
            "margherita": {
                "description": "Classic tomato sauce with fresh mozzarella cheese and basil on traditional crust",
                "price": "12.99",
                "toppings": "Tomato sauce, mozzarella, basil",
                "popularity": "Traditional favorite",
                "spice_level": "Mild",
                "cooking_time": "10-12 minutes"
            },
            "vegetarian": {
                "description": "Fresh vegetables including bell peppers, mushrooms, onions, and olives with mozzarella",
                "price": "13.99",
                "toppings": "Bell peppers, mushrooms, onions, olives, mozzarella",
                "popularity": "Healthy choice",
                "spice_level": "Mild",
                "cooking_time": "12-15 minutes"
            },
            "delivery": {
                "standard": "30-45 minutes",
                "express": "20-30 minutes (additional $3)",
                "free_threshold": "25",
                "areas": "All local areas within 10 miles",
                "tracking": "Real-time order tracking available"
            },
            "toppings": {
                "extra_cheese": "1.99",
                "mushrooms": "1.99",
                "bell_peppers": "1.99",
                "onions": "1.99",
                "olives": "1.99",
                "pepperoni": "2.99",
                "sausage": "2.99"
            }
        }
    
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
        Generate intelligent response to user message using AI or enhanced knowledge
        
        Args:
            user_message: User's input message
            session_id: Unique session identifier for conversation history
            
        Returns:
            Intelligent response string
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
            
            # Generate response using AI if available, otherwise use enhanced knowledge
            if self.conversation_pipeline and self.is_ai_available():
                response = self._generate_ai_response(user_message, session_id)
            else:
                # Use enhanced context-aware responses
                response = self._generate_context_aware_rule_response(user_message, session_id)
            
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
        """Generate intelligent AI response using conversation context"""
        try:
            # Prepare conversation context
            context = self._prepare_conversation_context(session_id)
            
            # Create a more intelligent prompt
            if context:
                # Use context for better understanding
                prompt = f"{context}{user_message}"
            else:
                # First message - give it a persona
                prompt = f"You are a helpful pizza delivery customer service assistant. Be friendly, knowledgeable, and helpful. User: {user_message}"
            
            # Generate response using the pipeline
            generated = self.conversation_pipeline(
                prompt,
                max_length=len(prompt.split()) + 80,  # Allow longer responses
                num_return_sequences=1,
                do_sample=True,
                temperature=0.8,  # Slightly higher for more creative responses
                repetition_penalty=1.3,
                top_p=0.9,
                top_k=50
            )
            
            # Extract and clean the response
            response = generated[0]['generated_text']
            response = self._clean_ai_response(response, prompt)
            
            # If response is too short or generic, enhance it
            if len(response.strip()) < 20 or response.strip() in ["I don't know", "I'm not sure", "I can't help with that"]:
                response = self._enhance_with_domain_knowledge(user_message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            # Fall back to rule-based but try to be more context-aware
            return self._generate_context_aware_rule_response(user_message, session_id)
    
    def _prepare_conversation_context(self, session_id: str) -> str:
        """Prepare conversation context from history for better AI responses"""
        if session_id not in self.conversation_history:
            return ""
        
        # Get last 4 exchanges (8 messages) for better context
        recent_messages = self.conversation_history[session_id][-8:]
        if not recent_messages:
            return ""
        
        # Build a more structured context
        context_parts = []
        for msg in recent_messages:
            if msg["role"] == "user":
                context_parts.append(f"User: {msg['content']}")
            else:
                context_parts.append(f"Assistant: {msg['content']}")
        
        # Join with proper spacing for better AI understanding
        context = " ".join(context_parts)
        
        # Add conversation starter to guide the AI
        if len(context_parts) >= 2:
            context = f"Previous conversation: {context}\n\nUser: "
        
        return context
    
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
        """Intelligently enhance AI response with pizza domain knowledge"""
        user_message_lower = user_message.lower()
        
        # Check for specific pizza-related queries with better context understanding
        if any(word in user_message_lower for word in ["menu", "pizza", "available", "what do you have"]):
            if "pepperoni" in user_message_lower:
                return "Our Pepperoni Pizza is a customer favorite! It features spicy pepperoni slices with melted mozzarella cheese on our signature crust. Priced at $14.99, it's perfect for meat lovers. Would you like to know about delivery options or place an order?"
            elif "margherita" in user_message_lower:
                return "Our Margherita Pizza is a classic choice! It's made with fresh tomato sauce, mozzarella cheese, and basil on our traditional crust. At $12.99, it's our most affordable option and perfect for those who love traditional Italian flavors."
            elif "vegetarian" in user_message_lower:
                return "Our Vegetarian Pizza is loaded with fresh vegetables including bell peppers, mushrooms, onions, and olives with mozzarella. Priced at $13.99, it's a healthy and delicious choice for everyone!"
            else:
                menu_info = "\n\nHere's our complete menu:\n" + "\n".join(self.pizza_knowledge["menu"])
                return ai_response + menu_info + "\n\nWhich pizza interests you most? I can tell you more about any specific one!"
        
        elif any(word in user_message_lower for word in ["price", "cost", "how much", "expensive"]):
            if "pepperoni" in user_message_lower:
                return "Our Pepperoni Pizza is $14.99 - it's our premium meat pizza and worth every penny! We also offer free delivery on orders over $25."
            elif "margherita" in user_message_lower:
                return "Our Margherita Pizza is $12.99 - it's our most affordable option and perfect for budget-conscious customers. Plus, free delivery on orders over $25!"
            elif "vegetarian" in user_message_lower:
                return "Our Vegetarian Pizza is $13.99 - great value for a pizza loaded with fresh vegetables. And remember, free delivery on orders over $25!"
            else:
                price_info = "\n\nOur pricing:\n" + "\n".join(self.pizza_knowledge["prices"])
                return ai_response + price_info + "\n\nAll our pizzas come with free delivery on orders over $25!"
        
        elif any(word in user_message_lower for word in ["delivery", "time", "how long", "fast", "when"]):
            delivery_info = "\n\nOur delivery options:\n" + "\n".join(self.pizza_knowledge["delivery"])
            return ai_response + delivery_info + "\n\nWhere would you like your pizza delivered? I can help you estimate the exact time for your area!"
        
        elif any(word in user_message_lower for word in ["payment", "pay", "cash", "card", "credit", "how to pay"]):
            payment_info = "\n\nWe accept:\n" + "\n".join(self.pizza_knowledge["payment"])
            return ai_response + payment_info + "\n\nCash on delivery is our most popular option - you pay when your pizza arrives!"
        
        elif any(word in user_message_lower for word in ["order", "buy", "purchase", "get", "place order"]):
            return "Great! To place your order, you can use our website or mobile app. Select your pizzas, choose delivery options, and we'll get it to you fast! What would you like to order today?"
        
        elif any(word in user_message_lower for word in ["topping", "extra", "customize"]):
            return "We offer a variety of toppings including extra cheese, mushrooms, bell peppers, onions, olives, and more! Each topping is $1.99 extra. What would you like to add to your pizza?"
        
        return ai_response
    
    def _generate_context_aware_rule_response(self, user_message: str, session_id: str) -> str:
        """Generate intelligent context-aware responses using enhanced knowledge"""
        user_message_lower = user_message.lower()
        
        # Check conversation history for context
        if session_id in self.conversation_history:
            recent_messages = self.conversation_history[session_id][-6:]  # Last 3 exchanges
            
            # Look for context clues in recent messages
            context_keywords = []
            for msg in recent_messages:
                if msg["role"] == "user":
                    content_lower = msg["content"].lower()
                    if "pepperoni" in content_lower:
                        context_keywords.append("pepperoni")
                    elif "margherita" in content_lower:
                        context_keywords.append("margherita")
                    elif "vegetarian" in content_lower:
                        context_keywords.append("vegetarian")
                    elif "delivery" in content_lower or "time" in content_lower or "how long" in content_lower:
                        context_keywords.append("delivery")
                    elif "price" in content_lower or "cost" in content_lower or "how much" in content_lower:
                        context_keywords.append("price")
                    elif "topping" in content_lower:
                        context_keywords.append("toppings")
                    elif "menu" in content_lower or "what" in content_lower:
                        context_keywords.append("menu")
            
            # Handle follow-up questions based on context with enhanced knowledge
            if "pepperoni" in context_keywords:
                if any(word in user_message_lower for word in ["yes", "tell me", "about", "details", "what is", "want", "that one", "order"]):
                    pizza_info = self.enhanced_knowledge["pepperoni"]
                    return f"Great choice! Our Pepperoni Pizza is {pizza_info['description']}. It's {pizza_info['popularity']} and costs ${pizza_info['price']}. The {pizza_info['spice_level']} flavor comes from our premium pepperoni slices. Would you like to know about delivery options or add extra toppings?"
                
                elif any(word in user_message_lower for word in ["price", "cost", "how much"]):
                    return f"Our Pepperoni Pizza is ${self.enhanced_knowledge['pepperoni']['price']} - it's our premium meat pizza and worth every penny! We also offer free delivery on orders over ${self.enhanced_knowledge['delivery']['free_threshold']}."
                
                elif any(word in user_message_lower for word in ["topping", "extra", "add"]):
                    return f"You can customize your Pepperoni Pizza with extra toppings! Popular additions include extra cheese (${self.enhanced_knowledge['toppings']['extra_cheese']}), mushrooms (${self.enhanced_knowledge['toppings']['mushrooms']}), or even more pepperoni (${self.enhanced_knowledge['toppings']['pepperoni']}). What would you like to add?"
            
            elif "margherita" in context_keywords:
                if any(word in user_message_lower for word in ["yes", "tell me", "about", "details", "what is", "want", "that one", "order"]):
                    pizza_info = self.enhanced_knowledge["margherita"]
                    return f"Excellent choice! Our Margherita Pizza is {pizza_info['description']}. It's {pizza_info['popularity']} and costs ${pizza_info['price']}. The {pizza_info['spice_level']} flavor is perfect for those who love traditional Italian taste. Would you like to know about delivery options or add extra toppings?"
                
                elif any(word in user_message_lower for word in ["price", "cost", "how much"]):
                    return f"Our Margherita Pizza is ${self.enhanced_knowledge['margherita']['price']} - it's our most affordable option and perfect for budget-conscious customers. Plus, free delivery on orders over ${self.enhanced_knowledge['delivery']['free_threshold']}!"
                
                elif any(word in user_message_lower for word in ["topping", "extra", "add"]):
                    return f"You can customize your Margherita Pizza with extra toppings! Popular additions include extra cheese (${self.enhanced_knowledge['toppings']['extra_cheese']}), mushrooms (${self.enhanced_knowledge['toppings']['mushrooms']}), or even pepperoni (${self.enhanced_knowledge['toppings']['pepperoni']}). What would you like to add?"
            
            elif "vegetarian" in context_keywords:
                if any(word in user_message_lower for word in ["yes", "tell me", "about", "details", "what is", "want", "that one", "order"]):
                    pizza_info = self.enhanced_knowledge["vegetarian"]
                    return f"Healthy choice! Our Vegetarian Pizza is {pizza_info['description']}. It's {pizza_info['popularity']} and costs ${pizza_info['price']}. The {pizza_info['spice_level']} flavor is perfect for everyone. Would you like to know about delivery options or add extra toppings?"
                
                elif any(word in user_message_lower for word in ["price", "cost", "how much"]):
                    return f"Our Vegetarian Pizza is ${self.enhanced_knowledge['vegetarian']['price']} - great value for a pizza loaded with fresh vegetables. And remember, free delivery on orders over ${self.enhanced_knowledge['delivery']['free_threshold']}!"
                
                elif any(word in user_message_lower for word in ["topping", "extra", "add"]):
                    return f"You can customize your Vegetarian Pizza with extra toppings! Popular additions include extra cheese (${self.enhanced_knowledge['toppings']['extra_cheese']}), mushrooms (${self.enhanced_knowledge['toppings']['mushrooms']}), or even pepperoni (${self.enhanced_knowledge['toppings']['pepperoni']}). What would you like to add?"
            
            elif "delivery" in context_keywords:
                if any(word in user_message_lower for word in ["what about", "toppings", "extra", "add"]):
                    toppings_list = [f"{topping} ({price})" for topping, price in self.enhanced_knowledge["toppings"].items()]
                    return f"We offer a variety of delicious toppings: {', '.join(toppings_list)}. Each topping is added to your pizza for extra flavor and customization. What would you like to add to make your pizza perfect?"
                else:
                    delivery_info = self.enhanced_knowledge["delivery"]
                    return f"Our delivery times are: Standard delivery takes {delivery_info['standard']}, or you can choose Express delivery for {delivery_info['express']} with an additional $3 fee. We also offer free delivery on orders over ${delivery_info['free_threshold']}! Plus, we provide {delivery_info['tracking']} so you know exactly when your pizza will arrive."
            
            elif "price" in context_keywords:
                if any(word in user_message_lower for word in ["how much", "cost", "expensive"]):
                    return f"Our pizza prices are: Margherita ${self.enhanced_knowledge['margherita']['price']}, Pepperoni ${self.enhanced_knowledge['pepperoni']['price']}, and Vegetarian ${self.enhanced_knowledge['vegetarian']['price']}. We also offer free delivery on orders over ${self.enhanced_knowledge['delivery']['free_threshold']}, making it a great value!"
            
            elif "toppings" in context_keywords:
                if any(word in user_message_lower for word in ["what", "available", "options"]):
                    toppings_list = [f"{topping} ({price})" for topping, price in self.enhanced_knowledge["toppings"].items()]
                    return f"We offer a variety of delicious toppings: {', '.join(toppings_list)}. Each topping is added to your pizza for extra flavor and customization. What would you like to add to make your pizza perfect?"
            
            elif "menu" in context_keywords:
                if any(word in user_message_lower for word in ["yes", "tell me", "about", "details", "what is", "want", "that one", "order", "pepperoni", "margherita", "vegetarian"]):
                    # User is asking about a specific pizza after seeing the menu
                    if "pepperoni" in user_message_lower:
                        pizza_info = self.enhanced_knowledge["pepperoni"]
                        return f"Great choice! Our Pepperoni Pizza is {pizza_info['description']}. It's {pizza_info['popularity']} and costs {pizza_info['price']}. The {pizza_info['spice_level']} flavor comes from our premium pepperoni slices. Would you like to know about delivery options or add extra toppings?"
                    elif "margherita" in user_message_lower:
                        pizza_info = self.enhanced_knowledge["margherita"]
                        return f"Excellent choice! Our Margherita Pizza is {pizza_info['description']}. It's {pizza_info['popularity']} and costs {pizza_info['price']}. The {pizza_info['spice_level']} flavor is perfect for those who love traditional Italian taste. Would you like to know about delivery options or add extra toppings?"
                    elif "vegetarian" in user_message_lower:
                        pizza_info = self.enhanced_knowledge["vegetarian"]
                        return f"Healthy choice! Our Vegetarian Pizza is {pizza_info['description']}. It's {pizza_info['popularity']} and costs {pizza_info['price']}. The {pizza_info['spice_level']} flavor is perfect for everyone. Would you like to know about delivery options or add extra toppings?"
        
        # Fall back to regular rule-based responses if no context found
        return self._generate_rule_based_response(user_message)
    
    def _generate_rule_based_response(self, user_message: str) -> str:
        """Generate conversational rule-based response as fallback"""
        user_message_lower = user_message.lower()
        
        # Greeting patterns
        if any(word in user_message_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            return "Hello! Welcome to Pizza Delivery! 🍕 I'm here to help you with everything pizza-related. I can tell you about our menu, prices, delivery options, and help you place orders. What would you like to know today?"
        
        # Menu queries
        elif any(word in user_message_lower for word in ["menu", "what", "available", "pizza", "what do you have"]):
            return "Here's our delicious menu:\n" + "\n".join(self.pizza_knowledge["menu"]) + "\n\nEach pizza is made with fresh ingredients and our signature crust. Which one sounds most delicious to you? I can tell you more about any specific pizza!"
        
        # Price queries
        elif any(word in user_message_lower for word in ["price", "cost", "how much", "expensive", "cheap"]):
            return "Our pricing is very competitive:\n" + "\n".join(self.pizza_knowledge["prices"]) + "\n\nWe also offer free delivery on orders over $25, making it an even better value! Which pizza are you interested in?"
        
        # Delivery queries
        elif any(word in user_message_lower for word in ["delivery", "time", "how long", "fast", "when", "deliver"]):
            return "We offer fast delivery:\n" + "\n".join(self.pizza_knowledge["delivery"]) + "\n\nWhere would you like your pizza delivered? I can help you estimate the exact delivery time for your area!"
        
        # Order status and tracking
        elif any(word in user_message_lower for word in ["status", "track", "where", "when", "order status", "tracking"]):
            return "Great question! We provide real-time order tracking so you know exactly when your pizza will arrive. Once you place an order, you'll get a tracking link to monitor your delivery. Would you like to place an order now?"
        
        # Order queries
        elif any(word in user_message_lower for word in ["order", "buy", "purchase", "get", "place order", "want to order", "ready to order"]):
            return "Excellent choice! 🎉 To place your order, you can use our website or mobile app. You can select your pizzas, add extra toppings, choose delivery options, and we'll get it to you fast! What would you like to order today?"
        
        # Payment queries
        elif any(word in user_message_lower for word in ["payment", "pay", "cash", "card", "credit", "how to pay", "payment method"]):
            return "We accept multiple payment methods:\n" + "\n".join(self.pizza_knowledge["payment"]) + "\n\nCash on delivery is our most popular option - you pay when your delicious pizza arrives! What's your preferred payment method?"
        
        # Thank you
        elif any(word in user_message_lower for word in ["thank", "thanks", "appreciate", "thank you"]):
            return "You're very welcome! 😊 I'm here to make your pizza experience amazing. Is there anything else I can help you with today? Maybe you'd like to know about our special toppings or delivery areas?"
        
        # Toppings and customization
        elif any(word in user_message_lower for word in ["topping", "extra", "customize", "add", "more"]):
            return "Great question! We offer a variety of delicious toppings including extra cheese, mushrooms, bell peppers, onions, olives, and more! Each topping is just $1.99 extra. What would you like to add to make your pizza perfect?"
        
        # Special offers and deals
        elif any(word in user_message_lower for word in ["deal", "offer", "special", "discount", "promotion"]):
            return "We have great deals! 🎉 Free delivery on orders over $25, and we often run special promotions. Our current special is 10% off when you order 2 or more pizzas! What would you like to order?"
        
        # Default response
        else:
            return "I'm here to help with your pizza delivery needs! 🍕 You can ask me about our menu, prices, delivery options, toppings, or how to place an order. What would you like to know? I'm excited to help you find the perfect pizza!"
    
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
    
    def test_ai_model(self) -> Dict:
        """Test the AI model to ensure it's working properly"""
        try:
            if not self.conversation_pipeline:
                return {
                    "status": "failed",
                    "error": "AI pipeline not available",
                    "fallback_mode": True
                }
            
            # Test with a simple prompt
            test_prompt = "Hello, I'm interested in your pizza menu."
            test_response = self.conversation_pipeline(
                test_prompt,
                max_length=len(test_prompt.split()) + 30,
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7
            )
            
            if test_response and len(test_response) > 0:
                return {
                    "status": "success",
                    "test_response": test_response[0]['generated_text'][:100] + "...",
                    "fallback_mode": False
                }
            else:
                return {
                    "status": "failed",
                    "error": "No response generated",
                    "fallback_mode": True
                }
                
        except Exception as e:
            logger.error(f"AI model test failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "fallback_mode": True
            }
    
    def get_system_stats(self) -> Dict:
        """Get system statistics and health information"""
        return {
            "ai_model_loaded": self.conversation_pipeline is not None,
            "model_name": self.model_name,
            "active_sessions": len(self.conversation_history),
            "total_conversations": sum(len(conv) for conv in self.conversation_history.values()),
            "fallback_mode": self.conversation_pipeline is None
        }
