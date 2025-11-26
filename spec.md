# Initial spec

## Agents

- OpenAI API
- Like/comment/follow
- Basic bio

## Basic prototype

- 10 turns
- Agents can get a feed, choose to like/comment/follow the post author (if they don't already follow)
- Give reasoning for why they like/follow
- Record at each timestep

## Tickets

- Ticket 1: basic setup
- Ticket 2: telemetry with Langfuse
- Ticket 3: Basic Streamlit UI.

## Backlog

- Create basic recommendation algorithm
- Might want a pipeline to get new fresh firehose posts and then see what we think they'd engage with.

## 2025-11-25

12:25pm: I think the next ticket can be a basic recommendation algorithm. Let's make it simple but have some complexity. Let's have the following rules:

- RAG: pick the top X posts in the database that are most similar to theirs (but of course not theirs) and were not picked in previous rounds.
- Re-sample each round.

Let's actually have two feeds:

- Feed 1: simple reverse-chronological. Sample from posts not theirs, pick by created_at timestamp, get top X. Re-sample each round so that they get brand new posts each round.
- Feed 2: RAG-based approach.

3:32pm: Working on the chronological feed now.

- I want to have a GeneratedPost model as well, so I know which posts are original and which ones are generated. Should this be separate tables or one table? Maybe I'll do separate tables, so I know which ones are the "ground truth" posts.

- For a V1, let's just make it so that they can only look at the original Bluesky posts. Let's incorporate the ability to inject new posts later on.

7:12pm: What I need to do is track the "seen" posts (so basically, I need to track past feeds from a given run).

What I need to do is:

- For each run, I need to store that metadata.
- I need to add that run ID to the feed ID, so the generated feed PK is the run ID, the turn number, and the user handle.
- I need to create a new table called "generated_feeds".
- I need to load the "generated_feeds" for the given run ID, at the start of each turn.
- Then I need to create a dict, with key = user handle and value = set of all posts across all feeds from that user that they've already seen this run. That has to be what's in load_seen_post_uris.
