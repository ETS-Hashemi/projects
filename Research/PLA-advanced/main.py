import sys
from scenario_loader import load_scenario
from prob import InferenceEngine

def main():
    # Check if scenario file and context number are provided as arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <scenario_config.json> <context_number>")
        sys.exit(1)

    # Load the scenario from the configuration file
    config_path = sys.argv[1]
    context_number = sys.argv[2]
    kb, queries = load_scenario(config_path)

    # Display the knowledge base
    print("=" * 60)
    print("                  KNOWLEDGE BASE")
    print("=" * 60)
    print("\nFacts:")
    for fact in kb.facts:
        print(f"  - {fact}")
    print("\nRules:")
    for rule in kb.rules:
        print(f"  - {rule}")
    print("=" * 60)

    # Set the context based on the context number
    context = {}
    try:
        context_number = int(context_number)  # Convert context_number to an integer
        for rule in kb.rules:
            if hasattr(rule, "context") and str(context_number) in rule.context:
                context.update(rule.context[str(context_number)])
    except ValueError:
        print("Error: Context number must be an integer.")
        sys.exit(1)

    kb.set_context(context)

    # Display the active context
    print("\n                  ACTIVE CONTEXT")
    print("=" * 60)
    if context:
        for var, weight in context.items():
            print(f"  - {var}: Weight = {weight}")
    else:
        print("  No active context variables.")
    print("=" * 60)

    # Initialize the inference engine
    engine = InferenceEngine(kb)

    # Query the knowledge base
    print("\n                  QUERIES AND RESULTS")
    print("=" * 60)
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        prob, explanation = engine.query(query)
        print(f"  Probability: {prob:.3f}")
        print("  Explanation:")
        for sentence in explanation.split("\n"):
            print(f"    - {sentence.strip()}")
        print("-" * 60)

if __name__ == "__main__":
    main()