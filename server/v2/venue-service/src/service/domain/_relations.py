from hypermea.core.domain import Relation, external, local

RELATION_REGISTRY = [
    Relation(parent='venue', child=external('event'))
]
