## Formal Algorithm Specification for Story Generation

**SUBIT Narrative Engine — v1.0.0**

*6 bits = 64 archetypes = infinite stories*

---

## 📜 Introduction

This document provides the complete formal specification of the SUBIT Narrative Engine algorithm — a computational system for generating literary plots based on archetypal transmutations.

The algorithm implements the fundamental law:

```
Initial State ⊕ External Impulse ⊕ Catalyst = New State
```

where ⊕ is the XOR operation over 6-bit vectors representing archetypal states.

---

## 1. DATA STRUCTURES

### 1.1 Enumerations

```python
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

class WHO(Enum):
    ME = "ME"      # 10
    WE = "WE"      # 11
    YOU = "YOU"    # 01
    THEY = "THEY"  # 00

class WHERE(Enum):
    EAST = "EAST"      # 10
    SOUTH = "SOUTH"    # 11
    WEST = "WEST"      # 01
    NORTH = "NORTH"    # 00

class WHEN(Enum):
    SPRING = "SPRING"  # 10
    SUMMER = "SUMMER"  # 11
    AUTUMN = "AUTUMN"  # 01
    WINTER = "WINTER"  # 00
```

### 1.2 Core Structures

```python
@dataclass
class Archetype:
    """A 6-bit archetypal state."""
    who: WHO
    where: WHERE
    when: WHEN
    
    @property
    def bits(self) -> str:
        """Return 6-bit binary representation."""
        who_bits = {
            WHO.ME: "10",
            WHO.WE: "11", 
            WHO.YOU: "01",
            WHO.THEY: "00"
        }[self.who]
        
        where_bits = {
            WHERE.EAST: "10",
            WHERE.SOUTH: "11",
            WHERE.WEST: "01", 
            WHERE.NORTH: "00"
        }[self.where]
        
        when_bits = {
            WHEN.SPRING: "10",
            WHEN.SUMMER: "11",
            WHEN.AUTUMN: "01",
            WHEN.WINTER: "00"
        }[self.when]
        
        return f"{who_bits} {where_bits} {when_bits}"
    
    @property
    def binary(self) -> str:
        """Return compact binary without spaces."""
        return self.bits.replace(" ", "")
    
    def __xor__(self, other: 'Archetype') -> 'Archetype':
        """XOR operation between two archetypes."""
        # Convert to integers for bitwise operations
        a = int(self.binary, 2)
        b = int(other.binary, 2)
        result_int = a ^ b
        
        # Convert back to binary string with leading zeros
        result_bin = format(result_int, '06b')
        
        # Parse back into components
        who_val = result_bin[0:2]
        where_val = result_bin[2:4]
        when_val = result_bin[4:6]
        
        # Map back to enums
        who_map = {"10": WHO.ME, "11": WHO.WE, "01": WHO.YOU, "00": WHO.THEY}
        where_map = {"10": WHERE.EAST, "11": WHERE.SOUTH, "01": WHERE.WEST, "00": WHERE.NORTH}
        when_map = {"10": WHEN.SPRING, "11": WHEN.SUMMER, "01": WHEN.AUTUMN, "00": WHEN.WINTER}
        
        return Archetype(
            who=who_map[who_val],
            where=where_map[where_val],
            when=when_map[when_val]
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Archetype):
            return False
        return self.bits == other.bits
    
    def __hash__(self):
        return hash(self.bits)
    
    def __repr__(self) -> str:
        return f"[{self.who.value}, {self.where.value}, {self.when.value}]"

@dataclass
class Character:
    """A character with an archetypal state."""
    name: str
    current_state: Archetype
    background: str
    attributes: Dict[str, Any]
    
    def transmute(self, impulse: 'Archetype', catalyst: 'Archetype') -> 'Character':
        """Apply transmutation to character."""
        new_state = self.current_state ^ impulse ^ catalyst
        return Character(
            name=self.name,
            current_state=new_state,
            background=self.background,
            attributes={**self.attributes, "previous_state": self.current_state}
        )

@dataclass
class Event:
    """A plot event representing a state change."""
    event_type: str  # "WHO", "WHERE", "WHEN"
    description: str
    previous_state: Archetype
    new_state: Archetype
    significance: float  # 0.0 to 1.0
    
    @property
    def bits_changed(self) -> str:
        """Return which bits changed."""
        prev_int = int(self.previous_state.binary, 2)
        new_int = int(self.new_state.binary, 2)
        changed = prev_int ^ new_int
        return format(changed, '06b')

@dataclass
class NarrativeArc:
    """A complete character arc."""
    protagonist: Character
    initial_state: Archetype
    final_state: Archetype
    plot_points: List[Event]
    
    @property
    def is_complete(self) -> bool:
        """Check if arc reaches final state."""
        return self.protagonist.current_state == self.final_state
    
    @property
    def dramatic_tension(self) -> float:
        """Calculate dramatic tension (0-1)."""
        if not self.plot_points:
            return 0.0
        max_tension = 0.0
        for event in self.plot_points:
            prev = int(event.previous_state.binary, 2)
            new = int(event.new_state.binary, 2)
            tension = bin(prev ^ new).count('1') / 6.0
            max_tension = max(max_tension, tension)
        return max_tension

@dataclass
class StoryWorld:
    """The world in which the story takes place."""
    setting: str
    dominant_archetype: Archetype
    rules: Dict[str, Any]

@dataclass
class Story:
    """A complete generated story."""
    title: str
    text: str
    arc: NarrativeArc
    world: StoryWorld
    metadata: Dict[str, Any]
```

