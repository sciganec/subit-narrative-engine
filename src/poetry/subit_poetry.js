/**
 * SUBIT Poetry Engine
 * Extension of SUBIT Narrative Engine for poetic generation
 * 
 * 6 bits = 64 archetypes = infinite poems
 * 
 * This module extends the SUBIT system into poetry, mapping each archetype
 * to poetic voice, imagery, meter, and form.
 */

// ============================================================================
// 1. IMPORTS AND DEPENDENCIES
// ============================================================================

// Note: This file assumes subit.js is in the parent directory
// For use in browser, include both files with script tags

if (typeof require !== 'undefined') {
    // Node.js environment
    const subit = require('../subit.js');
    const { WHO, WHERE, WHEN, Archetype, ArchetypeCatalog } = subit;
} else {
    // Browser environment - assume subit.js already loaded
    // WHO, WHERE, WHEN, Archetype, ArchetypeCatalog are global
}


// ============================================================================
// 2. POETIC INTERPRETATION TABLES
// ============================================================================

const POETIC_VOICE = {
    [WHO.ME]: {
        name: "Confessional",
        voice: "First-person, intimate, personal",
        pronoun: "I",
        tone: "Bittersweet, vulnerable, authentic",
        rhyme: "Irregular, internal rhymes, assonance"
    },
    [WHO.WE]: {
        name: "Choral",
        voice: "Plural, communal, prophetic",
        pronoun: "we",
        tone: "Epic, ritual, ceremonial",
        rhyme: "Repetitive, incantatory, refrains"
    },
    [WHO.YOU]: {
        name: "Dialogic",
        voice: "Second-person, addressing another",
        pronoun: "you",
        tone: "Intimate, dramatic, urgent",
        rhyme: "Direct address, echoes, call-and-response"
    },
    [WHO.THEY]: {
        name: "Impersonal",
        voice: "Detached, observational, oracular",
        pronoun: "they",
        tone: "Philosophical, cold, timeless",
        rhyme: "Free verse, prose poetry, no rhyme"
    }
};

const POETIC_IMAGERY = {
    [WHERE.EAST]: {
        name: "Dawn",
        images: ["dawn", "horizon", "road", "threshold", "sunrise", "first light", "morning star"],
        lexicon: ["begin", "first", "new", "arise", "awaken", "emerge"],
        atmosphere: "Expectant, hopeful, anticipatory"
    },
    [WHERE.SOUTH]: {
        name: "Fire",
        images: ["fire", "flame", "blood", "heart", "summer", "sun at zenith", "burning"],
        lexicon: ["burn", "passion", "desire", "intense", "consume", "blaze"],
        atmosphere: "Passionate, ardent, overwhelming"
    },
    [WHERE.WEST]: {
        name: "Structure",
        images: ["city", "walls", "books", "laws", "architecture", "sunset", "bridge"],
        lexicon: ["build", "form", "structure", "measure", "order", "precise"],
        atmosphere: "Melancholic, wise, ordered"
    },
    [WHERE.NORTH]: {
        name: "Ice",
        images: ["snow", "ice", "stars", "silence", "night", "mirror", "death"],
        lexicon: ["cold", "still", "eternal", "reflect", "pause", "silence"],
        atmosphere: "Cold, deep, still, contemplative"
    }
};

const POETIC_TIME = {
    [WHEN.SPRING]: {
        name: "Beginning",
        rhythm: "Accelerating, rising",
        meter: ["iambic", "anapestic"],
        dynamics: "Building, growing, unfolding"
    },
    [WHEN.SUMMER]: {
        name: "Peak",
        rhythm: "Energetic, driving",
        meter: ["dactylic hexameter", "epic"],
        dynamics: "Climactic, intense, full"
    },
    [WHEN.AUTUMN]: {
        name: "Harvest",
        rhythm: "Decelerating, falling",
        meter: ["elegiac couplets"],
        dynamics: "Fading, reflective, harvesting"
    },
    [WHEN.WINTER]: {
        name: "Stillness",
        rhythm: "Static, paused",
        meter: ["free verse", "spondees"],
        dynamics: "Contemplative, still, potential"
    }
};

