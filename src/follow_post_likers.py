import logging
import random

import time

from .user_lists import get_all_likers


def follow_likers_list_by_post(self, shortcode, count):
    """ Get likers list by post """
    if self.login_status:
        try:
            likers = get_all_likers(self, short_code=shortcode)
            for user in likers:
                rand = random.randint(10, 20)
                if user['node']['is_private'] or user['node']['followed_by_viewer']:
                    print("private follow sleeping ", rand)
                    time.sleep(rand)
                    print ("skip following private user:", user['node']['username'])
                    continue

                id = user['node']['id']
                user_info = self.get_userinfo_by_name(self.get_username_by_user_id(user_id=id))
                if user_info != None:
                    if user_info['edge_follow']['count'] < user_info['edge_followed_by']['count']:
                        print("private follow sleeping ", rand)
                        time.sleep(rand)
                        print("followed by more people than he follows", user['node']['username'])
                        # continue
                    self.follow(user_id=id)
                    rand = random.randint(70, 110)
                    print("follow sleeping ", rand)
                    time.sleep(rand)
                    count += 1
                    print("follow count", count)
            return count
        except:
            logging.exception("Except on getting likers info")
            return
    else:
        return False