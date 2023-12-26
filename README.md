# PygamePlatformerEngine
A simple 2D platformer engine written in Python/Pygame. Contains some simple souls-like elements such as stamina handling for flavor, but this logic may be removed in a future branch.

## NOTES:
1. This branch name has been changed to reflect that this branch is for the version of the engine that includes frame interpolation logic, and changed to be the deafult working branch for this project. The prior main branch has been renamed. If you would like to access the older version, you'll find it there.
2. Also, I'm back after having been pulled away from this project due to work.

## TO DO (Interpolation):
Fully implement interpolation for the following piece of logic:
1. Stamina drain/recharge.
2. Jump Power drain/recharge.
3. Animation cycles.
4. Find, locate, and correct collision bugs arising from new interpolation logic.

## TO DO (General):
1. Finish player character spritesheet so development can proceed.
2. Rewrite stamina_handler function in player.py to adequately address how to handle stamina when in the ground vs. in the air.
3. Begin planning zones, level transitions, and maps.
4. Fix Low-Grav Collision Bug where Vertical Collision = Horizontal Collision when scrolling top. 
5. Implement delta-time frame interpolation to the game. This will be a big project.

## IN PROGRESS:
1. Create art for the game.
2. Fix small bug when hold-jumping from out of a 64h px corridor.

## TO PLAN:
1. Tighten the current player tracking camera so that feels much smoother for the player.
2. Start thinking about level design and zone transitions.
3. Consider adding a branch for the project without stamina mechanics in case I decide to scrap it in the future.
4. Refactor the code so the code is more understandable, and so that adding additional future features is easier to manage.

## DONE:
1. Further address stamina handler so that stamina reductions when jumping (especially when between ceiling and floor) are more sensible.
2. Add more detailed comments in the code so that its purpose is more clear (this is important for future development of features).
3. Begin working on the stamina and jumping handler so that they affect player behavior once the values are depleted.
4. Rewrote the Camera Groups in camera.py so that they are fully instanced objects and drastically cut down on function complexity.
5. Add logic for generating SpriteSheet objects and handling sprite asset importing, specifically for the Player.
6. Perform additional testing, especially for new collision bugs and scrolling hiccups since CameraGroups have been heavily rewritten.
7. Moved animation dictionaries to entity class attribute and added animation state builders so the same logic can be implemented for building sprite sheets for other entities as they are added.
8. Build a utility for constructing _config.json files for sprite sheets.
9. Develop the logic for how the game will handle animations for players and other entities.
10. Implement functionality to gather information on the player state (idling, running, jumping, falling, attacking, taking damage, ect.
11. Fix level layout decoupling/drifting when screen scrolling (due to rounding errors).
12. Fix state-switching bug when player is jumping between ceiling/floor.
