import math

def get_distance(entity1, entity2):
    """
    Calculate the Euclidean distance between two entities.
    """
    dx = entity1.rect.centerx - entity2.rect.centerx
    dy = entity1.rect.centery - entity2.rect.centery
    return math.hypot(dx, dy)
