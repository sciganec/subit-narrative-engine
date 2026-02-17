/**
 * SUBIT Narrative Engine
 * 6 bits = 64 archetypes = infinite stories
 * 
 * A formal system for generating narratives based on archetypal transmutations.
 */

// ============================================================================
// 1. ENUMS AND CONSTANTS
// ============================================================================

const WHO = Object.freeze({
    ME: "ME",      // 10 — individual, first person
    WE: "WE",      // 11 — collective, first person plural
    YOU: "YOU",    // 01 — second person, dialogic
    THEY: "THEY"   // 00 — third person, impersonal
});

const WHERE = Object.freeze({
    EAST: "EAST",      // 10 — beginning, initiation, sunrise
    SOUTH: "SOUTH",    // 11 — passion, emotion, fire
    WEST: "WEST",      // 01 — structure, order, sunset
    NORTH: "NORTH"     // 00 — reflection, wisdom, cold
});

const WHEN = Object.freeze({
    SPRING: "SPRING",  // 10 — beginning, hope, birth
    SUMMER: "SUMMER",  // 11 — peak, action, fulfillment
    AUTUMN: "AUTUMN",  // 01 — decline, harvest, reflection
    WINTER: "WINTER"   // 00 — end, death, potential
});


// ============================================================================
// 2. BIT ENCODING TABLES
// ============================================================================

const WHO_ENCODE = {
    [WHO.ME]: "10",
    [WHO.WE]: "11",
    [WHO.YOU]: "01",
    [WHO.THEY]: "00"
};

const WHO_DECODE = {
    "10": WHO.ME,
    "11": WHO.WE,
    "01": WHO.YOU,
    "00": WHO.THEY
};

const WHERE_ENCODE = {
    [WHERE.EAST]: "10",
    [WHERE.SOUTH]: "11",
    [WHERE.WEST]: "01",
    [WHERE.NORTH]: "00"
};

const WHERE_DECODE = {
    "10": WHERE.EAST,
    "11": WHERE.SOUTH,
    "01": WHERE.WEST,
    "00": WHERE.NORTH
};

const WHEN_ENCODE = {
    [WHEN.SPRING]: "10",
    [WHEN.SUMMER]: "11",
    [WHEN.AUTUMN]: "01",
    [WHEN.WINTER]: "00"
};

const WHEN_DECODE = {
    "10": WHEN.SPRING,
    "11": WHEN.SUMMER,
    "01": WHEN.AUTUMN,
    "00": WHEN.WINTER
};


// ============================================================================
// 3. CORE DATA STRUCTURES
// ============================================================================

/**
 * Archetype class — a 6-bit archetypal state
 */
class Archetype {
    /**
     * Create a new archetype
     * @param {string} who - WHO value (ME, WE, YOU, THEY)
     * @param {string} where - WHERE value (EAST, SOUTH, WEST, NORTH)
     * @param {string} when - WHEN value (SPRING, SUMMER, AUTUMN, WINTER)
     */
    constructor(who, where, when) {
        this.who = who;
        this.where = where;
        this.when = when;
    }
    
    /**
     * Get 6-bit representation with spaces (for readability)
     * @returns {string}
     */
    get bits() {
        return `${WHO_ENCODE[this.who]} ${WHERE_ENCODE[this.where]} ${WHEN_ENCODE[this.when]}`;
    }
    
    /**
     * Get compact 6-bit string without spaces (for computation)
     * @returns {string}
     */
    get binary() {
        return this.bits.replace(/ /g, '');
    }
    
    /**
     * Get integer value of the 6-bit string (0-63)
     * @returns {number}
     */
    get intValue() {
        return parseInt(this.binary, 2);
    }
    
    /**
     * Get canonical name of this archetype
     * @returns {string}
     */
    get name() {
        return ARCHETYPE_NAMES[this.bits] || "Unknown";
    }
    
    /**
     * XOR operation between two archetypes
     * This is the fundamental operation of the SUBIT system
     * @param {Archetype} other
     * @returns {Archetype}
     */
    xor(other) {
        if (!(other instanceof Archetype)) {
            throw new Error("XOR operation requires another Archetype");
        }
        
        // XOR the integer values
        const resultInt = this.intValue ^ other.intValue;
        
        // Convert back to binary
        const resultBin = resultInt.toString(2).padStart(6, '0');
        
        // Parse into components
        const whoBits = resultBin.substring(0, 2);
        const whereBits = resultBin.substring(2, 4);
        const whenBits = resultBin.substring(4, 6);
        
        return new Archetype(
            WHO_DECODE[whoBits],
            WHERE_DECODE[whereBits],
            WHEN_DECODE[whenBits]
        );
    }
    
    /**
     * Alias for xor method
     * @param {Archetype} other
     * @returns {Archetype}
     */
    _xor(other) {
        return this.xor(other);
    }
    
    /**
     * Check equality with another archetype
     * @param {Archetype} other
     * @returns {boolean}
     */
    equals(other) {
        if (!(other instanceof Archetype)) return false;
        return this.bits === other.bits;
    }
    
    /**
     * Convert to string representation
     * @returns {string}
     */
    toString() {
        return `[${this.who}, ${this.where}, ${this.when}]`;
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            who: this.who,
            where: this.where,
            when: this.when,
            bits: this.bits,
            binary: this.binary,
            int: this.intValue,
            name: this.name
        };
    }
    
    /**
     * Create archetype from 6-bit string
     * @param {string} bits - 6-bit string (with or without spaces)
     * @returns {Archetype}
     */
    static fromBits(bits) {
        const clean = bits.replace(/ /g, '');
        if (clean.length !== 6) {
            throw new Error(`Expected 6 bits, got ${clean.length}: ${bits}`);
        }
        
        const whoBits = clean.substring(0, 2);
        const whereBits = clean.substring(2, 4);
        const whenBits = clean.substring(4, 6);
        
        return new Archetype(
            WHO_DECODE[whoBits],
            WHERE_DECODE[whereBits],
            WHEN_DECODE[whenBits]
        );
    }
    
    /**
     * Create archetype from integer 0-63
     * @param {number} value - Integer between 0 and 63
     * @returns {Archetype}
     */
    static fromInt(value) {
        if (value < 0 || value > 63) {
            throw new Error(`Expected 0-63, got ${value}`);
        }
        const bits = value.toString(2).padStart(6, '0');
        return Archetype.fromBits(bits);
    }
}


/**
 * Character class — a character with an archetypal state
 */
