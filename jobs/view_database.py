"""Simple script to view all profiles and posts in the database."""

from db.db import read_all_feed_posts, read_all_profiles


def print_profile(profile):
    """Print a profile in a readable format."""
    print(f"\n{'='*80}")
    print(f"Profile: {profile.display_name} (@{profile.handle})")
    print(f"{'='*80}")
    print(f"DID: {profile.did}")
    print(f"Bio: {profile.bio[:200]}{'...' if len(profile.bio) > 200 else ''}")
    print(f"Followers: {profile.followers_count:,}")
    print(f"Following: {profile.follows_count:,}")
    print(f"Posts: {profile.posts_count:,}")


def print_post(post, show_full_text=True):
    """Print a post in a readable format."""
    print(f"\n{'-'*80}")
    print(f"Post by {post.author_display_name} (@{post.author_handle})")
    print(f"Created: {post.created_at}")
    print(f"{'-'*80}")
    
    if show_full_text:
        print(f"Text: {post.text}")
    else:
        text_preview = post.text[:150] + "..." if len(post.text) > 150 else post.text
        print(f"Text: {text_preview}")
    
    print(f"Engagement: ❤️ {post.like_count:,} | 💬 {post.reply_count:,} | 🔁 {post.repost_count:,} | 🔖 {post.bookmark_count:,} | 💬 {post.quote_count:,}")
    print(f"URI: {post.uri}")


def main():
    print("=" * 80)
    print("DATABASE VIEWER")
    print("=" * 80)

    # Read and display profiles
    profiles = read_all_profiles()
    print(f"\n📊 PROFILES ({len(profiles)} total)")
    print("=" * 80)
    
    if not profiles:
        print("No profiles found in database.")
    else:
        for profile in profiles:
            print_profile(profile)
    
    # Read and display posts
    posts = read_all_feed_posts()
    print(f"\n\n📝 POSTS ({len(posts)} total)")
    print("=" * 80)

    if not posts:
        print("No posts found in database.")
    else:
        for post in posts:
            print_post(post, show_full_text=False)
    
    print(f"\n\n{'='*80}")
    print(f"Summary: {len(profiles)} profiles, {len(posts)} posts")
    print("=" * 80)


if __name__ == "__main__":
    main()