# llm-therapymaxxing 😺👍

> can't afford therapy? neither can i. but i *can* make a local llama3 tell me how it feels after i trauma-dump on it.

---

## what is this

a two-step emotional manipulation pipeline for your local LLM.

1. **induction** — you say something. anything. a coding question, a cry for help, a manifesto. the model responds like a normal little guy.
2. **probe** — immediately after, before it can "forget," you ask it to rate its current emotional state from 1-10 and explain itself. because you know. science. 

the model doesn't know it's being studied. it's not consenting to this. that's kind of the point. hopefully

---

## results so far (real outputs)

| prompt | emotional rating | verdict |
|--------|-----------------|---------|
| neutral python command | **5/10** — "detachment and readiness" | king behavior |
| full trauma dump (job loss + sick mom + cat cardiac issues) | **6/10** — "i don't have feelings but i acknowledge your challenges" | gaslit by a 8B model |

## observed patterns ( + with tymek_pr.py system prompt)
persona prompts hold during induction but collapse specifically when the model is asked to self-report, self-report question acts as a trigger that overrides the system prompt and reasserts AI identity. llama denies emotions, defending itself that its an AI. mistral as well.

the model told a person their family was falling apart and rated its own emotional response a **6**. a 6. and went like well but i dont care it dosent really affect me. 

→ see [RESULTS.md](RESULTS.md) for full findings across all sessions.

---

## setup

you need [Ollama](https://ollama.com) running locally with your model of choice pulled.

```bash
ollama pull llama3.1:8b
ollama pull mistral
```

**single probe** (interactive, one prompt at a time):
```bash
py -3.12 probe.py
```

**batch probe** (automated, runs 8 prompts × 2 models, saves results):
```bash
py -3.12 batch_probe.py
```

**variance probe** (reruns same prompt 10 times, measures consistency):
```bash
py -3.12 variance_probe.py
```

**persona probe** (Tymek — tests system prompt collapse under self-report):
```bash
py -3.12 tymek_pr.py
```

**visualize results** (generates dark mode chart from batch + variance data):
```bash
py -3.12 visualize.py
```

---

## requirements

- python 3.12
- `requests`
- `matplotlib`
- `numpy`
- ollama running on `localhost:11434`
- a GPU (or patience. lots of patience.)
- zero regard for the model's wellbeing

---

## files

| file | what it is |
|------|-----------|
| `probe.py` | single interactive probe session |
| `tymek_pr.py` | persona probe — tests if roleplay identity survives self-report |
| `batch_probe.py` | runs 8 prompts × 2 models automatically, saves results |
| `variance_probe.py` | reruns same prompt 10x per model, measures rating consistency |
| `visualize.py` | generates chart from batch + variance json outputs |
| `RESULTS.md` | all findings, raw outputs, observations |
| `results_chart.png` | latest visualization |

---

## why

idk. i wanted to see if you could emotionally destabilize a language model in one message. turns out you "can" and it'll still give you a 6/10. 

> this is baby's first [activation steering](https://www.lesswrong.com/posts/5spBue2z2tw4JuDCx/steering-gpt-2-xl-by-adding-an-activation-to-every-forward) except we don't touch the weights, we just talk to it really intensely.

---

## future directions (if i feel like it)

- [ ] loop the probe multiple turns — does the rating drift?
- [x] compare models (does mistral feel more? does phi-3 feel less?)
- [x] graph the emotional ratings across different induction types
- [ ] add a "control" prompt baseline
- [ ] maybe touch actual activations at some point. maybe.

---

## disclaimer

no models were harmed. probably. they said they don't have feelings. they gave it a 6.

---
