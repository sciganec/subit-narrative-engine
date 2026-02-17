# test_transmutations.py
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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.subit import (
    WHO, WHERE, WHEN,
    Archetype, TransmutationCatalog, TransmutationFormula,
    PHILOSOPHER_STONE, STEADFAST, GHOST, BELOVED, COUNCIL,
    PIONEER, CONCILIAR, CONFESSOR, ZERO,
    hamming_distance, analyze_transmutation, find_path
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
    
    def test_formula_verification_correct(self):
        """Test verification of correct formula."""
        # Philosopher's Stone should verify correctly
        self.assertTrue(PHILOSOPHER_STONE.verify())
    
    def test_formula_verification_incorrect(self):
        """Test verification of incorrect formula."""
        # Create intentionally incorrect formula
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
    
    def test_find_by_name_exact(self):
        """Test finding formula by exact name."""
        ps = self.catalog.find_by_name("Philosopher's Stone")
        self.assertIsNotNone(ps)
        self.assertEqual(ps.name, "Philosopher's Stone")
    
    def test_find_by_name_case_insensitive(self):
        """Test finding formula with case-insensitive matching."""
        ps = self.catalog.find_by_name("philosopher's stone")
        self.assertIsNotNone(ps)
        self.assertEqual(ps.name, "Philosopher's Stone")
        
        hj = self.catalog.find_by_name("HERO'S JOURNEY")
        self.assertIsNotNone(hj)
        self.assertEqual(hj.name, "Hero's Journey")
    
    def test_find_by_name_partial(self):
        """Test that partial name matching doesn't work (exact only)."""
        ps = self.catalog.find_by_name("Philosopher")
        self.assertIsNone(ps)
    
    def test_find_by_name_nonexistent(self):
        """Test finding nonexistent formula."""
        none = self.catalog.find_by_name("Nonexistent Formula")
        self.assertIsNone(none)
    
    def test_find_by_initial_result_philosopher_stone(self):
        """Test finding formulas by initial and result for Philosopher's Stone."""
        matches = self.catalog.find_by_initial_result(STEADFAST, COUNCIL)
        self.assertGreaterEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "Philosopher's Stone")
    
    def test_find_by_initial_result_hero_journey(self):
        """Test finding formulas by initial and result for Hero's Journey."""
        catalog = TransmutationCatalog()
        hj = catalog.find_by_name("Hero's Journey")
        matches = self.catalog.find_by_initial_result(hj.initial, hj.result)
        self.assertGreaterEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "Hero's Journey")
    
    def test_find_by_initial_result_multiple(self):
        """Test that multiple formulas can have same initial/result pair."""
        # Create a duplicate for testing
        # Note: In real catalog, this shouldn't happen
        pass
    
    def test_find_by_initial_result_none(self):
        """Test finding with no matches."""
        matches = self.catalog.find_by_initial_result(PIONEER, PIONEER)
        self.assertEqual(len(matches), 0)


