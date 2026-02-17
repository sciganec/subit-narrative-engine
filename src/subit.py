"""
SUBIT Narrative Engine
6 bits = 64 archetypes = infinite stories

A formal system for generating narratives based on archetypal transmutations.
"""

import random
import json
from enum import Enum
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from collections import deque
import hashlib


# ============================================================================
# 1. ENUMS AND CONSTANTS
# ============================================================================

class WHO(Enum):
    """WHO axis — the subject of experience."""
    ME = "ME"      # 10 — individual, first person
    WE = "WE"      # 11 — collective, first person plural
    YOU = "YOU"    # 01 — second person, dialogic
    THEY = "THEY"  # 00 — third person, impersonal


class WHERE(Enum):
    """WHERE axis — the space of experience."""
    EAST = "EAST"      # 10 — beginning, initiation, sunrise
    SOUTH = "SOUTH"    # 11 — passion, emotion, fire
    WEST = "WEST"      # 01 — structure, order, sunset
    NORTH = "NORTH"    # 00 — reflection, wisdom, cold


class WHEN(Enum):
    """WHEN axis — the time of experience."""
    SPRING = "SPRING"  # 10 — beginning, hope, birth
    SUMMER = "SUMMER"  # 11 — peak, action, fulfillment
    AUTUMN = "AUTUMN"  # 01 — decline, harvest, reflection
    WINTER = "WINTER"  # 00 — end, death, potential


# ============================================================================
# 2. BIT ENCODING TABLES
# ============================================================================

# WHO encoding (2 bits)
WHO_ENCODE = {
    WHO.ME: "10",
    WHO.WE: "11",
    WHO.YOU: "01",
    WHO.THEY: "00"
}

WHO_DECODE = {v: k for k, v in WHO_ENCODE.items()}

# WHERE encoding (2 bits)
WHERE_ENCODE = {
    WHERE.EAST: "10",
    WHERE.SOUTH: "11",
    WHERE.WEST: "01",
    WHERE.NORTH: "00"
}

WHERE_DECODE = {v: k for k, v in WHERE_ENCODE.items()}

# WHEN encoding (2 bits)
WHEN_ENCODE = {
    WHEN.SPRING: "10",
    WHEN.SUMMER: "11",
    WHEN.AUTUMN: "01",
    WHEN.WINTER: "00"
}

WHEN_DECODE = {v: k for k, v in WHEN_ENCODE.items()}


# ============================================================================
# 3. CORE DATA STRUCTURES
# ============================================================================

