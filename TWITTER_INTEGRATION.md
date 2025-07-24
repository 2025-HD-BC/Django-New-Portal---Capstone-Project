# X (Twitter) API Integration Guide

This Django News App includes automatic posting to X (formerly Twitter) when articles are approved by editors.

## 🔧 Setup Instructions

### 1. Create X Developer Account
1. Go to [X Developer Platform](https://developer.twitter.com/en/portal/dashboard)
2. Apply for a developer account if you don't have one
3. Create a new app or use an existing one

### 2. Generate API Credentials
You need to obtain the following credentials from your X Developer Portal:

- **API Key** (Consumer Key)
- **API Secret** (Consumer Secret)
- **Access Token**
- **Access Token Secret**
- **Bearer Token**

### 3. Configure Environment Variables
Add these credentials to your `.env` file:

```env
# X (Twitter) API Configuration
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
X_BEARER_TOKEN=your_bearer_token_here
```

### 4. Test the Integration
Run the test command to verify your setup:

```bash
python manage.py test_twitter_api
```

## 🚀 How It Works

### Automatic Posting
When an editor approves an article, the Django signal system automatically:

1. **Sends email notifications** to subscribers
2. **Posts to X/Twitter** with article details

### Tweet Format
The app creates tweets in this format:
```
📰 New Article: [Article Title] by [Author Username] [Article Link]
```

### Character Limits
- Respects X's 280-character limit
- Truncates content intelligently
- Always includes the article link when possible

## 🔍 Monitoring

### Debug Mode
When `DEBUG=True` in settings, you'll see console output for X API calls:
```
[SIGNAL] ✅ Successfully posted to X (Tweet ID: 1234567890): New Article: Breaking News...
[SIGNAL] ❌ Failed to post to X. Status: 401, Error: Unauthorized
```

### Production Mode
In production (`DEBUG=False`), errors are silently logged without disrupting the article approval process.

## 🛠️ API Details

### Endpoint Used
- **URL**: `https://api.twitter.com/2/tweets`
- **Method**: POST
- **Authentication**: Bearer Token (OAuth 2.0)

### Required Permissions
Your X app needs the following permissions:
- **Read and Write**: To post tweets
- **Tweet**: Basic tweet posting capability

### Rate Limits
X API v2 has rate limits:
- **User context**: 300 requests per 15-minute window
- **App context**: 300 requests per 15-minute window

## 🔒 Security Notes

1. **Never commit API keys** to version control
2. **Use environment variables** for all credentials
3. **Regenerate tokens** if they are compromised
4. **Monitor API usage** in X Developer Portal

## 🐛 Troubleshooting

### Common Issues

#### 1. "Invalid or expired token"
- Check that your Bearer Token is correct
- Verify token hasn't expired in X Developer Portal

#### 2. "Forbidden" (403 error)
- Ensure your app has write permissions
- Check that you're using the correct credentials

#### 3. "Tweet appears to be automated"
- X may flag repetitive content
- Vary your tweet formats or add randomness

#### 4. "Rate limit exceeded"
- Wait for rate limit window to reset
- Implement rate limiting in your application

### Debug Steps
1. Run `python manage.py test_twitter_api` to test credentials
2. Check Django console output for detailed error messages
3. Verify credentials in X Developer Portal
4. Test with a manual article approval

## 📚 API Documentation
- [X API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Authentication Guide](https://developer.twitter.com/en/docs/authentication/overview)
- [Tweet Management](https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/introduction)