---

## 2. BIT ENCODING

### 2.1 Encoding Tables

```python
# WHO axis encoding (2 bits)
WHO_ENCODE = {
    WHO.ME: "10",
    WHO.WE: "11",
    WHO.YOU: "01",
    WHO.THEY: "00"
}

WHO_DECODE = {v: k for k, v in WHO_ENCODE.items()}

# WHERE axis encoding (2 bits)
WHERE_ENCODE = {
    WHERE.EAST: "10",
    WHERE.SOUTH: "11",
    WHERE.WEST: "01",
    WHERE.NORTH: "00"
}

WHERE_DECODE = {v: k for k, v in WHERE_ENCODE.items()}

# WHEN axis encoding (2 bits)
WHEN_ENCODE = {
    WHEN.SPRING: "10",
    WHEN.SUMMER: "11",
    WHEN.AUTUMN: "01",
    WHEN.WINTER: "00"
}

WHEN_DECODE = {v: k for k, v in WHEN_ENCODE.items()}
```

### 2.2 Encoding/Decoding Functions

```python
def encode_archetype(archetype: Archetype) -> str:
    """Convert Archetype to 6-bit string."""
    return (WHO_ENCODE[archetype.who] + 
            WHERE_ENCODE[archetype.where] + 
            WHEN_ENCODE[archetype.when])

def decode_archetype(bits: str) -> Archetype:
    """Convert 6-bit string to Archetype."""
    if len(bits) != 6:
        raise ValueError(f"Expected 6 bits, got {len(bits)}")
    
    who_bits = bits[0:2]
    where_bits = bits[2:4]
    when_bits = bits[4:6]
    
    return Archetype(
        who=WHO_DECODE[who_bits],
        where=WHERE_DECODE[where_bits],
        when=WHEN_DECODE[when_bits]
    )

def bits_to_int(bits: str) -> int:
    """Convert 6-bit string to integer."""
    return int(bits, 2)

def int_to_bits(value: int) -> str:
    """Convert integer to 6-bit string."""
    return format(value, '06b')
```

---

## 3. CORE OPERATIONS

### 3.1 Transmutation Function

```python
def transmute(
    initial: Archetype,
    impulse: Archetype,
    catalyst: Archetype
) -> Archetype:
    """
    Apply the fundamental transmutation operation.
    
    Law: Initial ⊕ Impulse ⊕ Catalyst = New State
    
    Args:
        initial: Starting archetypal state
        impulse: External event or force
        catalyst: Transforming agent or guide
        
    Returns:
        New archetypal state
    """
    return initial ^ impulse ^ catalyst

def transmute_sequence(
    initial: Archetype,
    transformations: List[Tuple[Archetype, Archetype]]
) -> List[Archetype]:
    """
    Apply a sequence of transmutations.
    
    Args:
        initial: Starting state
        transformations: List of (impulse, catalyst) pairs
        
    Returns:
        List of states after each transmutation
    """
    states = [initial]
    current = initial
    
    for impulse, catalyst in transformations:
        current = transmute(current, impulse, catalyst)
        states.append(current)
    
    return states
```

### 3.2 Inverse Transmutation

```python
def inverse_transmute(
    current: Archetype,
    target: Archetype,
    catalyst: Optional[Archetype] = None
) -> Tuple[Archetype, Archetype]:
    """
    Find impulse and catalyst to reach target state.
    
    If catalyst is provided, solves for impulse.
    If not, returns all possible (impulse, catalyst) pairs.
    
    Args:
        current: Current state
        target: Desired state
        catalyst: Optional known catalyst
        
    Returns:
        Tuple of (impulse, catalyst) or raises ValueError
    """
    required_change = current ^ target
    
    if catalyst is not None:
        # Solve for impulse: required_change = impulse ⊕ catalyst
        # Therefore: impulse = required_change ⊕ catalyst
        impulse = required_change ^ catalyst
        return impulse, catalyst
    
    # Find all factorizations of required_change
    results = []
    for i in range(64):
        impulse = decode_archetype(int_to_bits(i))
        catalyst = required_change ^ impulse
        results.append((impulse, catalyst))
    
    return results  # Returns all 64 possibilities
```

