"""
Usage: github_location_search.py India Bangalore Singapore Chennai Pune \
       Mumbai Delhi Colombo Gurgaon Hyderabad Noida London New+York San+Francisco

Saves all user information into users.csv. Can be run incrementally.
"""

import sys
import json
import urllib
import os.path
import logging
import pandas as pd
import urllib.request
import os

# Max pages per location
MAX_PAGES = 20


def users(location, pages, token=None):
    """Get list of user objects at a given location"""
    url = 'https://api.github.com/legacy/user/search/location:' + location
    data = []
    for page in range(1, pages + 1):
        logging.info('location %s: %d/%d', location, page, pages)
        try:
            link = url + '?start_page=%d&access_token=%s' % (page, token)
            result = json.load(urllib.request.urlopen(link))
        except IOError as e:
            logging.info('location %s: %d/%d failed: %s', location, page, pages, e)
            result = {}
        if 'users' in result and len(result['users']):
            data += result['users']
        else:
            break
    return data


def search_locations(locations, userfile, token=None):
    """Search & merge user objects for multiple locations into userfile"""
    userdata = []
    for location in locations:
        userdata += users(location, pages=MAX_PAGES, token=token)
    if not len(userdata):
        return

    data = pd.DataFrame(userdata).set_index('login')

    if os.path.exists(userfile):
        data = data.combine_first(pd.read_csv(userfile).set_index('login'))

    data = data.reset_index().drop_duplicates(subset=['login'], keep='last')
    data.sort_values('followers_count', ascending=False, inplace=True)
    data.to_csv(userfile, index=False, encoding='utf-8')


def followers(user, count, token=None):
    """Get followers for user who has count followers"""
    url = 'https://api.github.com/users/{:s}/followers?access_token={:s}'
    url = (url + '&per_page=100').format(user, token)
    results = []
    pages = int(count + 99) // 100
    for page in range(pages):
        logging.info('user %s: %d/%d', user, page + 1, pages)
        try:
            result = json.load(urllib.request.urlopen(url + '&page=%d' % page))
        except IOError:
            result = []
        if len(result):
            results += result
    return results


def fill_followers(userfile, followerfile, token=None):
    """Fill in missing followers into followerfile for users in userfile"""
    if not os.path.exists(userfile):
        return

    userlist = pd.read_csv(userfile).set_index('login')
    if os.path.exists(followerfile):
        data = pd.read_csv(followerfile)
    else:
        data = pd.DataFrame(columns=['login', 'follower'])

    logins = set(data['login'])
    dataset = []
    for login, row in userlist.iterrows():
        actual_followers = int(row['followers_count'])
        if actual_followers < 2:
            continue
        if login in logins:
            recorded_followers = sum(data['login'] == login)
            if (actual_followers < 100 or
                    recorded_followers > actual_followers * 0.85):
                continue
            logging.info('repeating %s: %d/%d',
                         login, recorded_followers, actual_followers)
        result = followers(login, actual_followers, token)
        dataset += [[login, row['login']] for row in result]

    if len(dataset):
        dataset = pd.DataFrame(dataset, columns=['login', 'follower'])
        data = pd.concat([data, dataset], ignore_index=True)
        data = data.drop_duplicates(subset=['login', 'follower'])
        data.to_csv(followerfile, index=False, encoding='utf-8')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TOKEN = os.getenv('PERSNOL_TOKEN')  # Get the token from environment variable
    if not TOKEN:
        raise ValueError("GitHub token is required.")
    if len(sys.argv) > 1:
        search_locations(sys.argv[1:], 'users.csv', token=TOKEN)
    if os.path.exists('users.csv'):
        fill_followers('users.csv', 'followers.csv', token=TOKEN)
