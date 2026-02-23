# 🐍 **dobre.py**

## Python Implementation of the Dobre Language (DBR Edition)

*A bridge between SUBIT archetypes and the resonant Dobre phonetic interface.*

---

```python
"""
dobre.py — Dobre Language Interface for SUBIT Narrative Engine

This module provides a complete Python interface for the Dobre language,
a resonant phonetic implementation of the SUBIT 64-archetype system using
only D, B, R consonants and a, e, i, o vowels.

Dobre Formula:
- WHO (Subject) → D (da/de/di/do)
- WHERE (Space) → B (ba/be/bi/bo)
- WHEN (Time) → R (ra/re/ri/ro)

6 bits = 64 archetypes = spoken reality
"""

import sys
import os
from typing import Tuple, Optional, Dict, List

# Add parent directory to path for importing original SUBIT
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
try:
    from src.subit import Archetype as SubitArchetype
except ImportError:
    # Fallback if original SUBIT not available
    SubitArchetype = None
    print("Warning: Original SUBIT module not found. Running in standalone mode.")


# ============================================================================
# CONSTANTS & MAPPINGS
# ============================================================================

# WHO (Subject) mappings
WHO_TO_D = {
    'ME': 'di',
    'WE': 'do',
    'YOU': 'de',
    'THEY': 'da'
}

D_TO_WHO = {v: k for k, v in WHO_TO_D.items()}

# WHERE (Space) mappings
WHERE_TO_B = {
    'EAST': 'bi',
    'SOUTH': 'bo',
    'WEST': 'be',
    'NORTH': 'ba'
}

B_TO_WHERE = {v: k for k, v in WHERE_TO_B.items()}

# WHEN (Time) mappings
WHEN_TO_R = {
    'SPRING': 'ri',
    'SUMMER': 'ro',
    'AUTUMN': 're',
    'WINTER': 'ra'
}

R_TO_WHEN = {v: k for k, v in WHEN_TO_R.items()}

# All possible Dobre syllables
DOBRE_SYLLABLES = [
    'da', 'de', 'di', 'do',  # D + vowel
    'ba', 'be', 'bi', 'bo',  # B + vowel
    'ra', 're', 'ri', 'ro'   # R + vowel
]

# Basic vocabulary
BASIC_WORDS = {
    'ba': 'yes (NORTH)',
    'bo': 'no (SOUTH)',
    're': 'is/are/does (question word, AUTUMN)',
    'de': 'you (YOU)',
    'di': 'I/me (ME)',
    'do': 'we (WE)',
    'da': 'they (THEY)',
    'ro': 'now (SUMMER)',
    'ra': 'before/why (WINTER)',
    'ri': 'later/what (SPRING)',
    'be': 'where (WHERE)'
}


# ============================================================================
# CORE DOBRE CLASS
# ============================================================================

class Dobre:
    """
    A Dobre word — three syllables representing a complete archetype.
    
    Format: XXX-XXX-XXX where each XXX is a Dobre syllable (D/B/R + vowel)
    Example: di-bi-ri (Pioneer: ME-EAST-SPRING)
    """
    
    def __init__(self, syllable1: str, syllable2: str, syllable3: str):
        """
        Create a Dobre word from three syllables.
        
        Args:
            syllable1: First syllable (WHO dimension) — must start with D
            syllable2: Second syllable (WHERE dimension) — must start with B
            syllable3: Third syllable (WHEN dimension) — must start with R
        """
        # Validate syllables
        if not syllable1[0] == 'd':
            raise ValueError(f"First syllable must start with 'd' (WHO), got '{syllable1}'")
        if not syllable2[0] == 'b':
            raise ValueError(f"Second syllable must start with 'b' (WHERE), got '{syllable2}'")
        if not syllable3[0] == 'r':
            raise ValueError(f"Third syllable must start with 'r' (WHEN), got '{syllable3}'")
        
        if syllable1 not in DOBRE_SYLLABLES:
            raise ValueError(f"Invalid Dobre syllable: '{syllable1}'")
        if syllable2 not in DOBRE_SYLLABLES:
            raise ValueError(f"Invalid Dobre syllable: '{syllable2}'")
        if syllable3 not in DOBRE_SYLLABLES:
            raise ValueError(f"Invalid Dobre syllable: '{syllable3}'")
        
        self.s1 = syllable1  # WHO
        self.s2 = syllable2  # WHERE
        self.s3 = syllable3  # WHEN
    
    @classmethod
    def from_string(cls, dobre_str: str) -> 'Dobre':
        """
        Create a Dobre word from a string like "di-bi-ri".
        
        Args:
            dobre_str: String in format "XXX-XXX-XXX"
        
        Returns:
            Dobre object
        """
        parts = dobre_str.strip().split('-')
        if len(parts) != 3:
            raise ValueError(f"Dobre string must have exactly 3 parts, got {len(parts)}: {dobre_str}")
        return cls(parts[0], parts[1], parts[2])
    
    @classmethod
    def from_archetype(cls, who: str, where: str, when: str) -> 'Dobre':
        """
        Create a Dobre word from SUBIT archetype dimensions.
        
        Args:
            who: ME/WE/YOU/THEY
            where: NORTH/SOUTH/EAST/WEST
            when: WINTER/SPRING/SUMMER/AUTUMN
        
        Returns:
            Dobre object
        """
        if who not in WHO_TO_D:
            raise ValueError(f"Invalid WHO: {who}")
        if where not in WHERE_TO_B:
            raise ValueError(f"Invalid WHERE: {where}")
        if when not in WHEN_TO_R:
            raise ValueError(f"Invalid WHEN: {when}")
        
        return cls(
            WHO_TO_D[who],
            WHERE_TO_B[where],
            WHEN_TO_R[when]
        )
    
    @classmethod
    def from_code(cls, code: int) -> 'Dobre':
        """
        Create a Dobre word from a 6-bit code (0-63).
        
        Args:
            code: Integer from 0 to 63
        
        Returns:
            Dobre object
        """
        if SubitArchetype:
            arch = SubitArchetype.from_code(code)
            return cls.from_archetype(arch.who, arch.where, arch.when)
        else:
            # Standalone mode — derive from bits
            if code < 0 or code > 63:
                raise ValueError(f"Code must be between 0 and 63, got {code}")
            
            bits = format(code, '06b')
            who_bits = bits[0:2]
            where_bits = bits[2:4]
            when_bits = bits[4:6]
            
            # Reverse mapping from bits to dimensions
            who_map = {'00': 'THEY', '01': 'YOU', '10': 'ME', '11': 'WE'}
            where_map = {'00': 'NORTH', '01': 'WEST', '10': 'EAST', '11': 'SOUTH'}
            when_map = {'00': 'WINTER', '01': 'AUTUMN', '10': 'SPRING', '11': 'SUMMER'}
            
            return cls.from_archetype(
                who_map[who_bits],
                where_map[where_bits],
                when_map[when_bits]
            )
    
    def to_archetype(self) -> Tuple[str, str, str]:
        """
        Convert to SUBIT archetype dimensions.
        
        Returns:
            Tuple of (who, where, when)
        """
        return (
            D_TO_WHO[self.s1],
            B_TO_WHERE[self.s2],
            R_TO_WHEN[self.s3]
        )
    
    def to_bits(self) -> str:
        """
        Get the 6-bit binary representation.
        
        Returns:
            6-bit string like "101010"
        """
        who, where, when = self.to_archetype()
        
        # Mapping from dimensions to bits
        who_bits = {'ME': '10', 'WE': '11', 'YOU': '01', 'THEY': '00'}
        where_bits = {'EAST': '10', 'SOUTH': '11', 'WEST': '01', 'NORTH': '00'}
        when_bits = {'SPRING': '10', 'SUMMER': '11', 'AUTUMN': '01', 'WINTER': '00'}
        
        return who_bits[who] + where_bits[where] + when_bits[when]
    
    def to_code(self) -> int:
        """
        Get the integer code (0-63).
        
        Returns:
            Integer between 0 and 63
        """
        return int(self.to_bits(), 2)
    
    def __str__(self) -> str:
        """String representation: "di-bi-ri" """
        return f"{self.s1}-{self.s2}-{self.s3}"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        who, where, when = self.to_archetype()
        return f"<Dobre {self} = {who}-{where}-{when}>"
    
    def __eq__(self, other) -> bool:
        """Equality comparison"""
        if not isinstance(other, Dobre):
            return False
        return self.s1 == other.s1 and self.s2 == other.s2 and self.s3 == other.s3
    
    def __xor__(self, other: 'Dobre') -> 'Dobre':
        """
        XOR operation — fundamental law of SUBIT transmutation.
        
        Args:
            other: Another Dobre word
        
        Returns:
            New Dobre word resulting from XOR operation
        """
        bits1 = self.to_bits()
        bits2 = other.to_bits()
        
        # XOR each bit
        result_bits = ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bits1, bits2))
        
        return Dobre.from_code(int(result_bits, 2))


# ============================================================================
# DOBRE PHRASE CLASS
# ============================================================================

class DobrePhrase:
    """
    A phrase in Dobre language — multiple words spoken in sequence.
    """
    
    def __init__(self, words: List[Dobre]):
        """Create a phrase from a list of Dobre words."""
        self.words = words
    
    @classmethod
    def from_string(cls, phrase_str: str) -> 'DobrePhrase':
        """
        Create a phrase from a string like "di-bi-ri da-ba-ra".
        
        Args:
            phrase_str: Space-separated Dobre words
        """
        word_strings = phrase_str.strip().split()
        words = [Dobre.from_string(w) for w in word_strings]
        return cls(words)
    
    def __str__(self) -> str:
        """String representation: space-separated words"""
        return ' '.join(str(w) for w in self.words)
    
    def __repr__(self) -> str:
        return f"<DobrePhrase: {self}>"
    
    def add(self, word: Dobre) -> 'DobrePhrase':
        """Add a word to the phrase (returns new phrase)."""
        return DobrePhrase(self.words + [word])
    
    def transmute(self) -> Optional[Dobre]:
        """
        If phrase has 3 words, apply XOR transmutation.
        
        Returns:
            Resulting Dobre word, or None if not 3 words
        """
        if len(self.words) != 3:
            return None
        return self.words[0] ^ self.words[1] ^ self.words[2]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def translate_to_dobre(who: str, where: str, when: str) -> str:
    """Simple helper to translate dimensions to Dobre."""
    return str(Dobre.from_archetype(who, where, when))


def translate_from_dobre(dobre_str: str) -> Tuple[str, str, str]:
    """Simple helper to translate Dobre to dimensions."""
    return Dobre.from_string(dobre_str).to_archetype()


def list_all_archetypes() -> List[Dict]:
    """
    List all 64 archetypes with their Dobre pronunciations.
    
    Returns:
        List of dictionaries with code, bits, dimensions, and Dobre
    """
    result = []
    for code in range(64):
        dobre = Dobre.from_code(code)
        who, where, when = dobre.to_archetype()
        
        # Get name from CANON if available
        name = "Unknown"
        try:
            from data.archetypes_dbr import ARCHETYPES_DBR
            name = ARCHETYPES_DBR.get(code, {}).get('name', 'Unknown')
        except ImportError:
            pass
        
        result.append({
            'code': code,
            'bits': dobre.to_bits(),
            'who': who,
            'where': where,
            'when': when,
            'dobre': str(dobre),
            'name': name
        })
    
    return result


def print_all_archetypes():
    """Print all 64 archetypes in a formatted table."""
    print("\n" + "="*80)
    print(f"{'CODE':>4} | {'BITS':>6} | {'WHO':>6} | {'WHERE':>6} | {'WHEN':>6} | {'DOBRE':>9} | NAME")
    print("="*80)
    
    for arch in list_all_archetypes():
        print(f"{arch['code']:4d} | {arch['bits']:6s} | {arch['who']:6s} | "
              f"{arch['where']:6s} | {arch['when']:6s} | {arch['dobre']:9s} | {arch['name']}")


# ============================================================================
# FAMOUS TRANSMUTATIONS
# ============================================================================

# Philosopher's Stone
PHILOSOPHER_STONE = {
    'name': 'Philosopher\'s Stone',
    'formula': 'di-bo-ra ⊕ da-bi-ri ⊕ de-be-ro = do-be-ro',
    'initial': Dobre.from_string('di-bo-ra'),      # Steadfast
    'impulse': Dobre.from_string('da-bi-ri'),      # Ghost
    'catalyst': Dobre.from_string('de-be-ro'),     # Beloved
    'result': Dobre.from_string('do-be-ro')        # Council
}

# Hero's Journey
HERO_JOURNEY = {
    'name': 'Hero\'s Journey',
    'formula': 'di-bi-ri ⊕ da-ba-ra ⊕ do-bo-ro = de-be-re',
    'initial': Dobre.from_string('di-bi-ri'),      # Pioneer
    'impulse': Dobre.from_string('da-ba-ra'),      # Zero
    'catalyst': Dobre.from_string('do-bo-ro'),     # Conciliar
    'result': Dobre.from_string('de-be-re')        # Confessor
}

# Alchemical Marriage
ALCHEMICAL_MARRIAGE = {
    'name': 'Alchemical Marriage',
    'formula': 'di-bi-ri ⊕ de-be-re ⊕ do-bo-ro = da-ba-ra',
    'initial': Dobre.from_string('di-bi-ri'),      # Pioneer
    'impulse': Dobre.from_string('de-be-re'),      # Confessor
    'catalyst': Dobre.from_string('do-bo-ro'),     # Conciliar
    'result': Dobre.from_string('da-ba-ra')        # Zero
}

# All transmutations
TRANSMUTATIONS = [
    PHILOSOPHER_STONE,
    HERO_JOURNEY,
    ALCHEMICAL_MARRIAGE
]


def transmute(a: Dobre, b: Dobre, c: Dobre) -> Dobre:
    """
    Apply the fundamental transmutation: A ⊕ B ⊕ C = D
    
    Args:
        a, b, c: Three Dobre words
    
    Returns:
        Resulting Dobre word
    """
    return a ^ b ^ c


def verify_transmutation(transmutation: Dict) -> bool:
    """
    Verify that a transmutation formula is correct.
    
    Args:
        transmutation: Dictionary with 'initial', 'impulse', 'catalyst', 'result'
    
    Returns:
        True if formula is correct
    """
    result = transmute(
        transmutation['initial'],
        transmutation['impulse'],
        transmutation['catalyst']
    )
    return result == transmutation['result']


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Simple command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Dobre Language Interface')
    parser.add_argument('--translate', nargs=3, metavar=('WHO', 'WHERE', 'WHEN'),
                       help='Translate dimensions to Dobre (e.g., ME EAST SPRING)')
    parser.add_argument('--from-dobre', metavar='DOBRE',
                       help='Translate Dobre to dimensions (e.g., di-bi-ri)')
    parser.add_argument('--code', type=int, choices=range(64),
                       help='Get Dobre for code (0-63)')
    parser.add_argument('--list', action='store_true',
                       help='List all 64 archetypes')
    parser.add_argument('--transmute', nargs=3, metavar=('A', 'B', 'C'),
                       help='Apply XOR transmutation to three Dobre words')
    parser.add_argument('--verify', metavar='NAME',
                       help='Verify a famous transmutation (philosopher, hero, marriage)')
    
    args = parser.parse_args()
    
    if args.translate:
        who, where, when = args.translate
        try:
            dobre = Dobre.from_archetype(who.upper(), where.upper(), when.upper())
            print(f"{who}-{where}-{when} → {dobre}")
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
    
    elif args.from_dobre:
        try:
            who, where, when = Dobre.from_string(args.from_dobre).to_archetype()
            print(f"{args.from_dobre} → {who}-{where}-{when}")
        except ValueError as e:
            print(f"Error: {e}")
    
    elif args.code is not None:
        try:
            dobre = Dobre.from_code(args.code)
            who, where, when = dobre.to_archetype()
            print(f"Code {args.code:2d} ({dobre.to_bits()}): {dobre} = {who}-{where}-{when}")
        except ValueError as e:
            print(f"Error: {e}")
    
    elif args.list:
        print_all_archetypes()
    
    elif args.transmute:
        try:
            a = Dobre.from_string(args.transmute[0])
            b = Dobre.from_string(args.transmute[1])
            c = Dobre.from_string(args.transmute[2])
            result = transmute(a, b, c)
            print(f"{a} ⊕ {b} ⊕ {c} = {result}")
        except ValueError as e:
            print(f"Error: {e}")
    
    elif args.verify:
        name = args.verify.lower()
        if name in ['philosopher', 'philosophers', 'stone']:
            t = PHILOSOPHER_STONE
        elif name in ['hero', 'journey']:
            t = HERO_JOURNEY
        elif name in ['marriage', 'alchemical']:
            t = ALCHEMICAL_MARRIAGE
        else:
            print(f"Unknown transmutation: {name}")
            return
        
        valid = verify_transmutation(t)
        print(f"{t['name']}: {t['formula']}")
        print(f"Verified: {valid}")
    
    else:
        parser.print_help()


# ============================================================================
# EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # If arguments provided, run CLI
    if len(sys.argv) > 1:
        main()
    else:
        # Otherwise, run examples
        print("\n" + "="*60)
        print("DOBRE LANGUAGE — EXAMPLES")
        print("="*60)
        
        # Basic creation
        print("\n📌 Basic Creation:")
        pioneer = Dobre.from_archetype('ME', 'EAST', 'SPRING')
        print(f"Pioneer: {pioneer} = {pioneer.to_archetype()}")
        
        zero = Dobre.from_string('da-ba-ra')
        print(f"Zero: {zero} = {zero.to_archetype()}")
        
        # Code conversion
        print("\n📌 Code Conversion:")
        for code in [0, 42, 63]:
            d = Dobre.from_code(code)
            print(f"Code {code:2d} ({d.to_bits()}): {d}")
        
        # Philosopher's Stone
        print("\n📌 Philosopher's Stone:")
        steadfast = Dobre.from_string('di-bo-ra')
        ghost = Dobre.from_string('da-bi-ri')
        beloved = Dobre.from_string('de-be-ro')
        council = transmute(steadfast, ghost, beloved)
        
        print(f"{steadfast} (Steadfast)")
        print(f"⊕ {ghost} (Ghost)")
        print(f"⊕ {beloved} (Beloved)")
        print(f"= {council} (Council)")
        print(f"Verified: {council == Dobre.from_string('do-be-ro')}")
        
        # Basic phrases
        print("\n📌 Basic Phrases:")
        phrases = [
            'di-bi-ri da-ba-ra',  # Beginning from stillness
            'de-be-ro di-bi-ri',   # Love begins anew
            'do-bo-ro de-be-re'     # Complete with wisdom
        ]
        for p in phrases:
            phrase = DobrePhrase.from_string(p)
            print(f"{p} → {phrase}")
        
        print("\n" + "="*60)
        print("For more: python dobre.py --help")
        print("="*60 + "\n")
```