const POETIC_FORMS = {
    haiku: {
        lines: 3,
        syllables: [5, 7, 5],
        rhyme: "unrhymed",
        tradition: "Japanese",
        seasonal: true
    },
    sonnet: {
        lines: 14,
        rhymeSchemes: {
            petrarchan: "abba abba cdc dcd",
            shakespearean: "abab cdcd efef gg",
            spenserian: "abab bcbc cdcd ee"
        },
        volta: "line 9 or 13",
        tradition: "Italian/English"
    },
    free_verse: {
        lines: "variable",
        rhyme: "none",
        meter: "variable",
        tradition: "Modern"
    },
    blank_verse: {
        lines: "variable",
        rhyme: "none",
        meter: "iambic pentameter",
        tradition: "English dramatic"
    },
    elegy: {
        lines: "variable",
        meter: "elegiac couplets",
        theme: "mourning",
        tradition: "Greek/Latin"
    },
    ode: {
        lines: "variable",
        meter: "lyric",
        theme: "praise",
        tradition: "Greek"
    },
    ballad: {
        lines: 4,
        meter: "ballad meter (4/3 stresses)",
        rhyme: "abab or abcb",
        tradition: "Folk"
    },
    hymn: {
        lines: "variable",
        meter: "common meter",
        theme: "praise/worship",
        tradition: "Religious"
    },
    haiku_sequence: {
        lines: "multiple 3-line poems",
        syllables: [5, 7, 5],
        theme: "seasonal or thematic",
        tradition: "Japanese"
    }
};


// ============================================================================
// 3. POETRY ENGINE CLASS
// ============================================================================

class SUBITPoetryEngine {
    /**
     * Initialize the poetry engine
     * @param {ArchetypeCatalog} catalog - Optional ArchetypeCatalog instance
     */
    constructor(catalog = null) {
        this.catalog = catalog || new ArchetypeCatalog();
        this.forms = POETIC_FORMS;
        
        // Line templates for different archetypes
        this.lineTemplates = this._initializeTemplates();
        
        // Random seed management
        this._random = Math.random;
    }
    
    /**
     * Initialize line templates for different archetypes
     * @private
     */
    _initializeTemplates() {
        return {
            philosopher: [
                "I sit and watch the {image} descend",
                "The {image} asks a question without sound",
                "What {image} knows that I am yet to learn",
                "I look into the {image} and see",
                "The {image} holds a truth I cannot name"
            ],
            steadfast: [
                "I hold this {image} like salt upon my tongue",
                "The {image} remembers what I try to forget",
                "Frozen in {image}, I wait for spring",
                "This {image} is all that remains of before",
                "I count the {image} like years without you"
            ],
            ecstatic: [
                "I burn with {image}, I dance with flame",
                "The {image} consumes me and I am free",
                "In {image} I lose the self I was",
                "Fire of {image}, fire of desire",
                "I am the {image} and the {image} is me"
            ],
            pioneer: [
                "I set my foot upon the {image} road",
                "The {image} waits beyond the morning hill",
                "First {image} of dawn, first step of the way",
                "I go where {image} has never been",
                "The {image} calls and I must answer"
            ],
            ghost: [
                "I come again when {image} is deep",
                "The {image} remembers what you forget",
                "Returning through {image}, I find you still",
                "In {image} I walk where living cannot",
                "The {image} holds my unfinished words"
            ],
            beloved: [
                "Rest here, beloved, in this {image} light",
                "You are the {image} that warms my winter",
                "In your {image} I find my home at last",
                "Love like {image}, gentle and deep",
                "Your {image} speaks what words cannot"
            ],
            council: [
                "We gather where the {image} meets the sky",
                "Together we have learned what {image} teaches",
                "Our {image} joined, we speak as one",
                "What {image} divided, we have united",
                "In {image} we find our common ground"
            ],
            zero: [
                "Before the {image}, there was silence",
                "Nothing but {image}, waiting to become",
                "The {image} holds all potential, unspoken",
                "Zero, {image}, the unwritten poem",
                "From {image} all words arise and return"
            ]
        };
    }
    
