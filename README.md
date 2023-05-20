# PygamePlatformerEngine
A simple 2D platformer engine written in Python/Pygame.

## TO DO:
1. Perform additional testing, especially for new collision bugs and scrolling hiccups since CameraGroups have been heavily rewritten.
2. Further address stamina handler so that stamina reductions when jumping (especially when between ceiling and floor) are more sensible.
3. Implement a way to control sprites and animations.
4. Tighten the current player tracking camera so that feels much smoother for the player.
5. Start thinking about level design and zone transitions.
6. Consider adding a branch for the project without stamina mechanics in case I decide to scrap it in the future.

## IN PROGRESS:
2. Refactor the code so the code is more understandable, and so that adding additional future features is easier to manage.
3. Create sprites and assets for the game (ongoing).
4. Implement functionality to gather information on the player state (idling, running, jumping, falling, attacking, taking damage, ect.

## DONE:
1. Add more detailed comments in the code so that its purpose is more clear (this is important for future development of features).
2. 1. Begin working on the stamina and jumping handler so that they affect player behavior once the values are depleted.
3. Rewrote the Camera Groups in camera.py so that they are fully instanced objects and drastically cut down on function complexity. 
