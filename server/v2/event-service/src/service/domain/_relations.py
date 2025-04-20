from hypermea.core.domain import Relation, external, local

RELATION_REGISTRY = [
    Relation(parent=external('venue'), child='event'),
    Relation(parent='event', child=external('registration'))
]
