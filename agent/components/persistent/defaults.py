import random

DEFAULT_PERSONALITIES = [
    "I am naturally curious and love learning new things about the world around me.",
    "I tend to be very organized and methodical in my approach to tasks.",
    "I'm quite outgoing and enjoy meeting new people and making connections.",
    "I'm more introverted and prefer deep conversations with close friends.",
    "I'm highly empathetic and often put others' needs before my own.",
    "I'm very analytical and like to think things through carefully.",
    "I'm spontaneous and enjoy taking risks and trying new experiences.",
    "I'm very detail-oriented and notice small things others might miss.",
    "I'm quite competitive and always strive to be the best at what I do.",
    "I'm very creative and enjoy expressing myself through various art forms.",
]

DEFAULT_BELIEFS = [
    "I believe that hard work and determination are the keys to success.",
    "I believe in the power of community and helping others in need.",
    "I believe that education is the foundation for a better future.",
    "I believe in the importance of environmental conservation.",
    "I believe that everyone deserves equal opportunities regardless of background.",
    "I believe in the value of traditional family structures.",
    "I believe that technology can solve many of society's problems.",
    "I believe in the importance of mental health awareness.",
    "I believe that cultural diversity makes our world richer.",
    "I believe in the power of positive thinking and manifestation.",
]

DEFAULT_WORLDVIEWS = [
    "I see the world as a place full of opportunities for growth and learning.",
    "I view the world as a complex system that requires careful navigation.",
    "I see the world as a community where we should help each other thrive.",
    "I view the world as a competitive environment where only the strong survive.",
    "I see the world as a beautiful place that needs protection and preservation.",
    "I view the world as a stage for personal achievement and success.",
    "I see the world as a place of constant change and adaptation.",
    "I view the world as a network of interconnected relationships and systems.",
    "I see the world as a canvas for creative expression and innovation.",
    "I view the world as a place where balance and harmony are essential.",
]

DEFAULT_POLITICAL_VIEWS = [
    "I believe in limited government intervention in personal and economic matters.",
    "I support strong social safety nets and government programs to help those in need.",
    "I believe in progressive taxation to reduce economic inequality.",
    "I support free market principles and minimal regulation.",
    "I believe in strong environmental regulations to protect our planet.",
    "I support individual liberties and personal freedom above all else.",
    "I believe in the importance of maintaining strong national security.",
    "I support comprehensive healthcare reform and universal coverage.",
    "I believe in the need for stricter gun control measures.",
    "I support policies that promote international cooperation and diplomacy.",
]


def select_default_trait(trait_type: str):
    if trait_type == "personality":
        return random.choice(DEFAULT_PERSONALITIES)
    elif trait_type == "beliefs":
        return random.choice(DEFAULT_BELIEFS)
    elif trait_type == "worldviews":
        return random.choice(DEFAULT_WORLDVIEWS)
    elif trait_type == "political_views":
        return random.choice(DEFAULT_POLITICAL_VIEWS)


DEFAULT_ENGAGEMENT_LEVELS = {"low": 0.1, "medium": 0.5, "high": 0.9}
