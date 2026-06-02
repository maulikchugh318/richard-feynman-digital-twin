from research.analyzer import ResearchAnalyzer


project_text = """
Project Title: Understanding Quantum Electrodynamics

This project attempts to explain quantum electrodynamics using animated diagrams and simplified analogies.

The system explains how photons mediate electromagnetic interactions between charged particles.

The project focuses on intuitive understanding rather than mathematical derivations.

The objective is to make advanced physics accessible to undergraduate students.
"""

analyzer = ResearchAnalyzer()

review = analyzer.analyze_project(
    project_text,
    max_words=500
)

print(review)