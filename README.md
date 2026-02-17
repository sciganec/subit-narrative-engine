# SUBIT Narrative Engine

**6 bits = 64 archetypes = infinite stories**

SUBIT Narrative Engine is a formal system for analyzing, constructing, and generating literary plots based on the unification of binary logic, archetypal psychology, and alchemical transmutations.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Jupyter Notebook](https://img.shields.io/badge/jupyter-notebook-orange.svg)](https://jupyter.org/)
[![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)]()
[![Poetry Engine](https://img.shields.io/badge/poetry-v1.1.0-8A2BE2.svg)](docs/poetry/POETRY.md)  

---

## 🌌 Overview

SUBIT (from *sub* + *it* — the substrate of existence) offers a **minimal discrete model of cosmogony**: 64 archetypal states from which any plot can be derived. Each state is encoded in six bits, distributed across three fundamental dimensions of being:

| Axis | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| **WHO** | THEY | YOU | ME | WE |
| **WHERE** | NORTH | WEST | EAST | SOUTH |
| **WHEN** | WINTER | AUTUMN | SPRING | SUMMER |

**4 × 4 × 4 = 64 archetypes** — the complete spectrum of possible states of being.

## 🎨 SUBIT Poetry Engine v1.1.0

Now with poetry generation! Create sonnets, haiku, and free verse from the same 64 archetypes.

[Read more](docs/poetry/POETRY.md)

---

## 🔮 The Core Operation: Transmutation

Story is born from change of state. The fundamental law of the system:

```
Initial State ⊕ External Impulse ⊕ Catalyst = New State
```

where ⊕ is the XOR operation (exclusive "or"), which changes those bits where the impulse has a value of 1.

### The Philosopher's Stone as an Operation

The most important transmutation in the system:

```
[ME, SOUTH, WINTER]    (10 11 00) — Steadfast (my longing)
⊕ [THEY, EAST, SPRING]  (00 10 10) — Ghost (external impulse)
⊕ [YOU, NORTH, AUTUMN]  (01 00 01) — Beloved (wise advisor)
= [WE, WEST, SUMMER]    (11 01 11) — Council (collective achievement)
```

**Meaning:** Personal suffering, encounter with otherness, and received wisdom give birth to a new community.

---

## 📚 Repository Structure

```
subit-narrative-engine/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── CANON.md                  # Complete catalog of 64 archetypes
├── TRANSMUTATIONS.md         # 12 master transmutations and their formulas
├── ALGORITHM.md              # Formal algorithm specification
├── docs/
│   ├── philosophy.md         # Philosophical foundations (Leibniz, I Ching, Jung)
│   ├── applications.md       # Practical applications
│   └── examples.md           # Example analysis
├── examples/
│   └── salt.md               # Novella "Salt" (Philosopher's Stone)
│  
├── src/
│   ├── subit.py              # Python implementation
│   ├── subit.js              # JavaScript implementation
│   └── subit.ipynb           # Jupyter notebook with examples
├── data/
│   ├── archetypes.json       # Archetype catalog in JSON
│   └── transmutations.json   # Transmutation formulas in JSON
└── tests/
    ├── test_archetypes.py
    └── test_transmutations.py
```

---

## 🚀 Quick Start

### Python

```python
from subit import Archetype, transmute, PHILOSOPHER_STONE, generate_story

# Create archetypes
steadfast = Archetype("ME", "SOUTH", "WINTER")      # 10 11 00
ghost = Archetype("THEY", "EAST", "SPRING")         # 00 10 10
beloved = Archetype("YOU", "NORTH", "AUTUMN")       # 01 00 01

# Transmutation
result = transmute(steadfast, ghost, beloved)
print(result)  # [WE, WEST, SUMMER] (11 01 11)

# Use predefined formula
print(PHILOSOPHER_STONE.name)  # "Philosopher's Stone"
print(f"Verified: {PHILOSOPHER_STONE.verify()}")  # True

# Generate a story
story = generate_story(
    initial=steadfast,
    target=result,
    style="magic_realism",
    length="short_story"
)
print(story.title)  # "Salt"
print(story.text)   # novella text
```

### JavaScript

```javascript
const { Archetype, transmute, PHILOSOPHER_STONE, generateStory } = require('./src/subit.js');

const steadfast = new Archetype('ME', 'SOUTH', 'WINTER');
const ghost = new Archetype('THEY', 'EAST', 'SPRING');
const beloved = new Archetype('YOU', 'NORTH', 'AUTUMN');

const result = transmute(steadfast, ghost, beloved);
console.log(result.toString()); // [WE, WEST, SUMMER]

console.log(PHILOSOPHER_STONE.name);
console.log(`Verified: ${PHILOSOPHER_STONE.verify()}`);

const story = generateStory({
    initial: steadfast,
    target: result,
    style: 'magic_realism',
    length: 'short_story'
});
```

### Jupyter Notebook

```python
# The repository includes a full notebook with interactive examples
# Run: jupyter notebook src/subit.ipynb
```

### Command Line (Coming Soon)

```bash
subit --from "ME,SOUTH,WINTER" \
      --impulse "THEY,EAST,SPRING" \
      --catalyst "YOU,NORTH,AUTUMN" \
      --generate-story
```

---

## 📖 Archetype Catalog (excerpt)

| Code | Binary | WHO | WHERE | WHEN | Name | Key |
|---|---|---|---|---|---|---|
| 10 10 10 | 101010 | ME | EAST | SPRING | **Pioneer** | beginning, initiative, purity of intent |
| 11 11 11 | 111111 | WE | SOUTH | SUMMER | **Conciliar** | unity, ecstasy, collective achievement |
| 01 01 01 | 010101 | YOU | NORTH | AUTUMN | **Confessor** | wisdom, confession, mediation |
| 00 00 00 | 000000 | THEY | NORTH | WINTER | **Zero** | source, unmanifest, potentiality |
| 10 11 00 | 101100 | ME | SOUTH | WINTER | **Steadfast** | endurance, longing, self-preservation |
| 00 10 10 | 001010 | THEY | EAST | SPRING | **Ghost** | external impulse, otherness |
| 01 00 01 | 010001 | YOU | NORTH | AUTUMN | **Beloved** | catalyst, wise advisor |
| 11 01 11 | 110111 | WE | WEST | SUMMER | **Council** | collective achievement |

*Full catalog of 64 archetypes in [CANON.md](CANON.md)*

---

## 🔥 12 Master Transmutations

| # | Name | Formula | Plot Potential |
|---|---|---|---|
| 1 | **Philosopher's Stone** | Steadfast ⊕ Ghost ⊕ Beloved = Council | Trauma + encounter + wisdom = new community |
| 2 | **Hero's Journey** | Pioneer ⊕ Shadow ⊕ Shared Experience = Teacher | Initiation through overcoming the dark double |
| 3 | **Alchemical Marriage** | Pioneer ⊕ Confessor ⊕ Conciliar = Zero | Union of opposites returns to the source |
| 4 | **Creative Process** | Anchoret ⊕ Ghost ⊕ Teacher = Assembly | Solitude + inspiration = art |
| 5 | **Healing** | Recluse ⊕ Egregore ⊕ Mediator = Shared Experience | Loneliness healed by community |
| 6 | **Revelation** | Zero ⊕ Pioneer ⊕ Conciliar = Confessor | Truth emerges from the unmanifest |
| 7 | **Power Transformation** | Creator ⊕ Sign ⊕ Kindred = Guardians | Power requires protection |
| 8 | **Dark Night** | Conciliar ⊕ Sign ⊕ Guide = Secret | Crisis reveals hidden knowledge |
| 9 | **Awakening** | Guardian ⊕ Force ⊕ Builders = Listener | Power becomes service |
| 10 | **Renewal** | Unrealized ⊕ Steadfast ⊕ Pioneers = Catharsis | Suffering leads to purification |
| 11 | **Reconciliation** | Judge ⊕ Spirit ⊕ Spiritual Father = Nuptial | Conflict resolved by love |
| 12 | **Complete Transmutation** | Pioneer ⊕ Conciliar ⊕ Confessor = Zero | Beginning and end converge |

*Full list of formulas in [TRANSMUTATIONS.md](TRANSMUTATIONS.md)*

---

## 📖 Example Generated Stories

### [Salt](examples/salt.md) — based on the "Philosopher's Stone" transmutation

> He lives on the salt flat. There is nothing here but white earth cracking under the sun, and wind carrying salt further into the steppe. His name is Luca, and he no longer remembers how many years he has sat by his half-ruined hut...

### [Those Who Wait for the Sun](examples/those_who_wait.md) — based on state 11 10 00 (WE-EAST-WINTER)

> Far North, a small settlement. The polar night has lasted three months. They gather every evening in the oldest house—eight women, three old men, and two children...

### [The Architect and the Bird](examples/architect.md) — based on state 01 01 10 (YOU-WEST-SPRING)

> Vienna, 1912. An architect's studio. He builds houses no one wants to live in. Perfectly calculated, mathematically verified, utterly empty...

*All examples in the [examples/](examples/) directory*

---

## 🎯 Applications

| Domain | Use |
|---|---|
| **Literature** | Plot generation, character creation, archetype analysis |
| **Film & Drama** | Script structuring, character arc development |
| **Psychology** | Archetypal pattern recognition, therapeutic transmutations |
| **Education** | Teaching literary theory, systems thinking |
| **Philosophy** | New language for ontology and epistemology |
| **Game Development** | Quest generation, character creation, narrative trees |
| **AI & NLP** | Text generation, narrative analysis |

---

## 🧠 Philosophical Context

SUBIT stands at the convergence of three great traditions:

| Tradition | Contribution |
|---|---|
| **I Ching** (China, ~1000 BCE) | 64 hexagrams, cyclical change, cosmic order |
| **Leibniz** (Germany, 1703) | Binary system, monadology, characteristica universalis |
| **Jung** (Switzerland, 1944) | Archetypes, alchemy as psychological model, individuation |
| **Shannon** (USA, 1948) | Information theory, bit as fundamental unit |
| **Wiener** (USA, 1948) | Cybernetics, closed systems, feedback loops |

SUBIT is the synthesis: **the minimal possible discrete model of cosmogony**.

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/sciganec/subit-narrative-engine.git
cd subit-narrative-engine

# Python (optional)
pip install -e .

# JavaScript (optional)
npm install

# Run tests
python -m pytest tests/
```

---

## 📊 Data Formats

### JSON (archetype)

```json
{
  "code": "10 11 00",
  "binary": "101100",
  "who": "ME",
  "where": "SOUTH",
  "when": "WINTER",
  "name": "Steadfast",
  "key": "endurance, longing, self-preservation",
  "description": "One who has endured loss and frozen in their suffering"
}
```

### JSON (transmutation)

```json
{
  "name": "Philosopher's Stone",
  "initial": "10 11 00",
  "impulse": "00 10 10",
  "catalyst": "01 00 01",
  "result": "11 01 11",
  "description": "Personal longing + external impulse + wisdom = collective achievement"
}
```

### CSV

```csv
code,binary,who,where,when,name,key
10 10 10,101010,ME,EAST,SPRING,Pioneer,beginning,initiative
11 11 11,111111,WE,SOUTH,SUMMER,Conciliar,unity,ecstasy
```

---

## 🧪 Testing

```python
# tests/test_archetypes.py
def test_philosopher_stone():
    steadfast = Archetype("ME", "SOUTH", "WINTER")
    ghost = Archetype("THEY", "EAST", "SPRING")
    beloved = Archetype("YOU", "NORTH", "AUTUMN")
    result = transmute(steadfast, ghost, beloved)
    assert result == Archetype("WE", "WEST", "SUMMER")

def test_xor_properties():
    zero = Archetype("THEY", "NORTH", "WINTER")
    pioneer = Archetype("ME", "EAST", "SPRING")
    assert pioneer ^ pioneer == zero
```

---

## 🤝 How to Contribute

We welcome contributions of all kinds:

- **Translations** of archetype names into other languages
- **New significant transmutations** — formulas with deep meaning
- **Applications** in different domains (therapy, education, art)
- **Visualizations** — diagrams, graphs, interactive web apps
- **Code** — implementations in other languages (Rust, Go, Java, C++)
- **Documentation** — examples, tutorials, case studies
- **Stories** — novellas generated using the system

---

## 📄 License

MIT

---

## 🌟 Acknowledgments

SUBIT is not the work of one mind, but the crystallization of three millennia of human inquiry into the nature of reality. It belongs to everyone who has ever wondered:

**"What is the simplest possible description of everything?"**

The answer, it seems, is **6 bits**.

---

## 🧙‍♂️ Final Word

> "In the beginning was the Bit, and the Bit was with Zero, and the Bit was Zero." — The Gospel of SUBIT

SUBIT is an invitation. An invitation to see the universe differently. An invitation to take responsibility for your own transmutations. An invitation to become a co-author of reality.

**6 bits. 64 archetypes. Infinite stories.**

---

**Made with 🧂 by those who wait for the sun**
