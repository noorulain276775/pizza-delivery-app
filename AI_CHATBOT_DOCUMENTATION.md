# AI Chatbot Technical Documentation

Comprehensive technical implementation details for the AI-powered customer support chatbot in the Pizza Delivery Application.

## Overview

The AI chatbot is a sophisticated customer support system that leverages Hugging Face Transformers to provide intelligent, context-aware responses to customer queries. It's specifically designed for pizza delivery business operations and can handle a wide range of customer interactions.

## Technical Architecture

### System Components
```
AI Chatbot System
├── Backend Service Layer
│   ├── AI Service (PizzaAIService)
│   ├── Chat Routes (chat_bp)
│   └── Rate Limiting (Flask-Limiter)
├── AI Model Layer
│   ├── Hugging Face Transformers
│   ├── DialoGPT-medium Model
│   └── Tokenizer & Pipeline
├── Frontend Integration
│   ├── React Chatbot Component
│   ├── Real-time Messaging
│   └── Session Management
└── Data Layer
    ├── Conversation History
    ├── Session Storage
    └── Performance Metrics
```

### Technology Stack
- **AI Framework**: Hugging Face Transformers
- **Model**: Microsoft DialoGPT-medium (345M parameters)
- **Backend**: Flask with Python
- **Frontend**: React.js
- **Rate Limiting**: Flask-Limiter
- **Deep Learning**: PyTorch

## Implementation Details

### Backend Implementation

#### AI Service Class
Located in `backend/app/services/ai_service.py`:

```python
class PizzaAIService:
    def __init__(self, config):
        self.model_name = getattr(config, 'AI_MODEL_NAME', 'microsoft/DialoGPT-medium')
        self.max_length = getattr(config, 'AI_MAX_LENGTH', 100)
        self.temperature = getattr(config, 'AI_TEMPERATURE', 0.7)
        self.tokenizer = None
        self.model = None
        self.conversation_pipeline = None
        self.conversation_history = {}
        self.pizza_knowledge = {...}
        self._initializing = True
        self._load_models()
```

#### Key Methods
- **`_load_models()`**: Downloads and initializes AI models with proper error handling
- **`generate_response()`**: Main response generation logic with fallback support
- **`_generate_ai_response()`**: AI-powered response generation using DialoGPT
- **`_generate_rule_based_response()`**: Fallback rule-based responses when AI is unavailable

#### Model Loading Process
```python
def _load_models(self):
    try:
        logger.info(f"Loading AI models: {self.model_name}")
        hf_token = os.environ.get('HUGGING_FACE_HUB_TOKEN')
        cache_dir = os.environ.get('HUGGING_FACE_HUB_CACHE_DIR')
        
        from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            token=hf_token,
            cache_dir=cache_dir
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            token=hf_token,
            cache_dir=cache_dir
        )
        
        self.conversation_pipeline = pipeline(
            "conversational",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        logger.info("AI models loaded successfully")
        self._initializing = False
    except Exception as e:
        logger.error(f"Error loading AI models: {e}")
        logger.warning("Falling back to rule-based responses")
        self._setup_fallback()
        self._initializing = False
```

### API Endpoints

#### Chat Endpoints
- **`POST /api/chat/`**: Main chat interface
- **`GET /api/chat/history/<session_id>`**: Retrieve chat history
- **`DELETE /api/chat/clear/<session_id>`**: Clear chat history
- **`GET /api/chat/stats`**: Get usage statistics
- **`GET /api/chat/health`**: Health check endpoint
- **`GET /api/chat/help`**: Help information

#### Rate Limiting Implementation
```python
# Manual rate limiting application in chat_routes.py
@chat_bp.route('/', methods=['POST'])
def chat():
    limiter = current_app.extensions['limiter']
    limiter.limit("20 per minute")(lambda: None)()
    # Chat implementation
```

### AI Model Details

#### DialoGPT-medium
- **Model Size**: 345M parameters
- **Training Data**: Reddit conversations
- **Context Length**: 1024 tokens
- **Response Quality**: High-quality conversational responses
- **Memory Usage**: ~500MB RAM
- **Initialization**: Asynchronous loading to prevent server blocking

#### Tokenization Process
```python
def _prepare_conversation_context(self, message, session_id):
    history = self.conversation_history.get(session_id, [])
    context = " ".join([msg["content"] for msg in history[-5:]])
    return f"{context} {message}".strip()
```

### Domain Knowledge Integration

#### Pizza Business Rules
```python
self.pizza_knowledge = {
    "menu": ["Margherita Pizza - Classic tomato and mozzarella", 
             "Pepperoni Pizza - Spicy pepperoni and cheese", 
             "Vegetarian Pizza - Fresh vegetables and cheese"],
    "prices": ["Margherita: $12.99", "Pepperoni: $14.99", "Vegetarian: $13.99"],
    "delivery": ["Standard delivery: 30-45 minutes", 
                 "Express delivery: 20-30 minutes (additional $3)", 
                 "Free delivery on orders over $25"],
    "payment": ["Cash on delivery", "Credit card", "Digital wallets accepted"]
}
```

#### Response Enhancement
```python
def _enhance_with_domain_knowledge(self, response, user_message):
    # Enhance AI responses with business-specific information
    if "pizza" in user_message.lower():
        response += f" {random.choice(self.pizza_knowledge['menu'])}"
    return response
```

## Frontend Integration

### React Component Structure

#### Chatbot Component
Located in `frontend/src/components/Chatbot.js`:

```javascript
const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
};
```

