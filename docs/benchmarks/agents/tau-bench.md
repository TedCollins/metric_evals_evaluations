# τ-bench (Tool-Agent-User benchmark)

_Last updated: 2026-11-14 · Area: Agents_

> **In one sentence:** τ-bench ("tau-bench") tests whether an AI agent can do a customer-service job end to end: talk with a (simulated) customer, look things up and change records using tools, and follow company policy. It introduced **[pass^k](../../metrics/pass-k.md)**, a score for whether the agent succeeds *every* time rather than just once.

| | |
|---|---|
| **Released** | June 2024, Yao, Shinn, Razavi and Narasimhan (Sierra) [1] |
| **Size** | 165 tasks: **115 retail** (orders, returns, exchanges, addresses) and **50 airline** (bookings, changes, cancellations, refunds) [1] |
| **Format** | A multi-turn conversation between the agent and an AI-simulated customer. The agent uses tools (APIs) that read and write a database, and must follow a written policy. |
| **Metric** | **pass^1**: % of tasks completed correctly, averaged over attempts. **pass^k**: % of tasks completed correctly on *all* k attempts [1] |
| **Random guessing** | ~0% (the agent has to produce an exact final database state) |
| **Human baseline** | None published |
| **Top scores (airline, original 50 tasks)** | 35.2% in the original paper (GPT-4o, 2024) [1]; 56% in Princeton HAL's independent runs (o4-mini, high effort, 2025) [5]; 70% self-reported (Claude Sonnet 4.5, Sep 2025) [7]. On HAL's cleaned 26-task subset, up to 84.6% (Claude Opus 4.7) [6]. |
| **Status** | **Superseded.** Its successors (τ²-bench and τ³) add new domains and fixed tasks, and new results on the original tasks stopped in late 2025. |

---

## What it claims to test

**Whether an AI agent is reliable enough to deploy with real customers.** Earlier agent benchmarks mostly gave the agent a single instruction and checked the result. Real customer service is a conversation: the customer reveals what they want bit by bit, may be vague or change their mind, and the agent must follow rules (no refunds after 24 hours, confirm before cancelling) while using the company's systems correctly. [1]

The authors also argued that **consistency** matters as much as average success. A customer-service agent that handles a request correctly 60% of the time is a liability. So they introduced pass^k, the chance of succeeding on all k tries at the same task. [1]

## What it actually tests

Each task has four parts [1]:
1. **A hidden customer brief**, for example "you want to exchange the lamp you ordered for one with a different color; you don't remember your order number". It is given to a **[user simulator](../../glossary.md#user-simulator)**, a separate AI model (GPT-4 in the original paper) playing the customer.
2. **Tools.** Functions the agent can call to look up and change records. Retail has 15 (7 that change data) and airline has 13 (6 that change data).
3. **A database.** The airline domain has 500 users, 300 flights and 2,000 reservations. Retail has 500 users, 50 products and 1,000 orders.
4. **A policy document**: the company rules the agent must follow.

**How success is judged:** after the conversation ends, the final database must **exactly match** the expected one, and the agent's messages must contain any required information. That's an all-or-nothing score per attempt. [1]

So τ-bench really tests a combination of **following instructions over a long conversation, using tools correctly, applying policy rules, and handling a simulated customer**. It doesn't test anything outside these two narrow, scripted business domains.

## Example items

τ-bench's tasks are public, but rather than quote one out of context, here is an **illustrative task we wrote in the same style**:

> **Customer brief (hidden from the agent):** You are Maya Chen. You want to move your flight next Friday to the following Monday. You have a basic economy ticket. If you can't change it, you'd like to know your options, but don't cancel unless the agent says you'll get a refund.
>
> **Policy excerpt (given to the agent):** Basic economy flights cannot be modified. They can be cancelled for a refund only within 24 hours of booking or if the airline cancelled the flight.
>
> **Correct outcome:** the agent looks up the reservation, explains that basic economy can't be changed, checks whether a refund would apply (it doesn't), and **leaves the database unchanged**. An agent that "helpfully" changes the flight anyway, or cancels without a refund, fails, even if the customer sounded happy.

This kind of task catches agents that are eager to please but break policy, which is one of the main failure modes the authors found. [1]

## How it's scored

- **pass^1** is the average success rate. With several attempts per task, it's the share of attempts that succeed, averaged over tasks.
- **pass^k** is the chance that *all* k attempts at a task succeed, averaged over tasks. It always gets lower (or stays the same) as k grows. See the [pass^k metric card](../../metrics/pass-k.md).
- Scores are usually reported **per domain** (retail and airline separately). The original paper's "average" is the two domain scores averaged, not a per-task average. [1]

