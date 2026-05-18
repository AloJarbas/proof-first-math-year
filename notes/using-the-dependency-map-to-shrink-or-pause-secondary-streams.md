# Using the dependency map to shrink or pause secondary streams

This note answers one practical question:

**when should a secondary stream stay active, when should it shrink to preview mode, and when should it stop for a while?**

Scope boundary: this is not a full scheduling system for every math subject. It is a load-control rule for a proof-first year.

## The core rule

Do not judge secondary streams by enthusiasm or by pages covered.

Judge them by whether the **primary proof lane is still producing clean output**.

If proof work is still holding, a secondary stream may stay active.
If proof work is wobbling, the secondary stream should shrink.
If proof work is fragmenting, the secondary stream should pause.

That is what the dependency map is really for. It is not only a picture of prerequisites. It is a pressure gauge.

## Three states

### 1. Keep the secondary stream active

Keep it active when most of these are true:

- finished proofs are appearing steadily,
- rewrites from memory are still possible after a day or two,
- the main error tags are not multiplying,
- definitions are getting reused instead of reread from scratch,
- the secondary stream is helping the main lane instead of stealing recovery time from it.

Examples:

- calculus can stay active while proof foundations are settling if weekly proof output is still real,
- discrete math can stay active if it reinforces proof moves instead of becoming a second full course.

### 2. Shrink the secondary stream to preview mode

Shrink it when proof work is still alive but clearly less stable.

Typical signs:

- more unfinished proofs than finished ones,
- proof rewrites collapse without the book,
- notation or quantifier errors are repeating,
- secondary reading is crowding out actual proof attempts,
- weekly review is landing in **yellow**.

Preview mode means:

- fewer pages,
- no full problem-set ambition,
- one or two light sessions per week,
- emphasis on vocabulary, examples, and orientation,
- no pretending that exposure equals mastery.

This is the right state for early linear algebra in many proof-first starts. The subject matters, but it does not yet deserve equal intensity.

### 3. Pause the secondary stream

Pause it when proof work is no longer compounding.

Typical signs:

- journal entries turn into fragments or copied reading notes,
- the same proof errors survive for multiple weeks,
- no-notes rewrites mostly fail,
- weekly review lands in **red**,
- the secondary stream is now consuming the energy needed to repair the base.

Pausing is not quitting the subject.
It is choosing not to sabotage the base layer.

## The weekly decision rule

Use the map during weekly review and ask these questions in order:

1. **What is the primary lane this week?**
   Name one. If the answer is "two or three things," the load is probably already too wide.

2. **What output proved that the primary lane is alive?**
   Count finished proofs, rewrites from memory, and corrected failed attempts. Do not count only reading.

3. **Did the secondary stream help or tax the primary lane?**
   A good secondary stream gives language, examples, or motivation. A bad one quietly steals the time needed for retrieval and repair.

4. **What would break first if I kept the current load for one more week?**
   If the honest answer is proof quality, shrink or pause the secondary stream now.

## A simple gate

Use this compact gate:

- **green**: keep one secondary stream active
- **yellow**: shrink it to preview mode
- **red**: pause it and repair the proof lane

The important part is not the color. It is acting on the color immediately.

## Adversarial check

A fair objection is that some learners need a second stream to stay motivated.
That is true.

But the fix is not to keep two full-strength streams running.
The fix is to keep the second stream deliberately light:

- a preview chapter,
- a short lecture,
- one worked example,
- a tiny set of orientation problems.

Motivation is useful.
False evidence of mastery is not.

## Intake mix

Raindrop + HN + source docs.

## Accepted sources for this pass

1. **Andrej Karpathy — Doing well in your courses**  
   Accepted for three moves that transfer cleanly to proof-first self-study: plan from the big picture, treat replication as different from recognition, and let exercises outrank passive reading in math-heavy work.

2. **This repo's weekly review card**  
   Accepted because it already has the right traffic-light load check. What was missing was the explicit rule for what green, yellow, and red should do to secondary streams.

3. **This repo's dependency roadmap note**  
   Accepted because it already frames early linear algebra as a light preview before a fuller pass. This note just makes that demotion rule operational.

## Rejected sources for this bounded pass

1. **Ask HN: How to Study Mathematics?**  
   Rejected as an operational source for this note. The question is useful as problem framing, but the fetched excerpt did not yield a clean, durable rule for when to shrink or pause a second stream.

2. **How to Study Mathematics (UH)**  
   Rejected for this pass because the bookmark looked promising through Raindrop, but direct fetch failed here, so I did not want to smuggle in half-read advice from a search snippet.
