# Contamination

_Last updated: 2026-11-11_

> **In one sentence:** Contamination is when a model has already seen the test questions during training, so a high score may reflect memory, not ability.

## Why it happens

Modern AI models learn from huge amounts of text gathered from the web. Many benchmarks are *also* on the web: in GitHub repositories, on dataset sites, in blog posts that quote questions, and in practice-exam sites the questions were originally taken from. Unless a model's builders deliberately filter that text out, the test ends up in the study material.

## An analogy

It's like a student who has seen last year's exam *with the answers* before the test. A high mark is still possible if they understand the subject, but you can no longer tell.

## How researchers detect it

- **Overlap search:** look for test questions word-for-word in the training data. This only works if the training data is public, which it often isn't.
- **Fill-in-the-blank probes:** hide part of a test question, such as one *wrong* answer option, and see whether the model can reproduce it exactly. A model that has never seen the question shouldn't manage this. (Example: [MMLU](../benchmarks/knowledge-reasoning/mmlu.md#contamination-and-saturation).)
- **Fresh variants:** rewrite or re-create the questions. A large drop in score on the new versions suggests memorization.

## What it means for readers

A contaminated benchmark can still be informative, but it **overstates** ability, and by an unknown amount. Benchmarks that are newer, kept private, or regularly refreshed are more trustworthy for comparing recent models.
