from ai.agents import (
    load_agents, SocialMediaAgent,
    record_agent_actions,
)

def simulate_turn():
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



def main():
    for i in range(10):
        print(f"Turn {i+1}")
        simulate_turn()


if __name__ == "__main__":
    main()
