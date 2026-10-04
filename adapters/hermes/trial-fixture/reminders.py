"""Disposable subsystem for evidence-based pstack walkthrough trials."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Session:
    minutes: int
    paused: bool = False

def reminder(session: Session, threshold: int = 30):
    if session.paused or session.minutes < threshold:
        return None
    return {'kind': 'stretch', 'minutes': session.minutes}

def render(session):
    event = reminder(session)
    return 'quiet' if event is None else f"stretch after {event['minutes']} minutes"

if __name__ == '__main__':
    print(render(Session(30)))
