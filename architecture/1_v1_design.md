# Proposed architecture design

Proposed V1 design of architecture + file structure for repo.

```markdown
/agents
    - llm.py: manages sending/receiving LLM requests. Also contains decorators for Opik/Langsmith for LLM telemetry.
    - chains.py: manages agentic chains. Uses Langchain.
    - agent_core.py: core agent logic. Exposes a core 'Agent' class
    - /agent_components
        /persistent: components that are meant to be long-lived, across "days", in a given simulation. These are the
        persistent characteristics that should change and be updated (if at all) over time. Each of these exposes a simple API, and manages all I/O as well as change related to each (e.g., they can expose a "update()" method and then each will abstract how it manages updating the given agent's personality, beliefs, etc.). Each of these uses the "MemoryManager" for I/O.
            - personality.py: manages the personality of agents.
            - beliefs.py: manages the beliefs of agents.
            - worldview.py: manages the worldview of agents.
            - political_views.py: manages the political views of agents.
            - profile.py: manages the agent profile.
            - engagement_preferences.py: manages the engagement tendencies of each agent, e.g., how likely they are to like/reply, to which content they're likely to engage with, etc. Should have the following fields:
                - preferences_by_engagement_type: dict, where key = engagement type (post, comment, like, etc.) and value is a float between 0 and 1 that describes how likely someone is to do that type of engagement with a "qualified post" (meaning, a post that we've determined they possibly would engage with).
                - topics_more_likely_to_engage_with: list of topics that a user is more likely to engage with.
                - accounts_more_likely_to_engage_with: list of accounts that a user is more likely to engage with.
                - other_engagement_preferences: list of free-form strings that describe other ways that their engagement behavior can be modified.
            - history.py: manages the full history of all agent characteristics, behaviors, and actions. Helpful for
            tracing and interpretability purposes later on, so we can see for a given agent how it evolves over time.
        /state: components that are meant to vary every single "day" of the simulation.
            - emotion_state.py: manages session-specific emotional state, i.e., how an agent is "feeling" when they're scrolling a feed. Meant to change and refresh every single "day" of the simulation.
    - init_agents.py: manages initializing agents for a simulation.
        - Handles things like default characteristics, preferences, traits, etc.
    - agent_manager.py: Exposes an "AgentManager" interface that wraps all the agents in a simulation, so that the simulation
    platform can be agnostic to the agents themselves. Exposes an interface that the simulation platform can simply interact with.
/config
    - models.py: Pydantic models defining config fields.
    - agent_config.yml: Config for the agents themselves.
    - simulation_config.yml: Config for the simulation.
/feeds
    build_feeds.py: manages building feeds
/db
    - memory.py: manages memory I/O. Manages both short-term and long-term memory.
    Exposes a simple API for the agents to use, via a "MemoryManager" class.
/simulation: contains interface for actual simulation platform.
    simulation_manager.py: Manages the simulations themselves.
/evals
/ui
    app.py: core Streamlit app
    /components
        /config
            agent_config.py
            simulation_config.py
        /user
            user.py
            user_feed.py
            user_feed_posts.py
            user_feed_observations.py
            user_feed_interactions.py
        /network
            social_network.py
        /analysis
            analyze_network.py
/planning
/progress_updates
/rules
```
