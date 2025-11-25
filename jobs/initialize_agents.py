"""Job for initializing the agents.

For now, what this looks like is:
- Getting a series of Bluesky profiles from a list of handles.
- Using that information to create a bio for the agent.
- Persisting the agent to the SQLite database.
"""

from lib.bluesky_client import BlueskyClient

bsky_client = BlueskyClient()

BLUESKY_HANDLES = [
    "https://bsky.app/profile/aoc.bsky.social",
    "https://bsky.app/profile/did:plc:ks3gpa6ftoyaq7hmf6c4qx4c",
    "https://bsky.app/profile/did:plc:77lswp42lgjyw36ozuo7kt7e",
    "https://bsky.app/profile/did:plc:ksjfbda7262bbqmuoly54lww",
    "https://bsky.app/profile/did:plc:2q2hs5o42jhbd23pp6lkiauh",
    "https://bsky.app/profile/did:plc:j37zetcnytvnfjlk4ca3d2yv",
    "https://bsky.app/profile/did:plc:zbrhmanjs62oyqywjwdazxz3"
]

def main():
    pass


if __name__ == "__main__":
    print("Initializing agents...")
    main()
    print("Agents initialized successfully.")
