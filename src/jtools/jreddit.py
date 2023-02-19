"""
Module for creating a RedditScript class that authorizes with Reddit via the OAuth client-credentials grant type. The RedditScript 
class provides an access token to be be used for simple userless API access. One or more methods for this type of access are included. 

For other user-based Reddit API access, use the PRAW API wrapper instead.
"""
import requests
import json
from datetime import datetime, timedelta
import os.path
import time


class RedditScript:

    def __init__(self, client_id="UarOpRNv1XfXlA", client_secret="oe0UkFwP1STezDjkL5RfCYS01oU", user_agent="that ole diet-coke bot v1"):
        """ defaults to using the client id and secret for the "random getter" app registered to u/diet-coke-or-kill-me
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.TOKEN_CACHE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '/../../resources/access_token.txt'))
        self.token = self.get_client_credentials_token()
        self.last_known_rate_limit_remaining = 0

    class TokenNotAcquired(Exception):
        pass

    def get_client_credentials_token(self):
        """Requests and caches an access token from Reddit using the OAuth client-credentials grant type.
        """
        # Check if cached token has expired
        try:
            with open(self.TOKEN_CACHE_FILE, 'r') as f:
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
        resp = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=data, headers=headers)
        self.check_API_ratelimit(resp.headers)
        if resp.ok:
            token = resp.json()['access_token']
            # Cache the token and the time it expires
            with open(self.TOKEN_CACHE_FILE, 'w') as f:
                # 90% (safety factor) of the "expires_in" value from the http access token response (converted to hours)
                time_to_expiration = 0.9 * float(resp.json()['expires_in']) / 3600
                expiration = datetime.now() + timedelta(hours=time_to_expiration)
                cache = {'access_token': token, 'expiration': expiration.timestamp()}
                json.dump(cache, f, indent=2)
            return token
        else:
            raise self.TokenNotAcquired

    def check_API_ratelimit(self, http_header):
        """"Checks how many more requests are allowed in the current period after an api call"""
        remaining = http_header['X-Ratelimit-Remaining']
        self.last_known_rate_limit_remaining = remaining
        if int(remaining) < 10:
            # sleep till the current period ends and requests limit is reset
            wait_time = int(http_header['X-Ratelimit-Reset'])
            print(f'Waiting for Reddit servers to grant more http requests: {wait_time} seconds')
            time.sleep(wait_time + 5)

    def api_call(self, call_lambda):
        """" Ensures auth token and request rate limits are checked at each API call.

            call_lambda should be a lambda function that sends the desired http request and returns the response.
        """
        self.get_client_credentials_token()
        response = call_lambda()
        self.check_API_ratelimit(response.headers)
        return response

    def get_subreddit_listings(self, subreddits):
        """Returns a list of Reddit API subreddit "Listings" as dictionaries
            Suggest max of 100 listings at a time.
        subreddits -- string or list of strings
        """
        nonexistent_subs = []
        # Clean up list of subreddits and prepare the comma separated string needed in the API call
        if type(subreddits) == str:
            subreddits = [subreddits.casefold()]
        # names with commas in them can't be real and need to be removed before the api call so they
        # don't fuck up the sr_name query string.
        for x in range(len(subreddits)):
            if ',' in subreddits[x]:
                nonexistent_subs.append(subreddits.pop(x))
        subreddits = [str.casefold(x) for x in subreddits]
        subsstr = ','.join(subreddits)

        # Make API call
        api_base = 'https://oauth.reddit.com/'
        sub_endpoint = 'r/subreddit/api/info.json'
        headers = {'authorization': f'bearer {self.token}', 'user-agent': self.user_agent}
        response = self.api_call(
            lambda: requests.get(api_base + sub_endpoint, headers=headers, params={'sr_name': subsstr})
        )

        # Parse response
        j = response.json()
        returned_subs_listings = [x for x in j['data']['children'] if x['kind'] == 't5']
        if len(subreddits) != len(returned_subs_listings):
            returned_subs_names = [x['data']['display_name'].casefold() for x in returned_subs_listings]
            nonexistent_subs = [x for x in subreddits if x not in returned_subs_names]

        return {'subreddit_listings': returned_subs_listings, 'nonexistent_subreddits': nonexistent_subs}

    def _check_sub_ban_status(self, subreddit):
        """determine if given subreddit is banned

            subreddit -- must be a dictionary Listing of a subreddit from Reddit's API
        """
        banned_clues = ['subscribers', 'accounts_active', 'header_title']
        for clue in banned_clues:
            if subreddit['data'][clue] is not None:
                return False
        return True

    def check_subreddit_status(self, subreddits):
        """determine if given subreddits are open, banned, or nonexistent and whether they are marked NSFW.
            Suggest max of 100 subreddits at a time. Returns list of dicts [{name, status, content_type}]

            subreddits -- string or list of strings
        """
        api_response = self.get_subreddit_listings(subreddits)
        sub_listings = api_response['subreddit_listings']
        nonexistent = [
            {'name': x, 'status': 'nonexistent', 'content_type': 'null'}
            for x in api_response['nonexistent_subreddits']]
        results = []
        for sub in sub_listings:
            name = sub['data']['display_name']
            over18 = sub['data']['over18']
            status = 'banned' if self._check_sub_ban_status(sub) else 'open'
            if status == 'banned':
                content_type = 'null'
            elif over18:
                content_type = 'nsfw'
            else:
                content_type = 'sfw'
            results.append({'name': name, 'status': status, 'content_type': content_type})
        results.extend(nonexistent)
        return results



if __name__ == '__main__':
    from jtools.jconsole import test
    r = RedditScript()

    banned = ['Swirl_Life',
              'nikkiwoodsfans',
              'hannaowo_link',
              'PussyPounded',
              'vikingsvschargerslive','asj;fksa;f422']
    subs = ['wtf', 'askreddit', 'aww', 'trashy', 'gonewild']
    thirty = subs * 6
    fifty = subs * 10
    hudnred = subs * 20
    result = r.check_subreddit_status(banned)
    test(result, len(result), r.last_known_rate_limit_remaining)
    pass