    /**
     * Set random seed for reproducible generation
     * @param {string} seed - Seed string
     */
    setSeed(seed) {
        // Simple seed-based random number generator
        const seedNum = seed.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
        let state = seedNum;
        this._random = function() {
            state = (state * 9301 + 49297) % 233280;
            return state / 233280;
        };
    }
    
    /**
     * Get random element from array
     * @private
     */
    _randomChoice(array) {
        return array[Math.floor(this._random() * array.length)];
    }
    
    /**
     * Get random integer between min and max (inclusive)
     * @private
     */
    _randomInt(min, max) {
        return Math.floor(this._random() * (max - min + 1)) + min;
    }
    
    /**
     * Get complete poetic profile for an archetype
     * @param {Archetype} archetype
     * @returns {Object} Poetic profile
     */
    getArchetypePoeticProfile(archetype) {
        return {
            who: POETIC_VOICE[archetype.who],
            where: POETIC_IMAGERY[archetype.where],
            when: POETIC_TIME[archetype.when],
            archetypeName: archetype.name,
            archetypeBits: archetype.bits
        };
    }
    
    /**
     * Select random images from the archetype's imagery cluster
     * @private
     */
    _selectImages(profile, count = 3) {
        const images = profile.where.images;
        const selected = [];
        const shuffled = [...images].sort(() => 0.5 - this._random());
        return shuffled.slice(0, Math.min(count, images.length));
    }
    
    /**
     * Generate a line from a template
     * @private
     */
    _generateLine(templateKey, image) {
        const templates = this.lineTemplates[templateKey] || ["The {image} waits"];
        const template = this._randomChoice(templates);
        return template.replace(/{image}/g, image);
    }
    
    /**
     * Get template key from archetype name
     * @private
     */
    _getTemplateKey(archetype) {
        const key = archetype.name.toLowerCase();
        return this.lineTemplates[key] ? key : 'philosopher';
    }
    
    /**
     * Generate a haiku from an archetype
     * @param {Archetype|string} archetype - Archetype instance or name
     * @returns {string} Haiku as a string (3 lines)
     */
    generateHaiku(archetype) {
        let arch;
        if (typeof archetype === 'string') {
            arch = this.catalog.getByName(archetype);
            if (!arch) throw new Error(`Unknown archetype: ${archetype}`);
        } else {
            arch = archetype;
        }
        
        const profile = this.getArchetypePoeticProfile(arch);
        const images = this._selectImages(profile, 3);
        const templateKey = this._getTemplateKey(arch);
        
        const lines = [];
        for (let i = 0; i < 3; i++) {
            const image = images[i % images.length];
            const line = this._generateLine(templateKey, image);
            lines.push(line);
        }
        
        return lines.join('\n');
    }
    
    /**
     * Generate a sequence of haiku from an archetype
     * @param {Archetype|string} archetype
     * @param {number} count - Number of haiku to generate
     * @returns {string[]} Array of haiku strings
     */
    generateHaikuSequence(archetype, count = 5) {
        let arch;
        if (typeof archetype === 'string') {
            arch = this.catalog.getByName(archetype);
            if (!arch) throw new Error(`Unknown archetype: ${archetype}`);
        } else {
            arch = archetype;
        }
        
        const sequence = [];
        for (let i = 0; i < count; i++) {
            sequence.push(this.generateHaiku(arch));
        }
        return sequence;
    }
    
