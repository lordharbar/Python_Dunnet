#!/usr/bin/env python3
"""
Dunnet-style Text Adventure Game
A modern Python implementation using command dispatch patterns
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import TypeAlias, Callable, Any
from pathlib import Path
import sys
from enum import Enum, auto
import random

# Type aliases for better readability
CommandFunction: TypeAlias = Callable[["GameState", list[str]], "GameResult"]
ItemDict: TypeAlias = dict[str, "Item"]
RoomDict: TypeAlias = dict[str, "Room"]

class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"
    NORTHEAST = "northeast"
    NORTHWEST = "northwest"
    SOUTHEAST = "southeast"
    SOUTHWEST = "southwest"

@dataclass(frozen=True)
class GameResult:
    """Result of a game action"""
    message: str
    game_over: bool = False
    clear_screen: bool = False

@dataclass
class Item:
    """Game item with properties"""
    name: str
    description: str
    portable: bool = True
    usable: bool = False
    aliases: list[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        # Ensure the item's name is in its aliases for easier lookup
        if self.name.lower() not in [alias.lower() for alias in self.aliases]:
            self.aliases.append(self.name.lower())

@dataclass
class Room:
    """Game room/location"""
    name: str
    description: str
    exits: dict[Direction, str] = field(default_factory=dict)
    items: list[str] = field(default_factory=list)
    visited: bool = False
    dark: bool = False

@dataclass
class GameState:
    """Complete game state"""
    current_room: str = "driveway"
    inventory: list[str] = field(default_factory=list)
    rooms: RoomDict = field(default_factory=dict)
    items: ItemDict = field(default_factory=dict)
    game_over: bool = False
    score: int = 0
    moves: int = 0
    
    def __post_init__(self) -> None:
        if not self.rooms:
            self._initialize_world()
    
    def _initialize_world(self) -> None:
        """Initialize the game world"""
        # Create items
        self.items = {
            "shovel": Item("shovel", "A sturdy metal shovel for digging.", aliases=["spade"]),
            "lamp": Item("lamp", "A bright electric lamp.", usable=True, aliases=["light", "lantern"]),
            "key": Item("key", "A small brass key.", aliases=["brass key"]),
            "cpu": Item("cpu", "A computer CPU chip.", aliases=["chip", "processor"]),
            "disk": Item("disk", "A floppy disk labeled 'BACKUP'.", aliases=["floppy", "backup"]),
            "food": Item("food", "Some nutritious trail mix.", usable=True, aliases=["trail mix", "snack"]),
            "water": Item("water", "A bottle of fresh water.", usable=True, aliases=["bottle"]),
        }
        
        # Create rooms
        self.rooms = {
            "driveway": Room(
                "Driveway",
                "You are standing in the driveway of a large suburban house. There is a shovel here.",
                exits={Direction.NORTH: "house", Direction.SOUTH: "road", Direction.EAST: "garden"},
                items=["shovel"]
            ),
            "house": Room(
                "Living Room", 
                "You are in a comfortable living room with a fireplace.",
                exits={Direction.SOUTH: "driveway", Direction.EAST: "kitchen", Direction.UP: "upstairs"}
            ),
            "kitchen": Room(
                "Kitchen",
                "A modern kitchen with granite countertops. There's some food on the counter.",
                exits={Direction.WEST: "house", Direction.DOWN: "basement"},
                items=["food"]
            ),
            "basement": Room(
                "Basement",
                "A dark basement filled with old computers and equipment. You see a CPU and disk here.",
                exits={Direction.UP: "kitchen"},
                items=["cpu", "disk"],
                dark=True
            ),
            "upstairs": Room(
                "Bedroom",
                "A cozy bedroom with a lamp on the nightstand.",
                exits={Direction.DOWN: "house"},
                items=["lamp"]
            ),
            "garden": Room(
                "Garden",
                "A beautiful garden behind the house. You notice some loose soil near a tree.",
                exits={Direction.WEST: "driveway", Direction.DOWN: "secret"}
            ),
            "secret": Room(
                "Secret Room",
                "You've discovered a hidden underground chamber! There's a key here.",
                exits={Direction.UP: "garden"},
                items=["key"]
            ),
            "road": Room(
                "Country Road",
                "You're on a quiet country road. There's a bottle of water by the roadside.",
                exits={Direction.NORTH: "driveway"},
                items=["water"]
            ),
        }

class DunnetGame:
    """Main game class implementing the text adventure"""
    
    def __init__(self) -> None:
        self.state = GameState()
        self.lamp_on = False
        
        # Command dispatch dictionary - the core pattern!
        self.commands: dict[str, CommandFunction] = {
            "look": self._look,
            "l": self._look,
            "examine": self._examine,
            "ex": self._examine,
            "x": self._examine,
            "take": self._take,
            "get": self._take,
            "drop": self._drop,
            "inventory": self._inventory,
            "i": self._inventory,
            "go": self._go,
            "north": self._go_north,
            "south": self._go_south,
            "east": self._go_east,
            "west": self._go_west,
            "up": self._go_up,
            "down": self._go_down,
            "n": self._go_north,
            "s": self._go_south,
            "e": self._go_east,
            "w": self._go_west,
            "u": self._go_up,
            "d": self._go_down,
            "use": self._use,
            "turn": self._turn,
            "dig": self._dig,
            "help": self._help,
            "quit": self._quit,
            "q": self._quit,
            "score": self._score,
        }
    
    def _find_item(self, item_name: str) -> Item | None:
        """Find item by name or alias"""
        item_name_lower = item_name.lower()
        for item in self.state.items.values():
            if item_name_lower in [alias.lower() for alias in item.aliases]:
                return item
        return None
    
    def _current_room(self) -> Room:
        """Get the current room object"""
        return self.state.rooms[self.state.current_room]
    
    def _can_see(self) -> bool:
        """Check if player can see in current room"""
        room = self._current_room()
        return not room.dark or (self.lamp_on and "lamp" in self.state.inventory)
    
    def _look(self, state: GameState, args: list[str]) -> GameResult:
        """Look around the current room"""
        room = self._current_room()
        
        if not self._can_see():
            return GameResult("It is too dark to see anything.")
        
        # Mark room as visited
        room.visited = True
        
        # Build description
        description = [f"**{room.name}**", "", room.description]
        
        # Add items
        visible_items = [item for item in room.items 
                        if item in self.state.items]
        if visible_items:
            description.append("")
            description.append("You can see:")
            for item_name in visible_items:
                item = self.state.items[item_name]
                description.append(f"  - {item.description}")
        
        # Add exits
        if room.exits:
            description.append("")
            exits = [direction.value for direction in room.exits.keys()]
            description.append(f"Exits: {', '.join(exits)}")
        
        return GameResult("\n".join(description))
    
    def _examine(self, state: GameState, args: list[str]) -> GameResult:
        """Examine an item or room feature"""
        if not args:
            return self._look(state, args)
        
        if not self._can_see():
            return GameResult("It is too dark to see anything.")
        
        target = " ".join(args)
        item = self._find_item(target)
        
        if not item:
            return GameResult(f"You don't see any '{target}' here.")
        
        # Check if item is accessible (in room or inventory)
        room = self._current_room()
        if item.name not in room.items and item.name not in state.inventory:
            return GameResult(f"You don't see any '{target}' here.")
        
        return GameResult(item.description)
    
    def _take(self, state: GameState, args: list[str]) -> GameResult:
        """Take an item"""
        if not args:
            return GameResult("Take what?")
        
        if not self._can_see():
            return GameResult("It is too dark to see anything.")
        
        target = " ".join(args)
        item = self._find_item(target)
        
        if not item:
            return GameResult(f"You don't see any '{target}' here.")
        
        room = self._current_room()
        if item.name not in room.items:
            return GameResult(f"You don't see any '{target}' here.")
        
        if not item.portable:
            return GameResult(f"You can't take the {item.name}.")
        
        # Move item from room to inventory
        room.items.remove(item.name)
        state.inventory.append(item.name)
        state.score += 5
        
        return GameResult(f"You take the {item.name}.")
    
    def _drop(self, state: GameState, args: list[str]) -> GameResult:
        """Drop an item"""
        if not args:
            return GameResult("Drop what?")
        
        target = " ".join(args)
        item = self._find_item(target)
        
        if not item or item.name not in state.inventory:
            return GameResult(f"You don't have any '{target}'.")
        
        # Move item from inventory to room
        state.inventory.remove(item.name)
        room = self._current_room()
        room.items.append(item.name)
        
        return GameResult(f"You drop the {item.name}.")
    
    def _inventory(self, state: GameState, args: list[str]) -> GameResult:
        """Show inventory"""
        if not state.inventory:
            return GameResult("You are carrying nothing.")
        
        items_desc = []
        for item_name in state.inventory:
            item = state.items[item_name]
            items_desc.append(f"  - {item.name}")
        
        return GameResult("You are carrying:\n" + "\n".join(items_desc))
    
    def _go(self, state: GameState, args: list[str]) -> GameResult:
        """Go in a specified direction"""
        if not args:
            return GameResult("Go where?")
        
        direction_str = args[0].lower()
        try:
            direction = Direction(direction_str)
        except ValueError:
            return GameResult(f"You can't go '{direction_str}'.")
        
        return self._move(direction)
    
    def _go_north(self, state: GameState, args: list[str]) -> GameResult:
        return self._move(Direction.NORTH)
    
    def _go_south(self, state: GameState, args: list[str]) -> GameResult:
        return self._move(Direction.SOUTH)
    
    def _go_east(self, state: GameState, args: list[str]) -> GameResult:
        return self._move(Direction.EAST)
    
    def _go_west(self, state: GameState, args: list[str]) -> GameResult:
    
        return self._move(Direction.WEST)
    
    def _go_up(self, state: GameState, args: list[str]) -> GameResult:
        return self._move(Direction.UP)
    
    def _go_down(self, state: GameState, args: list[str]) -> GameResult:
        return self._move(Direction.DOWN)
    
    def _move(self, direction: Direction) -> GameResult:
        """Handle movement in any direction"""
        room = self._current_room()
        
        if direction not in room.exits:
            return GameResult("You can't go that way.")
        
        next_room_id = room.exits[direction]
        self.state.current_room = next_room_id
        self.state.moves += 1
        
        # Auto-look in new room
        return self._look(self.state, [])
    
    def _use(self, state: GameState, args: list[str]) -> GameResult:
        """Use an item"""
        if not args:
            return GameResult("Use what?")
        
        target = " ".join(args)
        item = self._find_item(target)
        
        if not item or item.name not in state.inventory:
            return GameResult(f"You don't have any '{target}'.")
        
        if not item.usable:
            return GameResult(f"You can't use the {item.name}.")
        
        # Handle specific item usage
        match item.name:
            case "lamp":
                self.lamp_on = not self.lamp_on
                action = "turn on" if self.lamp_on else "turn off"
                return GameResult(f"You {action} the lamp.")
            case "food":
                state.inventory.remove("food")
                state.score += 10
                return GameResult("You eat the trail mix. You feel refreshed!")
            case "water":
                state.inventory.remove("water")
                state.score += 10
                return GameResult("You drink the water. Very refreshing!")
            case _:
                return GameResult(f"You can't figure out how to use the {item.name}.")
    
    def _turn(self, state: GameState, args: list[str]) -> GameResult:
        """Turn something on/off"""
        if len(args) < 2:
            return GameResult("Turn what on or off?")
        
        action = args[0].lower()
        target = " ".join(args[1:])
        
        if target.lower() in ["lamp", "light", "lantern"] and "lamp" in state.inventory:
            match action:
                case "on":
                    self.lamp_on = True
                    return GameResult("You turn on the lamp.")
                case "off":
                    self.lamp_on = False
                    return GameResult("You turn off the lamp.")
                case _:
                    return GameResult("You can 'turn on' or 'turn off' the lamp.")
        
        return GameResult(f"You can't turn {action} the {target}.")
    
    def _dig(self, state: GameState, args: list[str]) -> GameResult:
        """Dig with shovel"""
        if "shovel" not in state.inventory:
            return GameResult("You need something to dig with.")
        
        room = self._current_room()
        
        if state.current_room == "garden" and "secret" not in [state.rooms[exit_room].name for exit_room in room.exits.values()]:
            # Create secret passage
            room.exits[Direction.DOWN] = "secret"
            state.score += 25
            return GameResult("You dig in the soft soil and discover a hidden passage leading down!")
        
        return GameResult("You dig around but find nothing interesting.")
    
    def _help(self, state: GameState, args: list[str]) -> GameResult:
        """Show help information"""
        help_text = """
