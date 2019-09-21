from datetime import date
class Tweet:
    content: str
    userid: str
    created_at: date
    likes: int

    def __init__(self, who: str, when: date, what: str) -> None:
        self.userid = who
        self.created_at: when
        self.content = what

    def edit(self, new_content: str) -> None:
        self.content = new_content

    def like(self, n: int) -> None:
        self.likes += n


class User:
    userid: str
    bio: str
    tweets: list[tweet: Tweet]
    follows: list[userid: str]

    def __init__(self, userid: str, bio: str) -> None:
        self.userid = userid
        self.bio = bio
        self.tweets = []
        self.follows = []

    def tweet(self, message: str) -> None:
        new_tweet = Tweet(self.userid, date.today(), message)
        self.tweets.append(new_tweet)

    def follow(self, userid: str) -> None:
        """
        :param userid:
        :return:

         Record that this User follows another user

        """

        self.follows.append(userid)




