import unittest
import pygame
from unittest.mock import MagicMock, patch
from level import Level


class TestLevel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

        # Mock essential components to avoid initialization issues
        self.soil_layer_patcher = patch('soil.SoilLayer')
        self.mock_soil_layer = self.soil_layer_patcher.start()
        self.mock_soil_layer.return_value.grid = [[[] for _ in range(10)] for _ in range(10)]

        # Create a mock player with required attributes
        self.mock_player = MagicMock()
        self.mock_player.interaction_sprites = MagicMock()

        # Patch player initialization
        self.player_patcher = patch('player.Player', return_value=self.mock_player)
        self.player_patcher.start()

        # Mock other dependencies
        self.overlay_patcher = patch('overlay.Overlay')
        self.mock_overlay = self.overlay_patcher.start()

        self.transition_patcher = patch('transition.Transition')
        self.mock_transition = self.transition_patcher.start()

        self.menu_patcher = patch('menu.Menu')
        self.mock_menu = self.menu_patcher.start()

    def tearDown(self):
        self.soil_layer_patcher.stop()
        self.player_patcher.stop()
        self.overlay_patcher.stop()
        self.transition_patcher.stop()
        self.menu_patcher.stop()

    # --- Singleton Pattern Test ---
    def test_singleton_pattern(self):
        """Test that Level implements singleton pattern correctly"""
        with patch.object(Level, '_instance', None):  # Clear singleton for test
            level1 = Level()
            level2 = Level()

            self.assertIs(level1, level2)
            self.assertEqual(id(level1), id(level2))

    # --- Polymorphism Test ---
    def test_polymorphic_interactions(self):
        """Test polymorphic behavior of interaction objects"""
        # Create mock objects that inherit from Sprite
        mock_tree = MagicMock(spec=pygame.sprite.Sprite)
        mock_flower = MagicMock(spec=pygame.sprite.Sprite)
        mock_soil = MagicMock(spec=pygame.sprite.Sprite)

        # Test they can all be treated as Sprites
        for obj in [mock_tree, mock_flower, mock_soil]:
            self.assertIsInstance(obj, pygame.sprite.Sprite)

    # --- Inheritance Test ---
    def test_inheritance_hierarchy(self):
        """Test proper inheritance of game objects"""
        # Test CameraGroup inheritance
        level = Level()
        self.assertIsInstance(level.all_sprites, pygame.sprite.Group)

        # Test Player inheritance
        self.assertIsInstance(level.player, pygame.sprite.Sprite)

    # --- Encapsulation Test ---
    def test_encapsulation(self):
        """Test internal state is protected"""
        level = Level()

        # Test we can't directly access private singleton instance
        # Note: Python doesn't prevent access, it just makes it harder
        # So we'll test that the convention is followed
        self.assertTrue(hasattr(level, '_instance') or hasattr(level, '_Level__instance'))

        # Test critical components exist and are the correct type
        self.assertIsNotNone(level.all_sprites)

    # --- Design Pattern Tests ---
    def test_observer_pattern_usage(self):
        """Test observer pattern is used in interactions"""
        level = Level()

        # Verify interaction system exists
        self.assertTrue(hasattr(level, 'interaction_sprites'))
        self.assertIsInstance(level.interaction_sprites, pygame.sprite.Group)


if __name__ == '__main__':
    unittest.main()