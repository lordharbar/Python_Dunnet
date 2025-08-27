#!/usr/bin/env python3
"""
ASCII Art Manager for Dunnet Adventure Game
Stores and manages all game artwork and visual elements
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import shutil
from typing import TypeAlias

class ArtType(Enum):
    ROOM = "room"
    ITEM = "item"
    BANNER = "banner"
    DECORATION = "decoration"

@dataclass(frozen=True)
class AsciiArt:
    """ASCII art storage and retrieval system"""
    
    @staticmethod
    def get_terminal_width() -> int:
        """Get terminal width, default to 80 if unavailable"""
        try:
            return shutil.get_terminal_size().columns
        except (OSError, AttributeError):
            return 80
    
    @staticmethod
    def center_art(art: str, width: int | None = None) -> str:
        """Center ASCII art based on terminal width"""
        if width is None:
            width = AsciiArt.get_terminal_width()
        
        lines = art.strip().split('\n')
        centered_lines = []
        for line in lines:
            # Calculate padding for centering
            padding = max(0, (width - len(line)) // 2)
            centered_lines.append(' ' * padding + line)
        
        return '\n'.join(centered_lines)
    
    @classmethod
    def get_game_banner(cls) -> str:
        """Get the main game banner - corrected title"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    ██████╗ ██╗   ██╗███╗   ██╗███╗   ██╗███████╗████████║