class Character {
    /**
     * Create a new character
     * @param {string} name
     * @param {Archetype} currentState
     * @param {string} background
     * @param {Object} attributes
     */
    constructor(name, currentState, background, attributes = {}) {
        this.name = name;
        this.currentState = currentState;
        this.background = background;
        this.attributes = attributes;
    }
    
    /**
     * Apply transmutation to character
     * @param {Archetype} impulse
     * @param {Archetype} catalyst
     * @returns {Character} New character with updated state
     */
    transmute(impulse, catalyst) {
        const newState = this.currentState.xor(impulse).xor(catalyst);
        const newAttrs = { ...this.attributes };
        newAttrs.previousState = this.currentState.bits;
        newAttrs.impulse = impulse.bits;
        newAttrs.catalyst = catalyst.bits;
        
        return new Character(
            this.name,
            newState,
            this.background,
            newAttrs
        );
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            name: this.name,
            currentState: this.currentState.toJSON(),
            background: this.background,
            attributes: this.attributes
        };
    }
}


/**
 * Event class — a plot event representing a state change
 */
class Event {
    /**
     * Create a new event
     * @param {string} eventType - "WHO", "WHERE", "WHEN", or combination
     * @param {string} description
     * @param {Archetype} previousState
     * @param {Archetype} newState
     * @param {number} significance - 0.0 to 1.0
     */
    constructor(eventType, description, previousState, newState, significance) {
        this.eventType = eventType;
        this.description = description;
        this.previousState = previousState;
        this.newState = newState;
        this.significance = significance;
    }
    
    /**
     * Get bits that changed (1 = changed)
     * @returns {string}
     */
    get bitsChanged() {
        const prevInt = this.previousState.intValue;
        const newInt = this.newState.intValue;
        const changed = prevInt ^ newInt;
        return changed.toString(2).padStart(6, '0');
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            eventType: this.eventType,
            description: this.description,
            previousState: this.previousState.bits,
            newState: this.newState.bits,
            bitsChanged: this.bitsChanged,
            significance: this.significance
        };
    }
}


/**
 * NarrativeArc class — a complete character arc
 */
class NarrativeArc {
    /**
     * Create a new narrative arc
     * @param {Character} protagonist
     * @param {Archetype} initialState
     * @param {Archetype} finalState
     * @param {Event[]} plotPoints
     */
    constructor(protagonist, initialState, finalState, plotPoints = []) {
        this.protagonist = protagonist;
        this.initialState = initialState;
        this.finalState = finalState;
        this.plotPoints = plotPoints;
    }
    
    /**
     * Check if arc reaches final state
     * @returns {boolean}
     */
    get isComplete() {
        return this.protagonist.currentState.equals(this.finalState);
    }
    
    /**
     * Calculate dramatic tension (0-1) based on maximum bit change
     * @returns {number}
     */
    get dramaticTension() {
        if (this.plotPoints.length === 0) return 0.0;
        
        let maxTension = 0.0;
        for (const event of this.plotPoints) {
            const bits = event.bitsChanged;
            const tension = (bits.match(/1/g) || []).length / 6.0;
            maxTension = Math.max(maxTension, tension);
        }
        
        return maxTension;
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            protagonist: this.protagonist.toJSON(),
            initialState: this.initialState.bits,
            finalState: this.finalState.bits,
            plotPoints: this.plotPoints.map(e => e.toJSON()),
            dramaticTension: this.dramaticTension,
            isComplete: this.isComplete
        };
    }
}


/**
 * StoryWorld class — the world in which the story takes place
 */
class StoryWorld {
    /**
     * Create a new story world
     * @param {string} setting
     * @param {Archetype} dominantArchetype
     * @param {Object} rules
     */
    constructor(setting, dominantArchetype, rules = {}) {
        this.setting = setting;
        this.dominantArchetype = dominantArchetype;
        this.rules = rules;
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            setting: this.setting,
            dominantArchetype: this.dominantArchetype.bits,
            rules: this.rules
        };
    }
}


/**
 * Story class — a complete generated story
 */
class Story {
    /**
     * Create a new story
     * @param {string} title
     * @param {string} text
     * @param {NarrativeArc} arc
     * @param {StoryWorld} world
     * @param {Object} metadata
     */
    constructor(title, text, arc, world, metadata = {}) {
        this.title = title;
        this.text = text;
        this.arc = arc;
        this.world = world;
        this.metadata = metadata;
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            title: this.title,
            text: this.text,
            arc: this.arc.toJSON(),
            world: this.world.toJSON(),
            metadata: this.metadata
        };
    }
}


// ============================================================================
// 4. ARCHETYPE CATALOG (64 ARCHETYPES)
// ============================================================================

const ARCHETYPE_NAMES = {
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
};


/**
 * ArchetypeCatalog class — access to the 64 archetypes
 */
class ArchetypeCatalog {
    constructor() {
        this.archetypes = {};
        this._buildCatalog();
    }
    
    _buildCatalog() {
        for (const [bits, name] of Object.entries(ARCHETYPE_NAMES)) {
            const archetype = Archetype.fromBits(bits);
            
            // Generate key qualities based on axes
            const keyQualities = this._generateKeyQualities(archetype);
            
            this.archetypes[bits] = {
                name,
                archetype,
                bits,
                binary: archetype.binary,
                int: archetype.intValue,
                who: archetype.who,
                where: archetype.where,
                when: archetype.when,
                key: keyQualities,
                description: this._generateDescription(archetype, name, keyQualities)
            };
        }
    }
    
    _generateKeyQualities(a) {
        const whoMap = {
            [WHO.ME]: "individual, personal",
            [WHO.WE]: "collective, shared",
            [WHO.YOU]: "relational, dialogic",
            [WHO.THEY]: "impersonal, systemic"
        };
        
        const whereMap = {
            [WHERE.EAST]: "beginning, initiation",
            [WHERE.SOUTH]: "passion, emotion",
            [WHERE.WEST]: "structure, order",
            [WHERE.NORTH]: "reflection, wisdom"
        };
        
        const whenMap = {
            [WHEN.SPRING]: "hope, birth",
            [WHEN.SUMMER]: "peak, action",
            [WHEN.AUTUMN]: "harvest, decline",
            [WHEN.WINTER]: "end, potential"
        };
        
        return `${whoMap[a.who]}, ${whereMap[a.where]}, ${whenMap[a.when]}`;
    }
    