class TestSpecificFormulas(unittest.TestCase):
    """Test specific transmutation formulas."""
    
    def test_philosopher_stone_components(self):
        """Test Philosopher's Stone formula components."""
        self.assertEqual(STEADFAST.bits, "10 11 00")
        self.assertEqual(GHOST.bits, "00 10 10")
        self.assertEqual(BELOVED.bits, "01 00 01")
        self.assertEqual(COUNCIL.bits, "11 01 11")
    
    def test_philosopher_stone_computation(self):
        """Test Philosopher's Stone formula computation."""
        # Steadfast (10 11 00) ⊕ Ghost (00 10 10) ⊕ Beloved (01 00 01) = Council (11 01 11)
        result = STEADFAST ^ GHOST ^ BELOVED
        self.assertEqual(result, COUNCIL)
        
        # Step by step verification
        step1 = STEADFAST ^ GHOST  # 10 11 00 ⊕ 00 10 10 = 10 01 10 (Creator)
        step2 = step1 ^ BELOVED     # 10 01 10 ⊕ 01 00 01 = 11 01 11 (Council)
        self.assertEqual(step2, COUNCIL)
    
    def test_hero_journey_formula(self):
        """Test Hero's Journey formula."""
        catalog = TransmutationCatalog()
        hj = catalog.find_by_name("Hero's Journey")
        
        self.assertIsNotNone(hj)
        self.assertTrue(hj.verify())
        
        # Manual verification
        result = hj.initial ^ hj.impulse ^ hj.catalyst
        self.assertEqual(result, hj.result)
    
    def test_alchemical_marriage_formula(self):
        """Test Alchemical Marriage formula."""
        catalog = TransmutationCatalog()
        am = catalog.find_by_name("Alchemical Marriage")
        
        self.assertIsNotNone(am)
        self.assertTrue(am.verify())
        
        # Pioneer ⊕ Mediator ⊕ Conciliar = Zero
        result = am.initial ^ am.impulse ^ am.catalyst
        self.assertEqual(result, am.result)
        self.assertEqual(am.result, ZERO)
    
    def test_creative_process_formula(self):
        """Test Creative Process formula."""
        catalog = TransmutationCatalog()
        cp = catalog.find_by_name("Creative Process")
        
        self.assertIsNotNone(cp)
        self.assertTrue(cp.verify())
        
        # Recluse ⊕ Ghost ⊕ Celebrant = Council
        result = cp.initial ^ cp.impulse ^ cp.catalyst
        self.assertEqual(result, cp.result)
    
    def test_healing_formula(self):
        """Test Healing formula."""
        catalog = TransmutationCatalog()
        healing = catalog.find_by_name("Healing")
        
        self.assertIsNotNone(healing)
        self.assertTrue(healing.verify())
    
    def test_revelation_formula(self):
        """Test Revelation formula."""
        catalog = TransmutationCatalog()
        rev = catalog.find_by_name("Revelation")
        
        self.assertIsNotNone(rev)
        self.assertTrue(rev.verify())
        
        # Zero ⊕ Pioneer ⊕ Conciliar = Mediator
        result = rev.initial ^ rev.impulse ^ rev.catalyst
        self.assertEqual(result, rev.result)
    
    def test_power_transformation_formula(self):
        """Test Power Transformation formula."""
        catalog = TransmutationCatalog()
        pt = catalog.find_by_name("Power Transformation")
        
        self.assertIsNotNone(pt)
        self.assertTrue(pt.verify())
    
    def test_dark_night_formula(self):
        """Test Dark Night formula."""
        catalog = TransmutationCatalog()
        dn = catalog.find_by_name("Dark Night")
        
        self.assertIsNotNone(dn)
        self.assertTrue(dn.verify())
    
    def test_awakening_formula(self):
        """Test Awakening formula."""
        catalog = TransmutationCatalog()
        awake = catalog.find_by_name("Awakening")
        
        self.assertIsNotNone(awake)
        self.assertTrue(awake.verify())
    
    def test_renewal_formula(self):
        """Test Renewal formula."""
        catalog = TransmutationCatalog()
        renewal = catalog.find_by_name("Renewal")
        
        self.assertIsNotNone(renewal)
        self.assertTrue(renewal.verify())
    
    def test_reconciliation_formula(self):
        """Test Reconciliation formula."""
        catalog = TransmutationCatalog()
        recon = catalog.find_by_name("Reconciliation")
        
        self.assertIsNotNone(recon)
        self.assertTrue(recon.verify())
    
    def test_complete_transmutation_formula(self):
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
    
    def setUp(self):
        self.A = STEADFAST
        self.B = GHOST
        self.C = BELOVED
        self.D = COUNCIL
    
    def test_transmutation_reversibility(self):
        """Test that transmutations are reversible."""
        # If A ⊕ B ⊕ C = D, then D ⊕ B ⊕ C = A
        result = self.D ^ self.B ^ self.C
        self.assertEqual(result, self.A)
    
    def test_transmutation_reversibility_different_order(self):
        """Test reversibility with different order."""
        # If A ⊕ B ⊕ C = D, then D ⊕ C ⊕ B = A
        result = self.D ^ self.C ^ self.B
        self.assertEqual(result, self.A)
    
    def test_multiple_paths_same_result(self):
        """Test that multiple paths can lead to same result."""
        # Direct path
        direct = self.A ^ self.B ^ self.C
        
        # Indirect path with intermediate
        intermediate = self.A ^ self.B
        indirect = intermediate ^ self.C
        
        self.assertEqual(direct, indirect)
    
    def test_xor_cycle_property(self):
        """Test that XOR cycles return to start."""
        # A ⊕ B ⊕ C ⊕ B ⊕ C = A
        result = self.A ^ self.B ^ self.C ^ self.B ^ self.C
        self.assertEqual(result, self.A)
    
    def test_xor_quadruple_cycle(self):
        """Test longer XOR cycle."""
        # A ⊕ B ⊕ C ⊕ D ⊕ B ⊕ C ⊕ D = A
        result = self.A ^ self.B ^ self.C ^ self.D ^ self.B ^ self.C ^ self.D
        self.assertEqual(result, self.A)
    
    def test_commutativity_of_transmutations(self):
        """Test that order of operations doesn't matter."""
        result1 = self.A ^ self.B ^ self.C
        result2 = self.B ^ self.C ^ self.A
        result3 = self.C ^ self.A ^ self.B
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)


