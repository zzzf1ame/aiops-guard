# 🏗️ AIOpsGuard Architecture

## System Overview

AIOpsGuard is designed as a lightweight, non-invasive monitoring layer for LLM applications. It uses Python decorators to wrap existing functions without modifying their behavior.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Application                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    LLM Functions                         │  │
│  │                                                          │  │
│  │  @AIOpsGuard(agent_name="Agent1", model="gpt-4")        │  │
│  │  def my_llm_call(prompt: str) -> str:                   │  │
│  │      return llm_response                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AIOpsGuard Layer                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Decorator (guard.py)                    │  │
│  │                                                          │  │
│  │  • Intercept function calls                             │  │
│  │  • Extract input/output text                            │  │
│  │  • Measure execution time                               │  │
│  │  • Handle errors gracefully                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Token Counter (tiktoken)                    │  │
│  │                                                          │  │
│  │  • Count input tokens                                   │  │
│  │  • Count output tokens                                  │  │
│  │  • Model-specific encoding                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Cost Calculator (models.py)                 │  │
│  │                                                          │  │
│  │  • Get model pricing                                    │  │
│  │  • Calculate input cost                                 │  │
│  │  • Calculate output cost                                │  │
│  │  • Total cost computation                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
│                            ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Metrics Builder (models.py)                 │  │
│  │                                                          │  │
│  │  • Create CallMetrics object                            │  │
│  │  • Timestamp generation                                 │  │
│  │  • Success/failure tracking                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Storage Layer                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              CallTracker (tracker.py)                    │  │
│  │                                                          │  │
│  │  • Store call metrics                                   │  │
│  │  • Aggregate statistics                                 │  │
│  │  • Per-agent summaries                                  │  │
│  │  • Per-model summaries                                  │  │
│  │  • Global tracker instance                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Reporting Layer                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Rich Console (tracker.py)                   │  │
│  │                                                          │  │
│  │  • Format tables                                        │  │
│  │  • Generate reports                                     │  │
│  │  • Cost projections                                     │  │
│  │  • Terminal output                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Decorator Layer (`guard.py`)

**Purpose**: Intercept and monitor LLM function calls

**Key Classes**:
- `AIOpsGuard`: Main decorator class
- `get_global_tracker()`: Access global tracker instance

**Responsibilities**:
- Function wrapping
- Input/output extraction
- Execution timing
- Error handling
- Metrics creation

**Flow**:
```python
1. User calls decorated function
2. Decorator intercepts call
3. Extract input text
4. Start timer
5. Execute original function
6. Stop timer
7. Extract output text
8. Count tokens
9. Calculate costs
10. Create metrics
11. Store in tracker
12. Return result
```

### 2. Token Counting