    _generateDescription(a, name, key) {
        const templates = {
            "Pioneer": "The one who sets out first. Unburdened by experience, driven by vision.",
            "Steadfast": "One who has endured loss and frozen in their suffering.",
            "Ghost": "That which comes from outside. The unexpected visitor.",
            "Beloved": "The one who is loved and who therefore can speak truth.",
            "Council": "The new community born from transformed suffering.",
            "Zero": "The primordial state before manifestation. Pure potential."
        };
        
        return templates[name] || `A being embodying ${key}.`;
    }
    
    /**
     * Get metadata for an archetype
     * @param {Archetype|string} archetype
     * @returns {Object}
     */
    get(archetype) {
        let key;
        if (archetype instanceof Archetype) {
            key = archetype.bits;
        } else {
            key = archetype;
        }
        return this.archetypes[key] || {};
    }
    
    /**
     * Find archetype by name
     * @param {string} name
     * @returns {Archetype|null}
     */
    getByName(name) {
        for (const [bits, data] of Object.entries(this.archetypes)) {
            if (data.name.toLowerCase() === name.toLowerCase()) {
                return data.archetype;
            }
        }
        return null;
    }
    
    /**
     * Get all archetypes
     * @returns {Archetype[]}
     */
    all() {
        return Object.values(this.archetypes).map(data => data.archetype);
    }
    
    /**
     * Get all archetype metadata
     * @returns {Object[]}
     */
    allDicts() {
        return Object.values(this.archetypes);
    }
    
    /**
     * Get a random archetype
     * @returns {Archetype}
     */
    random() {
        const all = this.all();
        return all[Math.floor(Math.random() * all.length)];
    }
}


// ============================================================================
// 5. TRANSMUTATION CATALOG (12 MASTER FORMULAS)
// ============================================================================

/**
 * TransmutationFormula class — a master transmutation formula
 */
class TransmutationFormula {
    /**
     * Create a new transmutation formula
     * @param {string} name
     * @param {Archetype} initial
     * @param {Archetype} impulse
     * @param {Archetype} catalyst
     * @param {Archetype} result
     * @param {string} description
     */
    constructor(name, initial, impulse, catalyst, result, description) {
        this.name = name;
        this.initial = initial;
        this.impulse = impulse;
        this.catalyst = catalyst;
        this.result = result;
        this.description = description;
    }
    
    /**
     * Verify that the formula is mathematically correct
     * @returns {boolean}
     */
    verify() {
        const computed = this.initial.xor(this.impulse).xor(this.catalyst);
        return computed.equals(this.result);
    }
    
    /**
     * Convert to object for serialization
     * @returns {Object}
     */
    toJSON() {
        return {
            name: this.name,
            initial: this.initial.bits,
            impulse: this.impulse.bits,
            catalyst: this.catalyst.bits,
            result: this.result.bits,
            description: this.description,
            verified: this.verify()
        };
    }
}


/**
 * TransmutationCatalog class — access to master formulas
 */
class TransmutationCatalog {
    constructor() {
        this.formulas = [];
        this._buildFormulas();
    }
    
    /**
     * Helper to create archetypes
     * @private
     */
    _a(who, where, when) {
        return new Archetype(who, where, when);
    }
    
    _buildFormulas() {
        this.formulas = [
            // 1. Philosopher's Stone
            new TransmutationFormula(
                "Philosopher's Stone",
                this._a(WHO.ME, WHERE.SOUTH, WHEN.WINTER),
                this._a(WHO.THEY, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.YOU, WHERE.NORTH, WHEN.AUTUMN),
                this._a(WHO.WE, WHERE.WEST, WHEN.SUMMER),
                "Personal longing becomes collective achievement"
            ),
            
            // 2. Hero's Journey
            new TransmutationFormula(
                "Hero's Journey",
                this._a(WHO.ME, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.THEY, WHERE.SOUTH, WHEN.WINTER),
                this._a(WHO.WE, WHERE.WEST, WHEN.SUMMER),
                this._a(WHO.YOU, WHERE.NORTH, WHEN.SPRING),
                "Innocence confronts shadow, returns with wisdom"
            ),
            
            // 3. Alchemical Marriage
            new TransmutationFormula(
                "Alchemical Marriage",
                this._a(WHO.ME, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.YOU, WHERE.NORTH, WHEN.AUTUMN),
                this._a(WHO.WE, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.THEY, WHERE.WEST, WHEN.WINTER),
                "Union of opposites returns to the source"
            ),
            
            // 4. Creative Process
            new TransmutationFormula(
                "Creative Process",
                this._a(WHO.ME, WHERE.NORTH, WHEN.WINTER),
                this._a(WHO.THEY, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.YOU, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.WE, WHERE.WEST, WHEN.AUTUMN),
                "Solitude + inspiration + mastery = shared creation"
            ),
            
            // 5. Healing
            new TransmutationFormula(
                "Healing",
                this._a(WHO.ME, WHERE.WEST, WHEN.WINTER),
                this._a(WHO.THEY, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.YOU, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.WE, WHERE.NORTH, WHEN.AUTUMN),
                "Isolation + collective energy + mediator = integration"
            ),
            
            // 6. Revelation
            new TransmutationFormula(
                "Revelation",
                this._a(WHO.THEY, WHERE.NORTH, WHEN.WINTER),
                this._a(WHO.ME, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.WE, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.YOU, WHERE.WEST, WHEN.AUTUMN),
                "From void, through seeking and communion, wisdom emerges"
            ),
            
            // 7. Power Transformation
            new TransmutationFormula(
                "Power Transformation",
                this._a(WHO.ME, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.THEY, WHERE.WEST, WHEN.AUTUMN),
                this._a(WHO.YOU, WHERE.NORTH, WHEN.SPRING),
                this._a(WHO.WE, WHERE.EAST, WHEN.WINTER),
                "Individual power becomes collective guardianship"
            ),
            
            // 8. Dark Night
            new TransmutationFormula(
                "Dark Night",
                this._a(WHO.WE, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.THEY, WHERE.WEST, WHEN.AUTUMN),
                this._a(WHO.YOU, WHERE.EAST, WHEN.WINTER),
                this._a(WHO.ME, WHERE.NORTH, WHEN.SPRING),
                "Community joy, through crisis, retreats to potential"
            ),
            
            // 9. Awakening
            new TransmutationFormula(
                "Awakening",
                this._a(WHO.ME, WHERE.NORTH, WHEN.AUTUMN),
                this._a(WHO.THEY, WHERE.SOUTH, WHEN.SPRING),
                this._a(WHO.WE, WHERE.EAST, WHEN.SUMMER),
                this._a(WHO.YOU, WHERE.WEST, WHEN.WINTER),
                "Old patterns shattered by force become witness"
            ),
            
            // 10. Renewal
            new TransmutationFormula(
                "Renewal",
                this._a(WHO.THEY, WHERE.NORTH, WHEN.AUTUMN),
                this._a(WHO.ME, WHERE.SOUTH, WHEN.WINTER),
                this._a(WHO.WE, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.YOU, WHERE.WEST, WHEN.SUMMER),
                "Unrealized possibilities + endurance = catharsis"
            ),
            
            // 11. Reconciliation
            new TransmutationFormula(
                "Reconciliation",
                this._a(WHO.ME, WHERE.WEST, WHEN.AUTUMN),
                this._a(WHO.THEY, WHERE.EAST, WHEN.SUMMER),
                this._a(WHO.YOU, WHERE.NORTH, WHEN.WINTER),
                this._a(WHO.WE, WHERE.SOUTH, WHEN.SPRING),
                "Judgment + higher perspective + love = renewed union"
            ),
            
            // 12. Complete Transmutation
            new TransmutationFormula(
                "Complete Transmutation",
                this._a(WHO.ME, WHERE.EAST, WHEN.SPRING),
                this._a(WHO.WE, WHERE.SOUTH, WHEN.SUMMER),
                this._a(WHO.YOU, WHERE.WEST, WHEN.AUTUMN),
                this._a(WHO.THEY, WHERE.NORTH, WHEN.WINTER),
                "The three active pillars return to the source"
            )
        ];
        
        // Verify all formulas
        for (const f of this.formulas) {
            if (!f.verify()) {
                console.warn(`Formula ${f.name} failed verification`);
            }
        }
    }
    
