"""
examples/pocket_combo.py

Run the probability calculation for the specific Pocket deck discussed.
"""
import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.probability import calc_pocket_turn1_success

if __name__ == "__main__":
    print("🎮 Pokémon TCG Pocket — Turn 1 Combo Probability\n")
    print("Deck: 20 cards")
    print("  • Energy Baby (EB): 4")
    print("  • EX Pokémon (EX): 4")
    print("  • EX Searcher (ES): 1")
    print("  • Draw Supporters (DS): 2")
    print("  • Other: 9")
    print("\n" + "="*50 + "\n")
    
    result = calc_pocket_turn1_success(verbose=True)
    
    print("\n" + "="*50)
    print(f"🏁 FINAL: Turn 1 Success Rate = {result['total_success']:.2%}")
    print(f"   (Expected: ~64.49%)")