### 3.3 XOR Properties Implementation

```python
def xor_properties_demo():
    """Demonstrate XOR algebraic properties."""
    zero = Archetype(WHO.THEY, WHERE.NORTH, WHEN.WINTER)  # 00 00 00
    pioneer = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)  # 10 10 10
    
    # Identity: A ⊕ Zero = A
    assert pioneer ^ zero == pioneer
    
    # Self-inverse: A ⊕ A = Zero
    assert pioneer ^ pioneer == zero
    
    # Commutativity: A ⊕ B = B ⊕ A
    b = Archetype(WHO.WE, WHERE.SOUTH, WHEN.SUMMER)  # 11 11 11
    assert (pioneer ^ b) == (b ^ pioneer)
    
    # Associativity: (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)
    c = Archetype(WHO.YOU, WHERE.WEST, WHEN.AUTUMN)  # 01 01 01
    assert ((pioneer ^ b) ^ c) == (pioneer ^ (b ^ c))
    
    print("All XOR properties verified ✓")
```

---

## 4. ARCHETYPE CATALOG ACCESS

```python
class ArchetypeCatalog:
    """Access to the 64 archetypes."""
    
    def __init__(self, canon_path: str = "CANON.md"):
        self.archetypes: Dict[str, Dict[str, Any]] = {}
        self._load_canon()
    
    def _load_canon(self):
        """Load archetype data from CANON.md."""
        # In production, this would parse the actual file
        # For now, we define the four pillars
        self.archetypes["10 10 10"] = {
            "name": "Pioneer",
            "key": "beginning, initiative, purity of intent",
            "description": "The one who sets out first. Unburdened by experience, driven by vision."
        }
        self.archetypes["11 11 11"] = {
            "name": "Conciliar",
            "key": "unity, ecstasy, collective achievement",
            "description": "The state of perfect union. Collective ecstasy, shared triumph."
        }
        # ... load all 64
    
    def get(self, archetype: Archetype) -> Dict[str, Any]:
        """Get metadata for an archetype."""
        return self.archetypes.get(archetype.bits, {})
    
    def get_by_name(self, name: str) -> Optional[Archetype]:
        """Find archetype by name."""
        for bits, data in self.archetypes.items():
            if data.get("name") == name:
                return decode_archetype(bits.replace(" ", ""))
        return None
    
    def all(self) -> List[Archetype]:
        """Return all archetypes."""
        return [decode_archetype(bits.replace(" ", "")) 
                for bits in self.archetypes.keys()]
```

---

## 5. TRANSMUTATION CATALOG ACCESS

```python
class TransmutationCatalog:
    """Access to master transmutation formulas."""
    
    def __init__(self, transmutations_path: str = "TRANSMUTATIONS.md"):
        self.formulas: List[Dict[str, Any]] = []
        self._load_transmutations()
    
    def _load_transmutations(self):
        """Load transmutation data from TRANSMUTATIONS.md."""
        # The 12 master formulas
        self.formulas = [
            {
                "name": "Philosopher's Stone",
                "initial": Archetype(WHO.ME, WHERE.SOUTH, WHEN.WINTER),
                "impulse": Archetype(WHO.THEY, WHERE.EAST, WHEN.SPRING),
                "catalyst": Archetype(WHO.YOU, WHERE.NORTH, WHEN.AUTUMN),
                "result": Archetype(WHO.WE, WHERE.WEST, WHEN.SUMMER),
                "description": "Personal longing becomes collective achievement"
            },
            # ... load all 12
        ]
    
    def find_by_initial_result(
        self, 
        initial: Archetype, 
        result: Archetype
    ) -> List[Dict[str, Any]]:
        """Find formulas matching initial and result."""
        matches = []
        for f in self.formulas:
            if f["initial"] == initial and f["result"] == result:
                matches.append(f)
        return matches
    
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find formula by name."""
        for f in self.formulas:
            if f["name"].lower() == name.lower():
                return f
        return None
```

---

## 6. STORY GENERATION ENGINE

### 6.1 Character Generation

