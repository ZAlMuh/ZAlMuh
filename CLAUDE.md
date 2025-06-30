# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a scalable Arabic Telegram bot designed to handle 50,000-100,000 concurrent users for exam result queries. The bot integrates with Supabase for data storage and external APIs for real-time result fetching.

## Architecture

- **Backend**: FastAPI with async processing
- **Database**: Supabase PostgreSQL with optimized indexes
- **Caching**: Redis for API responses and rate limiting
- **Scaling**: 5 bot token shards with load balancing
- **Deployment**: Docker containers with Nginx load balancer
- **Monitoring**: Prometheus + Grafana

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run locally
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose -f docker/docker-compose.yml up --build

# Run specific services
docker-compose -f docker/docker-compose.yml up redis nginx bot-shard-0

# Scale bot shards
docker-compose -f docker/docker-compose.yml up --scale bot-shard-0=2
```

### Testing
```bash
# Run unit tests
pytest tests/

# Run specific test files
pytest tests/test_validation.py
pytest tests/test_api.py

# Run load tests (100K users simulation)
python tests/load_test.py --users 1000 --duration 300

# Run load test with custom settings
python tests/load_test.py --url http://localhost --users 5000 --duration 600
```

### Database Setup
```bash
# Run the schema in Supabase SQL editor
# File: database_schema.sql

# The schema includes:
# - students: student information
# - exam_results: exam scores and results  
# - result_cache: API response caching
# - user_sessions: bot state management
# - rate_limits: rate limiting per user
# - analytics: usage tracking
```

## Key Components

### Bot Handlers (`app/bot/handlers.py`)
- **TelegramBotManager**: Manages multiple bot instances for sharding
- **BotHandlers**: Handles commands, callbacks, and text messages
- Arabic-only interface with inline keyboards
- Rate limiting and session management

### Database Layer (`app/database/`)
- **supabase_client.py**: Async Supabase operations
- **models.py**: Pydantic models for data validation
- Optimized queries for name search and exam number lookup

### External APIs (`app/external/`)
- **najah_api.py**: External exam result API client with retry logic
- **cache.py**: Redis caching with TTL and rate limiting
- Circuit breaker pattern for API failures

### Message System (`app/bot/`)
- **messages.py**: Arabic message templates
- **keyboards.py**: Inline keyboard layouts
- Formatted result displays and error handling

## Performance Features

### Scalability (100K Users)
- **Bot Sharding**: 5 tokens handling 20K users each
- **Load Balancing**: Nginx distributes based on user_id % 5
- **Connection Pooling**: 50 DB connections per instance
- **Async Processing**: Non-blocking I/O operations

### Caching Strategy
- **Redis Cache**: 1-hour TTL for API responses
- **Rate Limiting**: 3 requests/minute per user
- **Session Management**: User state persistence
- **Cache Keys**: Structured as `prefix:identifier`

### Database Optimization
- **Indexes**: On name (trigram), exam number, governorate
- **Fuzzy Search**: Using pg_trgm extension
- **Covering Indexes**: Reduce I/O for common queries
- **Cleanup Functions**: Automatic cache and rate limit cleanup

## Configuration

### Environment Variables (.env)
```bash
# Bot tokens (5 for sharding)
BOT_TOKEN_1=your_bot_token_1
BOT_TOKEN_2=your_bot_token_2
# ... up to BOT_TOKEN_5

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Redis
REDIS_URL=redis://localhost:6379

# External API
NAJAH_API_BASE_URL=https://serapi3.najah.iq

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=3
CACHE_TTL_SECONDS=3600
```

### Webhook Setup
- Set webhooks for each bot token to: `https://your-domain.com/webhook/{shard_id}`
- Shard IDs: 0, 1, 2, 3, 4
- Load balancer routes based on URL path

## Monitoring

### Health Endpoints
- `GET /health` - Detailed health check (Redis, DB, bots)
- `GET /stats` - Bot statistics and metrics
- `GET /` - Basic health check

### Metrics (Prometheus)
- Request rates per shard
- Response times
- Cache hit rates
- Error rates
- Active user sessions

## User Flow

### Stage 1: Welcome
- `/start` → Arabic welcome menu
- Two options: Name search | Exam number search

### Stage 2: Name Search
- User enters Arabic name
- Select governorate from list
- Display matching students (max 5)
- Click to view result

### Stage 3: Exam Number Search  
- User enters 15-digit exam number
- Direct API call to fetch result
- Display formatted result

### Stage 4: Result Display
- Formatted Arabic result with all subjects
- Share button for social sharing
- Return to main menu option

## Error Handling

### Rate Limiting
- 3 requests per minute per user
- Arabic error messages
- Graceful degradation

### API Failures
- Retry logic with exponential backoff
- Circuit breaker pattern
- Cached fallback responses

### Database Errors
- Connection pooling with failover
- Graceful error messages in Arabic
- Automatic reconnection

## Arabic Language Support

### Message Templates
- All UI text in Arabic
- Proper RTL text formatting
- Cultural context in messaging

### Validation
- Arabic name validation using Unicode ranges
- Governorate filtering
- Input sanitization

### Search
- Fuzzy Arabic text search using trigrams
- Similarity scoring for name matches
- Case-insensitive search

## Deployment

### Production Deployment
```bash
# Using Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# Using Kubernetes
kubectl apply -f deployment/k8s/

# Monitor with Grafana
# Access: http://localhost:3000 (admin/admin123)
```

### SSL Configuration
- Uncomment SSL block in `docker/nginx.conf`
- Place certificates in `docker/ssl/`
- Update webhook URLs to HTTPS

This bot architecture can handle peak loads during exam result announcements while maintaining fast response times and reliability.