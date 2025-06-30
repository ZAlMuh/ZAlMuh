# 🤖 Single Bot Mode Deployment Guide

This guide shows you how to deploy your Arabic Telegram Bot using **ONLY your main bot token** with the other 16 tokens as backup.

## 🎯 **Single Bot Architecture**

```
100,000 Users
     ↓
All connect to MAIN BOT
(5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM)
     ↓
Single FastAPI Application
     ↓
Supabase Database + Redis Cache
     ↓
16 Backup Tokens Available for Failover
```

## ⚡ **Benefits of Single Bot Mode:**

### **Pros:**
- ✅ **Simpler Setup**: Only one webhook to manage
- ✅ **Easier Monitoring**: Single bot to track
- ✅ **Consistent Experience**: All users on same bot
- ✅ **Backup Ready**: 16 tokens available for failover
- ✅ **Lower Complexity**: No sharding logic needed

### **Cons:**
- ⚠️ **Telegram Limits**: ~30 messages/second maximum
- ⚠️ **Single Point**: If main bot fails, all users affected
- ⚠️ **Capacity**: Recommended for up to 15,000-20,000 active users

## 🚀 **Deployment Steps**

### **Step 1: Configure for Single Bot Mode**

Your `.env` file should have:
```bash
# MAIN bot (handles all users)
BOT_TOKEN_MAIN=5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM

# Enable single bot mode
USE_SINGLE_BOT=true

# Your Supabase credentials
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Other settings...
```

### **Step 2: Deploy to Render.com**

1. **Create Web Service** in Render Dashboard
2. **Environment Variables** (add these in Render):
   ```bash
   BOT_TOKEN_MAIN=5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM
   USE_SINGLE_BOT=true
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   REDIS_URL=redis://localhost:6379
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

3. **Build Settings**:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

### **Step 3: Set Up Single Bot Webhook**

After deployment, run:
```bash
python setup_webhooks_single.py setup https://your-app.onrender.com
```

This sets **ONE webhook** for your main bot:
- Webhook URL: `https://your-app.onrender.com/webhook`
- Only the main bot token gets the webhook
- All other tokens remain as backup (no webhooks)

### **Step 4: Verify Setup**

```bash
# Check webhook status
python setup_webhooks_single.py status

# Check bot info
python setup_webhooks_single.py info

# Test the application
curl https://your-app.onrender.com/health
```

## 📊 **Performance Expectations**

### **Capacity:**
- **Maximum**: ~30 messages/second (Telegram limit)
- **Recommended Users**: 15,000-20,000 active users
- **Peak Traffic**: ~1,800 requests/minute
- **Response Time**: <2 seconds average

### **Traffic Distribution:**
```
All 100,000 Users → Single Main Bot → Database
```

## 🔧 **Monitoring Single Bot Mode**

### **Health Check Endpoints:**
```bash
# Application health
GET https://your-app.onrender.com/health

# Bot statistics
GET https://your-app.onrender.com/stats
# Returns: {"mode": "single_bot", "active_shards": 1, "primary_bot_id": 0}

# Basic health
GET https://your-app.onrender.com/
```

### **Bot Statistics Response:**
```json
{
  "mode": "single_bot",
  "active_shards": 1,
  "total_bots": 1,
  "shard_ids": [0],
  "primary_bot_id": 0,
  "backup_tokens_available": 16
}
```

## 🛠️ **Failover Strategy**

### **If Main Bot Fails:**

1. **Quick Switch** (Manual):
   ```bash
   # Update environment variable in Render
   BOT_TOKEN_MAIN=7199941836:AAGc4YhuG93HgSYWYNVUbdf3VsqkF2Nhl9U
   
   # Redeploy service
   # Set new webhook
   python setup_webhooks_single.py setup https://your-app.onrender.com
   ```

2. **Automatic Failover** (Future Enhancement):
   - Monitor main bot health
   - Auto-switch to backup token
   - Update webhook automatically

### **Backup Token Priority:**
```
Primary:  5036504214:AAF4cZR-mvu-Q8z_WQYQaLmbzw-R2sybKFM
Backup 1: 7199941836:AAGc4YhuG93HgSYWYNVUbdf3VsqkF2Nhl9U
Backup 2: 6895814597:AAHtDIi6GGMWN_G9hvg-QmIcB5iX_aNm8WA
...and so on for 16 backup tokens
```

## 🔀 **Switching Between Modes**

### **To Enable Multi-Bot Mode:**
```bash
# In Render environment variables
USE_SINGLE_BOT=false

# Then run the multi-bot webhook setup
python setup_webhooks.py setup https://your-app.onrender.com
```

### **To Return to Single Bot Mode:**
```bash
# In Render environment variables
USE_SINGLE_BOT=true

# Then run the single bot webhook setup
python setup_webhooks_single.py setup https://your-app.onrender.com
```

## 📈 **Performance Optimization for Single Bot**

### **Database Optimization:**
- ✅ Ensure Arabic name indexes are created
- ✅ Use connection pooling (50 connections)
- ✅ Cache frequently accessed results

### **Application Optimization:**
- ✅ Redis caching with 1-hour TTL
- ✅ Rate limiting: 3 requests/minute per user
- ✅ Async processing for all operations

### **Render.com Optimization:**
- ✅ Use **Standard Plan** ($25/month) for better performance
- ✅ Enable **Auto-Deploy** from GitHub
- ✅ Set up **Health Check** monitoring

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"Bot manager not initialized"**:
   ```bash
   # Check logs in Render dashboard
   # Verify BOT_TOKEN_MAIN is set correctly
   ```

2. **Webhook not receiving updates**:
   ```bash
   python setup_webhooks_single.py delete
   python setup_webhooks_single.py setup https://your-app.onrender.com
   ```

3. **Database connection issues**:
   ```bash
   # Verify Supabase URL and key
   # Check if additional_tables.sql was run
   ```

4. **Rate limiting errors**:
   ```bash
   # Check Redis connection
   # Monitor rate limit logs in Render
   ```

### **Log Analysis:**
```bash
# In Render logs, look for:
grep "single_bot" logs.txt     # Bot mode confirmation
grep "webhook" logs.txt        # Webhook requests
grep "ERROR" logs.txt          # Any errors
```

## 💰 **Cost Estimate (Single Bot Mode)**

- **Render Web Service**: $25/month (Standard)
- **Render Redis**: $7/month (optional)
- **Supabase**: Free tier (up to 500MB)
- **Total**: ~$32/month

Much cheaper than multi-bot mode since you only use one service instance!

## 🎯 **Recommended Usage**

### **Single Bot Mode is Perfect For:**
- ✅ **Student exam results** (moderate traffic)
- ✅ **Regional services** (limited user base)
- ✅ **Testing and development**
- ✅ **Budget-conscious deployments**
- ✅ **Simple management requirements**

### **Consider Multi-Bot Mode If:**
- ❌ Expecting >20,000 concurrent users
- ❌ Peak traffic >30 messages/second
- ❌ Need maximum redundancy
- ❌ National-scale deployment

## 🎉 **Final Verification**

After deployment, verify everything works:

1. **Send `/start`** to your main bot
2. **Try Arabic name search**: "محمد أحمد"
3. **Try exam number search**: "272591110430082"
4. **Check response time** is under 2 seconds
5. **Verify database connectivity** with health endpoint

Your single bot setup is now ready to handle thousands of students checking their exam results! 📚🇮🇶