```python
import random

class CharacterGenerator:
    """Generate characters from archetypes."""
    
    def __init__(self, catalog: ArchetypeCatalog):
        self.catalog = catalog
    
    def generate(
        self,
        archetype: Archetype,
        seed: Optional[str] = None
    ) -> Character:
        """Generate a character from an archetype."""
        if seed:
            random.seed(seed)
        
        metadata = self.catalog.get(archetype)
        
        # Generate name based on archetype
        name = self._generate_name(archetype)
        
        # Generate background
        background = self._generate_background(archetype, metadata)
        
        # Derive attributes
        attributes = {
            "motivation": self._derive_motivation(archetype),
            "fear": self._derive_fear(archetype),
            "desire": self._derive_desire(archetype),
            "archetype_name": metadata.get("name", "Unknown"),
            "key_phrase": metadata.get("key", "")
        }
        
        return Character(
            name=name,
            current_state=archetype,
            background=background,
            attributes=attributes
        )
    
    def _generate_name(self, archetype: Archetype) -> str:
        """Generate a name appropriate for the archetype."""
        names = {
            (WHO.ME, WHERE.EAST, WHEN.SPRING): ["Aiden", "Nova", "Orion"],
            (WHO.ME, WHERE.SOUTH, WHEN.WINTER): ["Luca", "Morgan", "Sage"],
            # ... more name mappings
        }
        key = (archetype.who, archetype.where, archetype.when)
        choices = names.get(key, ["Alex", "Jordan", "Taylor"])
        return random.choice(choices)
    
    def _generate_background(self, archetype: Archetype, metadata: Dict) -> str:
        """Generate background story."""
        templates = {
            WHO.ME: f"A solitary figure who {metadata.get('key', '')}",
            WHO.WE: f"Part of a community that {metadata.get('key', '')}",
            WHO.YOU: f"Known for {metadata.get('key', '')}",
            WHO.THEY: f"An embodiment of {metadata.get('key', '')}"
        }
        return templates[archetype.who]
    
    def _derive_motivation(self, archetype: Archetype) -> str:
        """Derive character motivation from archetype."""
        motivations = {
            (WHO.ME, WHEN.SPRING): "To begin something new",
            (WHO.ME, WHEN.SUMMER): "To achieve greatness",
            (WHO.ME, WHEN.AUTUMN): "To understand what was lost",
            (WHO.ME, WHEN.WINTER): "To endure, to survive",
            # ... more mappings
        }
        key = (archetype.who, archetype.when)
        return motivations.get(key, "To find meaning")
    
    def _derive_fear(self, archetype: Archetype) -> str:
        """Derive character fear from archetype."""
        fears = {
            WHERE.EAST: "Fear of never beginning",
            WHERE.SOUTH: "Fear of being consumed by emotion",
            WHERE.WEST: "Fear of chaos, of losing control",
            WHERE.NORTH: "Fear of emptiness, of meaninglessness"
        }
        return fears.get(archetype.where, "Fear of the unknown")
    
    def _derive_desire(self, archetype: Archetype) -> str:
        """Derive character desire from archetype."""
        desires = {
            WHEN.SPRING: "Desire for new possibilities",
            WHEN.SUMMER: "Desire for fulfillment, for completion",
            WHEN.AUTUMN: "Desire to understand, to make peace",
            WHEN.WINTER: "Desire for rest, for release"
        }
        return desires.get(archetype.when, "Desire for change")
```

### 6.2 World Generation

```python
class WorldGenerator:
    """Generate story worlds from archetypes."""
    
    def __init__(self, catalog: ArchetypeCatalog):
        self.catalog = catalog
    
    def generate(self, dominant: Archetype) -> StoryWorld:
        """Generate a world dominated by an archetype."""
        
        setting = self._generate_setting(dominant)
        rules = self._derive_world_rules(dominant)
        
        return StoryWorld(
            setting=setting,
            dominant_archetype=dominant,
            rules=rules
        )
    
    def _generate_setting(self, archetype: Archetype) -> str:
        """Generate setting description."""
        where_templates = {
            WHERE.EAST: "a frontier, a place of beginnings, where the old world ends",
            WHERE.SOUTH: "a land of passion and fire, where emotions run high",
            WHERE.WEST: "a structured society, with laws and order, where everything has its place",
            WHERE.NORTH: "a cold, reflective place, of isolation and deep thought"
        }
        
        when_templates = {
            WHEN.SPRING: "in a time of hope and new beginnings",
            WHEN.SUMMER: "at the height of power and glory",
            WHEN.AUTUMN: "in an age of decline and reflection",
            WHEN.WINTER: "in a dark age, where memory fades"
        }
        
        who_templates = {
            WHO.ME: "where individuals matter more than the collective",
            WHO.WE: "where community is everything",
            WHO.YOU: "where relationships and dialogue shape all",
            WHO.THEY: "where impersonal forces govern life"
        }
        
        return (f"The story takes place in {where_templates[archetype.where]}, "
                f"{when_templates[archetype.when]}, "
                f"{who_templates[archetype.who]}.")
    
    def _derive_world_rules(self, archetype: Archetype) -> Dict[str, Any]:
        """Derive world rules from archetype."""
        rules = {
            "magic_system": self._derive_magic(archetype),
            "social_structure": self._derive_social(archetype),
            "cosmic_principle": self._derive_cosmic(archetype)
        }
        return rules
    
    def _derive_magic(self, archetype: Archetype) -> str:
        """Derive magic system from archetype."""
        where_magic = {
            WHERE.EAST: "magic of beginnings, of potential",
            WHERE.SOUTH: "emotional magic, fire, passion",
            WHERE.WEST: "structured magic, formulas, precision",
            WHERE.NORTH: "mental magic, telepathy, prophecy"
        }
        return where_magic.get(archetype.where, "subtle, almost imperceptible magic")
    
    def _derive_social(self, archetype: Archetype) -> str:
        """Derive social structure from archetype."""
        who_social = {
            WHO.ME: "individualistic, merit-based, often lonely",
            WHO.WE: "collectivist, communal, clan-based",
            WHO.YOU: "relational, dialogue-focused, therapeutic",
            WHO.THEY: "bureaucratic, impersonal, system-driven"
        }
        return who_social.get(archetype.who, "complex and layered")
    
    def _derive_cosmic(self, archetype: Archetype) -> str:
        """Derive cosmic principle from archetype."""
        when_cosmic = {
            WHEN.SPRING: "the universe is becoming, unfolding",
            WHEN.SUMMER: "the universe is at its peak, fully manifest",
            WHEN.AUTUMN: "the universe is declining, returning to source",
            WHEN.WINTER: "the universe is latent, potential, waiting"
        }
        return when_cosmic.get(archetype.when, "cyclical, ever-turning")
```

