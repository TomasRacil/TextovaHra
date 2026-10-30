from ..registry import command

@command("rozhledni", "popíše místnost, východy a předměty")
def look_command(game, argument: str) -> str:
    room = game.room
    lines = [f"== {room.name} =="]
    if room.description:
        lines.append(room.description)
    if room.exits:
        lines.append("Východy: " + ", ".join(sorted(room.exits)))
    else:
        lines.append("Odsud se nedá nikam jít.")
    if room.items:
        lines.append("Předměty: " + ", ".join(item.name for item in room.items))
    return "\n".join(lines)