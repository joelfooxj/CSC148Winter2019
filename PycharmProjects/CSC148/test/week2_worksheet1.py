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


