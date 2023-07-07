from events.events import *

class Config:
    EVENTS = {
        'github_pull_review_comment': {
            'event_class': GithubPullReviewComment
        }
    }

    @classmethod
    def get_event(cls, event):
        return cls.EVENTS[event]
    
    @classmethod
    def event_exists(cls, event):
        return event in cls.EVENTS