### 6.3 Plot Generation

```python
class PlotGenerator:
    """Generate plot points from transmutations."""
    
    def __init__(
        self,
        character_gen: CharacterGenerator,
        world_gen: WorldGenerator,
        transmutation_catalog: TransmutationCatalog
    ):
        self.character_gen = character_gen
        self.world_gen = world_gen
        self.transmutations = transmutation_catalog
    
    def generate_arc(
        self,
        initial: Archetype,
        target: Archetype,
        protagonist_name: Optional[str] = None,
        complexity: int = 3  # 1-5, number of plot points
    ) -> NarrativeArc:
        """Generate a narrative arc from initial to target state."""
        
        # Generate protagonist
        protagonist = self.character_gen.generate(
            initial, 
            seed=protagonist_name
        )
        
        # Calculate required change
        required_change = initial ^ target
        
        # Decompose into steps
        steps = self._decompose_change(required_change, complexity)
        
        # Generate plot points
        plot_points = []
        current = initial
        
        for i, (impulse_bits, catalyst_bits) in enumerate(steps):
            impulse = decode_archetype(impulse_bits)
            catalyst = decode_archetype(catalyst_bits)
            
            # Generate event
            event = self._generate_event(
                current, impulse, catalyst, i+1
            )
            plot_points.append(event)
            
            # Update current state
            current = transmute(current, impulse, catalyst)
        
        # Verify we reached target
        assert current == target, "Failed to reach target state"
        
        return NarrativeArc(
            protagonist=protagonist,
            initial_state=initial,
            final_state=target,
            plot_points=plot_points
        )
    
    def _decompose_change(
        self,
        required_change: Archetype,
        complexity: int
    ) -> List[Tuple[str, str]]:
        """
        Decompose required change into steps.
        
        Returns list of (impulse_bits, catalyst_bits) pairs.
        """
        required_int = int(required_change.binary, 2)
        
        if complexity == 1:
            # Single step: required_change = impulse ⊕ catalyst
            impulse_int = random.randint(0, 63)
            catalyst_int = required_int ^ impulse_int
            return [(int_to_bits(impulse_int), int_to_bits(catalyst_int))]
        
        # For multiple steps, decompose into smaller changes
        steps = []
        remaining = required_int
        step_size = required_int // complexity
        
        for i in range(complexity - 1):
            step_target = step_size
            # Find impulse and catalyst that sum to step_target
            impulse_int = random.randint(0, min(63, step_target))
            catalyst_int = step_target ^ impulse_int
            steps.append((int_to_bits(impulse_int), int_to_bits(catalyst_int)))
            remaining ^= step_target
        
        # Final step
        impulse_int = random.randint(0, 63)
        catalyst_int = remaining ^ impulse_int
        steps.append((int_to_bits(impulse_int), int_to_bits(catalyst_int)))
        
        return steps
    
    def _generate_event(
        self,
        current: Archetype,
        impulse: Archetype,
        catalyst: Archetype,
        step_number: int
    ) -> Event:
        """Generate a plot event from a transmutation step."""
        
        new_state = transmute(current, impulse, catalyst)
        
        # Determine which axes changed
        changed = []
        if current.who != new_state.who:
            changed.append("WHO")
        if current.where != new_state.where:
            changed.append("WHERE")
        if current.when != new_state.when:
            changed.append("WHEN")
        
        # Generate description based on what changed
        templates = {
            ("WHO",): f"A profound identity shift occurs",
            ("WHERE",): f"The world around them transforms",
            ("WHEN",): f"Their relationship to time changes",
            ("WHO", "WHERE"): f"Their place in the world is redefined",
            ("WHO", "WHEN"): f"Who they are and when they exist shifts",
            ("WHERE", "WHEN"): f"The very fabric of their reality bends",
            ("WHO", "WHERE", "WHEN"): f"Everything changes in a single moment"
        }
        
        event_type = ", ".join(changed) if changed else "None"
        description = templates.get(
            tuple(sorted(changed)), 
            "Something shifts, subtly but profoundly"
        )
        
        # Add specific details
        if impulse == Archetype(WHO.THEY, WHERE.EAST, WHEN.SPRING):  # Ghost
            description += " as a stranger arrives from the east."
        elif catalyst == Archetype(WHO.YOU, WHERE.NORTH, WHEN.AUTUMN):  # Beloved
            description += " through the words of one who truly sees them."
        # ... more specific templates
        
        significance = len(changed) / 3.0
        
        return Event(
            event_type=event_type,
            description=description,
            previous_state=current,
            new_state=new_state,
            significance=significance
        )
```

