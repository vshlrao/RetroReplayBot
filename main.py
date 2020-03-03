import praw
import feedparser
import config
import time

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

subreddit = reddit.subreddit(config.subreddit)


def main():
    while True:
        try:
            # update with latest entries
            rr_feed = feedparser.parse(config.feed)
            latest_title = rr_feed['entries'][0]['title']
            latest_link = rr_feed['entries'][0]['link']

            # get link of last uploaded/submitted video
            file = open("latest_link.txt", "r")

            # latest upload and latest submission not the same
            if file.read() != latest_link:
                # unsticky current top stickied post
                top_sticky = subreddit.sticky(number=1)
                top_sticky.mod.sticky(state=False)

                # submit new video and sticky to top of subreddit
                submission = subreddit.submit(latest_title, url=latest_link)

                # sticky [latest-1] submission to second sticky
                submission.mod.sticky(state=True, bottom=False)
                top_sticky.mod.sticky(bottom=True)

                # record latest submitted video's link
                f_link = open("latest_link.txt", "w")
                f_link.write(latest_link)
                f_link.close()
                f_title = open("latest_title.txt", "w")
                f_title.write(latest_title)
                f_title.close()

            file.close()
            time.sleep(300)
        except Exception as e:
            print(e)
            break



if __name__ == "__main__":
    main()








