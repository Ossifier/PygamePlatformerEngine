from settings import screen_width, screen_height


class CameraGroup:
    def __init__(self):

        # World Shift Variables #
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.scroll_threshold_left = 0.25
        self.scroll_threshold_right = 0.5
        self.scroll_threshold_top = 0.5
        self.scroll_threshold_bottom = 0.9
        
    def snap_camera(self, target, map_layout, offset_x, offset_y):
        """NOTES: This function snaps the camera to an object. It works by shifting the player sprite and level sprites
        simultaneously by an offset that is calculated by the target object's original x/y coordinates (obj_x/y), and
        the offset_x/y variables. These offset variables are percentages, and must be between 0 and 1 for the snap to
        land within the display screen.
        This function requires a target sprite (target), and the enumerated level layout (map_layout) so that the
        object/level offsets can be applied appropriately."""
        # Calculate Offsets #
        cam_adjust_x = screen_width * offset_x
        cam_adjust_y = screen_height * offset_y
        level_shift_x = target.rect.centerx - cam_adjust_x
        level_shift_y = target.rect.centery - cam_adjust_y

        # Center Object on Screen #
        target.rect.centerx = cam_adjust_x
        target.rect.centery = cam_adjust_y

        # Shift Level to Object's Location via Offset #
        for sprite in map_layout:
            sprite.rect.centerx -= level_shift_x
            sprite.rect.centery -= level_shift_y

        print('Centered from CameraGroup_Test')  # This is for testing purposes to ensure that importing works properly.
        
    def scroll_x_follow(self, target):
        """NOTES: This function scrolls the screen horizontally as the player approaches the edge of a specified
        threshold. These scrolling thresholds are controlled by the Level attributes self.scroll_threshold_leftx and
        self.scroll_threshold_rightx. They can be adjusted to meet the needs of a particular stage."""
        target_center_x = target.rect.centerx
        target_dir_x = target.direction.x

        if target_center_x < screen_width * self.scroll_threshold_left and target_dir_x < 0:
            self.world_shift_x = -round(target_dir_x)
            target.move_speed = 0
        elif target_center_x > screen_width * self.scroll_threshold_right and target_dir_x > 0:
            self.world_shift_x = -round(target_dir_x)
            target.move_speed = 0
        else:
            self.world_shift_x = 0
            target.move_speed = 1
            
    def scroll_y_follow(self, target):
        """NOTES: This function scrolls the screen horizontally as the target approaches the edge of a specified
        threshold. This particular function follows the target at the scroll threshold in the direction they are
        travelling to keep them within the inside of the screen.
        Special adjustments are made for when the target reaches the threshold to adjust the to ensure that collision
        bugs don't occur while the player is scrolling and landing/hitting the ceiling."""
        # Bottom Screen Scrolling #
        if target.rect.centery > screen_height * self.scroll_threshold_bottom:
            if self.world_shift_y == 0:                         # Border Offset
                target.rect.centery += target.direction.y

            self.world_shift_y = -round(target.direction.y)
            target.rect.centery -= target.direction.y

        # Top Screen Scrolling #
        elif target.rect.centery < screen_height * self.scroll_threshold_top and target.direction.y < 0:
            if self.world_shift_y == 0:                         # Border Offset
                target.rect.centery += target.direction.y

            self.world_shift_y = -round(target.direction.y - 1)
            target.rect.centery -= target.direction.y

        # Player Within Screen Scrolling Boundaries #
        else:
            self.world_shift_y = 0
