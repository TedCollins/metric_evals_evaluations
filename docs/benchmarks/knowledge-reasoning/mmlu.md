# MMLU (Massive Multitask Language Understanding)

_Last updated: 2026-11-11 · Area: Knowledge & reasoning_

> **In one sentence:** MMLU is a 14,000-question multiple-choice exam covering 57 school and professional subjects, from elementary math to law and medicine. It was the most widely quoted "how smart is this AI?" number from 2021 to 2024.

| | |
|---|---|
| **Released** | September 2020, Hendrycks et al. (UC Berkeley and collaborators) [1] |
| **Size** | ~15,900 questions: 14,042 test, 1,531 validation, 285 "dev" examples (5 per subject) [2]. The paper reports slightly different counts (14,079 test, 1,540 validation) [1]. |
| **Format** | Multiple choice, 4 options (A–D) |
| **Metric** | Accuracy (% of questions answered correctly), usually averaged over the 57 subjects |
| **Random guessing** | 25% |
| **Human baseline** | 34.5% for non-expert crowdworkers; ~89.8% estimated for experts [1] |
| **Top scores** | High 80s to low 90s for frontier models since 2024 (e.g. GPT-4o: 88.7%, vendor-reported, May 2024) [9] |
| **Status** | **Saturated.** Top models are close to the ceiling set by its own answer-key errors (see below). |

---

## What it claims to test

The authors wanted a test of **broad knowledge and problem-solving**, the kind of things a person learns across a whole education, instead of narrow language skills. Earlier benchmarks (such as GLUE and SuperGLUE) tested things like grammar and sentence understanding, and models had already caught up with humans on them. MMLU's pitch was: *don't just check whether the model understands sentences; check whether it knows things and can apply them, the way exams check students.* [1]

The questions are grouped into four broad areas: **Humanities**, **Social Science**, **STEM** and **Other** (e.g. medicine, business, nutrition). [1]

## What it actually tests

Mostly, **recognizing the right answer among four options for questions in exam style**. In practice, that breaks down into:

- **Recall of facts.** Most questions are "do you know this?" items lifted from practice tests and course materials. Graduate and undergraduate students collected the questions from freely available sources online, including practice questions for exams like the GRE and the US Medical Licensing Examination, and undergraduate course materials. [1]
- **Some reasoning.** The math, physics and logic subjects need a few steps of reasoning, but these are a minority of the 57 subjects.
- **Skill at taking multiple-choice tests.** Picking from four options is easier than producing an answer from nothing. A model can rule out obviously wrong options, or pick up on wording that hints at the answer, without fully knowing the material.

What it **doesn't** test: writing, explaining, holding a conversation, following instructions, or doing anything useful with the knowledge. A high MMLU score means "it does well on exam questions about this subject", not "it can work as a doctor or lawyer".

> **Key idea:** because the questions come from *publicly available* practice materials, the same text (or close paraphrases) may appear in the web data AI models learn from. See [contamination](../../concepts/contamination.md).

## Example items

Real items from the MMLU test split [2]. **Bold** marks the answer key.

**High school geography**
> The tendency for a population to continue to grow long after replacement fertility has been achieved is called
> (A) zero population growth. (B) rapid growth rate. (C) homeostatic plateau. **(D) demographic momentum.**

This is pure recall: either you've met the term or you haven't.

**College mathematics**
> Suppose P is the set of polynomials with coefficients in Z₅ and degree less than or equal to 7. If the operator D sends p(x) in P to its derivative p′(x), what are the dimensions of the null space n and range r of D?
> (A) n = 1 and r = 6 (B) n = 1 and r = 7 (C) n = 2 and r = 5 **(D) n = 2 and r = 6**

This one takes real multi-step reasoning. The catch is that in arithmetic mod 5, the derivative of x⁵ is 5x⁴ = 0, so the null space includes x⁵ as well as constants.

**Virology**, an example of a questionable key:
> How many human polyomaviruses are known at present?
> **(A) 100** (B) 1 (C) 10 (D) unknown