    /**
     * Get all formulas
     * @returns {TransmutationFormula[]}
     */
    all() {
        return this.formulas;
    }
    
    /**
     * Find formula by name
     * @param {string} name
     * @returns {TransmutationFormula|null}
     */
    findByName(name) {
        return this.formulas.find(f => f.name.toLowerCase() === name.toLowerCase()) || null;
    }
    
    /**
     * Find formulas matching initial and result
     * @param {Archetype} initial
     * @param {Archetype} result
     * @returns {TransmutationFormula[]}
     */
    findByInitialResult(initial, result) {
        return this.formulas.filter(f => 
            f.initial.equals(initial) && f.result.equals(result)
        );
    }
}


// Predefined instances for common use
const ZERO = new Archetype(WHO.THEY, WHERE.NORTH, WHEN.WINTER);      // 00 00 00
const PIONEER = new Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING);     // 10 10 10
const CONCILIAR = new Archetype(WHO.WE, WHERE.SOUTH, WHEN.SUMMER);  // 11 11 11
const CONFESSOR = new Archetype(WHO.YOU, WHERE.WEST, WHEN.AUTUMN);  // 01 01 01
const STEADFAST = new Archetype(WHO.ME, WHERE.SOUTH, WHEN.WINTER);  // 10 11 00
const GHOST = new Archetype(WHO.THEY, WHERE.EAST, WHEN.SPRING);     // 00 10 10
const BELOVED = new Archetype(WHO.YOU, WHERE.NORTH, WHEN.AUTUMN);   // 01 00 01
const COUNCIL = new Archetype(WHO.WE, WHERE.WEST, WHEN.SUMMER);     // 11 01 11

// The Philosopher's Stone formula
const PHILOSOPHER_STONE = new TransmutationFormula(
    "Philosopher's Stone",
    STEADFAST,
    GHOST,
    BELOVED,
    COUNCIL,
    "Personal longing becomes collective achievement"
);


// ============================================================================
// 6. UTILITY FUNCTIONS
// ============================================================================

/**
 * Calculate Hamming distance between two archetypes
 * @param {Archetype} a
 * @param {Archetype} b
 * @returns {number}
 */
function hammingDistance(a, b) {
    const aBits = a.binary;
    const bBits = b.binary;
    let distance = 0;
    for (let i = 0; i < 6; i++) {
        if (aBits[i] !== bBits[i]) distance++;
    }
    return distance;
}

/**
 * Find possible transmutation paths from start to end
 * Simplified version for JavaScript
 * @param {Archetype} start
 * @param {Archetype} end
 * @param {number} maxSteps
 * @returns {Array}
 */
function findPath(start, end, maxSteps = 3) {
    // Simple implementation - returns direct XOR difference
    const required = start.xor(end);
    const paths = [];
    
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const impulse = Archetype.fromInt(i * 8);
            const catalyst = Archetype.fromInt(j * 8);
            if (impulse.xor(catalyst).equals(required)) {
                paths.push([[impulse, catalyst]]);
            }
        }
    }
    
    return paths.slice(0, 5); // Return first 5 paths
}

/**
 * Analyze a transmutation between two states
 * @param {Archetype} initial
 * @param {Archetype} result
 * @returns {Object}
 */
function analyzeTransmutation(initial, result) {
    const required = initial.xor(result);
    
    const analysis = {
        initial: initial.bits,
        result: result.bits,
        requiredChange: required.bits,
        bitsChanged: hammingDistance(initial, result),
        axisChanges: {
            WHO: initial.who !== result.who,
            WHERE: initial.where !== result.where,
            WHEN: initial.when !== result.when
        },
        possibleCatalysts: []
    };
    
    // Find sample possible catalysts
    for (let i = 0; i < 64; i += 4) {
        const catalyst = Archetype.fromInt(i);
        const impulse = required.xor(catalyst);
        analysis.possibleCatalysts.push({
            catalyst: catalyst.bits,
            catalystName: catalyst.name,
            impulse: impulse.bits,
            impulseName: impulse.name
        });
    }
    
    return analysis;
}

/**
 * Convert bits to integer
 * @param {string} bits
 * @returns {number}
 */
function bitsToInt(bits) {
    const clean = bits.replace(/ /g, '');
    return parseInt(clean, 2);
}

/**
 * Convert integer to bits
 * @param {number} value
 * @returns {string}
 */
function intToBits(value) {
    return value.toString(2).padStart(6, '0');
}

/**
 * Convert archetype name to Archetype object
 * @param {string} name
 * @returns {Archetype|null}
 */
function nameToArchetype(name) {
    const catalog = new ArchetypeCatalog();
    return catalog.getByName(name);
}


// ============================================================================
// 7. GENERATOR CLASSES
// ============================================================================

