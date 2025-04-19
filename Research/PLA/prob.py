class ProbabilisticReasoner:
    def __init__(self):
        self.rules = {}

    def add_rule(self, rule):
        """Add a probabilistic rule to the reasoner."""
        condition, probability = rule.split("=")
        condition = condition.strip()[2:-1]  # Extract condition inside P()
        probability = float(probability.strip())
        self.rules[condition] = probability

    def query(self, query, facts):
        """
        Return the probability of the query if conditions are satisfied.
        :param query: The query symbol.
        :param facts: A set of facts from the knowledge base.
        """
        for condition, probability in self.rules.items():
            # Split the condition into individual symbols
            condition_symbols = [symbol.strip() for symbol in condition.split(",")]
            if query in condition_symbols:
                # Check if all other symbols in the condition are in the facts
                if all(symbol in facts for symbol in condition_symbols if symbol != query):
                    return probability, f"Rule P({condition}) = {probability}"
        return 0.0, f"No rule found for P({query})"

class ProbSymbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, ProbSymbol) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

class ProbRule:
    def __init__(self, condition, result, probability):
        self.condition = condition  # List of ProbSymbols
        self.result = result        # ProbSymbol
        self.probability = probability

    def __repr__(self):
        conditions = " and ".join([str(c) for c in self.condition])
        return f"If {conditions} -> {self.result} ({self.probability})"

class ProbKB:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        if isinstance(fact, str):
            fact = ProbSymbol(fact)
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def query(self, query):
        if isinstance(query, str):
            query = ProbSymbol(query)

        # Forward chaining to infer new facts with probabilities
        inferred_facts = {fact: 1.0 for fact in self.facts}  # Facts with certainty
        explanations = []
        while True:
            new_facts = {}
            for rule in self.rules:
                if rule.result not in inferred_facts:
                    # Check if all conditions are satisfied
                    conditions_met = all(c in inferred_facts for c in rule.condition)
                    if conditions_met:
                        # Calculate the probability of the result
                        prob = rule.probability * min(inferred_facts[c] for c in rule.condition)
                        new_facts[rule.result] = prob
                        explanations.append(f"Rule applied: {rule} with P={prob}")
            if not new_facts:
                break
            inferred_facts.update(new_facts)

        # Check if the query is in the inferred facts
        if query in inferred_facts:
            explanation = " -> ".join(explanations)
            return inferred_facts[query], explanation

        return 0.0, "No matching rule found."

class InferenceEngine:
    def __init__(self, kb):
        self.kb = kb

    def query(self, query):
        return self.kb.query(query)
