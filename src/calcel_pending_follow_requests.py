import json
import random

import time


def cancel_requested_follows(self):
    url_requested_follows = self.url_requested_follows
    try:
        no_requests_left = False
        while not no_requests_left:
            requested_follows = self.s.get(url_requested_follows)
            all_data = json.loads(requested_follows.text)
            if requested_follows.status_code == 200:
                if len(all_data['data']['data']) == 0:
                    no_requests_left = True
                for user in all_data['data']['data']:
                    url_user_id = self.url_user_id % (user['text'])  # 1329926153
                    user_id = self.s.get(url_user_id)
                    all_user_data = json.loads(user_id.text)
                    id = all_user_data['graphql']['user']['id']
                    url_unfollow = self.url_unfollow % (id)
                    try:
                        unfollow = self.s.post(url_unfollow)
                        if unfollow.status_code == 200:
                            self.unfollow_counter += 1
                            log_string = "Unfollowed: %s #%i." % (user,
                                                                  self.unfollow_counter)
                            self.write_log(log_string)
                            rand = random.randint(40, 70)
                            print("Sleeping ", rand)
                            time.sleep(rand)
                        elif unfollow.status_code == 403:
                            rand = random.randint(70, 120)
                            print("403 Request rejected, sleeping ", rand)
                            time.sleep(rand)
                    except:
                        self.write_log("Exept on unfollow!")
                        return False
                rand = random.randint(70, 120)
                print("Sleeping long break", rand)
                time.sleep(rand)

    except:
        self.write_log("Exept on cancel request!")
        return False

    return