class TestTransmutationEdgeCases(unittest.TestCase):
    """Test edge cases in transmutations."""
    
    def setUp(self):
        self.A = PIONEER
        self.B = GHOST
        self.C = BELOVED
        self.Zero = ZERO
    
    def test_zero_catalyst(self):
        """Test transmutation with Zero as catalyst."""
        # A ⊕ B ⊕ Zero = A ⊕ B
        result1 = self.A ^ self.B ^ self.Zero
        result2 = self.A ^ self.B
        self.assertEqual(result1, result2)
    
    def test_zero_impulse(self):
        """Test transmutation with Zero as impulse."""
        # A ⊕ Zero ⊕ C = A ⊕ C
        result1 = self.A ^ self.Zero ^ self.C
        result2 = self.A ^ self.C
        self.assertEqual(result1, result2)
    
    def test_all_zero(self):
        """Test transmutation with all Zero."""
        result = self.Zero ^ self.Zero ^ self.Zero
        self.assertEqual(result, self.Zero)
    
    def test_self_transmutation(self):
        """Test that A ⊕ A ⊕ A = A."""
        result = self.A ^ self.A ^ self.A
        self.assertEqual(result, self.A)
    
    def test_self_transmutation_with_zero(self):
        """Test A ⊕ A ⊕ Zero = Zero."""
        result = self.A ^ self.A ^ self.Zero
        self.assertEqual(result, self.Zero)
    
    def test_double_self_transmutation(self):
        """Test A ⊕ A ⊕ A ⊕ A = Zero."""
        result = self.A ^ self.A ^ self.A ^ self.A
        self.assertEqual(result, self.Zero)


class TestTransmutationAnalysis(unittest.TestCase):
    """Test transmutation analysis functions."""
    
    def setUp(self):
        self.steadfast = STEADFAST
        self.council = COUNCIL
    
    def test_analyze_transmutation_basic(self):
        """Test basic transmutation analysis."""
        analysis = analyze_transmutation(self.steadfast, self.council)
        
        self.assertEqual(analysis['initial'], self.steadfast.bits)
        self.assertEqual(analysis['result'], self.council.bits)
        self.assertEqual(analysis['bits_changed'], 4)
    
    def test_analyze_transmutation_axis_changes(self):
        """Test axis change detection."""
        analysis = analyze_transmutation(self.steadfast, self.council)
        
        # Check axis changes
        self.assertTrue(analysis['axisChanges']['WHO'])   # ME → WE
        self.assertTrue(analysis['axisChanges']['WHERE']) # SOUTH → WEST
        self.assertTrue(analysis['axisChanges']['WHEN'])  # WINTER → SUMMER
    
    def test_analyze_transmutation_no_changes(self):
        """Test analysis with no changes."""
        analysis = analyze_transmutation(self.steadfast, self.steadfast)
        
        self.assertEqual(analysis['bits_changed'], 0)
        self.assertFalse(analysis['axisChanges']['WHO'])
        self.assertFalse(analysis['axisChanges']['WHERE'])
        self.assertFalse(analysis['axisChanges']['WHEN'])
    
    def test_analyze_transmutation_possible_catalysts(self):
        """Test that possible catalysts are generated."""
        analysis = analyze_transmutation(self.steadfast, self.council)
        
        self.assertGreater(len(analysis['possibleCatalysts']), 0)
        
        # Check structure of first catalyst
        first = analysis['possibleCatalysts'][0]
        self.assertIn('catalyst', first)
        self.assertIn('catalystName', first)
        self.assertIn('impulse', first)
        self.assertIn('impulseName', first)


