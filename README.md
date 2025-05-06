# One Summer's Day - Farming Simulation Game

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange)
![OOP](https://img.shields.io/badge/OOP-4%20Pillars-success)
![Design Patterns](https://img.shields.io/badge/Patterns-5%20Implemented-important)

A 2D farming simulation game demonstrating advanced Object-Oriented Programming principles and design patterns.

## Table of Contents
- [Core Features](#core-features)
- [OOP Concepts](#oop-concepts-implemented)
- [Design Patterns](#design-patterns)
- [Farming System](#farming-system)
- [File I/O](#file-io-operations)
- [Testing](#testing)
- [Installation](#installation)
- [Controls](#controls)

## Core Features
- **Farming System**: Till, plant, water, and harvest crops
- **Day/Night Cycle**: Sleep to save and advance time
- **Inventory Management**: Track collected items
- **Tool System**: Hoe, axe, watering can, and pickaxe
- **Save/Load**: Persistent game state

## OOP Concepts Implemented

### Polymorphism
- **Growable ABC** with Plant implementation
- **Sprite system** handles different game objects uniformly
- **Tool actions** use same interface for different effects
- **Render strategies** with common draw interface

### Abstraction
- **SoilLayer** manages complex soil/plant interactions
- **Growable** interface abstracts plant growth
- **Timer system** hides timing details
- **Inventory system** provides clean interface

### Inheritance
- Game objects inherit from `pygame.sprite.Sprite`
- `Plant` implements `Growable` interface
- Custom sprite groups extend base functionality
- Tool system uses shared base behavior

### Encapsulation
- **Soil grid** state managed internally
- **Plant growth** logic encapsulated
- **Watering system** hides implementation
- **Collision detection** handled internally

## Design Patterns

### 1. Strategy Pattern
- Rendering strategies for different game states
- Tool system (hoe, axe, water, pickaxe)

### 2. Singleton Pattern
- **Level** class ensures single instance

### 3. State Pattern
- Plant growth stages
- Player animation states
- Game states (menu, playing, paused)

### 4. Composite Pattern
- Combined rendering strategies
- Hierarchical sprite groups

### 5. Observer Pattern
- Soil hydration affects plant growth
- Inventory changes update UI

## Farming System

### Soil Management

```python
def get_hit(self, point):
    # Check if point hits farmable land
    if 'F' in cell and not has_tree:
        self.grid[y][x].append('X')
        self.create_soil_tiles()
```
### Plant Growth

```python
def grow(self):
    if self.check_watered(self.rect.center):
        self.age += self.grow_speed
        if self.age >= self.max_age:
            self.harvestable = True
        self.image = self.frames[int(self.age)]
```
### Watering System
```python
def water(self, target_pos):
    if soil_sprite.rect.collidepoint(target_pos):
        self.grid[y][x].append('W')
        WaterTile(pos=pos, surf=water_surf, groups=[...])
```
## File I/O Operations

### Game Saving

Saves:
- Player position and inventory
- Soil grid sate
- Plant positions and growth stages

### Game Loading

Restores:
- World state
- Player progress
- Crop growth progress

## Testing

### Abstraction 
```python
def test_growable_is_abstract(self):
    class BadPlant(Growable): pass
    with self.assertRaises(TypeError):
        BadPlant()
```

### Inheritance
```python
def test_sprite_inheritance(self):
    soil = SoilTile(...)
    water = WaterTile(...)
    plant = Plant(...)
    for obj in [soil, water, plant]:
        assert isinstance(obj, pygame.sprite.Sprite)
```

### Encapsulation
```python
def test_plant_encapsulation(self):
    plant = Plant(...)
    # Tests internal state protection
    with pytest.raises(AttributeError):
        plant._private_attribute
```
## Installation 
1. Clone the repository
```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
```

2. Install dependencies:
```bash
pip install pygame pytest pytest-mock
```

### Controls

| Key | Action|
| --- | ---|
|W/A/S/D | Movement |
|SPACE | Use tool |
|Q | Cycle tools |
|E | Cycle seeds |
|T | Plant seed |
|Enter | Sleep/Save |
|LSHIFT | Open menu |
|ESC | Pause game |