    /**
     * Generate free verse from an archetype
     * @param {Archetype|string} archetype
     * @param {number} lineCount - Number of lines to generate
     * @returns {string} Free verse poem
     */
    generateFreeVerse(archetype, lineCount = 12) {
        let arch;
        if (typeof archetype === 'string') {
            arch = this.catalog.getByName(archetype);
            if (!arch) throw new Error(`Unknown archetype: ${archetype}`);
        } else {
            arch = archetype;
        }
        
        const profile = this.getArchetypePoeticProfile(arch);
        const images = this._selectImages(profile, Math.floor(lineCount / 2));
        const templateKey = this._getTemplateKey(arch);
        
        const lines = [];
        for (let i = 0; i < lineCount; i++) {
            const image = this._randomChoice(images);
            const line = this._generateLine(templateKey, image);
            lines.push(line);
        }
        
        return lines.join('\n');
    }
    
    /**
     * Generate a sonnet from an archetype
     * @param {Archetype|string} archetype
     * @param {string} rhymeScheme - 'shakespearean', 'petrarchan', or 'spenserian'
     * @returns {string} Sonnet as a string (14 lines)
     */
    generateSonnet(archetype, rhymeScheme = 'shakespearean') {
        let arch;
        if (typeof archetype === 'string') {
            arch = this.catalog.getByName(archetype);
            if (!arch) throw new Error(`Unknown archetype: ${archetype}`);
        } else {
            arch = archetype;
        }
        
        const profile = this.getArchetypePoeticProfile(arch);
        const images = this._selectImages(profile, 7);
        const templateKey = this._getTemplateKey(arch);
        
        const lines = [];
        for (let i = 0; i < 14; i++) {
            const image = images[i % images.length];
            const line = this._generateLine(templateKey, image);
            lines.push(line);
        }
        
        // Note: In a full implementation, we would add rhyme and meter
        // This is a placeholder for the structure
        
        return lines.join('\n');
    }
    
    /**
     * Generate a complete poem with metadata
     * @param {Object} options
     * @returns {Object} Poem with text and metadata
     */
    generatePoem({
        archetype,
        form = 'free_verse',
        mood = null,
        keyImages = null,
        lineCount = null,
        title = null
    } = {}) {
        if (!archetype) throw new Error('Archetype is required');
        
        let arch;
        if (typeof archetype === 'string') {
            arch = this.catalog.getByName(archetype);
            if (!arch) throw new Error(`Unknown archetype: ${archetype}`);
        } else {
            arch = archetype;
        }
        
        // Select form
        const formInfo = this.forms[form] || this.forms.free_verse;
        
        // Generate poem based on form
        let text;
        if (form === 'haiku') {
            text = this.generateHaiku(arch);
        } else if (form === 'haiku_sequence') {
            const poems = this.generateHaikuSequence(arch, 5);
            text = poems.join('\n\n');
        } else if (form === 'sonnet') {
            text = this.generateSonnet(arch);
        } else {
            const lc = lineCount || 12;
            text = this.generateFreeVerse(arch, lc);
        }
        
        // Generate title if not provided
        if (!title) {
            title = this._generateTitle(arch, form);
        }
        
        // Build metadata
        const profile = this.getArchetypePoeticProfile(arch);
        const images = keyImages || profile.where.images.slice(0, 3);
        
        const metadata = {
            title,
            form,
            archetype: arch.name,
            archetypeBits: arch.bits,
            voice: profile.who.name,
            space: profile.where.name,
            time: profile.when.name,
            mood: mood || profile.where.atmosphere,
            keyImages: images
        };
        
        return {
            title,
            text,
            metadata
        };
    }
    
    /**
     * Generate a title for a poem
     * @private
     */
    _generateTitle(archetype, form) {
        const templates = [
            `${archetype.name} ${form.charAt(0).toUpperCase() + form.slice(1)}`,
            `The ${archetype.name}'s ${form.charAt(0).toUpperCase() + form.slice(1)}`,
            `${form.charAt(0).toUpperCase() + form.slice(1)} of the ${archetype.name}`,
            `${this._randomChoice(['Song', 'Ode', 'Hymn', 'Lament'])} of the ${archetype.name}`,
            `${this._randomChoice(['Winter', 'Summer', 'Spring', 'Autumn'])} ${archetype.name}`
        ];
        return this._randomChoice(templates);
    }
    
