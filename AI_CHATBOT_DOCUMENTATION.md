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
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = None
        self.model = None
        self.conversation_pipeline = None
        self.conversation_history = {}
        self.pizza_knowledge = {...}
```

#### Key Methods
- **`_load_models()`**: Downloads and initializes AI models
- **`generate_response()`**: Main response generation logic
- **`_generate_ai_response()`**: AI-powered response generation
- **`_generate_rule_based_response()`**: Fallback rule-based responses

#### Model Loading Process
```python
def _load_models(self):
    try:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.conversation_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )
    except Exception as e:
        logger.error(f"Failed to load AI models: {e}")
        self._setup_fallback()
```

### API Endpoints

#### Chat Endpoints
- **`POST /api/chat/chat`**: Main chat interface
- **`GET /api/chat/history/<session_id>`**: Retrieve chat history
- **`DELETE /api/chat/clear/<session_id>`**: Clear chat history
- **`GET /api/chat/stats`**: Get usage statistics
- **`GET /api/chat/health`**: Health check endpoint
- **`GET /api/chat/help`**: Help information

#### Rate Limiting
```python
@chat_bp.route('/chat', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    # Chat implementation
```

### AI Model Details

#### DialoGPT-medium
- **Model Size**: 345M parameters
- **Training Data**: Reddit conversations
- **Context Length**: 1024 tokens
- **Response Quality**: High-quality conversational responses
- **Memory Usage**: ~500MB RAM

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
- **Floating Interface**: Always accessible chat button
- **Real-time Messaging**: Instant message display
- **Session Management**: Persistent chat history
- **Auto-scrolling**: Smooth conversation flow
- **Error Handling**: Graceful fallbacks

### API Communication

#### Message Sending
```javascript
const handleSendMessage = async () => {
  try {
    const response = await axios.post(
      `${API_CONFIG.BASE_URL}/api/chat/chat`,
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

## Performance Optimization

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
# Use smaller models for faster responses
self.model_name = "microsoft/DialoGPT-small"  # 117M parameters

# Implement response streaming
def stream_response(self, message):
    for token in self.model.generate_stream(message):
        yield token
```

## Security Considerations

### Data Protection
- **Session Isolation**: Separate conversation histories per user
- **Data Encryption**: Secure transmission of messages
- **Access Control**: Rate limiting and authentication
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
# Implement per-user rate limiting
@limiter.limit("20 per minute per user")
def chat():
    # Chat implementation

# Implement burst protection
@limiter.limit("5 per 10 seconds")
def chat_burst():
    # Handle burst requests
```

## Monitoring & Analytics

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

### Health Monitoring
```python
def health_check(self):
    return {
        "status": "healthy",
        "model_loaded": self.model is not None,
        "memory_usage": self.get_memory_usage(),
        "active_sessions": len(self.conversation_history),
        "response_time_avg": self.metrics.get_average_response_time()
    }
```

## Troubleshooting

### Common Issues

#### AI Models Not Loading
**Problem**: Models fail to download or load
**Solutions**:
1. Check internet connection
2. Verify sufficient disk space (2GB+)
3. Ensure PyTorch is properly installed
4. Check memory availability (4GB+ RAM recommended)

#### Slow Response Times
**Problem**: Chatbot responses take too long
**Solutions**:
1. Check system memory usage
2. Verify GPU availability (if using CUDA)
3. Monitor CPU usage during responses
4. Consider model optimization

### Debug Commands
```bash
# Test AI service directly
python -c "
from app.services.ai_service import PizzaAIService
ai = PizzaAIService()
response = ai.generate_response('Hello', 'test_session')
print(response)
"

# Check model files
find ~/.cache/huggingface/ -name "*.bin" | head -5
```

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

---

**For setup instructions and general project information, see the main README.md file.**
