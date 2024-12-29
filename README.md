# Interactive Particle Physics Simulator

A creative and interactive particle physics sandbox built with Pygame and Dear PyGui that lets you experiment with particle dynamics, force fields, and particle emitters in real-time!

## Key Features

- **Particle Physics Engine**
  - Realistic gravity and collision physics
  - Momentum conservation in particle collisions
  - Configurable restitution (bounciness) coefficient
  - Trail rendering with fade effect

- **Interactive Force Fields**
  - Create attractors and repulsors with customizable strength and radius
  - Visual feedback with color-coded field influence areas
  - Smooth force falloff based on distance

- **Particle Emitters**
  - Configurable emission rate, particle lifetime, and velocity
  - Adjustable emission angle range for directed particle streams
  - Visual preview of emission direction
  - Multiple emitters can work simultaneously

- **Real-time Controls & Visualization**
  - Intuitive GUI for tweaking physics parameters
  - Toggle gravity and collision detection
  - Velocity and acceleration vector visualization
  - Live statistics (particle count, average velocity, system energy)

You can create some amazing effects:
- Orbital systems with attractors
- Particle fountains and waterfalls
- Explosion simulations with repulsors
- Complex particle interactions with multiple force fields
- Beautiful visual patterns with particle trails

## Implementation

The simulator is built on several key components:

- **Vector Class**: Custom 2D vector implementation with support for basic operations and rotations
- **Particle System**: Efficient particle management with position, velocity, and acceleration updates
- **Force Fields**: Implements inverse square law for realistic force behavior
- **Collision Detection**: Optimized collision checking with correct momentum and energy conservation
- **GUI System**: Seamless integration of Dear PyGui for controls and real-time feedback

## How Can I Play?

1. Left Click - Add individual particles
2. Right Click - Create force fields (when in force field mode)
3. Middle Click - Place particle emitters (when in emitter mode)
4. Use GUI controls to:
   - Adjust particle properties (mass, initial velocity, direction)
   - Configure force field strength and radius
   - Set emitter parameters (rate, angle range, particle speed)
   - Monitor system statistics

## Performance

The simulator is optimized to handle:
- Up to 2000 particles simultaneously
- Multiple active force fields
- Several particle emitters

Have fun experimenting!