### 6.4 Text Rendering

```python
class StoryRenderer:
    """Render narrative arcs into prose."""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load story templates."""
        return {
            "opening": [
                "In a {setting}",
                "There once was a {protagonist} who {background}",
                "The story begins {setting}"
            ],
            "event": [
                "Then, {description}",
                "And so {description}",
                "But {description}"
            ],
            "closing": [
                "And so {protagonist} became {final_state}",
                "Thus ended the journey of {protagonist}",
                "{protagonist} was never the same again"
            ]
        }
    
    def render(self, arc: NarrativeArc, world: StoryWorld) -> str:
        """Render a complete story."""
        paragraphs = []
        
        # Opening
        opening = random.choice(self.templates["opening"])
        paragraphs.append(opening.format(
            setting=world.setting,
            protagonist=arc.protagonist.name,
            background=arc.protagonist.background
        ))
        
        # Introduction of protagonist
        intro = (f"{arc.protagonist.name} was {arc.protagonist.attributes['archetype_name']}, "
                 f"driven by {arc.protagonist.attributes['motivation'].lower()}, "
                 f"fearing {arc.protagonist.attributes['fear'].lower()}.")
        paragraphs.append(intro)
        
        # Plot points
        for i, event in enumerate(arc.plot_points):
            transition = random.choice(self.templates["event"])
            paragraphs.append(transition.format(description=event.description))
            
            # Add reflection
            if i < len(arc.plot_points) - 1:
                reflection = self._generate_reflection(event)
                paragraphs.append(reflection)
        
        # Closing
        closing = random.choice(self.templates["closing"])
        paragraphs.append(closing.format(
            protagonist=arc.protagonist.name,
            final_state=arc.final_state.bits
        ))
        
        return "\n\n".join(paragraphs)
    
    def _generate_reflection(self, event: Event) -> str:
        """Generate character reflection after an event."""
        templates = [
            "Nothing would ever be the same.",
            "They felt the change deep within.",
            "The world looked different now.",
            "Something had shifted, though they couldn't name it."
        ]
        return random.choice(templates)
```

---

## 7. MAIN GENERATION PIPELINE

```python
class SUBITNarrativeEngine:
    """Main story generation engine."""
    
    def __init__(self):
        self.catalog = ArchetypeCatalog()
        self.transmutations = TransmutationCatalog()
        self.character_gen = CharacterGenerator(self.catalog)
        self.world_gen = WorldGenerator(self.catalog)
        self.plot_gen = PlotGenerator(
            self.character_gen,
            self.world_gen,
            self.transmutations
        )
        self.renderer = StoryRenderer()
    
    def generate_story(
        self,
        initial: Optional[Archetype] = None,
        target: Optional[Archetype] = None,
        formula_name: Optional[str] = None,
        protagonist_name: Optional[str] = None,
        style: str = "magic_realism",
        complexity: int = 3
    ) -> Story:
        """
        Generate a complete story.
        
        Args:
            initial: Starting archetype (random if None)
            target: Target archetype (random if None)
            formula_name: Use predefined transmutation
            protagonist_name: Optional name for protagonist
            style: Literary style
            complexity: Number of plot points (1-5)
            
        Returns:
            Complete Story object
        """
        
        # Determine initial and target states
        if formula_name:
            formula = self.transmutations.find_by_name(formula_name)
            if formula:
                initial = formula["initial"]
                target = formula["result"]
            else:
                raise ValueError(f"Unknown formula: {formula_name}")
        
        if initial is None:
            initial = random.choice(self.catalog.all())
        
        if target is None:
            # Pick a random target different from initial
            targets = [a for a in self.catalog.all() if a != initial]
            target = random.choice(targets)
        
        # Generate world
        world = self.world_gen.generate(initial)
        
        # Generate narrative arc
        arc = self.plot_gen.generate_arc(
            initial=initial,
            target=target,
            protagonist_name=protagonist_name,
            complexity=complexity
        )
        
        # Render story
        text = self.renderer.render(arc, world)
        
        # Generate title
        title = self._generate_title(arc)
        
        # Collect metadata
        metadata = {
            "initial_state": initial.bits,
            "final_state": target.bits,
            "transmutations": [
                {
                    "step": i,
                    "event": e.description,
                    "bits_changed": e.bits_changed,
                    "from": e.previous_state.bits,
                    "to": e.new_state.bits
                }
                for i, e in enumerate(arc.plot_points)
            ],
            "dramatic_tension": arc.dramatic_tension,
            "style": style,
            "complexity": complexity
        }
        
        return Story(
            title=title,
            text=text,
            arc=arc,
            world=world,
            metadata=metadata
        )
    
    def _generate_title(self, arc: NarrativeArc) -> str:
        """Generate story title."""
        templates = [
            f"The {arc.final_state.bits} of {arc.protagonist.name}",
            f"{arc.protagonist.name}'s Journey",
            f"The Transmutation",
            f"Salt",
            f"Those Who Wait",
            f"The Architect and the Bird",
            f"The Last Dance",
            f"The Library of Dreams"
        ]
        return random.choice(templates)
    
    def batch_generate(
        self,
        count: int,
        **kwargs
    ) -> List[Story]:
        """Generate multiple stories."""
        return [self.generate_story(**kwargs) for _ in range(count)]
```

