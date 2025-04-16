# 🧠 Seyed Masoud Hashemi Ahmadi — Ongoing AI Research Projects

This repository documents and organizes the set of high-impact, novel research projects I am currently developing in the area of **symbolic reasoning**, **probabilistic logic**, and **explainable intelligent agents**.

All projects are being developed in **Python**, with a focus on **educational value**, **open scientific contribution**, and **real-world decision support applications**.

---

## 📊 Project Landscape Summary

| Extension | Academic Maturity | Novelty Today | Python Open Implementation | Publication Chance |
|----------|-------------------|----------------|------------------------------|---------------------|
| **Temporal Logic (LTL/CTL) Agents** | Rare in education, moderate in theory | ★★★★☆ | Almost none | 🔥 **HIGH** |
| **First-Order Logic (FOL) Agent** | Common in theory, rare in practical CS | ★★★☆☆ | Very few tools | ⚖️ **MEDIUM** |
| **Probabilistic Logic Agents** *(active)* | Active research (PGMs), but not integrated with symbolic KBs well | ⭐⭐⭐⭐⭐ | Very rare in symbolic+probabilistic blend | 🚀 **VERY HIGH** |
| **Multi-Agent KB System with Communication** | Explored conceptually, almost no educational tools | ⭐⭐⭐⭐⭐ | Not done in Python for education | 🚀 **VERY HIGH** |
| **XAI for Logical Reasoning (Traceable Inference)** | Talked about, few visual tools | ⭐⭐⭐⭐☆ | Basically none exist | 🔥 **HIGH** |
| **Hybrid Symbolic-Neural KB Agents** | Hot area, hard to do cleanly | ⭐⭐⭐☆☆ | Some experiments, no educational examples | ⚖️ **MEDIUM** |

---

## 📂 Current Work

### 🔷 [`PLA/`](./PLA) — Probabilistic Logic Agent Framework (active)

> A novel Python-based framework that integrates symbolic propositional logic with probabilistic reasoning, enabling agents to reason under uncertainty with full traceability and modular design.

- Combines logic rules (e.g. `A ∧ B → C`) with probabilistic weights (`0.9`)
- Designed for domains such as auditing, law, and AI safety
- Fully explainable inference
- Modular, human-readable, educational architecture
- Will be published under Apache License

📌 **Status**: Architecture complete, core engine under construction  
📅 **Goal**: Research paper submission by June–July 2025

---

## 🧠 Upcoming Projects (Planned)

### 🕒 `TemporalLogicAgent/`
- Agent that reasons about sequences of events over time using LTL/CTL
- Ideal for decision systems where *eventual* truths or obligations matter (e.g., planning, compliance)
- Will include time-step-based KB, temporal model checker, and interactive visualization

📌 **Planned start**: Summer 2025  
🎯 **Target**: ICAPS or KR workshops

---

### 🧠 `FOLAgent/`
- First-order logic agent with support for variables, quantifiers (`∀`, `∃`), and substitution
- Aims to fill the educational tooling gap for teaching FOL inference in Python
- Possibly extendable to resolution or unification-based theorem proving

📌 **Planned start**: Fall 2025  
🎯 **Target**: Education or AI logic workshops

---

### 🧠 `MultiAgentKB/`
- A multi-agent system where agents each hold independent KBs
- Supports rule exchange, belief negotiation, and consistency checks
- Agents may disagree, revise beliefs, or follow authority weighting
- Ideal for research in distributed reasoning and argumentation

📌 **Planned start**: Q3 2025  
🎯 **Target**: AAMAS, JAAMAS, or RuleML

---

### 🧠 `XAI-Logic-Explainer/`
- Visualization layer to add **traceability** to all symbolic or probabilistic logic agents
- Converts inference steps into readable chains or graphs using `networkx` or `Graphviz`
- Enables human-centered audits and debug views of decision logic

📌 **Planned start**: Q2 2025  
🎯 **Target**: AI & Society or Explainable AI venues

---

### 🧠 `NeuroSymbolic-KB/`
- Exploration into combining neural embedding models (e.g., BERT) with symbolic rules
- Goal is to enrich symbolic rules with latent features and improve recall
- Could be used for hybrid document reasoning or semi-structured inference

📌 **Planned start**: TBD (dependent on compute resources)  
🎯 **Target**: NeSy, NeurIPS workshop, or ECAI

---

## 📄 License

All code is licensed under the **Apache License 2.0**, unless otherwise noted.

---

##  Academic Attribution

This project is developed as part of the PhD research of  
**Seyed Masoud Hashemi Ahmadi**  
at **École de technologie supérieure (ÉTS), Montréal**.

If you use this work in academic research, citation is appreciated.


📬 [contact@AiCentralLab.com](mailto:contact@AiCentralLab.com)

---

## 🔐 Repository Status

- Current repositories are **private** due to research novelty
- To be made public following publication or preprint submission
- GitHub branch protection, 2FA, and backup repositories in place

---

## 📅 Timeline

| Phase | Dates | Description |
|-------|-------|-------------|
| **PLA Core Engine** | Apr–May 2025 | Base logic + probabilistic inference |
| **PLA Evaluation** | Jun 2025 | Benchmarks + use cases (audit, med, legal) |
| **Paper Draft & Submission** | Jul 2025 | RuleML, IJCAI, or XAI workshops |
| **Temporal Logic Agent Start** | Summer 2025 | Model checker with LTL |
| **FOL Agent Build** | Fall 2025 | Unification + resolution |
| **Multi-Agent System** | Q3 2025 | Agent interaction logic |
| **Traceable XAI Layer** | Ongoing | Shared across all projects |

---

## 📌 Goals

- Deliver the **first lightweight Python framework** combining symbolic logic with uncertainty
- Make logical AI **explainable, teachable, and applicable**
- Publish multiple **modular research agents** for auditing, safety, and reasoning under uncertainty

---

