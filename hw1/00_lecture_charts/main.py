"""Entry point: render every lecture-5 and lecture-6 figure from the fast-food data."""

import deck5_visualization
import deck6_distributions
import deck9_hypothesis
import deck10_pvalue
import skew_cases
from data import load
from style import FIG_DIR, apply_style


def main() -> None:
    apply_style()
    df = load()
    print(f"dataset: {df.shape[0]} items x {df.shape[1]} variables\n")

    print("Deck 5 - Basic Statistics and Visualization")
    deck5 = deck5_visualization.build_all(df)
    print(f"  {len(deck5)} figures\n")

    print("Deck 6 - Data and Distributions")
    deck6 = deck6_distributions.build_all(df)
    print(f"  {len(deck6)} figures\n")

    print("Deck 9 - Hypothesis Testing")
    deck9 = deck9_hypothesis.build_all()
    print(f"  {len(deck9)} figures\n")

    print("Deck 10 - P-value")
    deck10 = deck10_pvalue.build_all()
    print(f"  {len(deck10)} figures\n")

    print("Book 2.3.2 - Skew sign and direction")
    skew = skew_cases.build_all()
    print(f"  {len(skew)} figures\n")

    print(f"wrote {len(deck5) + len(deck6) + len(deck9) + len(deck10) + len(skew)} figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
