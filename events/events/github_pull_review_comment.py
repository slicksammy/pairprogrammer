from .base import Base

class GithubPullReviewComment(Base):
    @classmethod
    def parse_fields(cls):
        return {
            "repository": {
                "name": None,
                "owner": {
                    "login": None
                },
            },
            "comment": {
                "id": None,
                "body": None,
                "diff_hunk": None,
            },
            "pull_request": {
                "number": None,
            }
        }

    @classmethod
    def should_respond(cls, parsed):
        return "@pear-on" in parsed['comment']['body']

    @classmethod
    def parse_event(cls, event_data):
        return cls.parse_json(event_data, cls.parse_fields())