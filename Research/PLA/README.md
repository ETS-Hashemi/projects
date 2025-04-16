# 🧠 Probabilistic Logic Agent Framework

## Overview

The **Probabilistic Logic Agent Framework** is a Python-based system that integrates **symbolic propositional logic** with **probabilistic reasoning**. It enables reasoning in **uncertain environments** using **weighted logical rules** to infer probabilistic outcomes. Designed for **explainability** and **modularity**, this framework is ideal for domains like auditing, legal reasoning, medical AI, and decision support systems.

---

## 🎯 Motivation

Real-world decisions often involve uncertainty, such as:
> "If A and B, then probably C."

Existing AI systems force a choice between:
- **Symbolic logic**: Explainable but rigid and not uncertainty-aware.
- **Probabilistic models**: Flexible but opaque and not rule-driven.

This framework bridges the gap by combining **rules with probabilities**, enabling agents to answer **what they believe**, **how confident they are**, and **why**.

---

## 🚀 Features

- Define rules like `"If A and B → C (0.9)"`.
- Add facts to a knowledge base and query for probabilities.
- Trace all rule activations and logic chains for full explainability.
- Lightweight, modular architecture with no heavy dependencies.
- Works in low-data environments and supports easy rule editing.

---

## 🛠 Installation

```bash
git clone https://github.com/YOUR_USERNAME/probabilistic-logic-agent.git
cd probabilistic-logic-agent
pip install -r requirements.txt
```

> 📌 **Note**: This repository is private during development for novelty protection.

---

## 🧬 Example Usage

```python
from prob_agent import ProbSymbol, ProbRule, ProbKB, InferenceEngine

# Define symbols
large = ProbSymbol("LargeTransaction")
no_receipt = ProbSymbol("NoReceipt")
fraud = ProbSymbol("Fraud")

# Define a probabilistic rule
rule1 = ProbRule(
    condition=[large, no_receipt],
    result=fraud,
    probability=0.85
)

# Set up the knowledge base
kb = ProbKB()
kb.add_fact(large)
kb.add_fact(no_receipt)
kb.add_rule(rule1)

# Query the KB
engine = InferenceEngine(kb)
prob, explanation = engine.query(fraud)

print(f"P(Fraud) = {prob}")
print("Explanation:")
print(explanation)
```

---

## 🔍 Applications

- **Auditing & Accounting**: Fraud detection using rules like "Large transaction + no receipt = suspicious."
- **Legal Reasoning**: Evaluate liability or guilt from structured case facts.
- **Medical Diagnosis**: Diagnose based on symptoms with known probabilities.
- **Educational AI**: Infer student understanding from indirect indicators.
- **AI Governance**: Rule-aware, safe agents for decision support.

---

## 🧱 Planned Architecture

```
prob_agent/
│
├── symbols.py            # ProbSymbol class
├── rules.py              # ProbRule class
├── knowledge_base.py     # ProbKB class
├── inference.py          # InferenceEngine class
├── explanation.py        # Tracks reasoning chains
├── examples/             # Jupyter notebooks and real-world tests
├── tests/                # Unit tests
└── README.md             # Project documentation
```

---

## 📚 Roadmap

### ✅ Phase 1: Core Framework
- [x] Implement `ProbSymbol`, `ProbRule`, `ProbKB`.
- [x] Build inference engine with model checking.
- [x] Add traceable explanations.

### 🔄 Phase 2: Modular Extensions
- [ ] Add forward chaining and probabilistic facts.
- [ ] Integrate `pgmpy` or `pomegranate` for advanced inference.
- [ ] Optimize performance for large rule sets.

### 🧪 Phase 3: Evaluation
- [ ] Benchmark in domains like auditing, medical, and legal reasoning.
- [ ] Collect feedback on transparency and usability.

### 📝 Phase 4: Publication
- [ ] Write research paper for venues like IJCAI or RuleML.
- [ ] Prepare polished GitHub repo and Colab demo.

---

## 📄 License

Licensed under the **Apache License 2.0**.  
© 2025 Seyed Masoud Hashemi Ahmadi.

---

## 📬 Contact

For collaboration or inquiries:  
📧 [contact@AiCentralLab.com](mailto:contact@AiCentralLab.com)