/**
 * CharacterGenerator class — generate characters from archetypes
 */
class CharacterGenerator {
    constructor(catalog) {
        this.catalog = catalog;
        
        // Name pools by archetype
        this.namePools = {
            [WHO.ME]: ["Luca", "Mara", "Eli", "Nova", "Orion", "Sage", "Luna", "Kai"],
            [WHO.WE]: ["The People", "The Community", "The Tribe", "The Fellowship"],
            [WHO.YOU]: ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Morgan"],
            [WHO.THEY]: ["The Stranger", "The Voice", "The Force", "The System"]
        };
        
        // Background templates by archetype
        this.backgroundTemplates = {
            [`${WHO.ME},${WHERE.NORTH}`]: "lived alone in the mountains for as long as they can remember",
            [`${WHO.ME},${WHERE.SOUTH}`]: "carries a fire inside that never goes out",
            [`${WHO.ME},${WHERE.EAST}`]: "stands at the threshold of something new",
            [`${WHO.ME},${WHERE.WEST}`]: "has built their life with precision and care",
            [`${WHO.WE},${WHERE.NORTH}`]: "a community bound by shared silence",
            [`${WHO.WE},${WHERE.SOUTH}`]: "a people who feel everything together",
            [`${WHO.WE},${WHERE.EAST}`]: "a tribe on the edge of becoming",
            [`${WHO.WE},${WHERE.WEST}`]: "a society held together by laws and customs",
            [`${WHO.YOU},${WHERE.NORTH}`]: "known for their wisdom and counsel",
            [`${WHO.YOU},${WHERE.SOUTH}`]: "loved deeply by all who meet them",
            [`${WHO.YOU},${WHERE.EAST}`]: "appears when least expected",
            [`${WHO.YOU},${WHERE.WEST}`]: "speaks with clarity and precision",
            [`${WHO.THEY},${WHERE.NORTH}`]: "an impersonal force, like the weather",
            [`${WHO.THEY},${WHERE.SOUTH}`]: "a passion that sweeps through crowds",
            [`${WHO.THEY},${WHERE.EAST}`]: "news from far away",
            [`${WHO.THEY},${WHERE.WEST}`]: "the way things are done"
        };
    }
    
    /**
     * Generate a character from an archetype
     * @param {Archetype} archetype
     * @param {string|null} seed
     * @param {string|null} name
     * @returns {Character}
     */
    generate(archetype, seed = null, name = null) {
        if (seed) {
            // Simple seed-based randomization
            const seedNum = seed.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
            this._random = this._seededRandom(seedNum);
        } else {
            this._random = Math.random;
        }
        
        const metadata = this.catalog.get(archetype);
        
        // Generate name
        let charName;
        if (name) {
            charName = name;
        } else {
            const pool = this.namePools[archetype.who] || ["Alex"];
            charName = pool[Math.floor(this._random() * pool.length)];
            if (archetype.who === WHO.WE) {
                charName = `${charName} of ${archetype.name}`;
            }
        }
        
        // Generate background
        const templateKey = `${archetype.who},${archetype.where}`;
        let backgroundTemplate = this.backgroundTemplates[templateKey] ||
            "exists in a state of being";
        
        // Add temporal aspect
        const whenDesc = {
            [WHEN.SPRING]: "just beginning",
            [WHEN.SUMMER]: "at their peak",
            [WHEN.AUTUMN]: "in a time of reflection",
            [WHEN.WINTER]: "waiting"
        }[archetype.when];
        
        const background = `${charName} ${backgroundTemplate}, ${whenDesc}.`;
        
        // Derive attributes
        const attributes = {
            motivation: this._deriveMotivation(archetype),
            fear: this._deriveFear(archetype),
            desire: this._deriveDesire(archetype),
            archetypeName: metadata.name || "Unknown",
            keyPhrase: metadata.key || ""
        };
        
        return new Character(
            charName,
            archetype,
            background,
            attributes
        );
    }
    
    _seededRandom(seed) {
        return function() {
            seed = (seed * 9301 + 49297) % 233280;
            return seed / 233280;
        };
    }
    
    _deriveMotivation(a) {
        const motivations = {
            [`${WHO.ME},${WHEN.SPRING}`]: "To begin something new",
            [`${WHO.ME},${WHEN.SUMMER}`]: "To achieve greatness",
            [`${WHO.ME},${WHEN.AUTUMN}`]: "To understand what was lost",
            [`${WHO.ME},${WHEN.WINTER}`]: "To endure, to survive",
            [`${WHO.WE},${WHEN.SPRING}`]: "To build together",
            [`${WHO.WE},${WHEN.SUMMER}`]: "To celebrate what they've built",
            [`${WHO.WE},${WHEN.AUTUMN}`]: "To preserve their way of life",
            [`${WHO.WE},${WHEN.WINTER}`]: "To wait together",
            [`${WHO.YOU},${WHEN.SPRING}`]: "To help someone begin",
            [`${WHO.YOU},${WHEN.SUMMER}`]: "To guide someone to fulfillment",
            [`${WHO.YOU},${WHEN.AUTUMN}`]: "To help someone understand",
            [`${WHO.YOU},${WHEN.WINTER}`]: "To be present with someone",
            [`${WHO.THEY},${WHEN.SPRING}`]: "To announce what's coming",
            [`${WHO.THEY},${WHEN.SUMMER}`]: "To sweep through",
            [`${WHO.THEY},${WHEN.AUTUMN}`]: "To harvest what was sown",
            [`${WHO.THEY},${WHEN.WINTER}`]: "To be the silence"
        };
        return motivations[`${a.who},${a.when}`] || "To find meaning";
    }
    
    _deriveFear(a) {
        const fears = {
            [WHERE.EAST]: "Fear of never beginning",
            [WHERE.SOUTH]: "Fear of being consumed",
            [WHERE.WEST]: "Fear of chaos, of losing control",
            [WHERE.NORTH]: "Fear of emptiness, of meaninglessness"
        };
        return fears[a.where] || "Fear of the unknown";
    }
    
    _deriveDesire(a) {
        const desires = {
            [WHEN.SPRING]: "Desire for new possibilities",
            [WHEN.SUMMER]: "Desire for fulfillment",
            [WHEN.AUTUMN]: "Desire to understand",
            [WHEN.WINTER]: "Desire for rest"
        };
        return desires[a.when] || "Desire for change";
    }
}


/**
 * WorldGenerator class — generate story worlds from archetypes
 */
