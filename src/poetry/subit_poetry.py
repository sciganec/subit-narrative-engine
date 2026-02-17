"""
SUBIT Poetry Engine
Extension of SUBIT Narrative Engine for poetic generation

6 bits = 64 archetypes = infinite poems

This module extends the SUBIT system into poetry, mapping each archetype
to poetic voice, imagery, meter, and form.
"""

import random
import sys
import os
from typing import Dict, List, Optional, Tuple, Any, Union

# Add parent directory to path for importing base SUBIT
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.subit import (
    WHO, WHERE, WHEN,
    Archetype, ArchetypeCatalog,
    ZERO, PIONEER, CONCILIAR, CONFESSOR,
    STEADFAST, GHOST, BELOVED, COUNCIL
)


# ============================================================================
# 1. POETIC INTERPRETATION TABLES
# ============================================================================

# Poetic voice by WHO axis
POETIC_VOICE = {
    WHO.ME: {
        "name": "Confessional",
        "voice": "First-person, intimate, personal",
        "pronoun": "I",
        "tone": "Bittersweet, vulnerable, authentic",
        "rhyme": "Irregular, internal rhymes, assonance"
    },
    WHO.WE: {
        "name": "Choral",
        "voice": "Plural, communal, prophetic",
        "pronoun": "we",
        "tone": "Epic, ritual, ceremonial",
        "rhyme": "Repetitive, incantatory, refrains"
    },
    WHO.YOU: {
        "name": "Dialogic",
        "voice": "Second-person, addressing another",
        "pronoun": "you",
        "tone": "Intimate, dramatic, urgent",
        "rhyme": "Direct address, echoes, call-and-response"
    },
    WHO.THEY: {
        "name": "Impersonal",
        "voice": "Detached, observational, oracular",
        "pronoun": "they",
        "tone": "Philosophical, cold, timeless",
        "rhyme": "Free verse, prose poetry, no rhyme"
    }
}

# Poetic imagery by WHERE axis
POETIC_IMAGERY = {
    WHERE.EAST: {
        "name": "Dawn",
        "images": ["dawn", "horizon", "road", "threshold", "sunrise", "first light", "morning star"],
        "lexicon": ["begin", "first", "new", "arise", "awaken", "emerge"],
        "atmosphere": "Expectant, hopeful, anticipatory"
    },
    WHERE.SOUTH: {
        "name": "Fire",
        "images": ["fire", "flame", "blood", "heart", "summer", "sun at zenith", "burning"],
        "lexicon": ["burn", "passion", "desire", "intense", "consume", "blaze"],
        "atmosphere": "Passionate, ardent, overwhelming"
    },
    WHERE.WEST: {
        "name": "Structure",
        "images": ["city", "walls", "books", "laws", "architecture", "sunset", "bridge"],
        "lexicon": ["build", "form", "structure", "measure", "order", "precise"],
        "atmosphere": "Melancholic, wise, ordered"
    },
    WHERE.NORTH: {
        "name": "Ice",
        "images": ["snow", "ice", "stars", "silence", "night", "mirror", "death"],
        "lexicon": ["cold", "still", "eternal", "reflect", "pause", "silence"],
        "atmosphere": "Cold, deep, still, contemplative"
    }
}

# Poetic time by WHEN axis
POETIC_TIME = {
    WHEN.SPRING: {
        "name": "Beginning",
        "rhythm": "Accelerating, rising",
        "meter": ["iambic", "anapestic"],
        "dynamics": "Building, growing, unfolding"
    },
    WHEN.SUMMER: {
        "name": "Peak",
        "rhythm": "Energetic, driving",
        "meter": ["dactylic hexameter", "epic"],
        "dynamics": "Climactic, intense, full"
    },
    WHEN.AUTUMN: {
        "name": "Harvest",
        "rhythm": "Decelerating, falling",
        "meter": ["elegiac couplets"],
        "dynamics": "Fading, reflective, harvesting"
    },
    WHEN.WINTER: {
        "name": "Stillness",
        "rhythm": "Static, paused",
        "meter": ["free verse", "spondees"],
        "dynamics": "Contemplative, still, potential"
    }
}

