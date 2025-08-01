"""
Management command to test X/Twitter API integration
Usage: python manage.py test_twitter_api
"""
from django.core.management.base import BaseCommand
from decouple import config
import requests
from requests_oauthlib import OAuth1


class Command(BaseCommand):
    help = 'Test X/Twitter API integration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing X/Twitter API Integration'))
        
        # Check if credentials are configured
        api_key = config("X_API_KEY", default="")
        api_secret = config("X_API_SECRET", default="")
        access_token = config("X_ACCESS_TOKEN", default="")
        access_token_secret = config("X_ACCESS_TOKEN_SECRET", default="")
        
        missing_creds = []
        if not api_key:
            missing_creds.append("X_API_KEY")
        if not api_secret:
            missing_creds.append("X_API_SECRET")
        if not access_token:
            missing_creds.append("X_ACCESS_TOKEN")
        if not access_token_secret:
            missing_creds.append("X_ACCESS_TOKEN_SECRET")
            
        if missing_creds:
            self.stdout.write(self.style.ERROR(
                f'Missing credentials: {", ".join(missing_creds)}'
            ))
            return
            
        self.stdout.write('API credentials found')
        
        # Test API connection using OAuth 1.0a
        try:
            # Set up OAuth 1.0a authentication
            auth = OAuth1(
                api_key,
                client_secret=api_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret,
                signature_method='HMAC-SHA1',
                signature_type='AUTH_HEADER'
            )
            
            # Test with account verification endpoint
            response = requests.get(
                'https://api.twitter.com/1.1/account/verify_credentials.json',
                auth=auth,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('screen_name', 'unknown')
                user_id = user_data.get('id_str', 'unknown')
                self.stdout.write(self.style.SUCCESS(
                    f'API connection successful! Connected as: @{username} '
                    f'(ID: {user_id})'
                ))
                
                # Test posting a tweet (optional)
                post_test = input('Do you want to test posting a tweet? (y/N): ').lower()
                if post_test == 'y':
                    test_tweet = {
                        'text': 'Testing Django News App X/Twitter integration! #Django #NewsApp #Test'
                    }
                    
                    post_response = requests.post(
                        'https://api.twitter.com/2/tweets',
                        auth=auth,
                        headers={'Content-Type': 'application/json'},
                        json=test_tweet,
                        timeout=10
                    )
                    
                    if post_response.status_code == 201:
                        tweet_data = post_response.json()
                        tweet_id = tweet_data.get('data', {}).get('id', 'unknown')
                        self.stdout.write(self.style.SUCCESS(
                            f'Test tweet posted successfully! Tweet ID: {tweet_id}'
                        ))
                    else:
                        error_data = (post_response.json() 
                                    if post_response.headers.get('content-type', '')
                                    .startswith('application/json') 
                                    else post_response.text)
                        self.stdout.write(self.style.ERROR(
                            f'Failed to post test tweet: {error_data}'
                        ))
                
            else:
                error_data = (response.json() 
                            if response.headers.get('content-type', '')
                            .startswith('application/json') 
                            else response.text)
                self.stdout.write(self.style.ERROR(
                    f'API connection failed. Status: {response.status_code}'
                ))
                self.stdout.write(self.style.ERROR(f'Error: {error_data}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Connection error: {e}'))
            
        self.stdout.write('\nX/Twitter API Setup Requirements:')
        self.stdout.write('1. Go to https://developer.twitter.com/en/portal/dashboard')
        self.stdout.write('2. Create a new app or use existing one')
        self.stdout.write('3. Set up OAuth 1.0a permissions (Read and Write)')
        self.stdout.write('4. Generate your API keys and tokens')
        self.stdout.write('5. Add them to your .env file:')
        self.stdout.write('   X_API_KEY=your_api_key_here')
        self.stdout.write('   X_API_SECRET=your_api_secret_here')
        self.stdout.write('   X_ACCESS_TOKEN=your_access_token_here')
        self.stdout.write('   X_ACCESS_TOKEN_SECRET=your_access_token_secret_here')
        self.stdout.write('\nImportant: Your app must have "Read and Write" permissions!')
