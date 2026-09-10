# Assignment 1 Report

## Sanity Checks
The rimless wheel model was tested to verify the continuous dynamics and the impact/reset behavior. At first, the initial conditions were not generating enough energy to demonstrate the reset code since it stopped at the first spoke. After adjustements, a test case with `N = 6` spokes, a slope of `γ = 10°`, and an initial angular velocity of `2 rad/s` was used to show at least few rotations. 

### Continuous Dynamics Check
During the continuous portion of each step, the rimless wheel follows the inverted pendulum dynamics

\[
\ddot{\theta} = \frac{g}{l}\sin(\theta).
\]

The sign of the angular acceleration was checked at different angles. For `θ < 0`, representing the region where the spoke first contacts the ground to the vertical position, the angular acceleration is negative as expected, meaning the wheel is slowing as it reaches the vertical position. For `θ > 0`, representing the region from the vertical position until the reset when the next spoke contacts the ground, the angular acceleration is positive also as expected, with the wheel accelerating toward the next impact. 

### Reset Dynamics Check
For `N = 6`,

\[
\alpha = \frac{\pi}{N} = 30^\circ.
\]

With `γ = 10°`, the expected impact angle is

\[
\theta^- = \gamma + \alpha = 40^\circ \approx 0.6981 \text{ rad}.
\]

The simulation detected impacts at approximately `0.6981 rad`, consistent with the expected impact condition.

After impact, the stance leg changes and the angle is reset according to

\[
\theta^+ = \gamma - \alpha = -20^\circ \approx -0.3491 \text{ rad}.
\]

The simulation reset the angle to approximately `-0.3491 rad` after each impact.
These angles align with the expected reset positioning given the chosen initial conditions

### Impact Event
The angular velocity after impact is given by

\[
\dot{\theta}^+ = \dot{\theta}^-\cos(2\alpha).
\]

For `N = 6`, `cos(2α) = cos(60°) = 0.5`, so the angular velocity should be reduced by half at each impact. For example, the first simulated impact produced

\[
\dot{\theta}^- = 2.7216 \text{ rad/s}
\]

and

\[
\dot{\theta}^+ = 1.3608 \text{ rad/s},
\]

which agrees with the expected impact relationship.

The simulation also showed that after several impacts the wheel no longer had enough angular velocity to complete another step and began to fall backward, demonstrating that not all initial conditions result in sustained rolling.

## State-Space Plot

## Return-Map Plot

## Parameter Affects on RoA and Convergence