**Library**: tiktoken (OpenAI's official tokenizer)

**Process**:
```python
1. Initialize encoding for model
2. Encode input text → token IDs
3. Count token IDs
4. Encode output text → token IDs
5. Count token IDs
6. Sum for total tokens
```

**Supported Encodings**:
- `cl100k_base`: GPT-4, GPT-3.5-turbo
- `p50k_base`: Older models
- Auto-detection by model name

### 3. Cost Calculation (`models.py`)

**ModelPricing Class**:
```python
Pricing per 1M tokens (USD):
├── GPT-4 Turbo: $10 input, $30 output
├── GPT-4: $30 input, $60 output
├── GPT-3.5 Turbo: $0.50 input, $1.50 output
├── Claude 3 Opus: $15 input, $75 output
├── Claude 3 Sonnet: $3 input, $15 output
└── Claude 3 Haiku: $0.25 input, $1.25 output
```

**Calculation**:
```python
input_cost = (input_tokens / 1_000_000) * input_price
output_cost = (output_tokens / 1_000_000) * output_price
total_cost = input_cost + output_cost
```

### 4. Metrics Storage (`models.py`)

**CallMetrics Dataclass**:
```python
@dataclass
class CallMetrics:
    agent_name: str              # Agent identifier
    model_name: str              # Model used
    input_tokens: int            # Input token count
    output_tokens: int           # Output token count
    total_tokens: int            # Sum of tokens
    input_cost_usd: float        # Input cost
    output_cost_usd: float       # Output cost
    total_cost_usd: float        # Total cost
    execution_time_seconds: float # Execution time
    timestamp: datetime          # Call timestamp
    success: bool                # Success flag
    error_message: Optional[str] # Error details
```

### 5. Tracking & Aggregation (`tracker.py`)

**CallTracker Class**:

**Data Structure**:
```python
calls: List[CallMetrics]  # All tracked calls
```

**Aggregation Methods**:
```python
get_summary()        # Overall statistics
get_agent_summary()  # Per-agent breakdown
get_model_summary()  # Per-model breakdown
```

**Statistics Computed**:
- Total/successful/failed calls
- Success rate
- Token usage (total, input, output, average)
- Cost (total, input, output, average)
- Execution time (total, average)
- Per-agent metrics
- Per-model metrics

### 6. Reporting (`tracker.py`)

**Rich Library Integration**:
```python
Console → Table → Panel → Text
```

**Report Sections**:
1. **Header Panel**: Title and timestamp
2. **Overall Statistics**: Aggregated metrics
3. **Per-Agent Breakdown**: Agent comparison
4. **Per-Model Breakdown**: Model comparison
5. **Cost Projections**: Future cost estimates

## Data Flow

### Single Call Flow

```
User Function Call
       │
       ▼
Decorator Intercepts
       │
       ├─→ Extract Input
       │   └─→ Count Tokens
       │
       ├─→ Start Timer
       │
       ├─→ Execute Function
       │
       ├─→ Stop Timer
       │
       ├─→ Extract Output
       │   └─→ Count Tokens
       │
       ├─→ Calculate Costs
       │
       ├─→ Create Metrics
       │
       └─→ Store in Tracker
       │
       ▼
Return Result to User
```

### Reporting Flow

```
User Calls print_summary()
       │
       ▼
Tracker Aggregates Data
       │
       ├─→ Calculate Overall Stats
       ├─→ Group by Agent
       ├─→ Group by Model
       └─→ Compute Projections
       │
       ▼
Rich Formats Tables
       │
       ├─→ Create Header Panel
       ├─→ Build Statistics Table
       ├─→ Build Agent Table
       ├─→ Build Model Table
       └─→ Build Projection Table
       │
       ▼
Output to Terminal
```

## Design Patterns

### 1. Decorator Pattern
- Non-invasive monitoring
- Transparent to user code
- Composable with other decorators

### 2. Singleton Pattern
- Global tracker instance
- Centralized metrics storage
- Consistent state across calls

### 3. Strategy Pattern
- Model-specific pricing
- Encoding selection
- Flexible cost calculation

### 4. Builder Pattern
- Metrics construction
- Report generation
- Table formatting

## Performance Considerations

### Overhead
- **Token Counting**: ~1-5ms per call
- **Cost Calculation**: <1ms per call
- **Metrics Storage**: <1ms per call
- **Total Overhead**: ~2-10ms per call

### Memory Usage
- **Per Call**: ~1KB (CallMetrics object)
- **1000 Calls**: ~1MB
- **10000 Calls**: ~10MB

### Optimization Strategies
1. Lazy evaluation of summaries
2. Efficient token counting (tiktoken)
3. Minimal data structure overhead
4. Optional auto-print (disabled by default)

## Extensibility

### Adding New Models
```python
# In models.py
class ModelPricing:
    NEW_MODEL_INPUT: float = 5.00
    NEW_MODEL_OUTPUT: float = 15.00
    
    @classmethod
    def get_pricing(cls, model_name: str):
        if "new-model" in model_lower:
            return (cls.NEW_MODEL_INPUT, cls.NEW_MODEL_OUTPUT)
```

### Custom Trackers
```python
# Create isolated tracker
my_tracker = CallTracker()

@AIOpsGuard(agent_name="Agent", tracker=my_tracker)
def my_function(prompt: str) -> str:
    return response
```

### Export Formats
```python
# Current: Dictionary
data = tracker.export_to_dict()

# Future: JSON, CSV, Database
tracker.export_to_json("metrics.json")
tracker.export_to_csv("metrics.csv")
tracker.export_to_db(connection)
```

## Security Considerations

### Data Privacy
- No data sent to external services
- All processing local
- User controls data retention

### Input/Output Handling
- Truncation for large texts (optional)
- Sanitization of error messages
- No logging of sensitive data

## Testing Strategy

### Unit Tests
- Token counting accuracy
- Cost calculation correctness
- Metrics creation
- Aggregation logic

### Integration Tests
- Decorator functionality
- Tracker storage
- Report generation
- Error handling

### Performance Tests
- Overhead measurement
- Memory usage tracking
- Scalability testing

## Future Enhancements

### Planned Features
1. Async function support
2. Database persistence
3. Web dashboard
4. Alert thresholds
5. Custom pricing
6. Batch operations
7. Historical analysis
8. Export formats

### Architecture Evolution
```
Current: In-memory storage
    ↓
Phase 2: Optional persistence
    ↓
Phase 3: Distributed tracking
    ↓
Phase 4: Real-time analytics
```
