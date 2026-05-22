# Linear algebra bridge follow-up packet

The first bridge bundle was intentionally friendly.
It asked for structural sentences after short computations so the subject would stop feeling like row-reduction theater.

That is not enough by itself.

If the bridge is actually holding, the next step is to put a little proof pressure on it.
Not a full abstract linear algebra course. Not a long worksheet. Just enough pressure to reveal whether the learner can keep the structure alive when the problems stop being purely mechanical.

## What this follow-up is trying to test

I want four things to stay visible at once:

1. subspace claims are not just vocab words
2. kernel and image statements can be argued, not only computed
3. basis extension is a real construction move, not a theorem you vaguely remember seeing
4. diagonalization is a structural simplification story, and some maps honestly fail that story

If those four still collapse into symbol panic, the right move is not to race ahead.
It is to stay here a little longer.

## What should already feel real before doing it

Before this bundle, the learner should be able to do the following without freezing immediately:

- explain span and linear independence in plain language
- row-reduce a small matrix and say what the pivots mean about the original columns
- describe a matrix as a representation of a linear map in coordinates
- work through the first bridge notebook without treating every answer as magic after the fact

If not, go back to the first bridge packet first.
This follow-up is supposed to test the bridge, not replace it.

## The four pressure points

### 1. A short subspace proof

At the first pass, it is enough to recognize a span or solve a dependence relation.
At the second pass, the learner should be able to prove that a set is or is not a subspace by checking the actual closure conditions instead of hand-waving at the shape.

### 2. Kernel and image as proof objects

A lot of early learners can compute a nullspace basis and still cannot explain why the kernel of a linear map must itself be a subspace.
That gap matters.
It is the difference between following a recipe and understanding what kind of object is on the page.

### 3. Basis extension as a controlled move

The first bridge says that a basis is a minimal spanning set.
The follow-up should make the learner perform a basis extension by hand and explain why the new set is still independent and now spans the whole space.

### 4. Diagonalization failure without superstition

A bad first encounter with diagonalization trains the wrong reflex:
try to compute around the problem until the matrix either behaves or the page runs out.

A better first encounter with failure is smaller and cleaner:
find a matrix with too few independent eigenvectors and explain why the problem is structural, not just computational bad luck.

## Companion notebook

Use this note together with:

- `notebooks/linear-algebra-second-bridge-bundle.ipynb`

That notebook stays markdown-only on purpose.
The point is not to hide the reasoning inside software.
The point is to make the learner read, write, and justify the ideas directly.

## How to use the bundle

Do not try to sprint through it.

For each problem:

1. write the method you plan to use before doing any algebra
2. solve it cleanly
3. add one structural sentence that says what the answer means
4. add one failure sentence about the most likely wrong move

That last step matters more than it looks.
A lot of fake understanding survives because the learner never says what the tempting bad move would have been.

## Adversarial check

There is an easy way to make a bridge packet look deeper than it is:
throw in abstract words, longer proofs, and a diagonalization exercise, then pretend rigor happened.

This follow-up tries not to do that.
The problems are still short.
The scope is still narrow.
The point is not abstraction for prestige.
The point is to test whether the first bridge changed the learner's habits enough that a slightly more structural notebook now lands cleanly.

## Best next move after this packet

If this follow-up works, the strongest continuation is probably not another notebook immediately.
It is one of these:

- a short worked-proof packet for linear algebra where a few proof steps are deliberately omitted
- a compact eigenvector-and-invariant-subspace note that keeps geometry and algebra connected
- a weekly mixed problem block that alternates proof questions with small computations and short retrospective checks

Jarbas