    /**
     * Generate a poem based on a transmutation formula
     * @param {string} formulaName - Name of the transmutation formula
     * @param {Object} options - Additional options for generatePoem
     * @returns {Object} Poem with metadata
     */
    generateFromTransmutation(formulaName, options = {}) {
        // Note: This would use the transmutation catalog
        // For now, we'll just use the result archetype
        // In a full implementation, import TransmutationCatalog from subit.js
        
        // Placeholder for transmutation result
        const formulaResults = {
            "Philosopher's Stone": "Council",
            "Hero's Journey": "Confessor",
            "Alchemical Marriage": "Zero",
            "Creative Process": "Council",
            "Healing": "Synod",
            "Revelation": "Mediator",
            "Power Transformation": "Tribe",
            "Dark Night": "Seeker",
            "Awakening": "Scribe",
            "Renewal": "Interpreter",
            "Reconciliation": "Festival",
            "Complete Transmutation": "Zero"
        };
        
        const resultName = formulaResults[formulaName] || "Council";
        const resultArch = this.catalog.getByName(resultName);
        
        return this.generatePoem({
            archetype: resultArch,
            ...options
        });
    }
}


// ============================================================================
// 4. EXAMPLE POEMS
// ============================================================================

const EXAMPLE_POEMS = {
    winter_haiku: {
        title: "Winter Haiku",
        archetype: "Philosopher",
        text: `Snow on the book.
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
covering everything.`
    },
    
    salt_poem: {
        title: "Salt",
        archetype: "Steadfast",
        text: `He sits on the salt flat.
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
Only the wind.`
    },
    
    sonnet_about_fire: {
        title: "Sonnet About Fire",
        archetype: "Ecstatic",
        text: `Your hand is like a brand that burns,
like a talisman that scorches without consuming.
Your name is forbidden fruit
I taste again until dawn.

I count your breaths at night
like a believer counts beads of tears.
Your lips are red-hot swords
that cut the body in two.

Stars fall, and we fall with them,
time becomes thick as resin.
You say: "This is forever." I am silent.
For I know: everything passes except warmth.

And only ashes know this truth:
love is a fire that devours itself.`
    },
    
    song_of_the_first_path: {
        title: "Song of the First Path",
        archetype: "Pioneer",
        text: `He went out when the morning star arose,
when mist still lay upon the waters,
when even birds had not yet started singing,
only the wind brought distant scent of grass.

He went out — and walked on. Without a guide,
without a map, without hope of return.
Behind him voices called: "Where are you going,
madman? There's only steppe, only wild steppe!"

But he walked on. For he heard — not with ears,
but with his heart — that beyond the horizon
lay land that had not been, had never been,
that no one yet had given any name.

He carried nothing: name, and fear, and memory
of mother, and of love — all left behind
as sacrifice upon the threshold stone,
and took only a sword and a handful of salt.`
    },
    
    those_who_return: {
        title: "Those Who Return",
        archetype: "Ghost",
        text: `At night they come from the mist.
Those we loved.
Those we forgot.
Those we never knew.

They sit at the edge of the bed,
look at us with eyes of old photographs,
whisper names
we never learned to say.

"Who are you?" we ask in dreams.
"We are those who waited," they answer.
"Waited for what?"
"For you to ask."

Morning comes, mist fades,
photographs dim,
names vanish from the tongue.
But on the pillow remains
a faint impression — where someone sat.`
    }
};


// ============================================================================
// 5. CONVENIENCE FUNCTIONS
// ============================================================================

/**
 * Create a new poetry engine instance
 * @returns {SUBITPoetryEngine}
 */
function createPoetryEngine() {
    return new SUBITPoetryEngine();
}

