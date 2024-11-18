def prune():
    from channels_presence.models import Room
    Room.objects.prune_presences()