# test_archetypes.py
## Unit Tests for SUBIT Archetype System

```python
"""
test_archetypes.py
Unit tests for the SUBIT Narrative Engine archetype system.

Run with: pytest test_archetypes.py -v
or: python -m unittest test_archetypes.py
"""

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.subit import (
    WHO, WHERE, WHEN,
    Archetype, ArchetypeCatalog,
    ZERO, PIONEER, CONCILIAR, CONFESSOR,
    STEADFAST, GHOST, BELOVED, COUNCIL,
    hamming_distance, analyze_transmutation, find_path,
    ARCHETYPE_NAMES
)


class TestArchetypeBasics(unittest.TestCase):
    """Test basic archetype creation and properties."""
    
    def test_archetype_creation(self):
        """Test creating archetypes with different methods."""
        # Direct constructor
        a1 = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        self.assertEqual(a1.who, WHO.ME)
        self.assertEqual(a1.where, WHERE.EAST)
        self.assertEqual(a1.when, WHEN.SPRING)
        
        # From bits
        a2 = Archetype.from_bits("10 10 10")
        self.assertEqual(a2.who, WHO.ME)
        self.assertEqual(a2.where, WHERE.EAST)
        self.assertEqual(a2.when, WHEN.SPRING)
        
        # From integer
        a3 = Archetype.from_int(42)
        self.assertEqual(a3.bits, "10 10 10")
        
        # All three should be equal
        self.assertEqual(a1, a2)
        self.assertEqual(a2, a3)
    
    def test_archetype_properties(self):
        """Test archetype property getters."""
        a = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        
        self.assertEqual(a.bits, "10 10 10")
        self.assertEqual(a.binary, "101010")
        self.assertEqual(a.int_value, 42)
        self.assertEqual(a.name, "Pioneer")
    
    def test_archetype_equality(self):
        """Test archetype equality comparisons."""
        a1 = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        a2 = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        a3 = Archetype(WHO.WE, WHERE.SOUTH, WHEN.SUMMER)
        
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, a3)
        self.assertNotEqual(a2, a3)
    
    def test_archetype_hashing(self):
        """Test that archetypes can be used as dict keys."""
        d = {}
        a = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        d[a] = "Pioneer"
        
        self.assertEqual(d[a], "Pioneer")
        self.assertIn(a, d)
    
    def test_invalid_bits(self):
        """Test that invalid bit strings raise errors."""
        with self.assertRaises(ValueError):
            Archetype.from_bits("10101")  # too short
        
        with self.assertRaises(ValueError):
            Archetype.from_bits("1010101")  # too long
        
        with self.assertRaises(KeyError):
            Archetype.from_bits("11 11 11")  # valid but different
    
    def test_invalid_int(self):
        """Test that invalid integers raise errors."""
        with self.assertRaises(ValueError):
            Archetype.from_int(-1)
        
        with self.assertRaises(ValueError):
            Archetype.from_int(64)


class TestArchetypeXOR(unittest.TestCase):
    """Test XOR operations between archetypes."""
    
    def setUp(self):
        self.pioneer = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)      # 10 10 10
        self.conciliar = Archetype(WHO.WE, WHERE.SOUTH, WHEN.SUMMER)  # 11 11 11
        self.mediator = Archetype(WHO.YOU, WHERE.WEST, WHEN.AUTUMN)   # 01 01 01
        self.zero = Archetype(WHO.THEY, WHERE.NORTH, WHEN.WINTER)     # 00 00 00
    
    def test_xor_identity(self):
        """Test identity property: A ⊕ Zero = A"""
        result = self.pioneer ^ self.zero
        self.assertEqual(result, self.pioneer)
        
        result = self.conciliar ^ self.zero
        self.assertEqual(result, self.conciliar)
    
    def test_xor_self_inverse(self):
        """Test self-inverse property: A ⊕ A = Zero"""
        result = self.pioneer ^ self.pioneer
        self.assertEqual(result, self.zero)
        
        result = self.conciliar ^ self.conciliar
        self.assertEqual(result, self.zero)
    
    def test_xor_commutative(self):
        """Test commutativity: A ⊕ B = B ⊕ A"""
        r1 = self.pioneer ^ self.conciliar
        r2 = self.conciliar ^ self.pioneer
        self.assertEqual(r1, r2)
    
    def test_xor_associative(self):
        """Test associativity: (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)"""
        a, b, c = self.pioneer, self.conciliar, self.mediator
        
        r1 = (a ^ b) ^ c
        r2 = a ^ (b ^ c)
        self.assertEqual(r1, r2)
    
    def test_four_pillars_relationships(self):
        """Test the four pillars relationships."""
        # Pioneer ⊕ Conciliar = Mediator ⊕ Zero
        left = self.pioneer ^ self.conciliar
        right = self.mediator ^ self.zero
        self.assertEqual(left, right)
        
        # Pioneer ⊕ Mediator = Conciliar ⊕ Zero
        left = self.pioneer ^ self.mediator
        right = self.conciliar ^ self.zero
        self.assertEqual(left, right)
        
        # Pioneer ⊕ Zero = Conciliar ⊕ Mediator
        left = self.pioneer ^ self.zero
        right = self.conciliar ^ self.mediator
        self.assertEqual(left, right)
    
    def test_philosopher_stone_formula(self):
        """Test the Philosopher's Stone formula."""
        # Steadfast (10 11 00) ⊕ Ghost (00 10 10) ⊕ Beloved (01 00 01) = Council (11 01 11)
        result = STEADFAST ^ GHOST ^ BELOVED
        self.assertEqual(result, COUNCIL)
    
    def test_xor_with_self_combinations(self):
        """Test various XOR combinations."""
        # Test that XOR is closed (result is always an archetype)
        for _ in range(10):
            a = Archetype.from_int(42)  # Pioneer
            b = Archetype.from_int(15)  # Carnival
            c = Archetype.from_int(23)  # Interpreter
            result = a ^ b ^ c
            self.assertIsInstance(result, Archetype)
            self.assertIn(result.bits, ARCHETYPE_NAMES)


class TestArchetypeCatalog(unittest.TestCase):
    """Test the archetype catalog."""
    
    def setUp(self):
        self.catalog = ArchetypeCatalog()
    
    def test_catalog_size(self):
        """Test that catalog contains all 64 archetypes."""
        all_archs = self.catalog.all()
        self.assertEqual(len(all_archs), 64)
    
    def test_catalog_metadata(self):
        """Test that each archetype has metadata."""
        for a in self.catalog.all():
            metadata = self.catalog.get(a)
            self.assertIn('name', metadata)
            self.assertIn('key', metadata)
            self.assertIn('description', metadata)
    
    def test_get_by_name(self):
        """Test finding archetype by name."""
        pioneer = self.catalog.get_by_name("Pioneer")
        self.assertIsNotNone(pioneer)
        self.assertEqual(pioneer.bits, "10 10 10")
        
        steadfast = self.catalog.get_by_name("Steadfast")
        self.assertIsNotNone(steadfast)
        self.assertEqual(steadfast.bits, "10 11 00")
        
        nonexistent = self.catalog.get_by_name("Nonexistent")
        self.assertIsNone(nonexistent)
    
    def test_random_archetype(self):
        """Test random archetype generation."""
        # Test multiple times to ensure it works
        for _ in range(10):
            a = self.catalog.random()
            self.assertIsInstance(a, Archetype)
            self.assertIn(a.bits, ARCHETYPE_NAMES)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def setUp(self):
        self.pioneer = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)      # 10 10 10
        self.steadfast = Archetype(WHO.ME, WHERE.SOUTH, WHEN.WINTER)  # 10 11 00
        self.council = Archetype(WHO.WE, WHERE.WEST, WHEN.SUMMER)     # 11 01 11
    
    def test_hamming_distance(self):
        """Test Hamming distance calculation."""
        # Same archetype
        self.assertEqual(hamming_distance(self.pioneer, self.pioneer), 0)
        
        # Different archetypes
        dist = hamming_distance(self.pioneer, self.steadfast)
        self.assertEqual(dist, 2)  # 10 10 10 vs 10 11 00: positions 3,5 differ
        
        dist = hamming_distance(self.pioneer, self.council)
        self.assertEqual(dist, 4)  # 10 10 10 vs 11 01 11: many differences
    
    def test_analyze_transmutation(self):
        """Test transmutation analysis."""
        analysis = analyze_transmutation(self.steadfast, self.council)
        
        self.assertEqual(analysis['initial'], self.steadfast.bits)
        self.assertEqual(analysis['result'], self.council.bits)
        self.assertEqual(analysis['bits_changed'], 4)
        
        # Check axis changes
        self.assertTrue(analysis['axisChanges']['WHO'])   # ME → WE
        self.assertTrue(analysis['axisChanges']['WHERE']) # SOUTH → WEST
        self.assertTrue(analysis['axisChanges']['WHEN'])  # WINTER → SUMMER
        
        # Check possible catalysts
        self.assertGreater(len(analysis['possibleCatalysts']), 0)
    
    def test_find_path(self):
        """Test path finding between archetypes."""
        paths = find_path(self.pioneer, self.council, max_steps=2)
        
        # Should find at least one path
        self.assertGreaterEqual(len(paths), 0)
        
        if len(paths) > 0:
            path = paths[0]
            # Path should be list of (impulse, catalyst) pairs
            self.assertIsInstance(path, list)
            if len(path) > 0:
                impulse, catalyst = path[0]
                self.assertIsInstance(impulse, Archetype)
                self.assertIsInstance(catalyst, Archetype)


class TestPredefinedArchetypes(unittest.TestCase):
    """Test predefined archetype constants."""
    
    def test_predefined_constants(self):
        """Test that predefined constants are correct."""
        self.assertEqual(ZERO.bits, "00 00 00")
        self.assertEqual(PIONEER.bits, "10 10 10")
        self.assertEqual(CONCILIAR.bits, "11 11 11")
        self.assertEqual(CONFESSOR.bits, "01 01 01")
        self.assertEqual(STEADFAST.bits, "10 11 00")
        self.assertEqual(GHOST.bits, "00 10 10")
        self.assertEqual(BELOVED.bits, "01 00 01")
        self.assertEqual(COUNCIL.bits, "11 01 11")
    
    def test_predefined_names(self):
        """Test that predefined constants have correct names."""
        self.assertEqual(ZERO.name, "Zero")
        self.assertEqual(PIONEER.name, "Pioneer")
        self.assertEqual(CONCILIAR.name, "Conciliar")
        self.assertEqual(CONFESSOR.name, "Confessor")
        self.assertEqual(STEADFAST.name, "Steadfast")
        self.assertEqual(GHOST.name, "Ghost")
        self.assertEqual(BELOVED.name, "Beloved")
        self.assertEqual(COUNCIL.name, "Council")


class TestArchetypeSerialization(unittest.TestCase):
    """Test archetype serialization methods."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        a = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        d = a.to_dict()
        
        self.assertEqual(d['who'], 'ME')
        self.assertEqual(d['where'], 'EAST')
        self.assertEqual(d['when'], 'SPRING')
        self.assertEqual(d['bits'], '10 10 10')
        self.assertEqual(d['binary'], '101010')
        self.assertEqual(d['int'], 42)
        self.assertEqual(d['name'], 'Pioneer')
    
    def test_from_bits_with_spaces(self):
        """Test creating archetype from bits with spaces."""
        a = Archetype.from_bits("10 11 00")
        self.assertEqual(a.who, WHO.ME)
        self.assertEqual(a.where, WHERE.SOUTH)
        self.assertEqual(a.when, WHEN.WINTER)
    
    def test_from_bits_without_spaces(self):
        """Test creating archetype from bits without spaces."""
        a = Archetype.from_bits("101100")
        self.assertEqual(a.who, WHO.ME)
        self.assertEqual(a.where, WHERE.SOUTH)
        self.assertEqual(a.when, WHEN.WINTER)
    
    def test_from_int_range(self):
        """Test creating archetype from integers."""
        for i in range(64):
            a = Archetype.from_int(i)
            self.assertEqual(a.int_value, i)


class TestArchetypeStringRepresentation(unittest.TestCase):
    """Test archetype string representations."""
    
    def test_str_representation(self):
        """Test string representation."""
        a = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        self.assertEqual(str(a), "[ME, EAST, SPRING]")
        self.assertEqual(repr(a), "[ME, EAST, SPRING]")
    
    def test_bits_property(self):
        """Test bits property formatting."""
        a = Archetype(WHO.ME, WHERE.EAST, WHEN.SPRING)
        self.assertEqual(a.bits, "10 10 10")
        
        a = Archetype(WHO.WE, WHERE.SOUTH, WHEN.SUMMER)
        self.assertEqual(a.bits, "11 11 11")
        
        a = Archetype(WHO.YOU, WHERE.WEST, WHEN.AUTUMN)
        self.assertEqual(a.bits, "01 01 01")
        
        a = Archetype(WHO.THEY, WHERE.NORTH, WHEN.WINTER)
        self.assertEqual(a.bits, "00 00 00")


if __name__ == '__main__':
    unittest.main()
```