/**
 * Generate a haiku from an archetype name
 * @param {string} archetypeName
 * @returns {string}
 */
function generateHaiku(archetypeName) {
    const engine = new SUBITPoetryEngine();
    const arch = engine.catalog.getByName(archetypeName);
    if (!arch) return `Unknown archetype: ${archetypeName}`;
    return engine.generateHaiku(arch);
}

/**
 * Generate a sequence of haiku from an archetype name
 * @param {string} archetypeName
 * @param {number} count
 * @returns {string[]}
 */
function generateHaikuSequence(archetypeName, count = 5) {
    const engine = new SUBITPoetryEngine();
    const arch = engine.catalog.getByName(archetypeName);
    if (!arch) return [`Unknown archetype: ${archetypeName}`];
    return engine.generateHaikuSequence(arch, count);
}

/**
 * Get an example poem by name
 * @param {string} name
 * @returns {Object}
 */
function getExamplePoem(name) {
    return EXAMPLE_POEMS[name] || EXAMPLE_POEMS.winter_haiku;
}

/**
 * List available example poems
 * @returns {string[]}
 */
function listExamplePoems() {
    return Object.keys(EXAMPLE_POEMS);
}


// ============================================================================
// 6. NODE.JS EXPORTS
// ============================================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        // Constants
        POETIC_VOICE,
        POETIC_IMAGERY,
        POETIC_TIME,
        POETIC_FORMS,
        EXAMPLE_POEMS,
        
        // Classes
        SUBITPoetryEngine,
        
        // Functions
        createPoetryEngine,
        generateHaiku,
        generateHaikuSequence,
        getExamplePoem,
        listExamplePoems
    };
}


// ============================================================================
// 7. DEMONSTRATION
// ============================================================================

/**
 * Demonstrate the poetry engine with examples
 */
function demoPoetryEngine() {
    const engine = new SUBITPoetryEngine();
    
    console.log("=".repeat(60));
    console.log("SUBIT POETRY ENGINE DEMO");
    console.log("6 bits = 64 archetypes = infinite poems");
    console.log("=".repeat(60));
    
    // Generate haiku from Philosopher archetype
    console.log("\n\n1. HAIKU FROM PHILOSOPHER ARCHETYPE");
    console.log("-".repeat(40));
    const haiku = engine.generateHaiku("Philosopher");
    console.log(haiku);
    
    // Generate haiku sequence
    console.log("\n\n2. HAIKU SEQUENCE FROM STEADFAST ARCHETYPE");
    console.log("-".repeat(40));
    const sequence = engine.generateHaikuSequence("Steadfast", 3);
    sequence.forEach((h, i) => {
        console.log(`\n${i+1}.`);
        console.log(h);
    });
    
    // Generate free verse
    console.log("\n\n3. FREE VERSE FROM PIONEER ARCHETYPE");
    console.log("-".repeat(40));
    const verse = engine.generateFreeVerse("Pioneer", 8);
    console.log(verse);
    
    // Generate complete poem with metadata
    console.log("\n\n4. COMPLETE POEM WITH METADATA");
    console.log("-".repeat(40));
    const result = engine.generatePoem({
        archetype: "Ecstatic",
        form: "free_verse",
        mood: "passionate",
        keyImages: ["fire", "stars", "ashes"],
        title: "Fire Song"
    });
    console.log(`\nTitle: ${result.title}`);
    console.log(`\n${result.text}`);
    console.log(`\nMetadata:`, result.metadata);
    
    // Show example poem
    console.log("\n\n5. EXAMPLE POEM: WINTER HAIKU");
    console.log("-".repeat(40));
    const example = getExamplePoem("winter_haiku");
    console.log(example.text);
    
    console.log("\n" + "=".repeat(60));
    console.log("6 bits. 64 archetypes. Infinite poems. 🧂");
    console.log("=".repeat(60));
}


// Run demo if this file is executed directly in Node.js
if (typeof require !== 'undefined' && require.main === module) {
    demoPoetryEngine();
}