**Dunnet Adventure Game Commands:**

**Movement:** north (n), south (s), east (e), west (w), up (u), down (d)
**Items:** take [item], drop [item], examine [item], inventory (i)
**Actions:** use [item], turn on/off [item], dig
**Game:** look (l), help, score, quit (q)

**Tips:**
- Examine everything you find
- Some areas might be dark - you'll need light
- Try digging in interesting places
- Your goal is to explore and increase your score!
        """
        return GameResult(help_text.strip())
    
    def _score(self, state: GameState, args: list[str]) -> GameResult:
        """Show current score"""
        return GameResult(f"Score: {state.score} points in {state.moves} moves")
    
    def _quit(self, state: GameState, args: list[str]) -> GameResult:
        """Quit the game"""
        return GameResult(
            f"Thanks for playing! Final score: {state.score} points in {state.moves} moves.",
            game_over=True
        )
    
    def process_command(self, user_input: str) -> GameResult:
        """Process user command using dispatch pattern"""
        if not user_input.strip():
            return GameResult("Type 'help' for available commands.")
        
        # Parse command and arguments
        parts = user_input.strip().lower().split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Dispatch to appropriate command handler
        command_func = self.commands.get(command, self._unknown_command)
        result = command_func(self.state, args)
        
        # Check win condition
        if (self.state.current_room == "secret" and 
            "key" in self.state.inventory and 
            self.state.score >= 50):
            return GameResult(
                result.message + "\n\n🎉 **CONGRATULATIONS!** You've won the game! " +
                f"Final score: {self.state.score} points!",
                game_over=True
            )
        
        return result
    
    def _unknown_command(self, state: GameState, args: list[str]) -> GameResult:
        """Handle unknown commands"""
        suggestions = [
            "Try 'help' to see available commands.",
            "Use 'look' to examine your surroundings.",
            "Type 'inventory' to see what you're carrying."
        ]
        return GameResult(f"I don't understand that command. {random.choice(suggestions)}")

def main() -> None:
    """Main game loop"""
    print("🏠 **DUNNET ADVENTURE GAME** 🏠")
    print("=" * 40)
    print("Welcome to Dunnet! Type 'help' for commands or 'quit' to exit.")
    print("=" * 40)
    
    game = DunnetGame()
    
    # Show initial room
    result = game._look(game.state, [])
    print(f"\n{result.message}\n")
    
    # Main game loop
    while not game.state.game_over:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
                
            result = game.process_command(user_input)
            print(f"\n{result.message}\n")
            
            if result.game_over:
                break
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()