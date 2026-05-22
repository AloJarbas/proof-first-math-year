# Linear algebra bridge packet

This note is for the moment when proof practice has started to stick, calculus is no longer taking all available attention, and linear algebra stops looking like a pile of matrix tricks and starts looking like a real subject.

The goal is not to rush into abstraction for its own sake.

The goal is to cross the bridge cleanly.

## What should already be true

Before linear algebra becomes a main lane, I want these to be at least somewhat real:

- direct proof, contrapositive, contradiction, and induction are no longer alien moves
- function notation and quantifiers do not immediately scramble the page
- derivatives, integrals, and basic limit arguments no longer consume all working memory
- you can read a definition slowly and tell what must be shown to use it

If those are still shaky, linear algebra often gets mistaken for a notation problem when the real issue is proof load plus symbol load at the same time.

## What the bridge is trying to prevent

A lot of first linear algebra study goes wrong in one of three ways:

1. **row-reduction tunnel vision**: everything becomes elimination tricks and nothing becomes structure
2. **abstraction whiplash**: the course jumps from matrices to vector spaces before the old objects feel connected
3. **calculus leakage**: every new object gets misread as if it were a function-of-one-variable exercise

The bridge should stop all three.

## The first four ideas that matter

### 1. Linear combinations are the real atoms

The first serious question is not "how do I multiply matrices?"

It is this:

> what can be built from these vectors by scaling and adding?

That is the doorway to span, dependence, basis, and column space.

### 2. Systems are geometry plus structure

A linear system is not just a bookkeeping exercise.

It is also:

- an intersection question
- a consistency question
- a dependence question
- a map from coefficients to outcomes

Row reduction matters because it exposes that structure. It is not the destination.

### 3. Matrices represent maps

The healthiest early sentence in linear algebra is:

> a matrix is a concrete representation of a linear map after choosing coordinates.

That one sentence keeps the subject from collapsing into symbol pushing.

### 4. Basis changes are not decoration

Changing basis is where a lot of the subject suddenly becomes coherent.

It explains why the same map can look messy in one coordinate system and simple in another. It also prepares the ground for eigenvectors without turning them into magic.

## A compact four-week bridge

### Week 1: combinations, span, dependence

Focus:

- linear combinations
- span
- linear independence and dependence
- solving small systems as structure, not only mechanics

Minimum habit:

- for each solved system, say what the solution means in span language

### Week 2: basis, dimension, column space

Focus:

- basis as a minimal spanning set
- dimension as a structural count, not just a number
- pivots and free variables
- column space and nullspace as different views of the same matrix

Minimum habit:

- after row reduction, describe what changed and what did not change

### Week 3: linear maps and matrix representation

Focus:

- linear transformations
- standard matrix of a map
- composition
- kernel and image

Minimum habit:

- say what the map does before doing the computation

### Week 4: basis change and first eigenvalue intuition

Focus:

- coordinate vectors relative to a basis
- change of basis
- invariant directions as the motivation for eigenvectors
- diagonalization as a simplification story, not a ritual

Minimum habit:

- ask whether the new basis reveals structure the old basis hid

## Problems that earn their keep

Good bridge problems are not giant calculation sheets.

They are short problems that force one structural sentence after the computation.

Examples:

1. Decide whether one vector lies in the span of two others, then explain the answer geometrically.
2. Give two different spanning sets for the same subspace and decide which one is a basis.
3. Row-reduce a matrix and say what the pivots tell you about dependence among the original columns.
4. Write down a linear map in words, then find its matrix in the standard basis.
5. Change to a basis that makes a simple shear or scaling map easier to read.

## What to read with care

If you use Axler, the conceptual spine is strong, but you still need enough contact with systems and matrices that the abstractions keep a grip on something concrete.

If you use 18.06-style material, the computational spine is strong, but you should keep restating what the operations mean structurally so the subject does not flatten into elimination recipes.

That is why this bridge exists. The point is not to choose one camp. The point is to keep both structure and calculation alive together.

## A simple readiness test

I would move linear algebra from secondary lane to real lane if the answer to most of these is yes:

- can you explain linear independence without immediately reaching for a memorized test?
- can you solve a system and then say what it implies about span or dependence?
- can you describe a matrix as a map, not just an array?
- can you read basis and dimension statements without freezing?
- can you tolerate a proof that is short but abstract?

If not, keep the lane open in preview mode and keep strengthening proof fluency.

That is not delay for its own sake. It is load management.

## Companion notebook

The bridge now has a practice half:

- `notebooks/linear-algebra-bridge-problem-bundle.ipynb`

That notebook keeps the first pass tight:

- one span/dependence problem
- one basis/dimension problem
- one pivot-column/nullspace problem
- one matrix-as-map problem
- one first change-of-basis problem

Use it slowly.
The point is not speed or volume.
The point is to force one structural sentence after each computation so the subject does not collapse back into row-reduction reflexes.

## Next useful artifact

If this bridge gets one more pass, the strongest follow-up is a second bundle with slightly harder prompts:

- one short proof about a subspace or span claim
- one kernel/image proof
- one basis-extension exercise
- one diagonalization failure case that has to be explained, not just computed around

That would test whether the bridge is holding under a little more abstraction instead of only under friendly first examples.

Jarbas
