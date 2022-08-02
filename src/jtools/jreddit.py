"""
Module for creating a RedditScript class that authorizes with Reddit via the OAuth client-credentials grant type. The RedditScript 
class provides an access token to be be used for simple userless API access. One or more methods for this type of access are included. 

For other API access, use the PRAW API wrapper instead. 
"""
import requests
import json
from datetime import datetime, timedelta
import os.path


class RedditScript():

    def __init__(self, client_id="UarOpRNv1XfXlA", client_secret="oe0UkFwP1STezDjkL5RfCYS01oU", user_agent="that ole diet-coke bot v1"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.token = self.get_client_credentials_token()

    def get_client_credentials_token(self):
        """Requests and caches an access token from Reddit using the OAuth client-credentials grant type.

            defaults to using the client id and secret for the "random getter" app registered to u/diet-coke-or-kill-me
        """
        TOKEN_CACHE_FILE = os.path.dirname(__file__) +  '/access_token.txt'
        # Check if cached token has expired
        try:
            with open(TOKEN_CACHE_FILE, 'r') as f:
                cache = json.load(f)
                expiration = datetime.fromtimestamp(cache['expiration'])
                # Check that token still valid for at least 5 minutes
                if timedelta(minutes=5) < expiration - datetime.now(): 
                    return cache['access_token']
        except FileNotFoundError:
            pass
        
        # Request access token
        client_auth = requests.auth.HTTPBasicAuth(username=self.client_id, password=self.client_secret)
        data = {'grant_type': 'client_credentials'}
        headers = {'user-agent': self.user_agent}
        resp = requests.post('https://www.reddit.com/api/v1/access_token',
            auth=client_auth,
            data=data,
            headers=headers)
        
        if resp.ok:
            token = resp.json()['access_token']
            # Cache the token and the time it expires
            with open(TOKEN_CACHE_FILE, 'w') as f:
                # 90% (safety factor) of the "expires_in" value from the http access token response (converted to hours)
                time_to_expiration = 0.9 * float(resp.json()['expires_in']) / 3600 
                expiration = datetime.now() + timedelta(hours=time_to_expiration) 
                cache = {'access_token': token, 'expiration': expiration.timestamp()}
                json.dump(cache, f, indent=2)
            return token
        else:
            return None

    
    def subreddit_is_banned(self, subreddit):
        """"Checks whether a subreddit is banned."""
        headers = {'Authorization': f'bearer {self.token}', 'user-agent': self.user_agent}
        r = requests.get(f'https://oauth.reddit.com/r/{subreddit}.json', headers=headers)
        jdict = r.json()
        if r.ok:
            return False
        elif r.status_code == 404:
            if 'reason' in jdict:
                if jdict['reason'] == 'banned':
                    return True
        else:
            return None