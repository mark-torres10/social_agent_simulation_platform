from ai.agents import SocialMediaAgent, record_agent_actions
from ai.create_initial_agents import create_initial_agents

def simulate_turn(agents: list[SocialMediaAgent]) -> dict:
    total_actions = {
        "likes": 0,
        "comments": 0,
        "follows": 0,
    }
    for agent in agents:
        feed = agent.get_feed()
        
        likes = agent.like_posts(feed)
        comments = agent.comment_posts(feed)
        follows = agent.follow_users(feed)

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
    agents: list[SocialMediaAgent] = create_initial_agents()
    for i in range(10):
        print(f"Turn {i+1}")
        total_actions = simulate_turn(agents)
        print(f"Total actions on turn {i+1}: {total_actions}")


if __name__ == "__main__":
    main()
