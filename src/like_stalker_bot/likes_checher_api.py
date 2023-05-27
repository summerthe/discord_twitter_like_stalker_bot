import random
import re
from collections import defaultdict

import tweepy

from .config import Config


class LikesChecher:
    def __init__(self) -> None:
        # Twitter API credentials
        consumer_key = Config.twitter_consumer_key
        consumer_secret = Config.twitter_consumer_secret
        access_token = Config.twitter_access_token
        access_token_secret = Config.twitter_access_token_secret

        # Authenticate to Twitter API
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

        self.MAX_TWEET_LOOKUP = 1500
        self.CACHED_TWEETS = defaultdict(list)
        self.screen_name = Config.user_screen_name

    def extract_post_id(self, url: str) -> str | None:
        """Extract post id from twitter url.

        Parameters
        ----------
        url : str

        Returns
        -------
        str|None
        """
        pattern = r"\/status\/(\d+)"
        match = re.search(pattern, url)
        if match:
            post_id = match.group(1)
            return post_id
        else:
            return None

    def is_post_liked_by_user(self, post_id: str) -> bool:
        """Retrieves liked post from cache/twitter API and checks if post id
        liked or not.

        Parameters
        ----------
        post_id : str

        Returns
        -------
        bool
        """
        total_lookup_so_far = 0
        cursor = tweepy.Cursor(
            self.api.get_favorites,
            screen_name=self.screen_name,
            include_entities=False,
            count=200,
        )

        liked_posts = []
        for page in cursor.pages():
            liked_page_posts_ids = [str(like.id) for like in page]

            # fetch first liked posts and cached posts, if both are same then use all records of cached.
            # cache may have more than 200 records
            first_cached_tweets_ids = self.CACHED_TWEETS[self.screen_name][:5]
            first_liked_page_posts_ids = liked_page_posts_ids[:5]

            # using cached tweets
            if first_cached_tweets_ids == first_liked_page_posts_ids:
                if post_id in self.CACHED_TWEETS[self.screen_name]:
                    return True
            else:
                # max tweet look up before saying post didnt found
                if total_lookup_so_far > self.MAX_TWEET_LOOKUP:
                    break
                if post_id in liked_page_posts_ids:
                    # post is found in list
                    return True

                # if not found, update cache and counters
                total_lookup_so_far += len(liked_page_posts_ids)
                liked_posts.extend(liked_page_posts_ids)
                self.CACHED_TWEETS[self.screen_name] = liked_posts
        return False

    def check_post_is_liked(self, *, post_url: str) -> str:
        """Checks if post is liked or not by user.

        Parameters
        ----------
        post_url : str

        Returns
        -------
        str
        """
        post_id = self.extract_post_id(post_url)
        if post_id:
            is_liked = self.is_post_liked_by_user(str(post_id))
            if is_liked:
                return self.get_random_liked_msg()
            else:
                return self.get_random_not_liked_msg()
        else:
            return "Dudeee!!! That was Invalid Twitter post URL."

    def get_random_liked_msg(self):  # noqa: E501
        return random.choice(
            [
                "Oh snap, she already smashed that like button! D'oh.",  # noqa: E501
                "Oops-a-daisy, she's a seasoned liker who beat you to it. Whoopsie!",  # noqa: E501
                "Well, she's the Queen of Likes and that post already bowed down. Bam!",  # noqa: E501
                "Holy moly, she's a like-gobbling machine! That post didn't stand a chance. Ka-pow!",  # noqa: E501
                "Yikes, she's quicker than a hiccup! Already liked and done. Oopsie-doodle!",  # noqa: E501
                "Ahoy, she sailed through that post like a seasoned pirate! Avast!",  # noqa: E501
                "Well, she's a mind-reading ninja who liked that post before you even blinked. Zing!",  # noqa: E501
                "Oh dear, she's a like-wizard with magical reflexes! Abracadabra!",  # noqa: E501
                "Golly gee, she's got lightning fingers! Already hit that like button, zoom! Uh-huh.",  # noqa: E501
                "Ruh-roh, she's a like-saurus who left her mark on that post. Jinkies!",  # noqa: E501
                "Bravo, she's a likemaster extraordinaire! Already claimed that post. Woohoo!",  # noqa: E501
                "Oh boy, she's like a like-seeking missile! Nailed it on that post. Yippee!",  # noqa: E501
                "Huzzah, she's the fastest liker in the West! Already conquered that post, partner. Yeehaw!",  # noqa: E501
                "Goodness gracious, she's a like-surfing champion! Rode the wave on that post. Cowabunga!",  # noqa: E501
                "Well, she's a like ninja on a mission! Stealthily liked that post. Sneaky-sneaky!",  # noqa: E501
                "Holy guacamole, she's a like-gobbling monster! Devoured that post. Gulp!",  # noqa: E501
                "Look out, she's a like-hunting pro! Bagged her target on that post. Bullseye!",  # noqa: E501
                "Hot diggity dog, she's a liker with turbo speed! Already zapped that post. Booyah!",  # noqa: E501
                "Oh my, she's got the reflexes of a like panther! Pounced on that post. Meow!",  # noqa: E501
                "Great Scott, she's a like-time-traveler! Already liked that post in the past. Mind-blowing!",  # noqa: E501
                "Jeepers, she's like a like tornado! Swept through that post. Whoosh!",  # noqa: E501
                "Holy smokes, she's a like-superhero! Already saved the day on that post. Pow!",  # noqa: E501
                "Eureka, she's a like-scientist with the formula for speed! Already cracked it on that post. Eureka!",  # noqa: E501
                "Oh snap, she's a like-whisperer! That post felt her magic touch. Shazam!",  # noqa: E501
                "By George, she's a like-pioneer of epic proportions! Already claimed that post like a champ. Giddy-up!",  # noqa: E501
                "Whoa there, she's a like-magician with tricks up her sleeve! Already pulled a rabbit out of the like hat on that post. Ta-da!",  # noqa: E501
                "Gadzooks, she's a like-juggernaut! Already unleashed her powers on that post. Kablooey!",  # noqa: E501
                "Holy guacamole, she's a like-avenger on a mission! Saved the day by liking that post. Avengers, assemble!",  # noqa: E501
                "Jumpin' Jehoshaphat, she's a like-racer on turbo boost! Already crossed the finish line on that post. Vroom-vroom!",  # noqa: E501
                "Hold the phone, she's a like-connoisseur! Already added her artistic touch to that post. Voilà!",  # noqa: E501
            ],
        )

    def get_random_not_liked_msg(self):  # noqa: E501
        return random.choice(
            [
                "Hooray, she has yet to discover the greatness of that post! Victory awaits!",  # noqa: E501
                "Woohoo, she's yet to uncover the hidden gem that is that post. Success is on the horizon!",  # noqa: E501
                "Aha, the post is patiently waiting for her to hit that like button and claim the win. Game on!",  # noqa: E501
                "Oh yes, the post eagerly anticipates her arrival to bestow the ultimate victory with her like. Triumphant moments await!",  # noqa: E501
                "Victory dances in the shadows as she prepares to unleash her liking prowess upon that post. The win is within reach!",  # noqa: E501
                "The post stands tall, basking in the glory that is yet to come when she graces it with her like. Victory is inevitable!",  # noqa: E501
                "With every passing moment, the post becomes more deserving of her like, ensuring a triumphant win. The spotlight awaits!",  # noqa: E501
                "She holds the power to transform that post into a victorious masterpiece with a single click. The taste of success is near!",  # noqa: E501
                "The post yearns for her like, knowing it will emerge victorious and bask in the glory of her approval. The win is within sight!",  # noqa: E501
                "As she withholds her like, the post grows stronger, building anticipation for the inevitable win that awaits. The countdown begins!",  # noqa: E501
                "Eureka! The post holds within it a joyous surprise, ready to uplift her spirits and spark a triumphant smile.",  # noqa: E501
                "Oh, the post is a gateway to a moment of pure happiness and celebration, awaiting her discovery and bringing a resounding victory.",  # noqa: E501
                "The post holds a delightful secret, a treasure trove of positivity and delight that will light up her day with a resplendent win.",  # noqa: E501
                "Like a beacon of joy, the post shines brightly, eagerly awaiting her arrival to unlock a moment of pure bliss and victorious elation.",  # noqa: E501
                "The post carries within it a powerful message, a heartwarming revelation that will fill her with jubilant glee and the sweet taste of triumph.",  # noqa: E501
                "Ah, the post is a magical portal, ready to transport her into a realm of sheer delight and unbounded happiness, where every word is a win.",  # noqa: E501
                "Brace yourself, for the post is a gateway to a happy place, where her heart will dance with joy and she'll experience the exhilaration of a resounding victory.",  # noqa: E501
                "Get ready to soar on the wings of delight as the post reveals its hidden charm, igniting a cascade of pure happiness and a victorious celebration.",  # noqa: E501
                "Hold your breath, for the post carries within it a euphoric surprise, a moment of unparalleled joy that will make her heart sing and her smile shine with a glorious win.",  # noqa: E501
                "Let the anticipation build, for the post is an oasis of happiness, poised to shower her with an abundance of delightful emotions and the ultimate triumph of a joyous moment.",  # noqa: E501
                "Alas, she hasn't discovered the hidden gem that awaits her in that post, but oh, the delight it holds when she does.",  # noqa: E501
                "Oh my, the post patiently yearns for her affectionate like, eager to unleash a world of happiness upon her.",  # noqa: E501
                "Fret not, for the post patiently waits, longing for the day she graces it with her like, filling her world with an explosion of joy.",  # noqa: E501
                "The post wistfully dreams of her like, yearning for the moment it becomes a beacon of happiness in her life.",  # noqa: E501
                "Like a dormant firework, the post eagerly anticipates her like to ignite a spectacular display of celebration and elation.",  # noqa: E501
                "The post quietly whispers tales of joy and triumph, patiently awaiting her like to unlock a world of radiant happiness.",  # noqa: E501
                "Within the depths of the post lies a treasure trove of delight, yearning for her like to reveal its magnificent splendor.",  # noqa: E501
                "Oh, the post holds a wondrous secret, waiting for her like to open the floodgates of jubilation and create an unforgettable moment.",  # noqa: E501
                "The post humbly awaits her appreciation, ready to burst forth with a surge of bliss when her like finally graces its presence.",  # noqa: E501
                "Unbeknownst to her, the post carries a symphony of happiness, patiently longing for her like to unleash a chorus of joyful notes and create a harmonious win.",  # noqa: E501
            ],
        )