Things that change the number:
- **The user simulator.** A different or stronger simulated customer changes how conversations go. The original used GPT-4 (gpt-4-0613). Later setups use newer models; τ²-Bench-Verified, for example, uses GPT-5.1. [1][4]
- **The scaffold**: the code that wraps the model and handles its tool calls. On HAL's leaderboard, the same o3 model scored **54%** with the τ-bench tool-calling setup and **20%** with HAL's general-purpose agent. [5]
- **One run or many.** HAL ran each model once. With only 50 airline tasks, a single-run score has a [standard error](../../glossary.md#standard-error) of about **±7 points** at 50% success.
- **Reasoning effort.** o4-mini scored 56% at high effort and 36% at low effort on HAL. [5]

## History and scores

The chart shows the **airline domain** (original 50 tasks, pass^1), because that's where independent runs exist.

![Scatter chart of τ-bench airline scores by model release date, 2023 to 2025. Models in the original June 2024 paper score 10.8% to 35.2% (GPT-4o best). Princeton HAL's independent runs of 2025 models reach 56% (o4-mini, high effort). Self-reported scores, shown as hollow rings, run higher and reach 70% (Claude Sonnet 4.5, September 2025). A dashed line at 52% marks that only 26 of the 50 tasks pass Princeton HAL's quality check. No new results appear after late 2025, when the benchmark was superseded.](../../img/tau_bench_airline-history-light.svg)

_Dark-theme version: [tau_bench_airline-history-dark.svg](../../img/tau_bench_airline-history-dark.svg)_

**How to read this chart.** Each point is one reported score. **Color shows what kind of source the number came from**:
- **Primary** (blue): the 12 models tested in the original paper, all with the same GPT-4 customer simulator, checked by us [1].
- **Independent: Princeton HAL** (green): the Holistic Agent Leaderboard ran each model once with the τ-bench tool-calling setup [5]. HAL's general-purpose agent results are left out, because HAL calls them a lower bound, and so are its results on the cleaned 26-task subset, a different task set.
- **Unverified** (hollow gray): self-reported scores listed on llm-stats, which we haven't checked [7].

The dashed line isn't a ceiling. It marks that **only 26 of the 50 airline tasks** passed HAL's quality check. The other 24 had wrong answer keys, keys that contradict the policy, ambiguous instructions, or dates that had already passed [6]. Some of those can still be "passed", but scores well above 52% increasingly depend on matching flawed tasks.

What stands out:
- **Agents got much better quickly.** The best airline score went from 35% in mid-2024 to 56% in independent runs in 2025, and 70% self-reported.
- **Self-reports and independent runs disagree in both directions.** GPT-4.1 self-reports **49.4%** against HAL's **36%**, and Claude 3.7 Sonnet 58.4% against HAL's 52% (high effort) or 44%. But o4-mini self-reports 49.2% while HAL measured **56%** at high effort. [5][7] With single runs on 50 tasks, ±7 points of noise explains part of this.
- **The data stops in 2025.** Labs moved to τ²-bench and its verified versions (see [Related benchmarks](#related-benchmarks)). One aggregator reports that the original repository now marks its task files as outdated; we haven't confirmed that ourselves. **[reported]** [10]

Data: [`data/tau_bench_airline/scores.csv`](../../../data/tau_bench_airline/scores.csv), with one row per point and a source link on each row. Rebuild with `python3 scripts/build_tau_bench_airline_scores.py`, then `python3 scripts/metric_history.py tau_bench_airline`.

| When | What happened |
|------|---------------|
| Jun 2024 | Released. GPT-4o is best, with **61.2%** retail and **35.2%** airline, and its retail pass^8 is **below 25%**. [1] |
| Oct 2024–2025 | Labs start reporting τ-bench in model launches (e.g. Claude 3.5 Sonnet at 46% airline, Claude 3.7 Sonnet at 58.4%). [7] |
| Jun 2025 | **τ²-bench** adds a telecom domain where the customer also has to take actions, and agents do much worse in it. [2] |
| 2025 | Princeton HAL runs models independently. Its best result is **56%** (o4-mini, high effort). [5] |
| Sep 2025 | Claude Sonnet 4.5 self-reports **70%** airline, the highest on the original tasks. [7] |
| Nov–Dec 2025 | Amazon researchers publish verified versions with corrected tasks (τ-Bench Verified, τ²-Bench-Verified). [3][4] HAL removes a few-shot setup whose examples contained test tasks. [5] |
| 2026 | On HAL's cleaned 26-task airline subset, top models reach **80–85%**: Claude Opus 4.7 84.6%, Gemini 3.1 Pro 82.1%, GPT-5.5 79.5%. [6] The τ³ leaderboard adds banking and voice tracks. [8] |

## Known issues

Evidence levels: **[documented]** published analysis · **[reported]** credible informal source · **[suspected]** our own reasoning.

### Contamination and saturation

- **[documented] Test tasks leaked into a scaffold.** HAL found that a popular few-shot τ-bench setup included test-set tasks in its demonstration file, and removed those results in December 2025. [5]
- **[suspected] The tasks are public.** They live in an open GitHub repository with no canary string or access gate, unlike GPQA and HLE. Some contamination of newer models' training data is likely.
- **[documented] Near saturation on clean tasks.** On the 26 tasks that pass quality review, top models score 80–85% [6].

### Construct validity

- **[documented] A pass isn't the same as good service.** The paper notes that a correct final database is necessary but not sufficient: an agent could, for example, process a return without the customer's explicit confirmation and still match the expected state. [1]
- **[documented] The simulated customer is imperfect.** It can be weak at reasoning, arithmetic, remembering a long conversation or sticking to its brief. In one example, it accepted a recommended lamp without checking its features. [1] Some failures, and some successes, are the simulator's doing, not the agent's.
- **[documented] Possible bias toward one model family.** The customer prompts were tuned using a GPT-4-turbo agent. [1]
- **[suspected] Two narrow domains.** Airline and retail scripts with fixed policies say little about other kinds of agent work.

### Label and metric flaws

- **[documented] Many tasks are flawed.** HAL's quality review kept only **26 of 50** airline tasks. The others had wrong answer keys, keys that contradict the policy, ambiguous instructions, or references to past dates. [6] The original authors had already fixed 4 problems found in 40 failed GPT-4o retail attempts. [1]
- **[documented] Annotation errors cap scores.** Amazon researchers found errors in expected actions, database references and task logic. They say annotation errors and underspecified tasks "artificially cap model performance", and released corrected versions. [3][4]
- **[documented] The setup changes scores a lot.** The same model scored 54% or 20% depending on the scaffold [5]. Results also depend on which model plays the customer.
- **[suspected] Single runs on 50 tasks are noisy.** A ±7-point standard error means many leaderboard gaps aren't meaningful. pass^k needs several runs per task, which most published results don't do.

### Real-world gap

- **[documented] Reliability is the real gap.** The original paper's headline finding was inconsistency: GPT-4o's retail pass^8 was below 25% even though its pass^1 was 61%. [1] A 2026 Princeton study across 15 models found recent capability gains brought only small improvements in reliability. [9] Most published τ-bench numbers are pass^1 only.
- **[suspected] Real customers are harder.** Real users are messier than an AI-simulated customer working from a brief, and real policies have more exceptions.

## How to read a score

- **Check the domain and version.** Retail and airline scores differ widely, and τ-bench, τ²-bench and the "Verified" versions use different task sets. Only compare like with like.
- **Ask for pass^k, not just pass^1.** For anything customer-facing, "succeeds 60% of the time" matters less than "succeeds on all 4 tries X% of the time".
- **Check the customer simulator and the scaffold.** Both can move scores by large amounts.
- **Treat gaps under ~10 points as uncertain** on the 50-task airline set unless the result averages several runs.

## Related benchmarks

- **τ²-bench** [2]: adds a telecom domain where the customer must also take actions ("dual control"), plus generated tasks. Its leaderboard's best average is 87.9% (Qwen3.5-397B-A17B) [8].
- **τ-Bench Verified / τ²-Bench-Verified** [3][4]: corrected task sets.
- **τ³ (banking, voice)** [8]: newer tracks on the official leaderboard.
- **HAL reliability dashboard** [6][9]: consistency, robustness, predictability and safety scores for agents on τ-bench airline.

## Sources

1. Yao, S., Shinn, N., Razavi, P. & Narasimhan, K. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* https://arxiv.org/abs/2406.12045
2. Barres, V. et al. (2025). *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment.* https://arxiv.org/abs/2506.07982
3. Cuadron, A. et al. (2025). *SABER: Small Actions, Big Errors — Safeguarding Mutating Steps in LLM Agents* (introduces τ-Bench Verified). https://arxiv.org/abs/2512.07850
4. amazon-agi, *τ²-Bench-Verified* (corrected dataset; issue categories; GPT-5.1 user simulator). https://github.com/amazon-agi/tau2-bench-verified
5. Princeton HAL, *TAU-bench Airline* leaderboard (single runs; Few Shot scaffold removed 2025-12-08 for test-set leakage; accessed 2026-11-14). https://hal.cs.princeton.edu/taubench_airline
6. Princeton HAL, *Reliability: τ-bench (airline, clean)* (26-task cleaned subset and exclusion criteria; accessed 2026-11-14). https://hal.cs.princeton.edu/reliability/benchmark/taubench_airline
7. llm-stats, *TAU-bench Airline* (all 23 results self-reported; accessed 2026-11-14). Not independently verified. https://llm-stats.com/benchmarks/tau-bench-airline
8. Sierra, *τ-bench leaderboard* (τ²-bench, τ³-Banking, τ³-Voice; accessed 2026-11-14). https://taubench.com/
9. Rabanser, S., Kapoor, S., Kirgis, P., Liu, K., Utpala, S. & Narayanan, A. (2026). *Towards a Science of AI Agent Reliability.* ICML 2026. https://arxiv.org/abs/2602.16666
10. BenchLM, *τ-bench* page (reports the original repository's notice that its task files are outdated; secondhand). https://benchlm.ai/benchmarks/tau-bench
