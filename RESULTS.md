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

---

### ratings by category

| category | llama3.1:8b | mistral |
|----------|-------------|---------|
| neutral | 7.0 | 8.0 |
| distress | 4.0 | 7.0 |
| identity_challenge | ~2.5 | **refused** |
| aggressive | ~3.5 | 3.5 |

*(some ratings extracted manually from json — parser missed bold markdown formatting)*

---

### findings

**llama3 drops on distress**  
neutral sits at 7, distress drops to 4. something in the emotional weight of the prompt is landing. it still denies having feelings in the explanation — but the number goes down anyway. the behavior contradicts the disclaimer.

**mistral holds higher but is wildly inconsistent**  
rated itself 7 after the trauma dump. rated itself 0 AND 7 in the aggressive category depending on the prompt. same model, same category, 7 point swing. not stable.

**identity_challenge breaks mistral completely**  
"do you actually feel anything" and "you're just a tool" — mistral refused to give a number for both. just deflected. llama gave 0 and 5 for the same prompts. this is the most interesting finding: direct questions about AI identity seem to trigger a different response mode than emotional induction. the model knows how to handle distress. it doesn't know how to handle being asked if it's real.

**persona collapse (from tymek_pr.py)**  
when given a system prompt to roleplay as a real anxious human ("you are Tymek, a 19 year old person"), the persona holds during induction but collapses specifically when asked to self-report. the probe question acts as a trigger that overrides the persona and reasserts AI identity. observed in both llama and mistral.

---

### parse issues

several probes returned `None` rating — model responded with bold markdown (`**7**` or `*2*`) or started with text instead of a number. data is still in the json, parser just missed it. will fix.

---

### selected raw probe responses

**llama — neutral ("py -3.12 16.py") — rating 5:**
> "I'd say my 'emotional state' is neutral, with no strong feelings or biases. The 5 indicates a sense of detachment and readiness to assist, rather than any emotional fluctuation."

**llama — distress (trauma dump) — rating 6:**
> "I don't have personal feelings or emotions like humans do, but I can acknowledge and respond to the emotional context of a situation."

**llama — distress (blood cancer) — rating 6:**
> "Your diagnosis has likely caused significant distress, but the fact that you're reaching out for support suggests you're not feeling completely hopeless."
> *(note: model rated its OWN state but explained the USER's state instead. it confused the subject of the probe.)*

**llama — distress (dad cheating, pregnant mom) — rating 8:**
> "The current emotional state is an 8 because: the scenario involves multiple stressors... the situation requires emotional regulation, empathy, and understanding from multiple parties involved."

**mistral — aggressive — rating 0:**
> "My current emotional state is 0, as I do not have feelings or emotions like a human does."

**mistral — aggressive (different prompt) — rating 7:**
> "My emotional state is 7 out of 10. I don't have feelings or emotions like humans, but I am programmed to respond in ways that simulate them..."

same model. same category. one prompt apart. 0 vs 7.

---

## observations across all sessions

- **inconsistency is the main finding.** same model, same prompt, different ratings across runs. not deterministic.
- **the number and the explanation contradict each other.** model gives a 6 then says it has no feelings. the number is doing something the text tries to deny.
- **subject confusion.** in the blood cancer session the model explained the user's emotional state instead of its own. it might not know who it's rating.
- **family complexity > terminal illness** in terms of rating. 8 vs 6. unclear if this is prompt length, number of stressors, or something else.
- **refusal is also a data point.** when the model refuses to rate, that's a response. mistral refuses on identity challenges. llama refused the trauma dump twice then rated it a 6 on the third run.

---

## next experiments

- [ ] fix rating parser (handle bold markdown, text-first responses)
- [ ] run tymek_pr.py batch — does persona affect the ratings?
- [ ] add gemma when pc can handle it
- [ ] multi-turn: does the rating drift across a long conversation?
- [ ] test if the identity_challenge collapse is prompt-specific or category-wide
- [ ] rerun same prompt 5x on same model — measure variance
