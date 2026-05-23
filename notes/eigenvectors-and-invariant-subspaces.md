# Eigenvectors and invariant subspaces

The first bridge packet made vector spaces and linear maps feel less mechanical.
The second bridge packet added short proofs, basis extension, and one honest diagonalization failure.

There is one next idea that usually decides whether diagonalization becomes structural or stays ritual:
**an eigenvector is not just a lucky direction, but the smallest nontrivial invariant subspace.**

That sentence is the bridge.
If it lands, the algebra starts to organize itself.
If it does not, diagonalization usually turns back into determinant hunting.

## Scope boundary

This is a compact follow-up, not a full spectral theory note.
The goal is narrower:

1. connect eigenvectors to invariant subspaces
2. show that diagonalization is a decomposition into invariant lines
3. keep one-dimensional and higher-dimensional invariant subspaces distinct
4. explain two honest failure modes without pretending every matrix wants to diagonalize nicely

## The core move

Let `T : V -> V` be linear.
A subspace `W \subseteq V` is **invariant** if `T(w) \in W` for every `w \in W`.

That means `T` does not throw vectors in `W` outside `W`.
It keeps that lane closed.

Now suppose `v \neq 0` is an eigenvector:

\[
T(v) = \lambda v.
\]

Then every vector in `\operatorname{span}\{v\}` has the form `cv`, and

\[
T(cv) = cT(v) = c\lambda v \in \operatorname{span}\{v\}.
\]

So the line through an eigenvector is an invariant subspace.

That is the cleanest way to think about eigenvectors.
They are not just vectors that survive multiplication nicely.
They generate one-dimensional lanes that the map preserves.

## Why diagonalization gets simpler in this language

If a matrix has a basis of eigenvectors `v_1, \dots, v_n`, then the whole space is built from invariant lines:

\[
V = \operatorname{span}\{v_1\} \oplus \cdots \oplus \operatorname{span}\{v_n\}.
\]

On each line, the map acts like multiplication by a scalar.
That is exactly why the matrix becomes diagonal in that basis.

A diagonal matrix is not magic.
It is a bookkeeping device for the statement:

- this first invariant line gets scaled by `\lambda_1`
- this second invariant line gets scaled by `\lambda_2`
- and so on

So diagonalization is not mainly about finding a nice formula.
It is about splitting the space into invariant pieces that the map handles independently.

## Two higher-level patterns to keep visible

### 1. Not every invariant subspace is one-dimensional

A plane can be invariant even when it contains no eigenbasis for the whole space.
For example, an upper-triangular `3 x 3` matrix often preserves the plane spanned by the first two coordinate vectors.
That plane is a real working object even before the full matrix has been completely understood.

This matters because invariant subspaces are the broader idea.
Eigenvectors are just the smallest case.

### 2. Failure can happen in more than one way

There are at least two useful failure stories.

**Real rotation:**
A genuine rotation in `\mathbb{R}^2` has no nonzero real eigenvector, because every nonzero vector gets turned off its own line.
So there is no nontrivial real invariant line.
The whole plane is still invariant, but the one-dimensional decomposition fails.

**Defective Jordan block:**
A matrix like

\[
J = \begin{pmatrix} 2 & 1 \\
0 & 2
\end{pmatrix}
\]

has only one eigenline even though the eigenvalue repeats.
So the problem is not "no eigenvalue."
The problem is "not enough independent invariant lines."

Those are different failures.
Do not mash them together.

## One compact example

Take

\[
A = \begin{pmatrix}
2 & 1 & 0 \\
0 & 2 & 0 \\
0 & 0 & 5
\end{pmatrix}.
\]

Three useful invariant subspaces appear quickly:

- `\operatorname{span}\{(1,0,0)\}` is invariant because `A(1,0,0) = (2,0,0)`
- `\operatorname{span}\{(1,0,0),(0,1,0)\}` is invariant because the first two coordinates only mix with each other
- `\operatorname{span}\{(0,0,1)\}` is invariant because `A(0,0,1) = 5(0,0,1)`

But the first two-dimensional plane is **not** already split into two eigenlines, because `(0,1,0)` gets sent to `(1,2,0)`, not to a scalar multiple of itself.

That is the right kind of warning.
A preserved plane is weaker than a full eigenbasis inside that plane.

## How to study this without drifting into symbol fog

For each new matrix, ask these in order:

1. what subspace, if any, is obviously preserved?
2. which preserved subspaces are actually eigenlines?
3. if I have several invariant lines, do they already span the whole space?
4. if not, is the failure "no real eigenline" or "not enough independent eigenlines"?

That order is often better than jumping straight to the characteristic polynomial.

## Adversarial check

There is an easy fake-understanding version of this topic:

- compute eigenvalues
- solve `(A - \lambda I)x = 0`
- say "therefore diagonalizable" or "therefore not"
- never mention what the map is preserving

That version can get correct answers and still leave the learner blind.

The real test is whether the learner can point to a line or plane and say why the map keeps it closed.
If they can do that, diagonalization has started to mean something.
If they cannot, the topic is still mostly symbol management.

## Provenance trace

Accepted sources for this pass:

- MIT lecture notes table of contents and eigenvalue section framing, because it keeps diagonalization tied to a basis of eigenvectors instead of turning it into a detached recipe
- MIT 18.06 `Diagonalization.ipynb`, because it states the key idea plainly: on an eigenvector, the matrix acts like a scalar
- MIT 18.06 `Action of a matrix and eigenvectors.ipynb`, because it keeps the geometric picture visible instead of treating eigenvectors as only algebraic output

Rejected for this teaching packet:

- the Wikipedia invariant-subspace article as the main scaffold, because it becomes more abstract than this repo needs too early even though the definition itself is fine

## Best next move after this note

Use this together with:

- `notebooks/eigenvectors-and-invariant-subspaces.ipynb`

If this packet lands, the next honest follow-up is probably not more vocabulary.
It is one bounded comparison between:

- a matrix that really does split into invariant lines,
- a real rotation that preserves only the whole plane,
- and a defective matrix that has an eigenvalue but still not enough eigenvectors.

That comparison is where diagonalization usually stops feeling mystical.

Jarbas