class WorldGenerator {
    constructor(catalog) {
        this.catalog = catalog;
    }
    
    /**
     * Generate a world dominated by an archetype
     * @param {Archetype} dominant
     * @returns {StoryWorld}
     */
    generate(dominant) {
        const setting = this._generateSetting(dominant);
        const rules = this._deriveWorldRules(dominant);
        
        return new StoryWorld(
            setting,
            dominant,
            rules
        );
    }
    
    _generateSetting(a) {
        const whereTemplates = {
            [WHERE.EAST]: "a frontier, a place of beginnings, where the old world ends",
            [WHERE.SOUTH]: "a land of passion and fire, where emotions run high",
            [WHERE.WEST]: "a structured society, with laws and order, where everything has its place",
            [WHERE.NORTH]: "a cold, reflective place, of isolation and deep thought"
        };
        
        const whenTemplates = {
            [WHEN.SPRING]: "in a time of hope and new beginnings",
            [WHEN.SUMMER]: "at the height of power and glory",
            [WHEN.AUTUMN]: "in an age of decline and reflection",
            [WHEN.WINTER]: "in a dark age, where memory fades"
        };
        
        const whoTemplates = {
            [WHO.ME]: "where individuals matter more than the collective",
            [WHO.WE]: "where community is everything",
            [WHO.YOU]: "where relationships and dialogue shape all",
            [WHO.THEY]: "where impersonal forces govern life"
        };
        
        return `The story takes place in ${whereTemplates[a.where]}, ` +
               `${whenTemplates[a.when]}, ` +
               `${whoTemplates[a.who]}.`;
    }
    
    _deriveWorldRules(a) {
        return {
            magicSystem: this._deriveMagic(a),
            socialStructure: this._deriveSocial(a),
            cosmicPrinciple: this._deriveCosmic(a)
        };
    }
    
    _deriveMagic(a) {
        const whereMagic = {
            [WHERE.EAST]: "magic of beginnings, of potential",
            [WHERE.SOUTH]: "emotional magic, fire, passion",
            [WHERE.WEST]: "structured magic, formulas, precision",
            [WHERE.NORTH]: "mental magic, telepathy, prophecy"
        };
        return whereMagic[a.where] || "subtle, almost imperceptible magic";
    }
    
    _deriveSocial(a) {
        const whoSocial = {
            [WHO.ME]: "individualistic, merit-based, often lonely",
            [WHO.WE]: "collectivist, communal, clan-based",
            [WHO.YOU]: "relational, dialogue-focused, therapeutic",
            [WHO.THEY]: "bureaucratic, impersonal, system-driven"
        };
        return whoSocial[a.who] || "complex and layered";
    }
    
    _deriveCosmic(a) {
        const whenCosmic = {
            [WHEN.SPRING]: "the universe is becoming, unfolding",
            [WHEN.SUMMER]: "the universe is at its peak, fully manifest",
            [WHEN.AUTUMN]: "the universe is declining, returning to source",
            [WHEN.WINTER]: "the universe is latent, potential, waiting"
        };
        return whenCosmic[a.when] || "cyclical, ever-turning";
    }
}


/**
 * PlotGenerator class — generate plot points from transmutations
 */
class PlotGenerator {
    constructor(characterGen, worldGen, transmutationCatalog) {
        this.characterGen = characterGen;
        this.worldGen = worldGen;
        this.transmutations = transmutationCatalog;
        
        // Event description templates
        this.eventTemplates = {
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
        };
        
        // Specific templates for known archetypes
        this.specificTemplates = {
            [GHOST.bits]: " as a stranger arrives from the east",
            [BELOVED.bits]: " through the words of one who truly sees them",
            [PIONEER.bits]: " and they feel the pull of something new",
            [STEADFAST.bits]: " though they try to hold on",
            [COUNCIL.bits]: " and they are no longer alone"
        };
    }
    
    /**
     * Generate a narrative arc
     * @param {Archetype} initial
     * @param {Archetype} target
     * @param {string|null} protagonistName
     * @param {number} complexity
     * @returns {NarrativeArc}
     */
    generateArc(initial, target, protagonistName = null, complexity = 3) {
        // Generate protagonist
        const protagonist = this.characterGen.generate(
            initial,
            protagonistName,
            protagonistName
        );
        
        // Calculate required change
        const requiredChange = initial.xor(target);
        
        // Decompose into steps
        const steps = this._decomposeChange(requiredChange, complexity);
        
        // Generate plot points
        const plotPoints = [];
        let current = initial;
        
        for (let i = 0; i < steps.length; i++) {
            const [impulseBits, catalystBits] = steps[i];
            const impulse = Archetype.fromBits(impulseBits);
            const catalyst = Archetype.fromBits(catalystBits);
            
            // Generate event
            const event = this._generateEvent(
                current, impulse, catalyst, i + 1
            );
            plotPoints.push(event);
            
            // Update current state
            current = current.xor(impulse).xor(catalyst);
        }
        
        // Verify we reached target (approximately)
        if (!current.equals(target) && plotPoints.length > 0) {
            // Fallback: adjust last step
            const lastEvent = plotPoints[plotPoints.length - 1];
            lastEvent.newState = target;
        }
        
        return new NarrativeArc(
            protagonist,
            initial,
            target,
            plotPoints
        );
    }
    
    _decomposeChange(requiredChange, complexity) {
        const requiredInt = requiredChange.intValue;
        const steps = [];
        
        if (complexity === 1 || requiredInt === 0) {
            // Single step
            const impulseInt = Math.floor(Math.random() * 64);
            const catalystInt = requiredInt ^ impulseInt;
            return [[intToBits(impulseInt), intToBits(catalystInt)]];
        }
        
        // Simple decomposition
        if (requiredInt < 8) {
            const impulseInt = Math.floor(Math.random() * 8);
            const catalystInt = requiredInt ^ impulseInt;
            steps.push([intToBits(impulseInt), intToBits(catalystInt)]);
            return steps;
        }
        
        // Two steps
        const step1Int = Math.floor(Math.random() * 16) + 1;
        const step2Int = requiredInt ^ step1Int;
        
        const impulse1 = Math.floor(Math.random() * 64);
        const catalyst1 = step1Int ^ impulse1;
        steps.push([intToBits(impulse1), intToBits(catalyst1)]);
        
        const impulse2 = Math.floor(Math.random() * 64);
        const catalyst2 = step2Int ^ impulse2;
        steps.push([intToBits(impulse2), intToBits(catalyst2)]);
        
        return steps.slice(0, complexity);
    }
    