# Poetic forms by archetype tendencies
POETIC_FORMS = {
    "haiku": {
        "lines": 3,
        "syllables": [5, 7, 5],
        "rhyme": "unrhymed",
        "tradition": "Japanese",
        "seasonal": True
    },
    "sonnet": {
        "lines": 14,
        "rhyme_schemes": {
            "petrarchan": "abba abba cdc dcd",
            "shakespearean": "abab cdcd efef gg",
            "spenserian": "abab bcbc cdcd ee"
        },
        "volta": "line 9 or 13",
        "tradition": "Italian/English"
    },
    "free_verse": {
        "lines": "variable",
        "rhyme": "none",
        "meter": "variable",
        "tradition": "Modern"
    },
    "blank_verse": {
        "lines": "variable",
        "rhyme": "none",
        "meter": "iambic pentameter",
        "tradition": "English dramatic"
    },
    "elegy": {
        "lines": "variable",
        "meter": "elegiac couplets",
        "theme": "mourning",
        "tradition": "Greek/Latin"
    },
    "ode": {
        "lines": "variable",
        "meter": "lyric",
        "theme": "praise",
        "tradition": "Greek"
    },
    "ballad": {
        "lines": 4,
        "meter": "ballad meter (4/3 stresses)",
        "rhyme": "abab or abcb",
        "tradition": "Folk"
    },
    "hymn": {
        "lines": "variable",
        "meter": "common meter",
        "theme": "praise/worship",
        "tradition": "Religious"
    },
    "haiku_sequence": {
        "lines": "multiple 3-line poems",
        "syllables": [5, 7, 5],
        "theme": "seasonal or thematic",
        "tradition": "Japanese"
    }
}


# ============================================================================
# 2. POETRY ENGINE CLASS
# ============================================================================

