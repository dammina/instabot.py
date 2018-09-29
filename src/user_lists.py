import json
import random
import urllib
from collections import OrderedDict

import time

import request_types

def get_all_followers(self, user_id):#"8487895339"
    # query_url = "https://www.instagram.com/graphql/query/?query_hash=58712303d941c6855d4e888c5f0cd22f&variables=%7B%22id%22%3A%228487895339%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A50%7D"
    # my_followers = self.s.get(query_url)
    # all_data = json.loads(my_followers.text)
    url_followers_base = "https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&"
    log_string = "Trying to retrieve followers list of user : %s" % (user_id)
    self.write_log(log_string)
    return get_all_users(self, key=user_id, query_url_base=url_followers_base, request_type=request_types.FOLLOWERS)

def get_all_following(self, user_id):
    url_following_base = "https://www.instagram.com/graphql/query/?query_hash=c56ee0ae1f89cdbd1c89e2bc6b8f3d18&"
    log_string = "Trying to retrieve following list of user : %s" % (user_id)
    self.write_log(log_string)
    return get_all_users(self, key=user_id, query_url_base=url_following_base, request_type=request_types.FOLLOWING)

def get_all_likers(self, short_code):
    url_likes_base = "https://www.instagram.com/graphql/query/?query_hash=e0f59e4a1c8d78d0161873bc2ee7ec44&"
    log_string = "Trying to retrieve likes list of post : https://www.instagram.com/p/%s" % (short_code)
    self.write_log(log_string)
    return get_all_users(self, key=short_code, query_url_base=url_likes_base, request_type=request_types.LIKERS)

def get_all_users(self, key, query_url_base, request_type):
    #{'variables': ['{"shortcode":"Bn-3Qm6nWts","include_reel":true,"first":24}']}
    # print(urlparse.parse_qs("variables=%7B%22id%22%3A%228487895339%22%2C%22include_reel%22%3Atrue%2C%22first%22%3A50%7D"))
    list = []
    data = OrderedDict()
    if request_type is request_types.FOLLOWING or request_type is request_types.FOLLOWERS:
        data["id"] = key
    elif request_type is request_types.LIKERS:
        data["shortcode"] = key
    data["include_reel"] = True
    if request_type is request_types.FOLLOWING or request_type is request_types.FOLLOWERS:
        data["fetch_mutual"] = False
    data["first"] = 50
    variables = {}
    variables["variables"] = json.dumps(data).replace(" ", "")
    query_url = query_url_base + urllib.urlencode(variables)

    my_followers = self.s.get(query_url, headers="")
    all_data = json.loads(my_followers.text)

    base_data = []
    if request_type is request_types.FOLLOWING or request_type is request_types.FOLLOWERS:
        base_data = all_data['data']['user']['edge_followed_by']
    elif request_type is request_types.LIKERS:
        base_data = all_data['data']['shortcode_media']['edge_liked_by']

    edges = base_data['edges']
    end_cursor = base_data['page_info']['end_cursor']
    has_next_page = base_data['page_info']['has_next_page']

    for user in edges:
        list.append(user)

    while has_next_page != False:
        data["after"] = end_cursor
        variables["variables"] = json.dumps(data).replace(" ", "")
        query_url = query_url_base + urllib.urlencode(variables)
        my_followers = self.s.get(query_url, headers="")
        all_data = json.loads(my_followers.text)
        base_data = []
        if request_type is request_types.FOLLOWING or request_type is request_types.FOLLOWERS:
            base_data = all_data['data']['user']['edge_followed_by']
        elif request_type is request_types.LIKERS:
            base_data = all_data['data']['shortcode_media']['edge_liked_by']

        edges = base_data['edges']
        end_cursor = base_data['page_info']['end_cursor']
        has_next_page = base_data['page_info']['has_next_page']

        for user in edges:
            list.append(user)
        time.sleep(random.randint(5, 10))

    return list