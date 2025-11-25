from ai.agents import (
    load_agents, SocialMediaAgent,
    record_agent_actions,
)

def simulate_turn() -> dict:
    total_actions = {
        "likes": 0,
        "comments": 0,
        "follows": 0,
    }
    agents: list[SocialMediaAgent] = load_agents()
    for agent in agents:
        agent.get_feed()
        
        likes = agent.like_posts()
        comments = agent.comment_posts()
        follows = agent.follow_users()

        record_agent_actions({
            "likes": likes,
            "comments": comments,
            "follows": follows,
        })

        total_actions["likes"] += len(likes)
        total_actions["comments"] += len(comments)
        total_actions["follows"] += len(follows)

    return total_actions

def main():
    for i in range(10):
        print(f"Turn {i+1}")
        total_actions = simulate_turn()
        print(f"Total actions on turn {i+1}: {total_actions}")


if __name__ == "__main__":
    main()