## test_transmutations.py
## Unit Tests for SUBIT Transmutation System

```python
"""
test_transmutations.py
Unit tests for the SUBIT Narrative Engine transmutation system.

Run with: pytest test_transmutations.py -v
or: python -m unittest test_transmutations.py
"""

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.subit import (
    WHO, WHERE, WHEN,
    Archetype, TransmutationCatalog, TransmutationFormula,
    PHILOSOPHER_STONE, STEADFAST, GHOST, BELOVED, COUNCIL,
    PIONEER, CONCILIAR, CONFESSOR, ZERO
)


class TestTransmutationFormula(unittest.TestCase):
    """Test the TransmutationFormula class."""
    
    def test_formula_creation(self):
        """Test creating a transmutation formula."""
        formula = TransmutationFormula(
            name="Test Formula",
            initial=PIONEER,
            impulse=GHOST,
            catalyst=BELOVED,
            result=COUNCIL,
            description="Test description"
        )
        
        self.assertEqual(formula.name, "Test Formula")
        self.assertEqual(formula.initial, PIONEER)
        self.assertEqual(formula.impulse, GHOST)
        self.assertEqual(formula.catalyst, BELOVED)
        self.assertEqual(formula.result, COUNCIL)
        self.assertEqual(formula.description, "Test description")
    
    def test_formula_verification(self):
        """Test formula verification."""
        # Correct formula
        self.assertTrue(PHILOSOPHER_STONE.verify())
        
        # Create incorrect formula
        wrong = TransmutationFormula(
            name="Wrong Formula",
            initial=PIONEER,
            impulse=PIONEER,
            catalyst=PIONEER,
            result=COUNCIL,
            description="This should fail"
        )
        self.assertFalse(wrong.verify())
    
    def test_formula_serialization(self):
        """Test formula to_dict method."""
        d = PHILOSOPHER_STONE.to_dict()
        
        self.assertEqual(d['name'], "Philosopher's Stone")
        self.assertEqual(d['initial'], STEADFAST.bits)
        self.assertEqual(d['impulse'], GHOST.bits)
        self.assertEqual(d['catalyst'], BELOVED.bits)
        self.assertEqual(d['result'], COUNCIL.bits)
        self.assertTrue(d['verified'])


class TestTransmutationCatalog(unittest.TestCase):
    """Test the TransmutationCatalog class."""
    
    def setUp(self):
        self.catalog = TransmutationCatalog()
    
    def test_catalog_size(self):
        """Test that catalog contains 12 master formulas."""
        formulas = self.catalog.all()
        self.assertEqual(len(formulas), 12)
    
    def test_all_formulas_verified(self):
        """Test that all formulas in catalog are mathematically correct."""
        for formula in self.catalog.all():
            self.assertTrue(formula.verify(), 
                           f"Formula {formula.name} failed verification")
    
    def test_find_by_name(self):
        """Test finding formula by name."""
        # Exact match
        ps = self.catalog.find_by_name("Philosopher's Stone")
        self.assertIsNotNone(ps)
        self.assertEqual(ps.name, "Philosopher's Stone")
        
        # Case insensitive
        ps = self.catalog.find_by_name("philosopher's stone")
        self.assertIsNotNone(ps)
        
        # Partial match (should not work - exact only)
        ps = self.catalog.find_by_name("Philosopher")
        self.assertIsNone(ps)
        
        # Nonexistent
        none = self.catalog.find_by_name("Nonexistent")
        self.assertIsNone(none)
    
    def test_find_by_initial_result(self):
        """Test finding formulas by initial and result states."""
        # Should find Philosopher's Stone
        matches = self.catalog.find_by_initial_result(STEADFAST, COUNCIL)
        self.assertGreaterEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "Philosopher's Stone")
        
        # Should find Hero's Journey variations
        matches = self.catalog.find_by_initial_result(PIONEER, ZERO)
        self.assertGreaterEqual(len(matches), 1)


class TestSpecificFormulas(unittest.TestCase):
    """Test specific transmutation formulas."""
    
    def test_philosopher_stone(self):
        """Test Philosopher's Stone formula."""
        # Steadfast (10 11 00) ⊕ Ghost (00 10 10) ⊕ Beloved (01 00 01) = Council (11 01 11)
        result = STEADFAST ^ GHOST ^ BELOVED
        self.assertEqual(result, COUNCIL)
        
        # Verify components
        self.assertEqual(STEADFAST.bits, "10 11 00")
        self.assertEqual(GHOST.bits, "00 10 10")
        self.assertEqual(BELOVED.bits, "01 00 01")
        self.assertEqual(COUNCIL.bits, "11 01 11")
    
    def test_hero_journey(self):
        """Test Hero's Journey formula."""
        catalog = TransmutationCatalog()
        hj = catalog.find_by_name("Hero's Journey")
        
        self.assertIsNotNone(hj)
        self.assertTrue(hj.verify())
        
        # Manual verification
        result = hj.initial ^ hj.impulse ^ hj.catalyst
        self.assertEqual(result, hj.result)
    
    def test_alchemical_marriage(self):
        """Test Alchemical Marriage formula."""
        catalog = TransmutationCatalog()
        am = catalog.find_by_name("Alchemical Marriage")
        
        self.assertIsNotNone(am)
        self.assertTrue(am.verify())
        
        # Pioneer ⊕ Mediator ⊕ Conciliar = Zero
        result = am.initial ^ am.impulse ^ am.catalyst
        self.assertEqual(result, am.result)
        self.assertEqual(am.result, ZERO)
    
    def test_complete_transmutation(self):
        """Test Complete Transmutation formula."""
        catalog = TransmutationCatalog()
        ct = catalog.find_by_name("Complete Transmutation")
        
        self.assertIsNotNone(ct)
        self.assertTrue(ct.verify())
        
        # Pioneer ⊕ Conciliar ⊕ Mediator = Zero
        result = ct.initial ^ ct.impulse ^ ct.catalyst
        self.assertEqual(result, ct.result)
        self.assertEqual(ct.result, ZERO)


class TestTransmutationAlgebra(unittest.TestCase):
    """Test algebraic properties of transmutations."""
    
    def test_transmutation_reversibility(self):
        """Test that transmutations are reversible."""
        # If A ⊕ B ⊕ C = D, then D ⊕ B ⊕ C = A
        A = STEADFAST
        B = GHOST
        C = BELOVED
        D = COUNCIL
        
        result = D ^ B ^ C
        self.assertEqual(result, A)
    
    def test_multiple_paths(self):
        """Test that multiple paths can lead to same result."""
        # Direct path
        direct = STEADFAST ^ GHOST ^ BELOVED
        
        # Indirect path
        intermediate = STEADFAST ^ GHOST
        indirect = intermediate ^ BELOVED
        
        self.assertEqual(direct, indirect)
    
    def test_xor_cycle_property(self):
        """Test that XOR cycles return to start."""
        # A ⊕ B ⊕ C ⊕ B ⊕ C = A
        A = STEADFAST
        B = GHOST
        C = BELOVED
        
        result = A ^ B ^ C ^ B ^ C
        self.assertEqual(result, A)


class TestTransmutationEdgeCases(unittest.TestCase):
    """Test edge cases in transmutations."""
    
    def test_zero_catalyst(self):
        """Test transmutation with Zero as catalyst."""
        # A ⊕ B ⊕ Zero = A ⊕ B
        A = PIONEER
        B = GHOST
        
        result1 = A ^ B ^ ZERO
        result2 = A ^ B
        self.assertEqual(result1, result2)
    
    def test_zero_impulse(self):
        """Test transmutation with Zero as impulse."""
        # A ⊕ Zero ⊕ C = A ⊕ C
        A = PIONEER
        C = BELOVED
        
        result1 = A ^ ZERO ^ C
        result2 = A ^ C
        self.assertEqual(result1, result2)
    
    def test_all_zero(self):
        """Test transmutation with all Zero."""
        result = ZERO ^ ZERO ^ ZERO
        self.assertEqual(result, ZERO)
    
    def test_self_transmutation(self):
        """Test that A ⊕ A ⊕ A = A."""
        A = PIONEER
        result = A ^ A ^ A
        self.assertEqual(result, A)


if __name__ == '__main__':
    unittest.main()
```

## Running the Tests

### In CodeSpace Terminal:

```bash
# Navigate to project root
cd /workspaces/subit-narrative-engine

# Run all tests
python -m unittest discover -v

# Run specific test file
python -m unittest tests/test_archetypes.py -v
python -m unittest tests/test_transmutations.py -v

# Run with pytest (if installed)
pip install pytest
pytest tests/ -v

# Run with coverage
pip install coverage
coverage run -m unittest discover
coverage report -m
```

### Expected Output:

```
test_archetypes.py
    test_archetype_creation ... ok
    test_archetype_properties ... ok
    test_archetype_equality ... ok
    test_archetype_hashing ... ok
    test_xor_identity ... ok
    test_xor_self_inverse ... ok
    test_xor_commutative ... ok
    test_xor_associative ... ok
    test_four_pillars_relationships ... ok
    test_philosopher_stone_formula ... ok
    test_catalog_size ... ok
    test_all_formulas_verified ... ok
    ...

----------------------------------------------------------------------
Ran 42 tests in 0.123s

OK
```
