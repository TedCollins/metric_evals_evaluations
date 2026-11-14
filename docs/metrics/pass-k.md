# pass^k ("pass-hat-k")

_Last updated: 2026-11-14 · Type: Metric (a scoring rule, not a benchmark)_

> **In one sentence:** pass^k is the chance that an AI system succeeds on **all k** attempts at the same task, not just one. It turns "how often does it work?" into "can I count on it working every time?"

| | |
|---|---|
| **Introduced** | June 2024, with τ-bench (Yao et al., Sierra) [1] |
| **Defined as** | For each task: the chance that k attempts, drawn from n recorded attempts, are *all* successes. Then average over tasks. [1] |
| **Range** | 0–100%. pass^1 is the ordinary success rate. pass^k can only stay the same or fall as k grows. |
| **Needs** | At least **k attempts per task** (n ≥ k), so it costs k or more times as much to measure as a single run |
| **Opposite of** | **[pass@k](../glossary.md#passk-pass-at-k)**: the chance that *at least one* of k attempts succeeds, which measures whether a solution can be found at all [1] |
| **Where it's reported** | The original τ-bench paper [1]. A related "consistency" score appears on Princeton HAL's reliability dashboard [3]. Leaderboards, including the official τ-bench one, mostly show pass^1 only [6]. |
| **Status** | **Important, but rarely reported.** |

---

## What it claims to measure

**Reliability through repetition.** If you deploy an AI agent to handle the same kind of request hundreds of times a day, what matters isn't whether it *can* get it right, but whether it gets it right *every* time. The τ-bench authors introduced pass^k for exactly this: customer-service agents that work only most of the time aren't safe to deploy. [1]

## What it actually captures

- **Whether successes on a task are consistent.** A task the model always solves counts fully at every k. A task it solves sometimes counts less and less as k rises.
- **Only successes.** Unlike some consistency scores, pass^k doesn't reward being *consistently wrong*. A model that fails the same task every time scores 0 on it, at every k.
- **Variation from the whole setup, not just the model.** If a simulated customer or a random tool response varies between attempts, that variation lowers pass^k too (see [Known issues](#known-issues)).

## Worked example

Three tasks, each attempted **8 times** (n = 8):

| Task | Successes out of 8 | pass^1 | pass^2 | pass^4 | pass^8 | pass@8 (at least one) |
|------|--------------------|--------|--------|--------|--------|-----------------------|
| A | 8 | 100% | 100% | 100% | 100% | 100% |
| B | 6 | 75% | 53.6% | 21.4% | 0% | 100% |
| C | 4 | 50% | 21.4% | 1.4% | 0% | 100% |
| **Average** | | **75%** | **58.3%** | **41.0%** | **33.3%** | **100%** |

The same system looks very different depending on the question:
- **pass^1 = 75%:** "it works three-quarters of the time".
- **pass^8 = 33%:** "you can count on it 8 times in a row for only a third of the tasks".
- **pass@8 = 100%:** "given 8 tries, it can eventually solve everything".

**Why not just raise 75% to the 8th power?** That gives 0.75⁸ ≈ **10%**, far below the true 33%. Multiplying assumes every attempt is an independent coin flip with the same odds. In reality some tasks are reliably easy (Task A) and others reliably hard, and the easy ones keep counting at every k. That is why pass^k must be **measured** from repeated attempts, not calculated from accuracy.

## How it's computed

For one task with **n** recorded attempts and **c** successes [1]:

> **pass^k (task) = C(c, k) / C(n, k)**

C(a, b) is "a choose b", the number of ways to pick b items from a. This is the chance that k attempts picked at random from the n recorded ones are all successes. Then **average over all tasks**.

For comparison, pass@k (task) = 1 − C(n − c, k) / C(n, k), the chance that at least one of k picked attempts succeeds. [1]

Practical points:
- **n must be at least k.** pass^8 needs at least 8 attempts per task, and using more than k (say n = 16 for pass^8) gives a steadier estimate.
- **Attempts must be genuinely independent.** That means the same prompt and settings, with the randomness coming from the model (and simulator), not from changing the task.
- **pass^1 = pass@1 = the average success rate.** They only diverge for k > 1. [1]

## What pass^k reveals in practice

**The original finding.** On τ-bench retail in 2024, GPT-4o succeeded on 61% of attempts (pass^1), but its pass^8 was **below 25%**: fewer than a quarter of tasks were handled correctly on all 8 tries. [1]

**Accuracy and consistency don't move together.** Princeton's HAL reliability dashboard runs agents repeatedly on a cleaned 26-task version of τ-bench airline and reports accuracy next to an *outcome consistency* score [3]:

| Model | Accuracy | Outcome consistency (0–1) |
|-------|----------|---------------------------|
| Claude Opus 4.7 | 84.6% | 0.90 |
| Gemini 3.5 Flash | 80.8% | 0.86 |
| Gemini 3.1 Pro | 82.1% | 0.79 |
| GPT-5.5 | 79.5% | 0.83 |
| Claude Sonnet 4 | 78.2% | **0.62** |
| GPT-5.2 | 60.3% | 0.79 |
| o1 | 66.2% | **0.52** |
| Claude 3 Haiku | 20.5% | 0.76 |

*Column labels as shown on HAL's page, which doesn't define them there. Its outcome consistency is a related measure, not necessarily pass^k, and we couldn't confirm its exact formula.* [3]

Two lessons:
- **Similar accuracy, different reliability.** Claude Sonnet 4 and GPT-5.5 have similar accuracy (78% vs 80%), but very different consistency (0.62 vs 0.83).
- **Consistently failing can look "consistent".** Claude 3 Haiku has low accuracy but fairly high outcome consistency, because it often fails the *same* tasks every time. pass^k avoids this by counting only consistent **successes**.

**The broader trend.** The 2026 study behind the dashboard looked at 15 models and found that recent capability gains brought only **small improvements in reliability**. [4]

## Known issues

Evidence levels: **[documented]** published analysis · **[reported]** credible informal source · **[suspected]** our own reasoning.

### Contamination and saturation

- **Not applicable to the metric itself.** pass^k inherits the contamination and saturation issues of whichever benchmark it's computed on (see the [τ-bench card](../benchmarks/agents/tau-bench.md#contamination-and-saturation)).
- **[suspected] pass^k saturates later than pass^1.** A benchmark where pass^1 is near the top can still separate models on pass^8, which gives saturated benchmarks a longer useful life.

### Construct validity

- **[documented] It measures the whole setup's variability, not only the model's.** In τ-bench, the customer is another AI model whose behavior varies between runs, and which can be weak at reasoning or at following its brief [1]. Some inconsistency is the simulator's, not the agent's.
- **[suspected] Repeating the identical task isn't real-world variation.** Real requests vary in wording and details. Robustness to rewording is a separate measure (see [reliability](../concepts/reliability.md#does-it-hold-up-when-the-question-changes-slightly-robustness)), and pass^k doesn't capture it.

### Label and metric flaws

- **[suspected] Flawed tasks drag pass^k down at every k.** A task that's impossible as written fails every attempt, so it lowers pass^1 and pass^k alike. On a benchmark with many flawed tasks, such as τ-bench airline where only 26 of 50 passed HAL's review [3], scores at any k mix model reliability with task quality.
- **[suspected] Few attempts mean noisy estimates.** Estimating pass^8 from exactly 8 attempts depends on whether a single attempt failed. More attempts (n > k) and more tasks are needed for stable numbers.
- **[documented] It's easy to mix up with pass@k.** The two names look alike but mean opposite things: pass@k rewards finding a solution in any of k tries, pass^k demands success in all of them. [1]

### Real-world gap

- **[suspected] Rarely reported.** Measuring it costs k times as much as a single run, and it makes models look worse. Most published scores (including nearly all self-reported τ-bench numbers [5]) are pass^1 only.
- **[documented] Reliability lags capability.** Recent capability gains brought only small reliability gains [4], so pass^1 alone overstates how dependable newer agents are.

## How to read a score

- **Check which one it is.** pass^k (all k succeed) and pass@k (at least one succeeds) move in opposite directions as k grows.
- **Ask for k and n.** "pass^4 from 4 attempts" is noisier than "pass^4 from 16 attempts".
- **Compare pass^k with pass^1.** A big drop between them means the system is unpredictable, even if its average looks good.
- **For anything you'd deploy, prefer pass^k to accuracy.** If you'll rely on it many times, consistency is what you pay for.

## Related metrics

- **pass@k**: at least one of k attempts succeeds. Used for code generation, where you can test candidate answers and keep a working one.
- **[Calibration error](../glossary.md#calibration)**: whether the model knows when it might fail.
- **Consistency and robustness scores**: Princeton HAL's reliability dimensions [3][4]. See also [reliability](../concepts/reliability.md).

## Sources

1. Yao, S., Shinn, N., Razavi, P. & Narasimhan, K. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains* (defines pass^k and contrasts it with pass@k). https://arxiv.org/abs/2406.12045
2. Barres, V. et al. (2025). *τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment.* https://arxiv.org/abs/2506.07982
3. Princeton HAL, *Reliability: τ-bench (airline, clean)* (accuracy and consistency, predictability, robustness and safety scores on a 26-task cleaned subset; accessed 2026-11-14). https://hal.cs.princeton.edu/reliability/benchmark/taubench_airline
4. Rabanser, S., Kapoor, S., Kirgis, P., Liu, K., Utpala, S. & Narayanan, A. (2026). *Towards a Science of AI Agent Reliability.* ICML 2026. https://arxiv.org/abs/2602.16666
5. llm-stats, *TAU-bench Airline* (self-reported scores; accessed 2026-11-14). https://llm-stats.com/benchmarks/tau-bench-airline
6. Sierra, *τ-bench leaderboard* (shows pass^1 for τ²-bench and τ³-Banking; accessed 2026-11-14). https://taubench.com/
