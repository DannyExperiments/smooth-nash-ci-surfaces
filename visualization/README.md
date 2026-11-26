# Differential planes at the projective boundary

[Download the offline explorer ZIP](https://raw.githubusercontent.com/DannyExperiments/smooth-nash-ci-surfaces/v1.0.0/visualization/smooth-nash-ci-surfaces-explorer.zip). Extract the archive and open index.html in a browser. No network connection is needed. The keyboard-accessible controls switch the matrix, the example pair, and the viewing angle.

The diagram lives in the three-dimensional real coefficient space for differentials in the local chart $A=\begin{pmatrix}1&x\\y&z\end{pmatrix}$. The theorem uses the complexifications of these planes.

| Boundary point | Row differential plane | Column differential plane | Common line |
| --- | --- | --- | --- |
| $(x,y,z)=(0,0,0)$ | $\langle dy,dz\rangle$ | $\langle dx,dz\rangle$ | $\langle dz\rangle$ |
| $(x,y,z)=(-1,-1,1)$ | $\langle dx,dy+dz\rangle$ | $\langle dy,dx+dz\rangle$ | $\langle dx+dy+dz\rangle$ |

At a mixed point, each player independently supplies a vector in their plane. A pair loses rank when one vector is zero or both are in the common line. The allowed pair space has dimension four and each of those conditions defines a dimension-two locus. The explorer gives examples of both independent and dependent pairs. Section 4 of the [paper](../paper/manuscript.pdf) treats all strata and all generic solutions.

## Regenerate the GIF

Run this with Python 3 and Pillow already present.

    python3 visualization/render.py

Arial is used by default on macOS. Set the environment variables Q220_FONT and Q220_BOLD_FONT to font file paths when using another system. Font choice and Pillow version can change the resulting GIF bytes.
