from .seeds.source_types import seed_source_types
from .seeds.fact_types import seed_fact_types  # if you have this

def seed():
    seed_source_types()
    seed_fact_types()
    # Add more as you modularize
