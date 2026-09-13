# Positive-height feasibility is automatic at the equality stage

## Statement

For every physical-step equality partition in the current triangular tagged-lift ansatz, vertical equality imposes no feasibility obstruction.

If the horizontal equality system is rationally feasible, then the same coloring has a positive-height member with every normalized physical-step height equal to one.

## Proof

For a state edge `e=(s,t)`, the normalized vertical adjacent increment is

\[
1+c_t-c_s.
\]

Set every vertical state tag to zero:

\[
c_s=0\qquad\text{for every state }s.
\]

Then every reachable adjacent edge has vertical increment exactly

\[
1.
\]

Therefore any requested equality between physical steps is automatically satisfied in the vertical coordinate, and every adjacent height increment is strictly positive.

Thus the exact-five equality-feasibility problem is entirely controlled by the two horizontal coordinates.

---

## Cycle-space form

For color matrix `C` and cycle basis `Y`, with `M=YC`, the normalized height equation is

\[
Mr=Y\mathbf1.
\]

Because each edge belongs to exactly one color,

\[
C\mathbf1_5=\mathbf1_E,
\]

so

\[
M\mathbf1_5=Y\mathbf1_E.
\]

Hence

\[
\boxed{r=\mathbf1_5}
\]

is always a height solution.

For rank18 / `h=1`, if `n` spans `ker M`, all height-step solutions are

\[
r=\mathbf1_5+\lambda n.
\]

The positive-height interval always contains

\[
\boxed{\lambda=0},
\]

where all five height steps equal one.

## Consequence

CYCLE2 only needs to test horizontal cycle consistency. Every horizontal equality survivor already represents at least one positive-height tagged lift.

For later direct geometry, positivity is still useful to guarantee that parameter-independent proportional displacement witnesses correspond to three distinct visited points for every admissible positive-height member. But positivity is not an additional existence filter on the equality census.

## Claim boundary

This statement concerns feasibility of the vertical equality coordinate. It does not assert non-collinearity or construct a five-step walk satisfying the Erdős condition.