║    ██╔══██╗██║   ██║████╗  ██║████╗  ██║██╔════╝╚══██╔══║
║    ██║  ██║██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗     ██║  ║
║    ██║  ██║██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝     ██║  ║
║    ██████╔╝╚██████╔╝██║ ╚████║██║ ╚████║███████╗   ██║  ║
║    ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝   ╚═╝  ║
║                                                          ║
║               A D V E N T U R E   G A M E                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        return cls.center_art(banner)
    
    @classmethod
    def get_room_art(cls, room_id: str) -> str:
        """Get ASCII art for a specific room"""
        room_arts = {
            "driveway": """
    🏠 Suburban House Driveway 🏠
    
         ┌─────────────────┐
         │                 │
         │      🏠 HOUSE    │
         │                 │
    ═════┴═════════════════┴═════
         ║                 ║
         ║   🚗           ║
         ║      YOU ARE    ║
         ║       HERE      ║
    ═════╬═════════════════╬═════
         ║                 ║
         ║     ROAD        ║
            """,
            
            "house": """
    🏠 Cozy Living Room 🏠
    
    ┌─────────────────────────────┐
    │ 🖼️      🕰️           📚    │
    │                           │
    │   🔥      🛋️       📺     │
    │ FIRE     SOFA      TV     │
    │                           │
    │   ☕      🪑       🌱     │
    │ TABLE   CHAIR    PLANT    │
    └─────────────────────────────┘
            """,
            
            "kitchen": """
    👨‍🍳 Modern Kitchen 👨‍🍳
    
    ┌───┬─────────┬───┬─────────┐
    │ 🍞│  🍎🥪   │🥛 │   ☕    │
    ├───┼─────────┼───┼─────────┤
    │   │         │   │         │
    │ 🔥│   🍳    │❄️ │  FRIDGE │
    │   │ STOVE   │   │         │
    └───┴─────────┴───┴─────────┘
            """,
            
            "basement": """
    💻 Tech Basement 💻
    
    ┌─────────────────────────────┐
    │  💡                        │
    │                     📦📦   │
    │  🖥️     💾              │
    │ OLD PC  DISK       BOXES  │
    │                           │
    │    🔌⚡⚡⚡              │
    │   CABLES                  │
    │                    🕷️     │
    └─────────────────────────────┘
            """,
            
            "upstairs": """
    🛏️ Peaceful Bedroom 🛏️
    
    ┌─────────────────────────────┐
    │ 🖼️                    🪟   │
    │                           │
    │         🛏️                │
    │        BED                │
    │                           │
    │  🕯️              👕👔     │
    │ LAMP           CLOSET     │
    └─────────────────────────────┘
            """,
            
            "garden": """
    🌻 Beautiful Garden 🌻
    
         🌤️  ☁️    🌤️
    
    🌳    🌻  🌷  🌺    🌳
      🌱 🌿   🌸   🌿 🌱
    
         🌿  🕳️  🌿
       (suspicious soil)
    
    🌱 🌿 🌹   🌻   🌿 🌱
            """,
            
            "secret": """
    ✨ Hidden Underground Chamber ✨
    
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░  ═══════════════════════   ░
    ░  ║ 💎    ANCIENT     💎 ║  ░
    ░  ║                   ║  ░
    ░  ║   🗝️  SECRETS     ║  ░
    ░  ║     CHAMBER       ║  ░
    ░  ║                   ║  ░
    ░  ║  💰     💎     ⚱️  ║  ░
    ░  ═══════════════════════   ░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            """,
            
            "road": """
    🛣️ Quiet Country Road 🛣️
    
    ═══════════════════════════════
    ║                           ║
    ║  🚗  💨                   ║
    ║                           ║
    ═══════════════════════════════
        │                   │
        │    🌳        🌳   │
        │      TREES        │
        │                   │
        │   YOU ARE HERE    │
            """
        }
        
        art = room_arts.get(room_id, "")
        return cls.center_art(art) if art else ""
    
    @classmethod
    def get_item_art(cls, item_name: str) -> str:
        """Get ASCII art for a specific item"""
        item_arts = {
            "shovel": """
      Trusty Shovel
      
        ┌─┐
        │ │
        │ │
    ────┼─┼────
        └─┘
    """,
            
            "lamp": """
      Electric Lamp
      
        ╭─────╮
        │ 💡  │
        ╰─────╯
          │
         ───
        ╱   ╲
       ╱ ON  ╲
      ╱_______╲
    """,
            
            "key": """
      Brass Key
      
      ╭────╮ ╭─╮
      │    ├─┤ │
      ╰────╯ ╰─╯
         ╰─── Teeth
    """,
            
            "cpu": """
      Computer CPU
      
    ┌───────────────┐
    │ ◯ ◯ ◯ ◯ ◯ ◯ │
    │ ◯ ◯ ◯ ◯ ◯ ◯ │
    │    [CPU]    │
    │ ◯ ◯ ◯ ◯ ◯ ◯ │
    │ ◯ ◯ ◯ ◯ ◯ ◯ │
    └───────────────┘
    """,
            
            "disk": """
      Floppy Disk
      
    ┌─────────────┐
    │ ▐ BACKUP ▌  │
    │ ▐        ▌  │
    │ ▐        ▌  │
    │ ╱╲ 3.5" ╱╲  │
    └─────────────┘
    """,
            
            "food": """
      Trail Mix
      
        ╭─────╮
       ╱ ◉ ◉ ◉ ╲
      ╱  ◯ ◯ ◯  ╲
     ╱   ◉ ◯ ◉   ╲
     ╲ TRAIL MIX ╱
      ╲_________╱
    """,
            
            "water": """
      Water Bottle
      
       ╭───╮
       │ ╱╲│
       ╰─┴─╯
        │ │
        │~│
        │~│ H2O
        │~│
        ╰─╯
    """
        }
        
        art = item_arts.get(item_name, "")
        return cls.center_art(art) if art else ""
    
    @classmethod
    def get_inventory_header(cls) -> str:
        """Get decorative inventory header"""
        return cls.center_art("""
┌─ 🎒 YOUR INVENTORY 🎒 ─┐
        """)
    
    @classmethod
    def get_inventory_footer(cls) -> str:
        """Get decorative inventory footer"""
        return cls.center_art("""
└────────────────────────┘
        """)
    
    @classmethod
    def get_score_display(cls, score: int, moves: int) -> str:
        """Get decorated score display"""
        return cls.center_art(f"""
┌─ 📊 GAME STATS 📊 ─┐
│ Score: {score:>3} points  │
│ Moves: {moves:>3} steps   │
└──────────────────────┘
        """)
    
    @classmethod
    def get_help_banner(cls) -> str:
        """Get decorative help banner"""
        return cls.center_art("""
╔═══════════════════════════════════╗
║         🆘 HELP SYSTEM 🆘         ║
╚═══════════════════════════════════╝
        """)
    
    @classmethod
    def get_victory_art(cls) -> str:
        """Get victory celebration art"""
        return cls.center_art("""
    ✨🎉 CONGRATULATIONS! 🎉✨
    
    ██╗   ██╗ ██████╗ ██╗   ██╗
    ╚██╗ ██╔╝██╔═══██╗██║   ██║
     ╚████╔╝ ██║   ██║██║   ██║
      ╚██╔╝  ██║   ██║██║   ██║
       ██║   ╚██████╔╝╚██████╔╝
       ╚═╝    ╚═════╝  ╚═════╝
    
    ██╗    ██╗ ██████╗ ███╗   ██╗
    ██║    ██║██╔═══██╗████╗  ██║
    ██║ █╗ ██║██║   ██║██╔██╗ ██║
    ██║███╗██║██║   ██║██║╚██╗██║
    ╚███╔███╔╝╚██████╔╝██║ ╚████║
     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝
    
       🏆 DUNNET MASTER! 🏆
        """)
    
    @classmethod  
    def get_separator(cls, char: str = "═", length: int | None = None) -> str:
        """Get a decorative separator line"""
        if length is None:
            length = min(50, cls.get_terminal_width() - 10)
        return cls.center_art(char * length)
    
    @classmethod
    def get_loading_animation(cls, step: int) -> str:
        """Get simple loading animation frame"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        return frames[step % len(frames)]
    
    @classmethod
    def get_compass_rose(cls) -> str:
        """Get decorative compass for navigation help"""
        return cls.center_art("""
        ╭─────╮
        │  ↑  │
        │ ←⊕→ │
        │  ↓  │
        ╰─────╯
        """)
    
    @classmethod
    def get_welcome_message(cls) -> str:
        """Get formatted welcome message"""
        return cls.center_art("Welcome to Dunnet! Type 'help' for commands or 'quit' to exit.")