# 🎲 TCG Probability Engine

> A combinatorial analysis framework for modeling decision consistency and risk in sequential card games.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Overview

This engine calculates the probability of executing specific strategies in Trading Card Games (TCGs) using **exact multivariate hypergeometric distributions**. 

While built around *Pokémon TCG Pocket* as a case study, the underlying logic models **sequential decision-making under uncertainty with constraints** — directly applicable to:
- **Risk Analysis**: Modeling fraud rule cascades and transaction approval probabilities.
- **Product Analytics**: Simulating feature impact on user success funnels.
- **Data Engineering**: Building configurable, testable probability pipelines.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation
1. Clone the repository:
   `git clone https://github.com/YOUR_USERNAME/tcg-probability-engine.git`
2. Install dependencies:
   `pip install -r requirements.txt`

### Run the Example
`python examples/pocket_combo.py`

**Expected Output:**
- Turn 1 Success Rate: 64.49%
- Path A (Combo in opening): 55.44%
- Path B (Turn draw): 5.47%
- Path C (DS dig): 3.59%

### Run Tests
`pytest tests/ -v`

---

## 🧠 Methodology

The engine uses **exact multivariate hypergeometric enumeration** to calculate probabilities without simulation error.

**Key Components:**
1. **Opening Hand Distribution**: P(EB=e, Target=t, DS=d, Other=o) for all valid combinations.
2. **Sequential Draw Logic**: Models turn draw → supporter decision → dig effect as a conditional probability tree.
3. **Gate Constraints**: Enforces rules like "Must have Energy Baby in Active before playing Supporter."

---

## 📊 Case Study: Pokémon TCG Pocket

### Deck Configuration
| Card Type | Count | Role |
|-----------|-------|------|
| Energy Baby (EB) | 4 | Gate requirement (must be in opening) |
| EX Pokémon (EX) | 4 | Win condition |
| EX Searcher (ES) | 1 | Tutor: fetches EX from deck |
| Draw Supporter (DS) | 2 | Dig: draws 2 extra cards |
| Other | 9 | Utility / fallback |

### Key Findings
| Metric | Value | Insight |
|--------|-------|---------|
| **Turn 1 Success Rate** | **64.49%** | ~2 out of 3 games execute combo |
| **P(EB in Opening)** | 71.83% | Largest failure mode (28% miss rate) |
| **P(Target \| EB)** | 77.18% | When EB is present, combo usually ready |
| **Dig Success Rate** | 73.63% | DS + turn draw sequential advantage |

### Sensitivity Analysis
| Deck Change | New Success Rate | Delta |
|-------------|-----------------|-------|
| **Base Deck** | 64.49% | — |
| +1 Energy Baby | ~67.8% | +3.3% (Highest ROI) |
| +1 Draw Supporter | ~66.1% | +1.6% |
| +1 Target (EX/ES) | ~68.2% | +3.7% |

---

## 🛠️ Architecture

- `src/probability.py`: Core hypergeometric calculation engine
- `examples/pocket_combo.py`: Pre-configured Pocket deck analysis
- `tests/test_probability.py`: Unit tests for edge cases & accuracy
- `docs/methodology.md`: Mathematical derivation
- `requirements.txt`: Python dependencies

### Design Principles
- **Exact over Approximate**: Uses combinatorial enumeration instead of simulation where feasible.
- **Configurable**: Deck composition and rules defined via function parameters.
- **Tested**: Edge cases (e.g., eb_count=0) explicitly handled and validated.
- **Extensible**: Modular design supports additional TCGs (Magic, Yu-Gi-Oh!) with rule presets.

---

## 💼 Career Relevance

This project demonstrates skills transferable to multiple data roles:

| Role | Relevant Skills Demonstrated |
|------|-----------------------------|
| **Fraud/Risk Analyst** | Probabilistic risk modeling, Conditional rule logic, Sensitivity analysis |
| **Product Data Analyst** | Funnel analysis, Feature impact simulation, Metric definition |
| **Data Engineer** | Modular Python design, Configuration-driven logic, Unit testing |

### Interview Talking Points
"I built a probability engine that models sequential decision-making under constraints. It uses exact combinatorial math to calculate success rates, handles edge cases like 'gate requirements,' and includes sensitivity analysis to quantify the impact of configuration changes."

---

## 🗺️ Roadmap

- [x] v1.0: Core hypergeometric engine
- [x] v1.0: Unit test coverage
- [ ] v1.1: JSON/YAML deck configuration
- [ ] v1.1: Monte Carlo simulation fallback
- [ ] v1.2: Interactive Streamlit dashboard
- [ ] v2.0: Multi-TCG support

---

## 📬 Contact

**Your Name** — rifqisyahr@gmail.com  
**GitHub**: github.com/docksgit  
**LinkedIn**: linkedin.com/in/rifqisyahr

---

<p align="center">
  <strong>If you found this useful, please ⭐ star the repository!</strong>
</p>