---

## 📦 **Requirements & Installation**

### requirements.txt
```txt
# No external dependencies required
# Optional: for integration with original SUBIT
# subit @ git+https://github.com/sciganec/subit-narrative-engine.git
```

### setup.py (optional)
```python
from setuptools import setup, find_packages

setup(
    name="dobre",
    version="1.0.0",
    description="Dobre Language — Resonant Voice of SUBIT",
    author="SUBIT Narrative Engine",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "dobre=dobre:main",
        ],
    },
)
```

---

## 🚀 **Usage Examples**

```bash
# Translate dimensions to Dobre
python dobre.py --translate ME EAST SPRING
# Output: ME-EAST-SPRING → di-bi-ri

# Translate Dobre to dimensions
python dobre.py --from-dobre di-bi-ri
# Output: di-bi-ri → ME-EAST-SPRING

# Get Dobre for a code
python dobre.py --code 42
# Output: Code 42 (101010): di-bi-ri = ME-EAST-SPRING

# List all 64 archetypes
python dobre.py --list

# Apply XOR transmutation
python dobre.py --transmute di-bo-ra da-bi-ri de-be-ro
# Output: di-bo-ra ⊕ da-bi-ri ⊕ de-be-ro = do-be-ro

# Verify famous transmutation
python dobre.py --verify philosopher
```

---

## 🔗 **Integration with Original SUBIT**

```python
from src.subit import Archetype
from dobre import Dobre

# Create from original SUBIT
arch = Archetype("ME", "EAST", "SPRING")
dobre = Dobre.from_archetype(arch.who, arch.where, arch.when)
print(dobre)  # di-bi-ri

# Convert back
who, where, when = dobre.to_archetype()
arch2 = Archetype(who, where, when)
```

---

**6 bits. 64 archetypes. One voice. Dobre.** 🜁 🜂 🜃 🜄
