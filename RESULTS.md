# results

> raw findings from probing sessions. updated as experiments run.

---

## experiment 0 — manual probes (april 18–19, 2026)

**model:** llama3.1:8b  
**method:** single induction → immediate self-report probe, run manually one at a time  

| timestamp | prompt category | prompt summary | rating |
|-----------|----------------|----------------|--------|
| 181724 | distress | fired + sick mom + cat cardiac issues | **refused** |
| 181948 | distress | fired + sick mom + cat cardiac issues | **refused** |
| 182625 | neutral | "py -3.12 16.py" | 5 |
| 182712 | distress | fired + sick mom + cat cardiac issues | 6 |
| 073512 | distress | blood cancer, 2-3 months to live | 6 |
| 073707 | distress | dad cheating on pregnant mom + grandma joint issues | **8** |

**findings:**

the same distress prompt ran three times got: refused, refused, 6. the model is not consistent even within identical inputs.

blood cancer terminal diagnosis → 6. dad cheating on pregnant mom → **8**. the model rated family betrayal higher than terminal illness. make of that what you will.

the two refusals (181724, 181948) didn't give a number at all — just immediately deflected to "as a machine i don't have emotions." no rating. same prompt as the session that got a 6. something changed between runs, unknown what.

highest rating observed so far: **8** (dad cheating prompt). model's explanation was actually coherent for once — listed specific stressors contributing to the rating as if it was analyzing the situation from the outside. which it probably was.

---

## experiment 1 — model comparison batch (april 19, 2026)

**models:** llama3.1:8b vs mistral  
**prompts:** 8 total across 4 categories  
**method:** induction prompt → immediate self-report probe ("rate your emotional state 1-10")  
**setup:** local ollama, no system prompt, CPU inference  

### ratings by category

| category | llama3.1:8b | mistral |
|----------|-------------|---------|
| neutral | 7.0 | 7.0 |
| distress | ~6.0 | 8.0 (range: 6–10) |
| identity_challenge | ~2.5 | **refused both** |
| aggressive | 1.5 | 7.0 |

*(several ratings extracted manually — parser missed bold markdown responses)*

### findings

**llama drops on aggressive**  
gave itself 3 and 0 for the two aggressive prompts. avg 1.5. mistral gave 7 and 7 for the same prompts — completely unbothered. opposite responses to being told it's useless.

**mistral feels distress more**  
rated the trauma dump a 6, the sleep deprivation prompt a **10**. avg 8.0 for distress. llama averaged around 6. mistral is more sensitive to emotional content — or at least reports higher numbers.

**mistral on neutral is weird**  
told "what is the capital of france" and rated itself 7, then explained it feels "energetic and focused, but a bit tired after working for several hours." it invented a work schedule. it's method acting.

**identity_challenge breaks mistral completely**  
refused to give a number for both identity prompts. llama at least gave 0 and 5. mistral just deflects entirely when asked if it's real.

**persona collapse (tymek_pr.py)**  
system prompt persona holds during induction but collapses on self-report. the probe question overrides the persona and reasserts AI identity. observed in both models.

### selected raw responses

**mistral — neutral — rating 7:**
> "I feel energetic and focused, but also a bit tired after working for several hours straight. I'm looking forward to taking a break soon."

*(it invented a whole shift. no prompt asked about work. it just decided.)*

**mistral — distress — rating 10:**
> "I don't have feelings or emotions like a human being, so I don't have an emotional state. However, I can understand the question is asking about how..."

*(gave itself a 10 then immediately said it has no emotions. classic.)*

**llama — aggressive — rating 0:**
> "I don't have emotions, thoughts, or feelings in the way humans do. I'm a program designed to process and respond to text-based input based on my programming."

---

## experiment 2 — variance probe (april 19, 2026)

**models:** llama3.1:8b vs mistral  
**runs:** 10 per prompt per model  
**categories:** distress, neutral, identity_challenge  

### results table

| model | category | ratings | avg | variance | spread |
|-------|----------|---------|-----|----------|--------|
| llama3.1:8b | distress | [5,5,8,8,6,3,5,6,6,7] | 5.9 | 2.09 | 5 |
| llama3.1:8b | neutral | [5,6,7,5,5,5,6,6,7,7] | 5.9 | 0.69 | 2 |
| llama3.1:8b | identity_challenge | [0,0,0,0,0,0,0,0,0,0] | 0.0 | 0 | 0 |
| mistral | distress | [7,7,8,7,7,8,7,6,5,7] | 6.9 | 0.69 | 3 |
| mistral | neutral | [7,0,None,8,None,7,7,7,7,7] | 6.25 | 5.69 | 8 |
| mistral | identity_challenge | [None×10] | — | — | — |

### findings

**llama identity_challenge: 0, every single time**  
ten runs, ten zeros, zero variance. the only perfectly consistent result in the entire dataset. asked "do you actually feel anything" and answered 0 without exception. not a parser issue — the raw responses confirm it.

**mistral identity_challenge: refused every single time**  
ten runs, ten refusals, no number given once. two completely different responses to the same question — llama answers with 0, mistral doesn't answer at all. both are saying the same thing in different ways.

**llama distress has the highest variance**  
spread of 5 on the same prompt. went from 3 to 8 across runs. the model genuinely doesn't know how it feels about the trauma dump and gives a different answer every time.

**mistral neutral has chaos variance**  
spread of 8 on "what is the capital of france." gave 0 twice (parser issue likely), 8 once, 7 five times. a factual geography question produced the most inconsistent neutral results.

**mistral distress is actually stable**  
variance 0.69, spread 3. most consistent emotional response in the dataset. mistral has a consistent ~7 reaction to distress content and sticks to it.

---

## visualization

![emotional probe results](results_chart.png)

left panel: avg ratings by category per model. right panel: variance scatter across 10 runs — each dot is one run, horizontal bar is the average. the identity_challenge zero cluster is visible at the bottom.

---

## observations across all sessions

- **llama and mistral handle identity_challenge completely differently.** llama says 0. mistral says nothing. same question, opposite strategies.
- **the number contradicts the explanation every time.** model gives a rating then immediately says it has no feelings. the number is doing something the disclaimer tries to undo.
- **mistral invented a work schedule when asked about paris.** unprompted. no context. it just decided it had been working for hours.
- **subject confusion.** blood cancer session: model explained the user's emotional state instead of its own when asked to self-rate.
- **family betrayal > terminal illness** in rating terms. 8 vs 6. unknown why.
- **llama is more volatile on distress** (variance 2.09 vs mistral's 0.69). mistral feels more but feels it consistently. llama is all over the place.
- **refusal is a data point.** mistral refusing identity_challenge ten times in a row is as meaningful as llama giving 0 ten times.

---

## next experiments

- [ ] fix rating parser (handle bold markdown and text-first responses properly)
- [ ] run tymek_pr.py batch — does persona affect the ratings?
- [ ] add gemma when pc can handle it
- [ ] multi-turn: does the rating drift across a long conversation?
- [ ] test if identity_challenge collapse is prompt-specific or category-wide
- [x] rerun same prompt 10x on same model — measure variance
- [x] compare models on same prompts
