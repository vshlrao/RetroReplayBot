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
    try:
        # update with latest entries
        rr_feed = feedparser.parse(config.feed)
        latest_title = rr_feed['entries'][0]['title']
        latest_link = rr_feed['entries'][0]['link']

        # get history wikipage
        history_wp = subreddit.wiki['uploadhistory']

        # latest upload and latest submission not the same
        if history_wp.content_md != latest_link:
            # unsticky current top stickied post
            top_sticky = subreddit.sticky(number=1)
            top_sticky.mod.sticky(state=False)

            # submit new video and sticky to top of subreddit
            submission = subreddit.submit(latest_title, url=latest_link)

            # sticky [latest-1] submission to second sticky
            submission.mod.sticky(state=True, bottom=False)
            top_sticky.mod.sticky(bottom=True)

            # change wiki page to latest video
            # give title as reason for searchability
            history_wp.edit(content=latest_link, reason=latest_title)

    except Exception as e:
        reddit.redditor('supabatman').message('Bot Problem', e)


if __name__ == "__main__":
    main()








