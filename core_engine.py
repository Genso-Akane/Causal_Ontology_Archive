import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import uuid

# --- 16. Limiting Velocity of a Process ---
# The limit of process consistency, not the “speed of an object” [cite: 16, 30]
LIMITING_VELOCITY = 5.0

# --- 2. Event ---
# The first physical fact. Everything exists as a chain of events [cite: 2, 18, 25]
@dataclass
class Event:
    id: str
    cause_id: Optional[str] # 1. Causality [cite: 1]
    energy: float           # 3. Energy [cite: 3, 20]
    impulse: float          # 5. Momentum [cite: 5, 21]
    info: float             # 20. Information 
    system_id: str          # 7. System [cite: 7, 23]

# --- 8. System State ---
# Complete set of parameters determining further changes [cite: 8, 24]
@dataclass
class State:
    energy: float
    tempo: float            # 11. Tempo of Processes [cite: 11, 26]
    last_event: Optional[Event] = None

# --- 7. System ---
# Causally coherent aggregate of matter with stable regimes [cite: 7, 23]
@dataclass
class System:
    id: str
    state: State
    process: List[Event] = field(default_factory=list) # 9. Process [cite: 9, 25]
    measurements: List[Tuple[float, float]] = field(default_factory=list) # 21. Measurement [cite: 21, 35]
    entropy: float = 0.0    # 12. Entropy [cite: 12, 27]

# --- 25. Universe ---
# The complete causal process [cite: 25, 38]
@dataclass
class Universe:
    systems: List[System]
    global_process: List[Event] = field(default_factory=list)

# --- 13. Space & 15. Metric ---
# 13. Space is an index of differences; 15. Metric is computational consistency [cite: 13, 15, 28, 29]
def compute_position(state: State):
    return (state.energy, state.tempo)

def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# --- 17. Causal Horizon ---
# Boundary of possible influence [cite: 17, 31]
def within_horizon(dist):
    return dist <= LIMITING_VELOCITY

# --- 18. Gravitation ---
# Consequence of dynamical inhomogeneity [cite: 18, 32]
def compute_grav_field(systems: List[System]):
    epsilon = 1e-6
    fields = {s.id: 0.0 for s in systems}
    positions = {s.id: compute_position(s.state) for s in systems}

    for i in range(len(systems)):
        for j in range(len(systems)):
            if i == j: continue

            si, sj = systems[i], systems[j]
            dist = distance(positions[si.id], positions[sj.id])
            
            if not within_horizon(dist): continue

            # 19. Gravitational Influence: modification of accessible states [cite: 19, 33]
            tempo_delta = sj.state.tempo - si.state.tempo
            influence = sj.state.energy * tempo_delta / (dist + epsilon)
            influence = max(-LIMITING_VELOCITY, min(LIMITING_VELOCITY, influence))

            fields[si.id] += influence
    return fields

# --- 24. Energy-Conditioned Modification of Dynamics ---
# Principle of GR without geometry [cite: 24, 37]
def generate_event(system: System, grav_field: float):
    state = system.state
    cause_id = state.last_event.id if state.last_event else None
    base_energy = state.last_event.energy if state.last_event else state.energy

    alpha, beta, gamma = 0.01, 0.05, 0.01
    energy_factor = 1 / (1 + alpha * grav_field)

    new_energy = base_energy * energy_factor
    impulse = new_energy * (0.1 + beta * grav_field)
    new_tempo = max(0.0001, state.tempo * (1 - gamma * grav_field))
    
    # 20. Information: structure of an event outcome 
    info = new_energy * new_tempo 

    return Event(
        id=str(uuid.uuid4()),
        cause_id=cause_id,
        energy=new_energy,
        impulse=impulse,
        info=info,
        system_id=system.id
    ), new_tempo

# --- 21. Measurement ---
# Event of state fixation [cite: 21, 35]
def measure(system: System):
    system.measurements.append((system.state.energy, system.state.tempo))

# --- 12. Entropy ---
# Indicator of irreversibility and measure of accessible states [cite: 12, 27]
def update_entropy(system: System):
    unique = set(system.measurements)
    system.entropy = math.log(len(unique)) if len(unique) > 1 else 0.0

# --- 25. UNIVERSE ENGINE ---
class UniverseEngine:
    def __init__(self, universe: Universe):
        self.universe = universe

    def step(self):
        systems = self.universe.systems
        fields = compute_grav_field(systems)

        for s in systems:
            event, new_tempo = generate_event(s, fields[s.id])
            s.process.append(event)
            self.universe.global_process.append(event)

            # Update 8. System State
            s.state.energy = event.energy
            s.state.last_event = event
            s.state.tempo = new_tempo

            measure(s) # 21
            update_entropy(s) # 12

    def run(self, steps):
        for _ in range(steps):
            self.step()

# --- EXECUTION EXAMPLE ---
if __name__ == "__main__":
    universe = Universe(
        systems=[
            System("Alpha", State(100.0, 1.0)),
            System("Beta", State(120.0, 0.8)),
            System("Gamma", State(80.0, 1.2)),
        ]
    )

    engine = UniverseEngine(universe)
    engine.run(20)

    print(f"\n25. UNIVERSE GLOBAL PROCESS SIZE: {len(universe.global_process)}")

    for s in universe.systems:
        print(f"\n--- System {s.id} ---")
        print(f"12. Entropy: {s.entropy:.4f}")
        print(f"11. Final Tempo: {s.state.tempo:.4f}")
