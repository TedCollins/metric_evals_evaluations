# Multiple-choice scoring

_Last updated: 2026-11-11_

> **In one sentence:** "Did the model pick the right option?" sounds unambiguous, but there are several ways to decide *which* option a model picked, and they can produce very different scores.

## The problem

A language model doesn't tick a box. It produces text, or a probability for each possible next word. So evaluators have to choose how to turn the model's output into a letter:

| Method | What's measured | Trade-off |
|--------|-----------------|-----------|
| **Letter probability** | Which of "A"/"B"/"C"/"D" the model rates most likely to come next | Fast. It can reward a model that has learned the *format* even when its knowledge is weak. |
| **Answer-text probability** | Which full answer text the model rates most likely | Doesn't depend on letters, but is biased toward short or common phrases unless adjusted for length. |
| **Generate and parse** | Let the model write freely, then extract its answer | Closest to real use, but answers that don't parse, or that don't match the expected wording, are marked wrong. |

## Why it matters

The same model on the same questions can score 15 points apart depending on the method ([MMLU example](../benchmarks/knowledge-reasoning/mmlu.md#how-its-scored)). Even **shuffling the order of the options** can move models several places up or down a leaderboard.

## What it means for readers

Only compare multiple-choice scores when they were measured **with the same method and setup**. If a report doesn't say how answers were extracted, treat small differences with suspicion.