The key says 100. A 2013 medical review lists 10 known human polyomaviruses (JC, BK and eight more discovered recently) [10], and later counts are still in the low teens, which makes (C) the closest answer. A model that *knows the science* gets this "wrong". **[suspected]**. The broader problem with Virology questions is documented; see [Label and metric flaws](#label-and-metric-flaws).

## How it's scored

1. The model sees the question and the four options, usually after **5 worked examples** from the dev set (["5-shot"](../../glossary.md#few-shot)).
2. The model's answer is compared with the key. Score = % correct, typically averaged across subjects.

That sounds simple, but **there are several ways to work out "the model's answer"**, and they give very different numbers:

| Method | How the answer is picked |
|--------|--------------------------|
| **Letter probability** (original code) | Which of the letters "A", "B", "C", "D" the model thinks is most likely to come next. |
| **Generated text** (Stanford HELM) | Let the model write its answer, then check whether the text matches. |
| **Full-answer probability** (EleutherAI harness, early 2023) | Which full answer *text* the model finds most likely. |

In 2023, Hugging Face found that the same model (LLaMA-65B) scored **63.7%** with one method and **48.8%** with another. That is a 15-point gap, and both numbers were labeled "MMLU". [3] (See [multiple-choice scoring](../../concepts/multiple-choice-scoring.md).)

Newer reports often use **chain-of-thought** prompting, where the model reasons step by step before answering. That generally raises scores, so you can only compare numbers measured with the same setup.

## History and scores

| When | What happened |
|------|---------------|
| 2020 | Released. Most models score close to random (25%). The largest GPT-3 scores **43.9%** with few-shot prompting, and UnifiedQA scores 48.9%. [1] |
| Mar 2023 | GPT-4 is reported at **86.4%** (5-shot), close to the paper's estimated expert level. [12] |
| Dec 2023 | Google announces Gemini Ultra as the first model above 90% (**90.04%**). The headline figure used a different method ("CoT@32": 32 chain-of-thought samples combined) than the GPT-4 number it was compared with. Under the same 5-shot setup, Gemini Ultra scored **83.7%** against GPT-4's 86.4%. [7][8] |
| Jun 2024 | *Are We Done with MMLU?* [4] documents widespread answer-key errors. MMLU-Pro [5] launches as a harder replacement. |
| 2024–2025 | Frontier models cluster at around 88–92%. Leaderboards increasingly show MMLU "for reference only". [9] |

The Gemini episode is a useful lesson for readers: **a benchmark name alone doesn't tell you how the number was produced.**

## Known issues

Evidence levels: **[documented]** published analysis · **[reported]** credible informal source · **[suspected]** our own reasoning.

### Contamination and saturation

- **[documented] Signs of test-set memorization.** Deng et al. (2023) hid one *wrong* answer option in MMLU test questions and asked models to fill it in. A model that has never seen the question should almost never reproduce the exact wording of a wrong option. ChatGPT and GPT-4 matched the hidden option exactly **52%** and **57%** of the time, which strongly suggests the test questions appeared in their training data. [6]
- **[documented] Saturation.** Top scores have barely moved since 2024 and sit at roughly 88–92%. With an estimated ~6.5% of questions flawed [4], the highest score a model can *meaningfully* reach is somewhere in the low-to-mid 90s. The remaining gaps between top models are as likely to reflect noise in the key as real differences in ability. **[suspected]** (That inference is ours, built on [4].)

### Construct validity

- **[suspected] Recognition rather than knowledge.** Four-option multiple choice rewards ruling out wrong answers and spotting surface cues. That is a weaker skill than producing a correct answer or explanation from nothing.
- **[documented] Rankings depend on answer order.** Simply shuffling the order of the answer options, or changing the answer-selection method, can move a model by **up to 8 places** on a leaderboard. [11] If the order of the options matters that much, the benchmark is partly measuring how a model handles the test format, not only what it knows.
- **[suspected] Uneven subject coverage.** Subjects range from 100 test questions (e.g. abstract algebra) to 1,534 (professional law) [2], and the "average" headline weights them differently depending on how it is computed (per question or per subject). Reports rarely say which.

### Label and metric flaws

- **[documented] Wrong answers in the key.** Researchers re-checked 5,700 questions across all 57 subjects and estimate that **6.49%** of MMLU questions contain errors: wrong keys, unclear questions, or more than one correct answer. In the **Virology** subject, **57%** of the questions they analyzed had errors. [4]
- **[documented] Scores depend on implementation.** The same model can differ by 15+ points depending on how the answer is extracted (see [How it's scored](#how-its-scored)). [3]
- **[documented] Prompt sensitivity.** Changing the prompt wording alone moves MMLU scores by roughly **4–5 points**. [5]

### Real-world gap

- **[suspected] Exam questions are not real work.** People rarely use AI to answer four-option exam questions. They ask open-ended questions, request writing, or get help with tasks. A model can score well on MMLU and still give confident, wrong, unhelpful answers in practice.
- **[documented] Poor calibration in early models.** The original paper found GPT-3's confidence was only weakly related to whether it was right. In some subjects, its confidence and accuracy differed by up to 24 points. [1] Accuracy alone doesn't show whether a model *knows when it doesn't know*.

## How to read a score

- **Check the setup.** "MMLU 88%" means little unless you know whether it was 5-shot or 0-shot, with or without chain-of-thought, and how the answer was extracted. Only compare numbers measured the same way.
- **Treat gaps under ~2 points at the top as noise.** Answer-key errors and prompt sensitivity are about that size or larger.
- **A high score is a minimum bar, not proof of ability.** Today, a score below ~80% says a model lacks broad knowledge. A score above 88% no longer separates the leading models.
- **For newer models, look at harder successors** such as MMLU-Pro and GPQA, or at benchmarks that test applying knowledge rather than recognizing it.

## Related benchmarks

- **MMLU-Pro** [5]: 10 answer options instead of 4, harder reasoning questions, and fewer noisy items. Models score 16–33 points lower, and scores are less sensitive to prompt wording (~2 points).
- **MMLU-Redux** [4]: 5,700 MMLU questions re-checked and corrected.
- **GPQA** (page to come): graduate-level science questions written so that web search doesn't help.

## Sources

1. Hendrycks, D. et al. (2020). *Measuring Massive Multitask Language Understanding.* ICLR 2021. https://arxiv.org/abs/2009.03300
2. MMLU dataset card (MIT license), Hugging Face. https://huggingface.co/datasets/cais/mmlu
3. Fourrier, C. et al. (2023). *What's going on with the Open LLM Leaderboard?* Hugging Face blog. https://huggingface.co/blog/open-llm-leaderboard-mmlu
4. Gema, A. P. et al. (2024). *Are We Done with MMLU?* https://arxiv.org/abs/2406.04127
5. Wang, Y. et al. (2024). *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark.* https://arxiv.org/abs/2406.01574
6. Deng, C. et al. (2023). *Investigating Data Contamination in Modern Benchmarks for Large Language Models.* NAACL 2024. https://arxiv.org/abs/2311.09783
7. Gemini Team, Google (2023). *Gemini: A Family of Highly Capable Multimodal Models.* https://arxiv.org/abs/2312.11805
8. The Decoder (2023). *Are Google Gemini and OpenAI's GPT-4 peak LLM?* https://the-decoder.com/are-google-gemini-and-openais-gpt-4-peak-llm/
9. BenchLM, MMLU leaderboard (accessed 2026-11). https://www.benchlm.ai/benchmarks/mmlu. Vendor launch page for GPT-4o: https://openai.com/index/hello-gpt-4o
10. De Gascun, C. F. & Carr, M. J. (2013). *Human polyomavirus reactivation: disease pathogenesis and treatment approaches.* Clinical and Developmental Immunology. https://pmc.ncbi.nlm.nih.gov/articles/PMC3659475
12. OpenAI (2023). *GPT-4 Technical Report.* https://arxiv.org/abs/2303.08774
11. Alzahrani, N. et al. (2024). *When Benchmarks are Targets: Revealing the Sensitivity of Large Language Model Leaderboards.* ACL 2024. https://arxiv.org/abs/2402.01781
