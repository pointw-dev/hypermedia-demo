from hypermea.core.domain import Relation, external, local

RELATION_REGISTRY = [
    Relation(parent=external('event'), child='registration'),
    Relation(parent=external('account'), child='registration')
]