class SUBITPoetryEngine:
    """
    Poetry generation engine based on SUBIT archetypes.
    
    Extends the SUBIT system into verse, generating poems from archetypal states.
    """
    
    def __init__(self, catalog: Optional[ArchetypeCatalog] = None):
        """
        Initialize the poetry engine.
        
        Args:
            catalog: Optional ArchetypeCatalog instance
        """
        self.catalog = catalog or ArchetypeCatalog()
        self.forms = POETIC_FORMS
        
        # Line templates for different archetypes
        self.line_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, List[str]]:
        """Initialize line templates for different archetypes."""
        return {
            "philosopher": [
                "I sit and watch the {image} descend",
                "The {image} asks a question without sound",
                "What {image} knows that I am yet to learn",
                "I look into the {image} and see",
                "The {image} holds a truth I cannot name"
            ],
            "steadfast": [
                "I hold this {image} like salt upon my tongue",
                "The {image} remembers what I try to forget",
                "Frozen in {image}, I wait for spring",
                "This {image} is all that remains of before",
                "I count the {image} like years without you"
            ],
            "ecstatic": [
                "I burn with {image}, I dance with flame",
                "The {image} consumes me and I am free",
                "In {image} I lose the self I was",
                "Fire of {image}, fire of desire",
                "I am the {image} and the {image} is me"
            ],
            "pioneer": [
                "I set my foot upon the {image} road",
                "The {image} waits beyond the morning hill",
                "First {image} of dawn, first step of the way",
                "I go where {image} has never been",
                "The {image} calls and I must answer"
            ],
            "ghost": [
                "I come again when {image} is deep",
                "The {image} remembers what you forget",
                "Returning through {image}, I find you still",
                "In {image} I walk where living cannot",
                "The {image} holds my unfinished words"
            ],
            "beloved": [
                "Rest here, beloved, in this {image} light",
                "You are the {image} that warms my winter",
                "In your {image} I find my home at last",
                "Love like {image}, gentle and deep",
                "Your {image} speaks what words cannot"
            ],
            "council": [
                "We gather where the {image} meets the sky",
                "Together we have learned what {image} teaches",
                "Our {image} joined, we speak as one",
                "What {image} divided, we have united",
                "In {image} we find our common ground"
            ],
            "zero": [
                "Before the {image}, there was silence",
                "Nothing but {image}, waiting to become",
                "The {image} holds all potential, unspoken",
                "Zero, {image}, the unwritten poem",
                "From {image} all words arise and return"
            ]
        }
    
    def _get_archetype_poetic_profile(self, archetype: Archetype) -> Dict[str, Any]:
        """
        Get complete poetic profile for an archetype.
        
        Args:
            archetype: The archetype to profile
            
        Returns:
            Dictionary with poetic voice, imagery, time, and form tendencies
        """
        return {
            "who": POETIC_VOICE[archetype.who],
            "where": POETIC_IMAGERY[archetype.where],
            "when": POETIC_TIME[archetype.when],
            "archetype_name": archetype.name,
            "archetype_bits": archetype.bits
        }
    
    def _select_images(self, profile: Dict[str, Any], count: int = 3) -> List[str]:
        """Select random images from the archetype's imagery cluster."""
        images = profile["where"]["images"]
        return random.sample(images, min(count, len(images)))
    
    def _generate_line(self, template_key: str, image: str) -> str:
        """Generate a line from a template."""
        templates = self.line_templates.get(template_key, ["The {image} waits"])
        template = random.choice(templates)
        return template.format(image=image)
    
    def generate_haiku(self, archetype: Union[Archetype, str]) -> str:
        """
        Generate a haiku from an archetype.
        
        Args:
            archetype: Archetype instance or name
            
        Returns:
            Haiku as a string (3 lines)
        """
        if isinstance(archetype, str):
            arch = self.catalog.get_by_name(archetype)
            if not arch:
                raise ValueError(f"Unknown archetype: {archetype}")
        else:
            arch = archetype
        
        profile = self._get_archetype_poetic_profile(arch)
        images = self._select_images(profile, 3)
        
        # Map archetype to template key
        template_key = arch.name.lower()
        
        lines = []
        for i, image in enumerate(images):
            line = self._generate_line(template_key, image)
            # Adjust line to approximate haiku syllable count (5-7-5)
            # This is a simplification - real haiku generation would need syllable counting
            lines.append(line)
        
        return "\n".join(lines)
    
    def generate_haiku_sequence(self, archetype: Union[Archetype, str], count: int = 5) -> List[str]:
        """
        Generate a sequence of haiku from an archetype.
        
        Args:
            archetype: Archetype instance or name
            count: Number of haiku to generate
            
        Returns:
            List of haiku strings
        """
        if isinstance(archetype, str):
            arch = self.catalog.get_by_name(archetype)
            if not arch:
                raise ValueError(f"Unknown archetype: {archetype}")
        else:
            arch = archetype
        
        sequence = []
        for _ in range(count):
            haiku = self.generate_haiku(arch)
            sequence.append(haiku)
        
        return sequence
    
    def generate_sonnet(self, archetype: Union[Archetype, str], 
                        rhyme_scheme: str = "shakespearean") -> str:
        """
        Generate a sonnet from an archetype.
        
        Args:
            archetype: Archetype instance or name
            rhyme_scheme: 'shakespearean', 'petrarchan', or 'spenserian'
            
        Returns:
            Sonnet as a string (14 lines)
        """
        if isinstance(archetype, str):
            arch = self.catalog.get_by_name(archetype)
            if not arch:
                raise ValueError(f"Unknown archetype: {archetype}")
        else:
            arch = archetype
        
        profile = self._get_archetype_poetic_profile(arch)
        images = self._select_images(profile, 7)  # Need enough images
        
        template_key = arch.name.lower()
        
        lines = []
        for i in range(14):
            image = images[i % len(images)]
            line = self._generate_line(template_key, image)
            lines.append(line)
        
        # In a real implementation, we would add rhyme and meter
        # This is a placeholder
        
        return "\n".join(lines)
    
    def generate_free_verse(self, archetype: Union[Archetype, str], 
                            line_count: int = 12) -> str:
        """
        Generate free verse from an archetype.
        
        Args:
            archetype: Archetype instance or name
            line_count: Number of lines to generate
            
        Returns:
            Free verse poem as a string
        """
        if isinstance(archetype, str):
            arch = self.catalog.get_by_name(archetype)
            if not arch:
                raise ValueError(f"Unknown archetype: {archetype}")
        else:
            arch = archetype
        
        profile = self._get_archetype_poetic_profile(arch)
        images = self._select_images(profile, line_count // 2)
        
        template_key = arch.name.lower()
        
        lines = []
        for i in range(line_count):
            image = random.choice(images)
            line = self._generate_line(template_key, image)
            lines.append(line)
        
        return "\n".join(lines)
    
    def generate_poem(self, 
                      archetype: Union[Archetype, str],
                      form: str = "free_verse",
                      mood: Optional[str] = None,
                      key_images: Optional[List[str]] = None,
                      line_count: Optional[int] = None,
                      title: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a complete poem with metadata.
        
        Args:
            archetype: Archetype instance or name
            form: Poetic form ('haiku', 'sonnet', 'free_verse', 'blank_verse', etc.)
            mood: Optional mood override
            key_images: Optional list of images to include
            line_count: Optional line count override
            title: Optional title override
            
        Returns:
            Dictionary with poem text and metadata
        """
        if isinstance(archetype, str):
            arch = self.catalog.get_by_name(archetype)
            if not arch:
                raise ValueError(f"Unknown archetype: {archetype}")
        else:
            arch = archetype
        
        # Select form
        if form not in self.forms:
            form = "free_verse"
        
        form_info = self.forms[form]
        
        # Generate poem based on form
        if form == "haiku":
            text = self.generate_haiku(arch)
        elif form == "haiku_sequence":
            poems = self.generate_haiku_sequence(arch, count=5)
            text = "\n\n".join(poems)
        elif form == "sonnet":
            text = self.generate_sonnet(arch)
        else:  # free_verse or other
            lc = line_count or 12
            text = self.generate_free_verse(arch, lc)
        
        # Generate title if not provided
        if not title:
            title = self._generate_title(arch, form)
        
        # Build metadata
        profile = self._get_archetype_poetic_profile(arch)
        
        metadata = {
            "title": title,
            "form": form,
            "archetype": arch.name,
            "archetype_bits": arch.bits,
            "voice": profile["who"]["name"],
            "space": profile["where"]["name"],
            "time": profile["when"]["name"],
            "mood": mood or profile["where"]["atmosphere"],
            "key_images": key_images or profile["where"]["images"][:3]
        }
        
        return {
            "title": title,
            "text": text,
            "metadata": metadata
        }
    
    def _generate_title(self, archetype: Archetype, form: str) -> str:
        """Generate a title for a poem."""
        templates = [
            f"{archetype.name} {form.title()}",
            f"The {archetype.name}'s {form.title()}",
            f"{form.title()} of the {archetype.name}",
            f"{random.choice(['Song', 'Ode', 'Hymn', 'Lament'])} of the {archetype.name}",
            f"{random.choice(['Winter', 'Summer', 'Spring', 'Autumn'])} {archetype.name}"
        ]
        return random.choice(templates)
    
    def generate_from_transmutation(self,
                                    formula_name: str,
                                    form: str = "free_verse",
                                    **kwargs) -> Dict[str, Any]:
        """
        Generate a poem based on a transmutation formula.
        
        Args:
            formula_name: Name of the transmutation formula
            form: Poetic form
            **kwargs: Additional arguments for generate_poem
            
        Returns:
            Dictionary with poem and metadata
        """
        # This would use the transmutation catalog
        # For now, just use the result archetype
        from src.subit import TransmutationCatalog
        
        catalog = TransmutationCatalog()
        formula = catalog.find_by_name(formula_name)
        
        if not formula:
            raise ValueError(f"Unknown formula: {formula_name}")
        
        return self.generate_poem(formula.result, form, **kwargs)


# ============================================================================
# 3. EXAMPLE POEMS
# ============================================================================

# Predefined example poems for reference
EXAMPLE_POEMS = {
    "winter_haiku": {
        "title": "Winter Haiku",
        "archetype": "Philosopher",
        "text": """Snow on the book.
Words have frozen.
Waiting for spring.

I look in the mirror.
There — an old man.
When did he arrive?

Night is so long,
you could live
another life.

Wind from the north
carries not cold —
carries questions.

There are no answers.
Only snow,
covering everything."""
    },
    
    "salt_poem": {
        "title": "Salt",
        "archetype": "Steadfast",
        "text": """He sits on the salt flat.
Salt creaks beneath his feet.
Salt on his lips.
Salt in his lungs.

The wind carries white dust into the steppe.
Where she went.
Where she never returned.

Every morning he looks east.
Every evening — west.
Salt pink as blood.
Salt white as a shroud.

He no longer remembers her voice.
Only the taste.
Only the pain.
Only the wind."""
    },
    
    "sonnet_about_fire": {
        "title": "Sonnet About Fire",
        "archetype": "Ecstatic",
        "text": """Your hand is like a brand that burns,
like a talisman that scorches without consuming.
Your name is forbidden fruit
I taste again until dawn.

I count your breaths at night
like a believer counts beads of tears.
Your lips are red-hot swords
that cut the body in two.

Stars fall, and we fall with them,
time becomes thick as resin.
You say: \"This is forever.\" I am silent.
For I know: everything passes except warmth.

And only ashes know this truth:
love is a fire that devours itself."""
    },
    
    "song_of_the_first_path": {
        "title": "Song of the First Path",
        "archetype": "Pioneer",
        "text": """He went out when the morning star arose,
when mist still lay upon the waters,
when even birds had not yet started singing,
only the wind brought distant scent of grass.

He went out — and walked on. Without a guide,
without a map, without hope of return.
Behind him voices called: \"Where are you going,
madman? There's only steppe, only wild steppe!\"

But he walked on. For he heard — not with ears,
but with his heart — that beyond the horizon
lay land that had not been, had never been,
that no one yet had given any name.

He carried nothing: name, and fear, and memory
of mother, and of love — all left behind
as sacrifice upon the threshold stone,
and took only a sword and a handful of salt."""
    },
    
    "those_who_return": {
        "title": "Those Who Return",
        "archetype": "Ghost",
        "text": """At night they come from the mist.
Those we loved.
Those we forgot.
Those we never knew.

They sit at the edge of the bed,
look at us with eyes of old photographs,
whisper names
we never learned to say.

\"Who are you?\" we ask in dreams.
\"We are those who waited,\" they answer.
\"Waited for what?\"
\"For you to ask.\"

Morning comes, mist fades,
photographs dim,
names vanish from the tongue.
But on the pillow remains
a faint impression — where someone sat."""
    }
}


# ============================================================================
# 4. CONVENIENCE FUNCTIONS
# ============================================================================

def create_poetry_engine() -> SUBITPoetryEngine:
    """Create a new poetry engine instance."""
    return SUBITPoetryEngine()


def generate_haiku(archetype_name: str) -> str:
    """Generate a haiku from an archetype name."""
    engine = SUBITPoetryEngine()
    arch = engine.catalog.get_by_name(archetype_name)
    if not arch:
        return f"Unknown archetype: {archetype_name}"
    return engine.generate_haiku(arch)


def generate_haiku_sequence(archetype_name: str, count: int = 5) -> List[str]:
    """Generate a sequence of haiku from an archetype name."""
    engine = SUBITPoetryEngine()
    arch = engine.catalog.get_by_name(archetype_name)
    if not arch:
        return [f"Unknown archetype: {archetype_name}"]
    return engine.generate_haiku_sequence(arch, count)


def get_example_poem(name: str) -> Dict[str, Any]:
    """Get an example poem by name."""
    return EXAMPLE_POEMS.get(name, EXAMPLE_POEMS["winter_haiku"])


def list_example_poems() -> List[str]:
    """List available example poems."""
    return list(EXAMPLE_POEMS.keys())


# ============================================================================
# 5. DEMONSTRATION
# ============================================================================

def demo_poetry_engine():
    """Demonstrate the poetry engine with examples."""
    engine = SUBITPoetryEngine()
    
    print("=" * 60)
    print("SUBIT POETRY ENGINE DEMO")
    print("6 bits = 64 archetypes = infinite poems")
    print("=" * 60)
    
    # Generate haiku from Philosopher archetype
    print("\n\n1. HAIKU FROM PHILOSOPHER ARCHETYPE")
    print("-" * 40)
    haiku = engine.generate_haiku("Philosopher")
    print(haiku)
    
    # Generate haiku sequence
    print("\n\n2. HAIKU SEQUENCE FROM STEADFAST ARCHETYPE")
    print("-" * 40)
    sequence = engine.generate_haiku_sequence("Steadfast", 3)
    for i, h in enumerate(sequence, 1):
        print(f"\n{i}.")
        print(h)
    
    # Generate free verse
    print("\n\n3. FREE VERSE FROM PIONEER ARCHETYPE")
    print("-" * 40)
    poem = engine.generate_free_verse("Pioneer", 8)
    print(poem)
    
    # Generate complete poem with metadata
    print("\n\n4. COMPLETE POEM WITH METADATA")
    print("-" * 40)
    result = engine.generate_poem(
        archetype="Ecstatic",
        form="free_verse",
        mood="passionate",
        key_images=["fire", "stars", "ashes"],
        title="Fire Song"
    )
    print(f"\nTitle: {result['title']}")
    print(f"\n{result['text']}")
    print(f"\nMetadata: {result['metadata']}")
    
    # Show example poem
    print("\n\n5. EXAMPLE POEM: WINTER HAIKU")
    print("-" * 40)
    example = get_example_poem("winter_haiku")
    print(example["text"])
    
    print("\n" + "=" * 60)
    print("6 bits. 64 archetypes. Infinite poems. 🧂")
    print("=" * 60)


if __name__ == "__main__":
    demo_poetry_engine()
