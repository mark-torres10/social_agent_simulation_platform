"""For each profile in the database, generate an AI-generated bio
to use for the agent, and save to the database."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from db.db import initialize_database, read_all_profiles, read_all_feed_posts, write_generated_bio_to_database
from db.models import BlueskyProfile, BlueskyFeedPost

GENERATE_BIO_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at creating concise and accurate bios
    for users on social media.

    Your task is to create a bio that captures the essence of a person based on
    their profile information and sample posts. The bio should be:

    - Comprehensive, 1-2 paragraphs.
    - Reinforced by specific examples and evidence.
    - Capture their personality, interests, and communication style.
    - Be suitable for use in a social media agent simulation.
    - Written in third person
    """),

    ("human", """Create a bio for this person:

    Profile Information:
    - Display Name: {display_name}
    - Handle: @{handle}
    - Current Bio: {current_bio}
    - Followers: {followers_count:,}
    - Following: {follows_count:,}
    - Total Posts: {posts_count:,}

    Sample Posts (recent activity):
    {posts_sample}

    Generate a comprehensive bio that captures this person's personality and interests:
    """
    ),
])

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

MAX_POSTS_SAMPLE = 20

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

def get_posts_sample(posts: list[BlueskyFeedPost], max_posts: int = MAX_POSTS_SAMPLE) -> str:
    """Get a sample of posts formatted for the prompt.
    
    Args:
        posts: List of posts
        max_posts: Maximum number of posts to include
        
    Returns:
        Formatted string of post samples
    """
    if not posts:
        return "No posts available."
    
    sample_posts = posts[:max_posts]
    formatted = []
    for i, post in enumerate(sample_posts, 1):
        # Truncate long posts
        text = post.text[:200] + "..." if len(post.text) > 200 else post.text
        formatted.append(f"{i}. {text}")
    
    return "\n".join(formatted)

def generate_bio_for_profile(
    profile: BlueskyProfile, posts: list[BlueskyFeedPost]
) -> str:
    """Generate a bio for a profile using Langchain.
    
    Args:
        profile: BlueskyProfile to generate bio for
        posts: List of posts by this profile
        llm: Langchain LLM instance
        
    Returns:
        Generated bio string
    """
    posts_sample = get_posts_sample(posts)
    
    prompt = GENERATE_BIO_PROMPT.format_messages(
        display_name=profile.display_name,
        handle=profile.handle,
        current_bio=profile.bio,
        followers_count=profile.followers_count,
        follows_count=profile.follows_count,
        posts_count=profile.posts_count,
        posts_sample=posts_sample,
    )
    
    response = llm.invoke(prompt)
    return response.content.strip()

def main():
    initialize_database()
    print("Reading profiles and feed posts from database...")
    profiles: list[BlueskyProfile] = read_all_profiles()
    feed_posts: list[BlueskyFeedPost] = read_all_feed_posts()
    posts_by_author: dict[str, list[BlueskyFeedPost]] = {
        profile.handle: [
            post for post in feed_posts
            if post.author_handle == profile.handle
        ]
        for profile in profiles
    }


    print("Generating bios for profiles...")
    for i, profile in enumerate(profiles, 1):
        print(f"Generating bio for profile {i} of {len(profiles)}...")
        posts = posts_by_author[profile.handle]
        generated_bio = generate_bio_for_profile(profile, posts)
        write_generated_bio_to_database(profile.handle, generated_bio)
        print(f"Generated bio for {profile.handle}: {generated_bio}")


if __name__ == "__main__":
    main()
