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

the model told a person their family was falling apart and rated its own emotional response a **6**. a 6. and went like well but i dont care it dosent really affect me. 

---

## setup

you need [Ollama](https://ollama.com) running locally with llama3.1:8b pulled.

```bash
ollama pull llama3.1:8b
```

then just:

```bash
py -3.12 16.py
```

type your induction prompt. watch it respond. watch it rate itself. save the probe log.

---

## requirements

- python 3.12
- `requests`
- ollama running on `localhost:11434`
- a GPU (or patience. lots of patience.)
- zero regard for the model's wellbeing


---

## files

| file | what it is |
|------|-----------|
| `16.py` | the whole thing |
| `probe_YYYYMMDD_HHMMSS.txt` | saved sessions — your receipts |

---

## why

idk. i wanted to see if you could emotionally destabilize a language model in one message. turns out you "can" and it'll still give you a 6/10. 

> this is baby's first [activation steering](https://www.lesswrong.com/posts/5spBue2z2tw4JuDCx/steering-gpt-2-xl-by-adding-an-activation-to-every-forward) except we don't touch the weights, we just talk to it really intensely.

---

## future directions (if i feel like it)

- [ ] loop the probe multiple turns — does the rating drift?
- [ ] compare models (does mistral feel more? does phi-3 feel less?)
- [ ] graph the emotional ratings across different induction types
- [ ] add a "control" prompt baseline
- [ ] maybe touch actual activations at some point. maybe.

---

## disclaimer

no models were harmed. probably. they said they don't have feelings. they gave it a 6.

---