    _generateEvent(current, impulse, catalyst, stepNumber) {
        const newState = current.xor(impulse).xor(catalyst);
        
        // Determine which axes changed
        const changed = [];
        if (current.who !== newState.who) changed.push("WHO");
        if (current.where !== newState.where) changed.push("WHERE");
        if (current.when !== newState.when) changed.push("WHEN");
        
        const changedKey = changed.length > 0 ? changed.join(",") : "None";
        
        // Get base description
        let templates = this.eventTemplates[changedKey] ||
            ["Something shifts, subtly but profoundly"];
        let description = templates[Math.floor(Math.random() * templates.length)];
        
        // Add specific details for known archetypes
        const impulseBits = impulse.bits;
        if (this.specificTemplates[impulseBits]) {
            description += this.specificTemplates[impulseBits];
        }
        
        // Add step context
        if (stepNumber === 1) {
            description = "First, " + description[0].toLowerCase() + description.slice(1);
        } else if (stepNumber === 2) {
            description = "Then, " + description[0].toLowerCase() + description.slice(1);
        } else if (stepNumber === 3) {
            description = "Finally, " + description[0].toLowerCase() + description.slice(1);
        }
        
        const significance = changed.length / 3.0;
        
        return new Event(
            changedKey,
            description,
            current,
            newState,
            significance
        );
    }
}


/**
 * StoryRenderer class — render narrative arcs into prose
 */
class StoryRenderer {
    constructor() {
        this.templates = {
            opening: [
                "In {setting}",
                "There once was {protagonist} who {background}",
                "The story begins {setting}",
                "{protagonist} lived {background}",
                "Long ago, {setting}"
            ],
            intro: [
                "{name} was {archetype}, driven by {motivation}, fearing {fear}.",
                "{name} embodied the {archetype}, {motivation}, always aware of {fear}.",
                "They called {name} the {archetype}, for they {motivation} despite {fear}."
            ],
            event: [
                "{description}",
                "And so {description}",
                "But {description}",
                "Then {description}",
                "One day, {description}"
            ],
            reflection: [
                "Nothing would ever be the same.",
                "They felt the change deep within.",
                "The world looked different now.",
                "Something had shifted, though they couldn't name it.",
                "A door had opened that could never be closed."
            ],
            closing: [
                "And so {protagonist} became {finalState}.",
                "Thus ended the journey of {protagonist}.",
                "{protagonist} was never the same again.",
                "In the end, {protagonist} found {finalState}.",
                "And there, {protagonist} remained."
            ]
        };
    }
    
    /**
     * Render a complete story
     * @param {NarrativeArc} arc
     * @param {StoryWorld} world
     * @returns {string}
     */
    render(arc, world) {
        const paragraphs = [];
        
        // Opening
        const opening = this._randomChoice(this.templates.opening);
        paragraphs.push(this._format(opening, {
            setting: world.setting,
            protagonist: arc.protagonist.name,
            background: arc.protagonist.background
        }));
        
        // Introduction of protagonist
        const intro = this._randomChoice(this.templates.intro);
        paragraphs.push(this._format(intro, {
            name: arc.protagonist.name,
            archetype: arc.protagonist.attributes.archetypeName || "unknown",
            motivation: (arc.protagonist.attributes.motivation || "").toLowerCase(),
            fear: (arc.protagonist.attributes.fear || "").toLowerCase()
        }));
        
        // Plot points
        for (let i = 0; i < arc.plotPoints.length; i++) {
            const event = arc.plotPoints[i];
            
            // Event description
            const eventText = this._randomChoice(this.templates.event);
            paragraphs.push(this._format(eventText, {
                description: event.description
            }));
            
            // Add reflection (except after last event)
            if (i < arc.plotPoints.length - 1) {
                const reflection = this._randomChoice(this.templates.reflection);
                paragraphs.push(reflection);
            }
        }
        
        // Closing
        const closing = this._randomChoice(this.templates.closing);
        paragraphs.push(this._format(closing, {
            protagonist: arc.protagonist.name,
            finalState: arc.finalState.name
        }));
        
        return paragraphs.join("\n\n");
    }
    
    _randomChoice(array) {
        return array[Math.floor(Math.random() * array.length)];
    }
    
    _format(template, values) {
        return template.replace(/{(\w+)}/g, (match, key) => {
            return values[key] !== undefined ? values[key] : match;
        });
    }
}


// ============================================================================
// 8. MAIN ENGINE
// ============================================================================

/**
 * SUBITNarrativeEngine class — main story generation engine
 */
class SUBITNarrativeEngine {
    constructor() {
        this.catalog = new ArchetypeCatalog();
        this.transmutations = new TransmutationCatalog();
        this.characterGen = new CharacterGenerator(this.catalog);
        this.worldGen = new WorldGenerator(this.catalog);
        this.plotGen = new PlotGenerator(
            this.characterGen,
            this.worldGen,
            this.transmutations
        );
        this.renderer = new StoryRenderer();
        
        // Title templates
        this.titleTemplates = [
            "The {resultName} of {protagonist}",
            "{protagonist}'s Journey",
            "The Transmutation",
            "Salt",
            "Those Who Wait",
            "The Architect and the Bird",
            "The Last Dance",
            "The Library of Dreams",
            "The {initialName} and the {impulseName}",
            "How {protagonist} Became {resultName}",
            "The {catalystName}'s Gift",
            "A {resultName} Story"
        ];
    }
    