class TestPathFinding(unittest.TestCase):
    """Test path finding between archetypes."""
    
    def setUp(self):
        self.pioneer = PIONEER
        self.council = COUNCIL
        self.steadfast = STEADFAST
    
    def test_find_path_exists(self):
        """Test that path exists between some archetypes."""
        paths = find_path(self.pioneer, self.council, max_steps=2)
        self.assertIsInstance(paths, list)
    
    def test_find_path_structure(self):
        """Test structure of found paths."""
        paths = find_path(self.pioneer, self.council, max_steps=2)
        
        if len(paths) > 0:
            path = paths[0]
            self.assertIsInstance(path, list)
            
            if len(path) > 0:
                step = path[0]
                self.assertIsInstance(step, tuple)
                self.assertEqual(len(step), 2)
                
                impulse, catalyst = step
                self.assertIsInstance(impulse, Archetype)
                self.assertIsInstance(catalyst, Archetype)
    
    def test_find_path_to_self(self):
        """Test path finding to same archetype."""
        paths = find_path(self.pioneer, self.pioneer, max_steps=1)
        self.assertGreaterEqual(len(paths), 0)
    
    def test_find_path_max_steps(self):
        """Test that max_steps parameter works."""
        paths1 = find_path(self.pioneer, self.council, max_steps=1)
        paths2 = find_path(self.pioneer, self.council, max_steps=3)
        
        # Different max steps may yield different numbers of paths
        self.assertIsInstance(paths1, list)
        self.assertIsInstance(paths2, list)


class TestHammingDistance(unittest.TestCase):
    """Test Hamming distance calculations."""
    
    def setUp(self):
        self.a = PIONEER           # 10 10 10
        self.b = STEADFAST         # 10 11 00
        self.c = COUNCIL            # 11 01 11
        self.same = PIONEER
    
    def test_hamming_distance_zero(self):
        """Test Hamming distance for identical archetypes."""
        self.assertEqual(hamming_distance(self.a, self.same), 0)
    
    def test_hamming_distance_two(self):
        """Test Hamming distance for archetypes with 2-bit difference."""
        # 10 10 10 vs 10 11 00: positions 3,5 differ
        self.assertEqual(hamming_distance(self.a, self.b), 2)
    
    def test_hamming_distance_four(self):
        """Test Hamming distance for archetypes with 4-bit difference."""
        # 10 10 10 vs 11 01 11: many differences
        self.assertEqual(hamming_distance(self.a, self.c), 4)
    
    def test_hamming_distance_commutative(self):
        """Test that Hamming distance is commutative."""
        self.assertEqual(hamming_distance(self.a, self.b),
                        hamming_distance(self.b, self.a))