---

## 8. UTILITY FUNCTIONS

```python
def hamming_distance(a: Archetype, b: Archetype) -> int:
    """Calculate Hamming distance between two archetypes."""
    a_bits = a.binary
    b_bits = b.binary
    return sum(1 for i in range(6) if a_bits[i] != b_bits[i])

def find_path(
    start: Archetype,
    end: Archetype,
    max_steps: int = 3
) -> List[List[Tuple[Archetype, Archetype]]]:
    """
    Find all possible transmutation paths from start to end.
    
    Returns list of paths, where each path is a list of (impulse, catalyst) pairs.
    """
    from collections import deque
    
    # BFS to find shortest paths
    queue = deque([(start, [])])
    visited = {start: 0}
    paths = []
    
    while queue:
        current, path = queue.popleft()
        
        if current == end:
            paths.append(path)
            continue
        
        if len(path) >= max_steps:
            continue
        
        # Try all possible impulses and catalysts
        for i in range(64):
            for j in range(64):
                impulse = decode_archetype(int_to_bits(i))
                catalyst = decode_archetype(int_to_bits(j))
                next_state = transmute(current, impulse, catalyst)
                
                if next_state not in visited or visited[next_state] >= len(path) + 1:
                    visited[next_state] = len(path) + 1
                    queue.append((next_state, path + [(impulse, catalyst)]))
    
    return paths

def analyze_transmutation(initial: Archetype, result: Archetype) -> Dict[str, Any]:
    """Analyze a transmutation between two states."""
    required = initial ^ result
    
    analysis = {
        "initial": initial.bits,
        "result": result.bits,
        "required_change": required.bits,
        "bits_changed": hamming_distance(initial, result),
        "axis_changes": {
            "WHO": initial.who != result.who,
            "WHERE": initial.where != result.where,
            "WHEN": initial.when != result.when
        },
        "possible_catalysts": []
    }
    
    # Find all possible catalysts
    for i in range(64):
        catalyst = decode_archetype(int_to_bits(i))
        impulse = required ^ catalyst
        analysis["possible_catalysts"].append({
            "catalyst": catalyst.bits,
            "impulse": impulse.bits
        })
    
    return analysis
```

---

## 9. COMMAND LINE INTERFACE

