# Probabilistic Logic Agent Framework

## Overview

The **Probabilistic Logic Agent Framework** integrates symbolic and probabilistic reasoning with context-aware adjustments, and now also supports modeling complex parallel scenarios across diverse domains such as accounting, auditing, pharmaceutical, oncology, and logistics.

---

## Features

- **Hybrid Reasoning**: Combines symbolic logic with probabilistic reasoning.
- **Context-Aware Reasoning**: Dynamically adjusts rule probabilities using context variables.
- **Parallel Scenario Modeling**: Define and manage complex domain-specific scenarios in separate JSON files. For example:
  - `scenario_accounting_parallel.json`
  - `scenario_auditing_parallel.json`
  - `scenario_pharmaceutical_parallel.json`
  - `scenario_oncology_parallel.json`
  - `scenario_logistics_complex.json`
- **Explainability**: Provides clear reasoning chains for each query.
- **Modular and Lightweight**: Easily extended to support additional domains with minimal dependencies.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/probabilistic-logic-agent.git
   cd probabilistic-logic-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Use the Framework

### 1. Configure Scenarios

Use domain-specific JSON files to define facts, rules (including context data), and queries.

Example:
```json
{
  "facts": [
    "PersistentCough",
    "WeightLoss",
    "ChestPain"
  ],
  "rules": [
    {
      "condition": ["PersistentCough", "WeightLoss"],
      "result": "LungCancerRisk",
      "probability": 0.7,
      "context": {
        "1": {
          "AgeOver60": 1.2
        },
        "2": {
          "SmokingHistory": 1.3
        }
      }
    },
    {
      "condition": ["LungCancerRisk", "ChestPain"],
      "result": "BiopsyRequired",
      "probability": 0.9,
      "context": {
        "1": {
          "FamilyHistoryOfCancer": 1.0
        },
        "2": {
          "HighTumorMarkerLevels": 1.1
        }
      }
    }
  ],
  "queries": [
    "LungCancerRisk",
    "BiopsyRequired"
  ]
}
```
In this example, after loading the scenario, the framework “flattens” the rule contexts—only the active context (e.g., `"1"` or `"2"`) is used for probability adjustments.

### 2. Select a Scenario and Context

Run the framework with the desired scenario configuration:
```bash
python main.py <scenario_config.json> [context_number]
```
If the context number is omitted, it defaults to "1".

### 3. Examine Results

The output will display the knowledge base, active context, and query results, including adjusted probabilities.

### 4. Sample Output

Here’s an example output for the `scenario_pharmaceutical_complex.json` file:

```
==================================================
                KNOWLEDGE BASE
==================================================
Facts:
  • AdverseReaction
  • NewDrug
  • MultipleReports
  • RegulatoryWarning

Rules:
  • If AdverseReaction and NewDrug -> RecallRequired (0.7)
  • If MultipleReports and RegulatoryWarning -> RecallRequired (0.9)
  • If RecallRequired -> PublicNotification (0.95)
==================================================

                QUERIES AND RESULTS
==================================================
Query: PublicNotification
  Probability: 0.855
  Explanation:
    - AdverseReaction and NewDrug triggered RecallRequired with P=0.7
    - MultipleReports and RegulatoryWarning triggered RecallRequired with P=0.9
    - RecallRequired triggered PublicNotification with P=0.855
--------------------------------------------------
```

---

## Advanced Features

### Context-Aware Reasoning

The framework supports **context-aware reasoning**, where rule probabilities are dynamically adjusted based on the current context. For example:

```python
# Set the context
context = {"PatientAge>60": True, "SmokingHistory": True}
kb.set_context(context)
```

Rules can define context variables and their weights. For example:
```json
{
  "condition": ["PersistentCough", "WeightLoss"],
  "result": "LungCancerRisk",
  "probability": 0.7,
  "context": {
    "PatientAge>60": 1.2,
    "SmokingHistory": 1.5
  }
}
```

---

### Using the Hybrid Engine

The framework supports hybrid reasoning by combining symbolic and probabilistic reasoning. For example:

```python
from engine import HybridEngine
from kb import KnowledgeBase
from prob import ProbKB, ProbSymbol, ProbRule

# Symbolic KB
symbolic_kb = KnowledgeBase()
symbolic_kb.add_fact("A")
symbolic_kb.add_fact("B")
symbolic_kb.add_rule("A and B -> C")

# Probabilistic KB
prob_kb = ProbKB()
large = ProbSymbol("LargeTransaction")
no_receipt = ProbSymbol("NoReceipt")
fraud = ProbSymbol("Fraud")
rule = ProbRule([large, no_receipt], fraud, 0.85)
prob_kb.add_fact(large)
prob_kb.add_fact(no_receipt)
prob_kb.add_rule(rule)

# Hybrid Engine
hybrid_engine = HybridEngine(symbolic_kb, prob_kb)
result, explanation = hybrid_engine.query("C")
print(f"Result: {result}")
print(f"Explanation: {explanation}")
```

---

## Applications

- **Auditing & Accounting**: Detect fraud based on transaction patterns.
- **Medical Diagnosis**: Infer diagnoses from clinical indicators.
- **Legal Reasoning**: Evaluate liability from structured case facts.
- **Educational AI**: Support decision making in learning environments.
- **Supply Chain Optimization**: Adjust strategies based on dynamic market conditions.

---

## License

Licensed under the **Apache License 2.0**.  
© 2025 Seyed Masoud Hashemi Ahmadi.

---

## Contact

For collaboration or inquiries:  
📧 [contact@AiCentralLab.com](mailto:contact@AiCentralLab.com)