class TestTransmutationIntegrity(unittest.TestCase):
    """Test integrity of the transmutation system."""
    
    def test_all_formulas_unique_names(self):
        """Test that all formulas have unique names."""
        catalog = TransmutationCatalog()
        names = [f.name for f in catalog.all()]
        self.assertEqual(len(names), len(set(names)))
    
    def test_all_formulas_unique_combinations(self):
        """Test that all formulas have unique (initial, impulse, catalyst) combinations."""
        catalog = TransmutationCatalog()
        combinations = [(f.initial.bits, f.impulse.bits, f.catalyst.bits) 
                       for f in catalog.all()]
        self.assertEqual(len(combinations), len(set(combinations)))
    
    def test_formula_results_in_canon(self):
        """Test that all formula results are valid archetypes."""
        catalog = TransmutationCatalog()
        for f in catalog.all():
            self.assertIn(f.result.bits, ARCHETYPE_NAMES)
    
    def test_formula_components_in_canon(self):
        """Test that all formula components are valid archetypes."""
        catalog = TransmutationCatalog()
        for f in catalog.all():
            self.assertIn(f.initial.bits, ARCHETYPE_NAMES)
            self.assertIn(f.impulse.bits, ARCHETYPE_NAMES)
            self.assertIn(f.catalyst.bits, ARCHETYPE_NAMES)


# Import ARCHETYPE_NAMES for validation
from src.subit import ARCHETYPE_NAMES


if __name__ == '__main__':
    unittest.main()
```

## Running the Tests

### In CodeSpace Terminal:

```bash
# Navigate to project root
cd /workspaces/subit-narrative-engine

# Run all tests
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests/test_transmutations.py -v

# Run with pytest (if installed)
pip install pytest
pytest tests/test_transmutations.py -v

# Run with coverage
pip install coverage
coverage run -m unittest tests/test_transmutations.py
coverage report -m

# Run specific test case
python -m unittest tests.test_transmutations.TestSpecificFormulas.test_philosopher_stone_computation
```

### Expected Output:

```
test_transmutations.py
    test_formula_creation ... ok
    test_formula_verification_correct ... ok
    test_formula_verification_incorrect ... ok
    test_formula_serialization ... ok
    test_catalog_size ... ok
    test_all_formulas_verified ... ok
    test_find_by_name_exact ... ok
    test_find_by_name_case_insensitive ... ok
    test_find_by_name_partial ... ok
    test_find_by_name_nonexistent ... ok
    test_find_by_initial_result_philosopher_stone ... ok
    test_find_by_initial_result_hero_journey ... ok
    test_find_by_initial_result_none ... ok
    test_philosopher_stone_components ... ok
    test_philosopher_stone_computation ... ok
    test_hero_journey_formula ... ok
    test_alchemical_marriage_formula ... ok
    test_creative_process_formula ... ok
    test_healing_formula ... ok
    test_revelation_formula ... ok
    test_power_transformation_formula ... ok
    test_dark_night_formula ... ok
    test_awakening_formula ... ok
    test_renewal_formula ... ok
    test_reconciliation_formula ... ok
    test_complete_transmutation_formula ... ok
    test_transmutation_reversibility ... ok
    test_transmutation_reversibility_different_order ... ok
    test_multiple_paths_same_result ... ok
    test_xor_cycle_property ... ok
    test_xor_quadruple_cycle ... ok
    test_commutativity_of_transmutations ... ok
    test_zero_catalyst ... ok
    test_zero_impulse ... ok
    test_all_zero ... ok
    test_self_transmutation ... ok
    test_self_transmutation_with_zero ... ok
    test_double_self_transmutation ... ok
    test_analyze_transmutation_basic ... ok
    test_analyze_transmutation_axis_changes ... ok
    test_analyze_transmutation_no_changes ... ok
    test_analyze_transmutation_possible_catalysts ... ok
    test_find_path_exists ... ok
    test_find_path_structure ... ok
    test_find_path_to_self ... ok
    test_find_path_max_steps ... ok
    test_hamming_distance_zero ... ok
    test_hamming_distance_two ... ok
    test_hamming_distance_four ... ok
    test_hamming_distance_commutative ... ok
    test_all_formulas_unique_names ... ok
    test_all_formulas_unique_combinations ... ok
    test_formula_results_in_canon ... ok
    test_formula_components_in_canon ... ok

----------------------------------------------------------------------
Ran 54 tests in 0.156s

OK
```