@dataclass
class Archetype:
    """
    A 6-bit archetypal state.
    
    Each archetype is a unique combination of WHO, WHERE, and WHEN,
    representing a fundamental pattern of being.
    """
    who: WHO
    where: WHERE
    when: WHEN
    
    @property
    def bits(self) -> str:
        """Return 6-bit representation with spaces (for readability)."""
        return f"{WHO_ENCODE[self.who]} {WHERE_ENCODE[self.where]} {WHEN_ENCODE[self.when]}"
    
    @property
    def binary(self) -> str:
        """Return compact 6-bit string without spaces (for computation)."""
        return self.bits.replace(" ", "")
    
    @property
    def int_value(self) -> int:
        """Return integer value of the 6-bit string (0-63)."""
        return int(self.binary, 2)
    
    @property
    def name(self) -> str:
        """Return the canonical name of this archetype."""
        return ARCHETYPE_NAMES.get(self.bits, "Unknown")
    
    def __xor__(self, other: 'Archetype') -> 'Archetype':
        """
        XOR operation between two archetypes.
        
        This is the fundamental operation of the SUBIT system.
        """
        if not isinstance(other, Archetype):
            return NotImplemented
        
        # XOR the integer values
        result_int = self.int_value ^ other.int_value
        
        # Convert back to binary
        result_bin = format(result_int, '06b')
        
        # Parse into components
        who_bits = result_bin[0:2]
        where_bits = result_bin[2:4]
        when_bits = result_bin[4:6]
        
        return Archetype(
            who=WHO_DECODE[who_bits],
            where=WHERE_DECODE[where_bits],
            when=WHEN_DECODE[when_bits]
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Archetype):
            return False
        return self.bits == other.bits
    
    def __hash__(self):
        return hash(self.bits)
    
    def __repr__(self) -> str:
        return f"[{self.who.value}, {self.where.value}, {self.when.value}]"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for serialization."""
        return {
            "who": self.who.value,
            "where": self.where.value,
            "when": self.when.value,
            "bits": self.bits,
            "binary": self.binary,
            "int": self.int_value,
            "name": self.name
        }
    
    @classmethod
    def from_bits(cls, bits: str) -> 'Archetype':
        """Create archetype from 6-bit string (with or without spaces)."""
        clean = bits.replace(" ", "")
        if len(clean) != 6:
            raise ValueError(f"Expected 6 bits, got {len(clean)}: {bits}")
        
        who_bits = clean[0:2]
        where_bits = clean[2:4]
        when_bits = clean[4:6]
        
        return cls(
            who=WHO_DECODE[who_bits],
            where=WHERE_DECODE[where_bits],
            when=WHEN_DECODE[when_bits]
        )
    
    @classmethod
    def from_int(cls, value: int) -> 'Archetype':
        """Create archetype from integer 0-63."""
        if not 0 <= value <= 63:
            raise ValueError(f"Expected 0-63, got {value}")
        return cls.from_bits(format(value, '06b'))


@dataclass
class Character:
    """A character with an archetypal state."""
    name: str
    current_state: Archetype
    background: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def transmute(self, impulse: Archetype, catalyst: Archetype) -> 'Character':
        """Apply transmutation to character, returning new character state."""
        new_state = self.current_state ^ impulse ^ catalyst
        new_attrs = dict(self.attributes)
        new_attrs["previous_state"] = self.current_state.bits
        new_attrs["impulse"] = impulse.bits
        new_attrs["catalyst"] = catalyst.bits
        
        return Character(
            name=self.name,
            current_state=new_state,
            background=self.background,
            attributes=new_attrs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "current_state": self.current_state.to_dict(),
            "background": self.background,
            "attributes": self.attributes
        }


@dataclass
class Event:
    """A plot event representing a state change."""
    event_type: str  # "WHO", "WHERE", "WHEN", or combination
    description: str
    previous_state: Archetype
    new_state: Archetype
    significance: float  # 0.0 to 1.0
    
    @property
    def bits_changed(self) -> str:
        """Return which bits changed (1 = changed)."""
        prev_int = self.previous_state.int_value
        new_int = self.new_state.int_value
        changed = prev_int ^ new_int
        return format(changed, '06b')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "event_type": self.event_type,
            "description": self.description,
            "previous_state": self.previous_state.bits,
            "new_state": self.new_state.bits,
            "bits_changed": self.bits_changed,
            "significance": self.significance
        }


@dataclass
class NarrativeArc:
    """A complete character arc."""
    protagonist: Character
    initial_state: Archetype
    final_state: Archetype
    plot_points: List[Event] = field(default_factory=list)
    
    @property
    def is_complete(self) -> bool:
        """Check if arc reaches final state."""
        return self.protagonist.current_state == self.final_state
    
    @property
    def dramatic_tension(self) -> float:
        """Calculate dramatic tension (0-1) based on maximum bit change."""
        if not self.plot_points:
            return 0.0
        
        max_tension = 0.0
        for event in self.plot_points:
            bits = event.bits_changed
            tension = bits.count('1') / 6.0
            max_tension = max(max_tension, tension)
        
        return max_tension
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "protagonist": self.protagonist.to_dict(),
            "initial_state": self.initial_state.bits,
            "final_state": self.final_state.bits,
            "plot_points": [e.to_dict() for e in self.plot_points],
            "dramatic_tension": self.dramatic_tension,
            "is_complete": self.is_complete
        }


@dataclass
class StoryWorld:
    """The world in which the story takes place."""
    setting: str
    dominant_archetype: Archetype
    rules: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "setting": self.setting,
            "dominant_archetype": self.dominant_archetype.bits,
            "rules": self.rules
        }


@dataclass
class Story:
    """A complete generated story."""
    title: str
    text: str
    arc: NarrativeArc
    world: StoryWorld
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "text": self.text,
            "arc": self.arc.to_dict(),
            "world": self.world.to_dict(),
            "metadata": self.metadata
        }
    
    def save(self, path: str, format: str = "txt") -> None:
        """Save story to file."""
        if format == "txt":
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"# {self.title}\n\n")
                f.write(self.text)
                f.write(f"\n\n---\nGenerated by SUBIT Narrative Engine")
        elif format == "json":
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        elif format == "md":
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"# {self.title}\n\n")
                f.write(self.text)
                f.write("\n\n## Metadata\n\n")
                f.write(f"- Initial state: {self.arc.initial_state.bits}\n")
                f.write(f"- Final state: {self.arc.final_state.bits}\n")
                f.write(f"- Dramatic tension: {self.arc.dramatic_tension:.2f}\n")
                if "formula" in self.metadata:
                    f.write(f"- Formula: {self.metadata['formula']}\n")


# ============================================================================
# 4. ARCHETYPE CATALOG (64 ARCHETYPES)
# ============================================================================

# Canonical names for all 64 archetypes
ARCHETYPE_NAMES = {
    "00 00 00": "Zero",
    "00 00 01": "Anchorite",
    "00 00 10": "Oracle",
    "00 00 11": "Spectator",
    "00 01 00": "Judge",
    "00 01 01": "Custodian",
    "00 01 10": "Architect",
    "00 01 11": "Legislator",
    "00 10 00": "Ancestor",
    "00 10 01": "Chronicler",
    "00 10 10": "Ghost",
    "00 10 11": "Harbinger",
    "00 11 00": "Shadow",
    "00 11 01": "Scapegoat",
    "00 11 10": "Trickster",
    "00 11 11": "Carnival",
    "01 00 00": "Hermit",
    "01 00 01": "Beloved",
    "01 00 10": "Teacher",
    "01 00 11": "Confessor",
    "01 01 00": "Scribe",
    "01 01 01": "Mediator",
    "01 01 10": "Apprentice",
    "01 01 11": "Interpreter",
    "01 10 00": "Mentor",
    "01 10 01": "Witness",
    "01 10 10": "Guide",
    "01 10 11": "Prophet",
    "01 11 00": "Mourner",
    "01 11 01": "Lover",
    "01 11 10": "Muse",
    "01 11 11": "Celebrant",
    "10 00 00": "Recluse",
    "10 00 01": "Philosopher",
    "10 00 10": "Seeker",
    "10 00 11": "Sage",
    "10 01 00": "Artisan",
    "10 01 01": "Critic",
    "10 01 10": "Creator",
    "10 01 11": "Master",
    "10 10 00": "Heir",
    "10 10 01": "Guardian",
    "10 10 10": "Pioneer",
    "10 10 11": "Hero",
    "10 11 00": "Steadfast",
    "10 11 01": "Martyr",
    "10 11 10": "Wanderer",
    "10 11 11": "Ecstatic",
    "11 00 00": "Congregation",
    "11 00 01": "Synod",
    "11 00 10": "Academy",
    "11 00 11": "Pantheon",
    "11 01 00": "Guild",
    "11 01 01": "Council",
    "11 01 10": "Workshop",
    "11 01 11": "Assembly",
    "11 10 00": "Tribe",
    "11 10 01": "Chorus",
    "11 10 10": "Caravan",
    "11 10 11": "Nation",
    "11 11 00": "Sanctuary",
    "11 11 01": "Celebration",
    "11 11 10": "Festival",
    "11 11 11": "Conciliar"
}


class ArchetypeCatalog:
    """Access to the 64 archetypes and their metadata."""
    
    def __init__(self):
        self.archetypes: Dict[str, Dict[str, Any]] = {}
        self._build_catalog()
    
    def _build_catalog(self):
        """Build the archetype catalog with metadata."""
        for bits, name in ARCHETYPE_NAMES.items():
            archetype = Archetype.from_bits(bits)
            
            # Generate key qualities based on axes
            key_qualities = self._generate_key_qualities(archetype)
            
            self.archetypes[bits] = {
                "name": name,
                "archetype": archetype,
                "bits": bits,
                "binary": archetype.binary,
                "int": archetype.int_value,
                "who": archetype.who.value,
                "where": archetype.where.value,
                "when": archetype.when.value,
                "key": key_qualities,
                "description": self._generate_description(archetype, name, key_qualities)
            }
    
    def _generate_key_qualities(self, a: Archetype) -> str:
        """Generate key qualities for an archetype."""
        who_map = {
            WHO.ME: "individual, personal",
            WHO.WE: "collective, shared",
            WHO.YOU: "relational, dialogic",
            WHO.THEY: "impersonal, systemic"
        }
        
        where_map = {
            WHERE.EAST: "beginning, initiation",
            WHERE.SOUTH: "passion, emotion",
            WHERE.WEST: "structure, order",
            WHERE.NORTH: "reflection, wisdom"
        }
        
        when_map = {
            WHEN.SPRING: "hope, birth",
            WHEN.SUMMER: "peak, action",
            WHEN.AUTUMN: "harvest, decline",
            WHEN.WINTER: "end, potential"
        }
        
        return f"{who_map[a.who]}, {where_map[a.where]}, {when_map[a.when]}"
    
    def _generate_description(self, a: Archetype, name: str, key: str) -> str:
        """Generate a description for an archetype."""
        templates = {
            "Pioneer": "The one who sets out first. Unburdened by experience, driven by vision.",
            "Steadfast": "One who has endured loss and frozen in their suffering.",
            "Ghost": "That which comes from outside. The unexpected visitor.",
            "Beloved": "The one who is loved and who therefore can speak truth.",
            "Council": "The new community born from transformed suffering.",
            "Zero": "The primordial state before manifestation. Pure potential."
        }
        
        return templates.get(name, f"A being embodying {key}.")
    
    def get(self, archetype: Union[Archetype, str]) -> Dict[str, Any]:
        """Get metadata for an archetype."""
        if isinstance(archetype, Archetype):
            key = archetype.bits
        else:
            key = archetype
        return self.archetypes.get(key, {})
    
    def get_by_name(self, name: str) -> Optional[Archetype]:
        """Find archetype by name."""
        for bits, data in self.archetypes.items():
            if data["name"].lower() == name.lower():
                return data["archetype"]
        return None
    
    def all(self) -> List[Archetype]:
        """Return all archetypes."""
        return [data["archetype"] for data in self.archetypes.values()]
    
    def all_dicts(self) -> List[Dict[str, Any]]:
        """Return all archetype metadata."""
        return list(self.archetypes.values())
    
    def random(self) -> Archetype:
        """Return a random archetype."""
        return random.choice(self.all())


# ============================================================================
# 5. TRANSMUTATION CATALOG (12 MASTER FORMULAS)
# ============================================================================

@dataclass
class TransmutationFormula:
    """A master transmutation formula."""
    name: str
    initial: Archetype
    impulse: Archetype
    catalyst: Archetype
    result: Archetype
    description: str
    
    def verify(self) -> bool:
        """Verify that the formula is mathematically correct."""
        return (self.initial ^ self.impulse ^ self.catalyst) == self.result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "initial": self.initial.bits,
            "impulse": self.impulse.bits,
            "catalyst": self.catalyst.bits,
            "result": self.result.bits,
            "description": self.description,
            "verified": self.verify()
        }


class TransmutationCatalog:
    """Access to master transmutation formulas."""
    
    def __init__(self):
        self.formulas: List[TransmutationFormula] = []
        self._build_formulas()
    
   def _build_formulas(self):
    """Build the 12 master transmutation formulas (verified correct)."""
    
    # Helper to create archetypes
    def a(who: str, where: str, when: str) -> Archetype:
        who_map = {"ME": WHO.ME, "WE": WHO.WE, "YOU": WHO.YOU, "THEY": WHO.THEY}
        where_map = {"EAST": WHERE.EAST, "SOUTH": WHERE.SOUTH, 
                    "WEST": WHERE.WEST, "NORTH": WHERE.NORTH}
        when_map = {"SPRING": WHEN.SPRING, "SUMMER": WHEN.SUMMER,
                   "AUTUMN": WHEN.AUTUMN, "WINTER": WHEN.WINTER}
        return Archetype(
            who=who_map[who],
            where=where_map[where],
            when=when_map[when]
        )
    
    # VERIFIED CORRECT FORMULAS - each one has been tested
    self.formulas = [
        # 1. Philosopher's Stone ✅
        TransmutationFormula(
            name="Philosopher's Stone",
            initial=a("ME", "SOUTH", "WINTER"),      # 10 11 00
            impulse=a("THEY", "EAST", "SPRING"),      # 00 10 10
            catalyst=a("YOU", "NORTH", "AUTUMN"),     # 01 00 01
            result=a("WE", "WEST", "SUMMER"),         # 11 01 11
            description="Personal longing becomes collective achievement"
        ),
        
        # 2. Hero's Journey ✅ (corrected)
        TransmutationFormula(
            name="Hero's Journey",
            initial=a("ME", "EAST", "SPRING"),        # 10 10 10
            impulse=a("THEY", "SOUTH", "WINTER"),      # 00 11 00
            catalyst=a("WE", "WEST", "AUTUMN"),        # 11 01 01
            result=a("YOU", "NORTH", "SUMMER"),        # 01 00 11
            description="Innocence confronts shadow, returns with wisdom"
        ),
        
        # 3. Alchemical Marriage ✅
        TransmutationFormula(
            name="Alchemical Marriage",
            initial=a("ME", "EAST", "SPRING"),        # 10 10 10
            impulse=a("YOU", "WEST", "AUTUMN"),        # 01 01 01
            catalyst=a("WE", "SOUTH", "SUMMER"),       # 11 11 11
            result=a("THEY", "NORTH", "WINTER"),       # 00 00 00
            description="Union of opposites returns to the source"
        ),
        
        # 4. Creative Process ✅
        TransmutationFormula(
            name="Creative Process",
            initial=a("ME", "NORTH", "WINTER"),       # 10 00 00
            impulse=a("THEY", "EAST", "SPRING"),       # 00 10 10
            catalyst=a("YOU", "SOUTH", "SUMMER"),      # 01 11 11
            result=a("WE", "WEST", "AUTUMN"),          # 11 01 01
            description="Solitude + inspiration + mastery = shared creation"
        ),
        
        # 5. Healing ✅
        TransmutationFormula(
            name="Healing",
            initial=a("ME", "WEST", "WINTER"),        # 10 01 00
            impulse=a("THEY", "SOUTH", "SUMMER"),      # 00 11 11
            catalyst=a("YOU", "EAST", "SPRING"),       # 01 10 10
            result=a("WE", "NORTH", "AUTUMN"),         # 11 00 01
            description="Isolation + collective energy + mediator = integration"
        ),
        
        # 6. Revelation ✅
        TransmutationFormula(
            name="Revelation",
            initial=a("THEY", "NORTH", "WINTER"),     # 00 00 00
            impulse=a("ME", "EAST", "SPRING"),         # 10 10 10
            catalyst=a("WE", "SOUTH", "SUMMER"),       # 11 11 11
            result=a("YOU", "WEST", "AUTUMN"),         # 01 01 01
            description="From void, through seeking and communion, wisdom emerges"
        ),
        
        # 7. Power Transformation ✅
        TransmutationFormula(
            name="Power Transformation",
            initial=a("ME", "SOUTH", "SUMMER"),       # 10 11 11
            impulse=a("THEY", "WEST", "AUTUMN"),       # 00 01 01
            catalyst=a("YOU", "NORTH", "SPRING"),      # 01 00 10
            result=a("WE", "EAST", "WINTER"),          # 11 10 00
            description="Individual power becomes collective guardianship"
        ),
        
        # 8. Dark Night ✅
        TransmutationFormula(
            name="Dark Night",
            initial=a("WE", "SOUTH", "SUMMER"),       # 11 11 11
            impulse=a("THEY", "WEST", "AUTUMN"),       # 00 01 01
            catalyst=a("YOU", "EAST", "WINTER"),       # 01 10 00
            result=a("ME", "NORTH", "SPRING"),         # 10 00 10
            description="Community joy, through crisis, retreats to potential"
        ),
        
        # 9. Awakening ✅
        TransmutationFormula(
            name="Awakening",
            initial=a("ME", "NORTH", "AUTUMN"),       # 10 00 01
            impulse=a("THEY", "SOUTH", "SPRING"),      # 00 11 10
            catalyst=a("WE", "EAST", "SUMMER"),        # 11 10 11
            result=a("YOU", "WEST", "WINTER"),         # 01 01 00
            description="Old patterns shattered by force become witness"
        ),
        
        # 10. Renewal ✅
        TransmutationFormula(
            name="Renewal",
            initial=a("THEY", "NORTH", "AUTUMN"),     # 00 00 01
            impulse=a("ME", "SOUTH", "WINTER"),        # 10 11 00
            catalyst=a("WE", "EAST", "SPRING"),        # 11 10 10
            result=a("YOU", "WEST", "SUMMER"),         # 01 01 11
            description="Unrealized possibilities + endurance = catharsis"
        ),
        
        # 11. Reconciliation ✅
        TransmutationFormula(
            name="Reconciliation",
            initial=a("ME", "WEST", "AUTUMN"),        # 10 01 01
            impulse=a("THEY", "EAST", "SUMMER"),       # 00 10 11
            catalyst=a("YOU", "NORTH", "WINTER"),      # 01 00 00
            result=a("WE", "SOUTH", "SPRING"),         # 11 11 10
            description="Judgment + higher perspective + love = renewed union"
        ),
        
        # 12. Complete Transmutation ✅
        TransmutationFormula(
            name="Complete Transmutation",
            initial=a("ME", "EAST", "SPRING"),        # 10 10 10
            impulse=a("WE", "SOUTH", "SUMMER"),        # 11 11 11
            catalyst=a("YOU", "WEST", "AUTUMN"),       # 01 01 01
            result=a("THEY", "NORTH", "WINTER"),       # 00 00 00
            description="The three active pillars return to the source"
        )
    ]
    
    # Verify all formulas (this will now pass)
    for f in self.formulas:
        assert f.verify(), f"Formula {f.name} failed verification"
    
    def all(self) -> List[TransmutationFormula]:
        """Return all master formulas."""
        return self.formulas
    
    def find_by_name(self, name: str) -> Optional[TransmutationFormula]:
        """Find formula by name."""
        for f in self.formulas:
            if f.name.lower() == name.lower():
                return f
        return None
    
    def find_by_initial_result(self, initial: Archetype, result: Archetype) -> List[TransmutationFormula]:
        """Find formulas matching initial and result."""
        matches = []
        for f in self.formulas:
            if f.initial == initial and f.result == result:
                matches.append(f)
        return matches


# Predefined instances for common use
ZERO = Archetype(WHO.THEY, WHERE.NORTH, WHEN.WINTER)  # 00 00 00
PIONEER = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)  # 10 10 10
CONCILIAR = Archetype(WHO.WE, WHERE.SOUTH, WHEN.SUMMER)  # 11 11 11
CONFESSOR = Archetype(WHO.YOU, WHERE.WEST, WHEN.AUTUMN)  # 01 01 01
STEADFAST = Archetype(WHO.ME, WHERE.SOUTH, WHEN.WINTER)  # 10 11 00
GHOST = Archetype(WHO.THEY, WHERE.EAST, WHEN.SPRING)  # 00 10 10
BELOVED = Archetype(WHO.YOU, WHERE.NORTH, WHEN.AUTUMN)  # 01 00 01
COUNCIL = Archetype(WHO.WE, WHERE.WEST, WHEN.SUMMER)  # 11 01 11

# The Philosopher's Stone formula
PHILOSOPHER_STONE = TransmutationFormula(
    name="Philosopher's Stone",
    initial=STEADFAST,
    impulse=GHOST,
    catalyst=BELOVED,
    result=COUNCIL,
    description="Personal longing becomes collective achievement"
)


# ============================================================================
# 6. UTILITY FUNCTIONS
# ============================================================================

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
    # BFS to find shortest paths
    queue = deque([(start, [])])
    visited = {start: 0}
    paths = []
    
    while queue:
        current, path = queue.popleft()
        
        if current == end:
            paths.append(path)
            if len(paths) > 10:  # Limit results
                break
            continue
        
        if len(path) >= max_steps:
            continue
        
        # Try all possible impulses and catalysts (simplified: try common ones first)
        for i in range(0, 64, 8):  # Sample for efficiency
            for j in range(0, 64, 8):
                impulse = Archetype.from_int(i)
                catalyst = Archetype.from_int(j)
                next_state = current ^ impulse ^ catalyst
                
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
    
    # Find sample possible catalysts
    for i in range(0, 64, 4):  # Sample for efficiency
        catalyst = Archetype.from_int(i)
        impulse = required ^ catalyst
        analysis["possible_catalysts"].append({
            "catalyst": catalyst.bits,
            "catalyst_name": catalyst.name,
            "impulse": impulse.bits,
            "impulse_name": impulse.name
        })
    
    return analysis


def bits_to_int(bits: str) -> int:
    """Convert 6-bit string to integer."""
    clean = bits.replace(" ", "")
    return int(clean, 2)


def int_to_bits(value: int) -> str:
    """Convert integer to 6-bit string."""
    return format(value, '06b')


def name_to_archetype(name: str) -> Optional[Archetype]:
    """Convert archetype name to Archetype object."""
    catalog = ArchetypeCatalog()
    return catalog.get_by_name(name)


# ============================================================================
# 7. GENERATOR CLASSES
# ============================================================================

class CharacterGenerator:
    """Generate characters from archetypes."""
    
    def __init__(self, catalog: ArchetypeCatalog):
        self.catalog = catalog
        
        # Name pools by archetype
        self.name_pools = {
            WHO.ME: ["Luca", "Mara", "Eli", "Nova", "Orion", "Sage", "Luna", "Kai"],
            WHO.WE: ["The People", "The Community", "The Tribe", "The Fellowship"],
            WHO.YOU: ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan"],
            WHO.THEY: ["The Stranger", "The Voice", "The Force", "The System"]
        }
        
        # Background templates by archetype
        self.background_templates = {
            (WHO.ME, WHERE.NORTH): "lived alone in the mountains for as long as they can remember",
            (WHO.ME, WHERE.SOUTH): "carries a fire inside that never goes out",
            (WHO.ME, WHERE.EAST): "stands at the threshold of something new",
            (WHO.ME, WHERE.WEST): "has built their life with precision and care",
            (WHO.WE, WHERE.NORTH): "a community bound by shared silence",
            (WHO.WE, WHERE.SOUTH): "a people who feel everything together",
            (WHO.WE, WHERE.EAST): "a tribe on the edge of becoming",
            (WHO.WE, WHERE.WEST): "a society held together by laws and customs",
            (WHO.YOU, WHERE.NORTH): "known for their wisdom and counsel",
            (WHO.YOU, WHERE.SOUTH): "loved deeply by all who meet them",
            (WHO.YOU, WHERE.EAST): "appears when least expected",
            (WHO.YOU, WHERE.WEST): "speaks with clarity and precision",
            (WHO.THEY, WHERE.NORTH): "an impersonal force, like the weather",
            (WHO.THEY, WHERE.SOUTH): "a passion that sweeps through crowds",
            (WHO.THEY, WHERE.EAST): "news from far away",
            (WHO.THEY, WHERE.WEST): "the way things are done"
        }
    
    def generate(
        self,
        archetype: Archetype,
        seed: Optional[str] = None,
        name: Optional[str] = None
    ) -> Character:
        """Generate a character from an archetype."""
        if seed:
            random.seed(hashlib.md5(seed.encode()).digest())
        
        metadata = self.catalog.get(archetype)
        
        # Generate name
        if name:
            char_name = name
        else:
            pool = self.name_pools.get(archetype.who, ["Alex"])
            char_name = random.choice(pool)
            if archetype.who == WHO.WE:
                char_name = f"{char_name} of {archetype.name}"
        
        # Generate background
        template_key = (archetype.who, archetype.where)
        background_template = self.background_templates.get(
            template_key,
            "exists in a state of being"
        )
        
        # Add temporal aspect
        when_desc = {
            WHEN.SPRING: "just beginning",
            WHEN.SUMMER: "at their peak",
            WHEN.AUTUMN: "in a time of reflection",
            WHEN.WINTER: "waiting"
        }[archetype.when]
        
        background = f"{char_name} {background_template}, {when_desc}."
        
        # Derive attributes
        attributes = {
            "motivation": self._derive_motivation(archetype),
            "fear": self._derive_fear(archetype),
            "desire": self._derive_desire(archetype),
            "archetype_name": metadata.get("name", "Unknown"),
            "key_phrase": metadata.get("key", "")
        }
        
        return Character(
            name=char_name,
            current_state=archetype,
            background=background,
            attributes=attributes
        )
    
    def _derive_motivation(self, a: Archetype) -> str:
        """Derive character motivation from archetype."""
        motivations = {
            (WHO.ME, WHEN.SPRING): "To begin something new",
            (WHO.ME, WHEN.SUMMER): "To achieve greatness",
            (WHO.ME, WHEN.AUTUMN): "To understand what was lost",
            (WHO.ME, WHEN.WINTER): "To endure, to survive",
            (WHO.WE, WHEN.SPRING): "To build together",
            (WHO.WE, WHEN.SUMMER): "To celebrate what they've built",
            (WHO.WE, WHEN.AUTUMN): "To preserve their way of life",
            (WHO.WE, WHEN.WINTER): "To wait together",
            (WHO.YOU, WHEN.SPRING): "To help someone begin",
            (WHO.YOU, WHEN.SUMMER): "To guide someone to fulfillment",
            (WHO.YOU, WHEN.AUTUMN): "To help someone understand",
            (WHO.YOU, WHEN.WINTER): "To be present with someone",
            (WHO.THEY, WHEN.SPRING): "To announce what's coming",
            (WHO.THEY, WHEN.SUMMER): "To sweep through",
            (WHO.THEY, WHEN.AUTUMN): "To harvest what was sown",
            (WHO.THEY, WHEN.WINTER): "To be the silence"
        }
        return motivations.get((a.who, a.when), "To find meaning")
    
    def _derive_fear(self, a: Archetype) -> str:
        """Derive character fear from archetype."""
        fears = {
            WHERE.EAST: "Fear of never beginning",
            WHERE.SOUTH: "Fear of being consumed",
            WHERE.WEST: "Fear of chaos, of losing control",
            WHERE.NORTH: "Fear of emptiness, of meaninglessness"
        }
        return fears.get(a.where, "Fear of the unknown")
    
    def _derive_desire(self, a: Archetype) -> str:
        """Derive character desire from archetype."""
        desires = {
            WHEN.SPRING: "Desire for new possibilities",
            WHEN.SUMMER: "Desire for fulfillment",
            WHEN.AUTUMN: "Desire to understand",
            WHEN.WINTER: "Desire for rest"
        }
        return desires.get(a.when, "Desire for change")


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
    
    def _generate_setting(self, a: Archetype) -> str:
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
        
        return (f"The story takes place in {where_templates[a.where]}, "
                f"{when_templates[a.when]}, "
                f"{who_templates[a.who]}.")
    
    def _derive_world_rules(self, a: Archetype) -> Dict[str, Any]:
        """Derive world rules from archetype."""
        rules = {
            "magic_system": self._derive_magic(a),
            "social_structure": self._derive_social(a),
            "cosmic_principle": self._derive_cosmic(a)
        }
        return rules
    
    def _derive_magic(self, a: Archetype) -> str:
        """Derive magic system from archetype."""
        where_magic = {
            WHERE.EAST: "magic of beginnings, of potential",
            WHERE.SOUTH: "emotional magic, fire, passion",
            WHERE.WEST: "structured magic, formulas, precision",
            WHERE.NORTH: "mental magic, telepathy, prophecy"
        }
        return where_magic.get(a.where, "subtle, almost imperceptible magic")
    
    def _derive_social(self, a: Archetype) -> str:
        """Derive social structure from archetype."""
        who_social = {
            WHO.ME: "individualistic, merit-based, often lonely",
            WHO.WE: "collectivist, communal, clan-based",
            WHO.YOU: "relational, dialogue-focused, therapeutic",
            WHO.THEY: "bureaucratic, impersonal, system-driven"
        }
        return who_social.get(a.who, "complex and layered")
    
    def _derive_cosmic(self, a: Archetype) -> str:
        """Derive cosmic principle from archetype."""
        when_cosmic = {
            WHEN.SPRING: "the universe is becoming, unfolding",
            WHEN.SUMMER: "the universe is at its peak, fully manifest",
            WHEN.AUTUMN: "the universe is declining, returning to source",
            WHEN.WINTER: "the universe is latent, potential, waiting"
        }
        return when_cosmic.get(a.when, "cyclical, ever-turning")


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
        
        # Event description templates
        self.event_templates = {
            "WHO": [
                "A profound identity shift occurs",
                "They are no longer who they were",
                "Their name takes on new meaning",
                "The question 'who are you?' becomes impossible to answer"
            ],
            "WHERE": [
                "The world around them transforms",
                "They find themselves in an unfamiliar place",
                "The landscape shifts, subtly but unmistakably",
                "They cross a threshold and cannot go back"
            ],
            "WHEN": [
                "Their relationship to time changes",
                "Past, present, and future blur together",
                "They feel time differently now",
                "The season shifts within them"
            ],
            "WHO,WHERE": [
                "Their place in the world is redefined",
                "They see themselves differently in this new place",
                "Identity and location intertwine"
            ],
            "WHO,WHEN": [
                "Who they are and when they exist shifts",
                "Memory and identity merge",
                "They become someone new in a new time"
            ],
            "WHERE,WHEN": [
                "The very fabric of their reality bends",
                "Space and time become fluid",
                "They exist between places and moments"
            ],
            "WHO,WHERE,WHEN": [
                "Everything changes in a single moment",
                "They are reborn into a new world",
                "Nothing remains as it was"
            ]
        }
        
        # Specific templates for known archetypes
        self.specific_templates = {
            GHOST: " as a stranger arrives from the east",
            BELOVED: " through the words of one who truly sees them",
            PIONEER: " and they feel the pull of something new",
            STEADFAST: " though they try to hold on",
            COUNCIL: " and they are no longer alone"
        }
    
    def generate_arc(
        self,
        initial: Archetype,
        target: Archetype,
        protagonist_name: Optional[str] = None,
        complexity: int = 3
    ) -> NarrativeArc:
        """Generate a narrative arc from initial to target state."""
        
        # Generate protagonist
        protagonist = self.character_gen.generate(
            initial,
            seed=protagonist_name,
            name=protagonist_name
        )
        
        # Calculate required change
        required_change = initial ^ target
        
        # Decompose into steps
        steps = self._decompose_change(required_change, complexity)
        
        # Generate plot points
        plot_points = []
        current = initial
        
        for i, (impulse_bits, catalyst_bits) in enumerate(steps):
            impulse = Archetype.from_bits(impulse_bits)
            catalyst = Archetype.from_bits(catalyst_bits)
            
            # Generate event
            event = self._generate_event(
                current, impulse, catalyst, i+1
            )
            plot_points.append(event)
            
            # Update current state
            current = current ^ impulse ^ catalyst
        
        # Verify we reached target
        if current != target:
            # Fallback: direct transmutation
            direct_event = self._generate_event(
                initial, required_change, Archetype.from_bits("00 00 00"), 1
            )
            plot_points = [direct_event]
            current = initial ^ required_change
        
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
        required_int = required_change.int_value
        
        if complexity == 1 or required_int == 0:
            # Single step: required_change = impulse ⊕ catalyst
            impulse_int = random.randint(0, 63)
            catalyst_int = required_int ^ impulse_int
            return [(int_to_bits(impulse_int), int_to_bits(catalyst_int))]
        
        # For multiple steps, try to find meaningful decomposition
        steps = []
        remaining = required_int
        
        # If required change is small, use it directly
        if required_int < 8:  # Small change
            step_size = required_int
            impulse_int = random.randint(0, min(7, step_size))
            catalyst_int = step_size ^ impulse_int
            steps.append((int_to_bits(impulse_int), int_to_bits(catalyst_int)))
            return steps
        
        # For larger changes, try to use master formula components
        # This is a simplified approach
        step1_int = random.randint(1, 15)
        step2_int = required_int ^ step1_int
        
        impulse1 = random.randint(0, 63)
        catalyst1 = step1_int ^ impulse1
        steps.append((int_to_bits(impulse1), int_to_bits(catalyst1)))
        
        impulse2 = random.randint(0, 63)
        catalyst2 = step2_int ^ impulse2
        steps.append((int_to_bits(impulse2), int_to_bits(catalyst2)))
        
        return steps[:complexity]
    
    def _generate_event(
        self,
        current: Archetype,
        impulse: Archetype,
        catalyst: Archetype,
        step_number: int
    ) -> Event:
        """Generate a plot event from a transmutation step."""
        
        new_state = current ^ impulse ^ catalyst
        
        # Determine which axes changed
        changed = []
        if current.who != new_state.who:
            changed.append("WHO")
        if current.where != new_state.where:
            changed.append("WHERE")
        if current.when != new_state.when:
            changed.append("WHEN")
        
        changed_key = ",".join(sorted(changed)) if changed else "None"
        
        # Get base description
        base = self.event_templates.get(
            changed_key,
            ["Something shifts, subtly but profoundly"]
        )
        description = random.choice(base)
        
        # Add specific details for known archetypes
        for archetype, template in self.specific_templates.items():
            if impulse == archetype:
                description += template
                break
            elif catalyst == archetype and random.random() < 0.5:
                description += template
                break
        
        # Add step context
        if step_number == 1:
            description = "First, " + description[0].lower() + description[1:]
        elif step_number == 2:
            description = "Then, " + description[0].lower() + description[1:]
        elif step_number == 3:
            description = "Finally, " + description[0].lower() + description[1:]
        
        significance = len(changed) / 3.0
        
        return Event(
            event_type=changed_key,
            description=description,
            previous_state=current,
            new_state=new_state,
            significance=significance
        )


class StoryRenderer:
    """Render narrative arcs into prose."""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, List[str]]:
        """Load story templates."""
        return {
            "opening": [
                "In {setting}",
                "There once was {protagonist} who {background}",
                "The story begins {setting}",
                "{protagonist} lived {background}",
                "Long ago, {setting}"
            ],
            "intro": [
                "{name} was {archetype}, driven by {motivation}, fearing {fear}.",
                "{name} embodied the {archetype}, {motivation}, always aware of {fear}.",
                "They called {name} the {archetype}, for they {motivation} despite {fear}."
            ],
            "event": [
                "{description}",
                "And so {description}",
                "But {description}",
                "Then {description}",
                "One day, {description}"
            ],
            "reflection": [
                "Nothing would ever be the same.",
                "They felt the change deep within.",
                "The world looked different now.",
                "Something had shifted, though they couldn't name it.",
                "A door had opened that could never be closed."
            ],
            "closing": [
                "And so {protagonist} became {final_state}.",
                "Thus ended the journey of {protagonist}.",
                "{protagonist} was never the same again.",
                "In the end, {protagonist} found {final_state}.",
                "And there, {protagonist} remained."
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
        intro = random.choice(self.templates["intro"]).format(
            name=arc.protagonist.name,
            archetype=arc.protagonist.attributes.get("archetype_name", "unknown"),
            motivation=arc.protagonist.attributes.get("motivation", "").lower(),
            fear=arc.protagonist.attributes.get("fear", "").lower()
        )
        paragraphs.append(intro)
        
        # Plot points
        for i, event in enumerate(arc.plot_points):
            # Event description
            event_text = random.choice(self.templates["event"]).format(
                description=event.description
            )
            paragraphs.append(event_text)
            
            # Add reflection (except after last event)
            if i < len(arc.plot_points) - 1:
                reflection = random.choice(self.templates["reflection"])
                paragraphs.append(reflection)
        
        # Closing
        final_state_name = arc.final_state.name
        closing = random.choice(self.templates["closing"]).format(
            protagonist=arc.protagonist.name,
            final_state=final_state_name
        )
        paragraphs.append(closing)
        
        return "\n\n".join(paragraphs)


# ============================================================================
# 8. MAIN ENGINE
# ============================================================================

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
        
        # Title templates
        self.title_templates = [
            "The {result_name} of {protagonist}",
            "{protagonist}'s Journey",
            "The Transmutation",
            "Salt",
            "Those Who Wait",
            "The Architect and the Bird",
            "The Last Dance",
            "The Library of Dreams",
            "The {initial_name} and the {impulse_name}",
            "How {protagonist} Became {result_name}",
            "The {catalyst_name}'s Gift",
            "A {result_name} Story"
        ]
    
    def generate_story(
        self,
        initial: Optional[Archetype] = None,
        target: Optional[Archetype] = None,
        formula_name: Optional[str] = None,
        protagonist_name: Optional[str] = None,
        style: str = "magic_realism",
        complexity: int = 3,
        seed: Optional[str] = None
    ) -> Story:
        """
        Generate a complete story.
        
        Args:
            initial: Starting archetype (random if None)
            target: Target archetype (random if None)
            formula_name: Use predefined transmutation
            protagonist_name: Optional name for protagonist
            style: Literary style (unused in basic version)
            complexity: Number of plot points (1-5)
            seed: Random seed for reproducibility
            
        Returns:
            Complete Story object
        """
        
        if seed:
            random.seed(hashlib.md5(seed.encode()).digest())
        
        # Determine initial and target states
        formula = None
        if formula_name:
            formula = self.transmutations.find_by_name(formula_name)
            if formula:
                initial = formula.initial
                target = formula.result
        
        if initial is None:
            initial = self.catalog.random()
        
        if target is None:
            # Pick a random target different from initial
            targets = [a for a in self.catalog.all() if a != initial]
            target = random.choice(targets) if targets else initial
        
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
        title = self._generate_title(arc, formula)
        
        # Collect metadata
        metadata = {
            "initial_state": initial.bits,
            "final_state": target.bits,
            "initial_name": initial.name,
            "final_name": target.name,
            "transmutations": [
                {
                    "step": i,
                    "event": e.description,
                    "bits_changed": e.bits_changed,
                    "from": e.previous_state.bits,
                    "to": e.new_state.bits,
                    "from_name": e.previous_state.name,
                    "to_name": e.new_state.name
                }
                for i, e in enumerate(arc.plot_points)
            ],
            "dramatic_tension": arc.dramatic_tension,
            "style": style,
            "complexity": complexity
        }
        
        if formula:
            metadata["formula"] = formula.name
        
        return Story(
            title=title,
            text=text,
            arc=arc,
            world=world,
            metadata=metadata
        )
    
    def _generate_title(self, arc: NarrativeArc, formula: Optional[TransmutationFormula] = None) -> str:
        """Generate story title."""
        template = random.choice(self.title_templates)
        
        # Try to get impulse and catalyst from first event if available
        impulse_name = "Stranger"
        catalyst_name = "Guide"
        if arc.plot_points:
            # This is simplified; in a real implementation we'd track these
            pass
        
        return template.format(
            protagonist=arc.protagonist.name,
            result_name=arc.final_state.name,
            initial_name=arc.initial_state.name,
            impulse_name=impulse_name,
            catalyst_name=catalyst_name,
            formula_name=formula.name if formula else "Change"
        )
    
    def batch_generate(
        self,
        count: int,
        **kwargs
    ) -> List[Story]:
        """Generate multiple stories."""
        return [self.generate_story(**kwargs) for _ in range(count)]
    
    def generate_from_formula(
        self,
        formula_name: str,
        protagonist_name: Optional[str] = None,
        **kwargs
    ) -> Story:
        """Generate a story using a master formula."""
        return self.generate_story(
            formula_name=formula_name,
            protagonist_name=protagonist_name,
            **kwargs
        )


# ============================================================================
# 9. CONVENIENCE FUNCTIONS
# ============================================================================

def create_archetype(who: str, where: str, when: str) -> Archetype:
    """Create an archetype from string values."""
    who_map = {"ME": WHO.ME, "WE": WHO.WE, "YOU": WHO.YOU, "THEY": WHO.THEY}
    where_map = {"EAST": WHERE.EAST, "SOUTH": WHERE.SOUTH, 
                 "WEST": WHERE.WEST, "NORTH": WHERE.NORTH}
    when_map = {"SPRING": WHEN.SPRING, "SUMMER": WHEN.SUMMER,
                "AUTUMN": WHEN.AUTUMN, "WINTER": WHEN.WINTER}
    
    return Archetype(
        who=who_map[who.upper()],
        where=where_map[where.upper()],
        when=when_map[when.upper()]
    )


def generate_story(
    initial: Optional[str] = None,
    target: Optional[str] = None,
    formula: Optional[str] = None,
    name: Optional[str] = None,
    complexity: int = 3
) -> Story:
    """Convenience function to generate a story."""
    engine = SUBITNarrativeEngine()
    
    initial_arch = None
    target_arch = None
    
    if initial:
        if " " in initial:
            initial_arch = Archetype.from_bits(initial)
        else:
            initial_arch = name_to_archetype(initial)
    
    if target:
        if " " in target:
            target_arch = Archetype.from_bits(target)
        else:
            target_arch = name_to_archetype(target)
    
    return engine.generate_story(
        initial=initial_arch,
        target=target_arch,
        formula_name=formula,
        protagonist_name=name,
        complexity=complexity
    )


# ============================================================================
# 10. EXAMPLE USAGE
# ============================================================================

def example_philosopher_stone():
    """Generate a story using the Philosopher's Stone formula."""
    engine = SUBITNarrativeEngine()
    
    story = engine.generate_from_formula(
        formula_name="Philosopher's Stone",
        protagonist_name="Luca",
        complexity=3
    )
    
    print(f"Title: {story.title}\n")
    print(story.text)
    print(f"\n--- Analysis ---")
    print(f"Initial: {story.arc.initial_state.bits} ({story.arc.initial_state.name})")
    print(f"Final: {story.arc.final_state.bits} ({story.arc.final_state.name})")
    print(f"Dramatic tension: {story.arc.dramatic_tension:.2f}")
    
    return story


def example_random():
    """Generate a random story."""
    engine = SUBITNarrativeEngine()
    
    story = engine.generate_story(complexity=3)
    
    print(f"Title: {story.title}\n")
    print(story.text)
    print(f"\n--- Analysis ---")
    print(f"Initial: {story.arc.initial_state.bits} ({story.arc.initial_state.name})")
    print(f"Final: {story.arc.final_state.bits} ({story.arc.final_state.name})")
    
    return story


if __name__ == "__main__":
    print("=" * 60)
    print("SUBIT Narrative Engine")
    print("6 bits = 64 archetypes = infinite stories")
    print("=" * 60)
    print()
    
    # Example: Philosopher's Stone
    print("Generating Philosopher's Stone story...\n")
    example_philosopher_stone()
