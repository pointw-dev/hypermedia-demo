from hypermea.core.domain import Relation, external, local

RELATION_REGISTRY = [
    Relation(parent='venue', child='event'),
    Relation(parent='event', child='registration'),
    Relation(parent='account', child='registration'),
    
]