#### Key Features
- **Floating Interface**: Always accessible chat button with professional styling
- **Real-time Messaging**: Instant message display with typing indicators
- **Session Management**: Persistent chat history using UUID session IDs
- **Auto-scrolling**: Smooth conversation flow
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Responsive Design**: Mobile-first approach with modern UI/UX

### API Communication

#### Message Sending
```javascript
const sendMessage = async () => {
  try {
    const response = await axios.post(
      `${API_CONFIG.BASE_URL}/api/chat/`,
      {
        message: inputMessage,
        session_id: sessionId
      }
    );
    // Handle response
  } catch (error) {
    // Error handling
  }
};
```

#### Session Management
```javascript
useEffect(() => {
  if (!sessionId) {
    const newSessionId = uuidv4();
    setSessionId(newSessionId);
  }
}, [sessionId]);
```

## Configuration & Environment

### Environment Variables
```bash
# Required for AI functionality
AI_MODEL_NAME=microsoft/DialoGPT-medium
AI_MAX_LENGTH=100
AI_TEMPERATURE=0.7

# Optional Hugging Face configuration
HUGGING_FACE_HUB_TOKEN=your_hf_token_here
HUGGING_FACE_HUB_CACHE_DIR=~/.cache/huggingface
HF_HUB_DISABLE_SYMLINKS_WARNING=1
```

### Flask Configuration
```python
# In config.py
class Config:
    AI_MODEL_NAME = 'microsoft/DialoGPT-medium'
    AI_MAX_LENGTH = 100
    AI_TEMPERATURE = 0.7
```

## Performance Optimization

### Asynchronous Model Loading
```python
def __init__(self, config):
    # ... other initialization
    self._initializing = True
    # Load models in background to prevent server blocking
    threading.Thread(target=self._load_models, daemon=True).start()
```

### Response Caching
```python
def get_cached_response(self, query):
    cache_key = f"chat_response:{hash(query)}"
    cached = self.redis_client.get(cache_key)
    if cached:
        return cached.decode('utf-8')
    return None
```

### Model Optimization
```python
# Use GPU if available for faster responses
device = 0 if torch.cuda.is_available() else -1
self.conversation_pipeline = pipeline(
    "conversational",
    model=self.model,
    tokenizer=self.tokenizer,
    device=device
)
```

## Security Considerations

### Data Protection
- **Session Isolation**: Separate conversation histories per user session
- **Data Encryption**: Secure transmission of messages over HTTPS
- **Access Control**: Rate limiting and request validation
- **Data Retention**: Configurable conversation history limits

### Input Validation
```python
def validate_message(self, message):
    # Sanitize user input
    if len(message) > 500:
        raise ValueError("Message too long")
    
    # Check for malicious content
    if any(word in message.lower() for word in self.blocked_words):
        raise ValueError("Message contains blocked content")
    
    return message.strip()
```

### Rate Limiting
```python
# Implement per-endpoint rate limiting
@limiter.limit("20 per minute")
def chat():
    # Chat implementation

# Implement burst protection
@limiter.limit("5 per 10 seconds")
def chat_burst():
    # Handle burst requests
```

## Monitoring & Analytics

### Health Monitoring
```python
def health_check(self):
    return {
        "status": "healthy",
        "model_loaded": self.model is not None,
        "initializing": self._initializing,
        "active_sessions": len(self.conversation_history),
        "fallback_mode": self.conversation_pipeline is None
    }
```

### Performance Metrics
```python
def track_response_time(self, func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        self.metrics.record_response_time(end_time - start_time)
        return result
    return wrapper
```

## Troubleshooting

### Common Issues & Solutions

#### AI Service Unavailable
**Problem**: Chatbot returns "AI service unavailable" messages
**Solutions**:
1. Check backend logs for AI model loading errors
2. Verify sufficient disk space (2GB+) for model downloads
3. Ensure PyTorch and transformers are properly installed
4. Check memory availability (4GB+ RAM recommended)
5. Verify internet connection for model downloads

#### Slow Response Times
**Problem**: Chatbot responses take too long
**Solutions**:
1. Check system memory usage during AI operations
2. Verify GPU availability (if using CUDA)
3. Monitor CPU usage during responses
4. Consider using smaller models for faster responses

#### Frontend Display Issues
**Problem**: Chatbot appears as white box or buttons look weird
**Solutions**:
1. Check CSS styling in `Chatbot.css`
2. Verify component state management
3. Ensure proper React component rendering
4. Check browser console for JavaScript errors

### Debug Commands
```bash
# Test AI service directly
python -c "
from app.services.ai_service import PizzaAIService
from config import DevelopmentConfig
config = DevelopmentConfig()
ai = PizzaAIService(config)
response = ai.generate_response('Hello', 'test_session')
print(response)
"

# Check model files
find ~/.cache/huggingface/ -name "*.bin" | head -5

# Test API endpoints
curl -X POST http://localhost:5000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'
```

## Current Status

✅ **AI Chatbot is fully functional and working**
- Backend AI service successfully loads DialoGPT-medium model
- Frontend chat interface properly integrated
- All API endpoints responding correctly
- Rate limiting and security measures in place
- Professional UI/UX with responsive design

## Future Enhancements

### AI Model Improvements
- **GPT-4 Integration**: Higher quality responses
- **Multi-language Support**: International customer support
- **Voice Integration**: Speech-to-text and text-to-speech
- **Image Recognition**: Handle photo-based queries

### Feature Enhancements
- **Proactive Suggestions**: Suggest relevant information
- **Personalization**: Remember user preferences
- **Multi-modal Interface**: Support images and voice
- **Offline Mode**: Basic responses without internet
- **Analytics Dashboard**: Customer interaction insights

---

**For setup instructions and general project information, see the main README.md file.**