```python
#!/usr/bin/env python3
"""
SUBIT Narrative Engine - Command Line Interface
"""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(
        description="SUBIT Narrative Engine - Generate stories from archetypes"
    )
    
    parser.add_argument(
        "--from", dest="initial",
        help="Initial archetype (e.g., 'ME,SOUTH,WINTER' or '10 11 00')"
    )
    parser.add_argument(
        "--to", dest="target",
        help="Target archetype (e.g., 'WE,WEST,SUMMER' or '11 01 11')"
    )
    parser.add_argument(
        "--formula", dest="formula",
        help="Use predefined transmutation formula"
    )
    parser.add_argument(
        "--name", dest="protagonist_name",
        help="Protagonist name"
    )
    parser.add_argument(
        "--style", default="magic_realism",
        choices=["magic_realism", "fantasy", "sci_fi", "realism", "mythic"],
        help="Literary style"
    )
    parser.add_argument(
        "--complexity", type=int, default=3, choices=range(1, 6),
        help="Number of plot points (1-5)"
    )
    parser.add_argument(
        "--count", type=int, default=1,
        help="Number of stories to generate"
    )
    parser.add_argument(
        "--format", default="text",
        choices=["text", "json", "markdown"],
        help="Output format"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )
    
    args = parser.parse_args()
    
    # Parse archetypes if provided
    initial = None
    target = None
    
    if args.initial:
        if "," in args.initial:
            parts = args.initial.split(",")
            if len(parts) == 3:
                who_map = {"ME": WHO.ME, "WE": WHO.WE, "YOU": WHO.YOU, "THEY": WHO.THEY}
                where_map = {"EAST": WHERE.EAST, "SOUTH": WHERE.SOUTH, 
                           "WEST": WHERE.WEST, "NORTH": WHERE.NORTH}
                when_map = {"SPRING": WHEN.SPRING, "SUMMER": WHEN.SUMMER,
                          "AUTUMN": WHEN.AUTUMN, "WINTER": WHEN.WINTER}
                
                initial = Archetype(
                    who=who_map[parts[0].strip().upper()],
                    where=where_map[parts[1].strip().upper()],
                    when=when_map[parts[2].strip().upper()]
                )
        else:
            # Assume binary format
            bits = args.initial.replace(" ", "")
            if len(bits) == 6:
                initial = decode_archetype(bits)
    
    if args.target:
        if "," in args.target:
            parts = args.target.split(",")
            if len(parts) == 3:
                who_map = {"ME": WHO.ME, "WE": WHO.WE, "YOU": WHO.YOU, "THEY": WHO.THEY}
                where_map = {"EAST": WHERE.EAST, "SOUTH": WHERE.SOUTH,
                           "WEST": WHERE.WEST, "NORTH": WHERE.NORTH}
                when_map = {"SPRING": WHEN.SPRING, "SUMMER": WHEN.SUMMER,
                          "AUTUMN": WHEN.AUTUMN, "WINTER": WHEN.WINTER}
                
                target = Archetype(
                    who=who_map[parts[0].strip().upper()],
                    where=where_map[parts[1].strip().upper()],
                    when=when_map[parts[2].strip().upper()]
                )
        else:
            bits = args.target.replace(" ", "")
            if len(bits) == 6:
                target = decode_archetype(bits)
    
    # Initialize engine
    engine = SUBITNarrativeEngine()
    
    # Generate stories
    stories = []
    for i in range(args.count):
        story = engine.generate_story(
            initial=initial,
            target=target,
            formula_name=args.formula,
            protagonist_name=args.protagonist_name,
            style=args.style,
            complexity=args.complexity
        )
        stories.append(story)
    
    # Output
    output = None
    if args.format == "json":
        output = json.dumps({
            "stories": [
                {
                    "title": s.title,
                    "text": s.text,
                    "metadata": s.metadata
                }
                for s in stories
            ]
        }, indent=2, ensure_ascii=False)
    elif args.format == "markdown":
        output = ""
        for s in stories:
            output += f"# {s.title}\n\n"
            output += f"{s.text}\n\n"
            output += "---\n\n"
    else:  # text
        output = "\n\n---\n\n".join([f"# {s.title}\n\n{s.text}" for s in stories])
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print(output)

if __name__ == "__main__":
    main()
```

---

## 10. COMPLETE EXAMPLE

```python
# example_usage.py
from subit import *

# Initialize engine
engine = SUBITNarrativeEngine()

# Generate story using Philosopher's Stone formula
story = engine.generate_story(
    formula_name="Philosopher's Stone",
    protagonist_name="Luca",
    style="magic_realism",
    complexity=3
)

print(f"Title: {story.title}")
print(f"\n{story.text}")

# Analyze the arc
print(f"\n--- Analysis ---")
print(f"Initial: {story.arc.initial_state.bits}")
print(f"Final: {story.arc.final_state.bits}")
print(f"Dramatic tension: {story.arc.dramatic_tension:.2f}")
print(f"Plot points: {len(story.arc.plot_points)}")

for i, event in enumerate(story.arc.plot_points):
    print(f"\nEvent {i+1}: {event.description}")
    print(f"  Bits changed: {event.bits_changed}")
    print(f"  Significance: {event.significance:.2f}")
```

---

## 📊 COMPLEXITY ANALYSIS

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| XOR operation | O(1) | O(1) |
| Archetype lookup | O(1) | O(64) |
| Find transmutation path | O(64² × steps) | O(64²) |
| Generate character | O(1) | O(1) |
| Generate world | O(1) | O(1) |
| Generate arc (fixed steps) | O(steps) | O(steps) |
| Render story | O(steps × words) | O(story length) |

**State space:** 2⁶ = 64 archetypes  
**Possible transmutations:** 64³ = 262,144  
**Max steps to reach any state:** 3 (by XOR group properties)

---

## 🔗 RELATED DOCUMENTS

- [CANON.md](CANON.md) — Complete catalog of 64 archetypes
- [TRANSMUTATIONS.md](TRANSMUTATIONS.md) — 12 master transmutation formulas
- [examples/](examples/) — Generated stories

---

**End of ALGORITHM.md — Formal specification complete**
