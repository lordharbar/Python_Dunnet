# 🏠 Dunnet Adventure Game

*A text-based adventure game that'll make you nostalgic for the days when graphics were left to your imagination*

## What is this thing?

Remember when games didn't need 100GB of storage and your GPU didn't sound like a jet engine? This is a throwback to those simpler times - a text adventure game inspired by the classic "Dunnet" that shipped with Emacs (yes, people actually played games in their text editor).

You're standing in a driveway. There's a shovel here. What could possibly go wrong?

## Requirements

- Python 3.11+ (because..)
- UV
- A sense of adventure
- The ability to read (surprisingly important for a text game)
- Optional: Nostalgia for the 1980s

## Installation

```bash
git clone this-repo
cd dunnet-adventure
uv sync 
uv run main.py
```

That's it. No npm install hell, no Docker containers, no Kubernetes clusters. Just good old-fashioned Python.

## How to Play

Type commands like a civilized person:

- **Movement**: `north`, `south`, `east`, `west`, `up`, `down` (or just `n`, `s`, `e`, `w`, `u`, `d` if you're in a hurry)
- **Interaction**: `take shovel`, `examine lamp`, `use key`, `inventory`
- **Special Actions**: `dig` (with the right tool), `turn on lamp` (darkness is the enemy)
- **Meta**: `help`, `score`, `quit`

### Pro Tips

1. **Examine everything** - seriously, everything. That innocent-looking garden might hide secrets.
2. **Light is life** - some places are darker than a developer's sense of humor at 3 AM
3. **Dig where it makes sense** - not every room needs excavation, but some do
4. **Take everything that isn't nailed down** - classic adventure game rule
5. **Read the room descriptions** - they're not just flavor text (okay, some are)

## Game Features

- **Multiple rooms** to explore (more than a studio apartment!)
- **Items to collect** and actually use (revolutionary!)
- **Puzzles to solve** (nothing too brain-bending, we promise)
- **A scoring system** (for bragging rights)
- **Win condition** (yes, you can actually beat this game)

## Sample Gameplay

```
> look
**Driveway**

You are standing in the driveway of a large suburban house. There is a shovel here.

You can see:
  - A sturdy metal shovel for digging.

Exits: north, south, east

> take shovel
You take the shovel.

> north
**Living Room**

You are in a comfortable living room with a fireplace.

Exits: south, east, up

> examine fireplace
You don't see any 'fireplace' here.

> up
**Bedroom**

A cozy bedroom with a lamp on the nightstand.

You can see:
  - A bright electric lamp.

Exits: down
```
The core game loop uses a dictionary to map commands to functions, making it trivial to add new functionality without touching existing code. It's like the Open/Closed Principle actually works!

## Contributing

Found a bug? Want to add a room? Think the game needs more cowbell? 

- Fork it
- Fix it
- Submit a PR
- Profit??? (there's no profit, this is open source)

## License

MIT - Do whatever you want with this code. Build an empire, teach your kids, use it in job interviews, whatever. Just don't blame us if you get addicted to text adventures again.

## FAQ

**Q: Is this better than modern games?**  
A: Define "better". Does it have ray tracing? No. Will it run on a potato? Absolutely.

**Q: How long does it take to complete?**  
A: Anywhere from 10 minutes to 3 hours, depending on how thoroughly you explore and how often you get distracted trying to `examine` everything.

**Q: Can I add more rooms/items/features?**  
A: Yes! The code is designed to make this easy. Check out the `_initialize_world()` method to see how rooms and items are set up.

**Q: Why did you make this?**  
A: Someone needed to demonstrate command dispatch patterns, and making a calculator seemed boring.

**Q: Will this make me a better programmer?**  
A: Probably not, but you'll understand dictionaries and functions better, and that's something.

---

*Made with ❤️ and probably some wine*