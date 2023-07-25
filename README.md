# PygamePlatformerEngine
A simple 2D platformer engine written in Python/Pygame. Contains some simple souls-like elements such as stamina handling for flavor, but this logic may be removed in a future branch.

## TO DO:

1. Build a utility for constructing _config.json files for sprite sheets.
1. Fix the following bugs for stamina handling: Stamina depeltion while Jumping/Non-Sprinting doesn't wind... In air sprint --> No penalty.
2. Tighten the current player tracking camera so that feels much smoother for the player.
3. Start thinking about level design and zone transitions.
4. Consider adding a branch for the project without stamina mechanics in case I decide to scrap it in the future.

## IN PROGRESS:
1. Develop the logic for how the game will handle animations for players and other entities.
2. Refactor the code so the code is more understandable, and so that adding additional future features is easier to manage.
3. Create sprites and assets for the game (ongoing).
4. Implement functionality to gather information on the player state (idling, running, jumping, falling, attacking, taking damage, ect.

## DONE:
1. Further address stamina handler so that stamina reductions when jumping (especially when between ceiling and floor) are more sensible.
2. Add more detailed comments in the code so that its purpose is more clear (this is important for future development of features).
3. Begin working on the stamina and jumping handler so that they affect player behavior once the values are depleted.
4. Rewrote the Camera Groups in camera.py so that they are fully instanced objects and drastically cut down on function complexity.
5. Add logic for generating SpriteSheet objects and handling sprite asset importing, specifically for the Player.
6. Perform additional testing, especially for new collision bugs and scrolling hiccups since CameraGroups have been heavily rewritten.
7. Moved animation dictionaries to entity class attribute and added animation state builders so the same logic can be implemented for building sprite sheets for other entities as they are added.