    /**
     * Generate a complete story
     * @param {Object} options
     * @returns {Story}
     */
    generateStory({
        initial = null,
        target = null,
        formulaName = null,
        protagonistName = null,
        style = "magic_realism",
        complexity = 3,
        seed = null
    } = {}) {
        
        if (seed) {
            // Simple seed-based randomization
            const seedNum = seed.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
            this._random = this._seededRandom(seedNum);
        } else {
            this._random = Math.random;
        }
        
        // Determine initial and target states
        let formula = null;
        if (formulaName) {
            formula = this.transmutations.findByName(formulaName);
            if (formula) {
                initial = formula.initial;
                target = formula.result;
            }
        }
        
        if (!initial) {
            const all = this.catalog.all();
            initial = all[Math.floor(this._random() * all.length)];
        }
        
        if (!target) {
            const all = this.catalog.all().filter(a => !a.equals(initial));
            target = all[Math.floor(this._random() * all.length)] || initial;
        }
        
        // Generate world
        const world = this.worldGen.generate(initial);
        
        // Generate narrative arc
        const arc = this.plotGen.generateArc(
            initial,
            target,
            protagonistName,
            complexity
        );
        
        // Render story
        const text = this.renderer.render(arc, world);
        
        // Generate title
        const title = this._generateTitle(arc, formula);
        
        // Collect metadata
        const metadata = {
            initialState: initial.bits,
            finalState: target.bits,
            initialStateName: initial.name,
            finalStateName: target.name,
            transmutations: arc.plotPoints.map((e, i) => ({
                step: i,
                event: e.description,
                bitsChanged: e.bitsChanged,
                from: e.previousState.bits,
                to: e.newState.bits,
                fromName: e.previousState.name,
                toName: e.newState.name
            })),
            dramaticTension: arc.dramaticTension,
            style,
            complexity
        };
        
        if (formula) {
            metadata.formula = formula.name;
        }
        
        return new Story(
            title,
            text,
            arc,
            world,
            metadata
        );
    }
    
    _seededRandom(seed) {
        return function() {
            seed = (seed * 9301 + 49297) % 233280;
            return seed / 233280;
        };
    }
    
    _generateTitle(arc, formula = null) {
        const template = this.titleTemplates[
            Math.floor(this._random() * this.titleTemplates.length)
        ];
        
        return template
            .replace("{protagonist}", arc.protagonist.name)
            .replace("{resultName}", arc.finalState.name)
            .replace("{initialName}", arc.initialState.name)
            .replace("{impulseName}", "Stranger")
            .replace("{catalystName}", "Guide")
            .replace("{formulaName}", formula ? formula.name : "Change");
    }
    
    /**
     * Generate multiple stories
     * @param {number} count
     * @param {Object} options
     * @returns {Story[]}
     */
    batchGenerate(count, options = {}) {
        const stories = [];
        for (let i = 0; i < count; i++) {
            stories.push(this.generateStory(options));
        }
        return stories;
    }
    
    /**
     * Generate a story using a master formula
     * @param {string} formulaName
     * @param {Object} options
     * @returns {Story}
     */
    generateFromFormula(formulaName, options = {}) {
        return this.generateStory({
            ...options,
            formulaName
        });
    }
}


// ============================================================================
// 9. CONVENIENCE FUNCTIONS
// ============================================================================

/**
 * Create an archetype from string values
 * @param {string} who
 * @param {string} where
 * @param {string} when
 * @returns {Archetype}
 */
function createArchetype(who, where, when) {
    const whoMap = {
        "ME": WHO.ME, "WE": WHO.WE, "YOU": WHO.YOU, "THEY": WHO.THEY
    };
    const whereMap = {
        "EAST": WHERE.EAST, "SOUTH": WHERE.SOUTH,
        "WEST": WHERE.WEST, "NORTH": WHERE.NORTH
    };
    const whenMap = {
        "SPRING": WHEN.SPRING, "SUMMER": WHEN.SUMMER,
        "AUTUMN": WHEN.AUTUMN, "WINTER": WHEN.WINTER
    };
    
    return new Archetype(
        whoMap[who.toUpperCase()],
        whereMap[where.toUpperCase()],
        whenMap[when.toUpperCase()]
    );
}

/**
 * Convenience function to generate a story
 * @param {Object} options
 * @returns {Story}
 */
function generateStory(options = {}) {
    const engine = new SUBITNarrativeEngine();
    
    let initialArch = null;
    let targetArch = null;
    
    if (options.initial) {
        if (options.initial.includes(" ")) {
            initialArch = Archetype.fromBits(options.initial);
        } else {
            initialArch = nameToArchetype(options.initial);
        }
    }
    
    if (options.target) {
        if (options.target.includes(" ")) {
            targetArch = Archetype.fromBits(options.target);
        } else {
            targetArch = nameToArchetype(options.target);
        }
    }
    
    return engine.generateStory({
        initial: initialArch,
        target: targetArch,
        formulaName: options.formula,
        protagonistName: options.name,
        complexity: options.complexity || 3
    });
}


// ============================================================================
// 10. EXAMPLE USAGE
// ============================================================================

/**
 * Example: Generate a story using the Philosopher's Stone formula
 */
function examplePhilosopherStone() {
    const engine = new SUBITNarrativeEngine();
    
    const story = engine.generateFromFormula("Philosopher's Stone", {
        protagonistName: "Luca",
        complexity: 3
    });
    
    console.log(`Title: ${story.title}\n`);
    console.log(story.text);
    console.log(`\n--- Analysis ---`);
    console.log(`Initial: ${story.arc.initialState.bits} (${story.arc.initialState.name})`);
    console.log(`Final: ${story.arc.finalState.bits} (${story.arc.finalState.name})`);
    console.log(`Dramatic tension: ${story.arc.dramaticTension.toFixed(2)}`);
    
    return story;
}

/**
 * Example: Generate a random story
 */
function exampleRandom() {
    const engine = new SUBITNarrativeEngine();
    
    const story = engine.generateStory({ complexity: 3 });
    
    console.log(`Title: ${story.title}\n`);
    console.log(story.text);
    console.log(`\n--- Analysis ---`);
    console.log(`Initial: ${story.arc.initialState.bits} (${story.arc.initialState.name})`);
    console.log(`Final: ${story.arc.finalState.bits} (${story.arc.finalState.name})`);
    
    return story;
}


// ============================================================================
// 11. EXPORTS
// ============================================================================

module.exports = {
    // Enums
    WHO,
    WHERE,
    WHEN,
    
    // Core classes
    Archetype,
    Character,
    Event,
    NarrativeArc,
    StoryWorld,
    Story,
    
    // Catalogs
    ArchetypeCatalog,
    TransmutationFormula,
    TransmutationCatalog,
    
    // Predefined instances
    ZERO,
    PIONEER,
    CONCILIAR,
    CONFESSOR,
    STEADFAST,
    GHOST,
    BELOVED,
    COUNCIL,
    PHILOSOPHER_STONE,
    
    // Utility functions
    hammingDistance,
    findPath,
    analyzeTransmutation,
    bitsToInt,
    intToBits,
    nameToArchetype,
    createArchetype,
    
    // Generators
    CharacterGenerator,
    WorldGenerator,
    PlotGenerator,
    StoryRenderer,
    
    // Main engine
    SUBITNarrativeEngine,
    generateStory,
    
    // Examples
    examplePhilosopherStone,
    exampleRandom
};
