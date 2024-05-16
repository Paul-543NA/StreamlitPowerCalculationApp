markdown_header = """
This app calculates the minimum number of subjects needed to get a certain level of statistical significance for a given difference in proportions.

## Method

The statistical test in a [proportion z-test](proportions_ztest) with a [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction) for multiple testing. The code looks something like:
```python
total_trials_per_arm = n_participants * n_trials // (n_XAI_methods * n_uncertatinty_splits)
counts1 = int((0.5 + diff / 2) * total_trials_per_arm)
counts2 = int((0.5 - diff / 2) * total_trials_per_arm)
bonferroni_correction = (n_uncertatinty_splits - 1)

count = np.array([counts1, counts2])
nobs = np.array([total_trials_per_arm, total_trials_per_arm])
stat, pval = proportions_ztest(count, nobs)
pval = pval * bonferroni_correction
```
"""

markdown_info = """
### Statistical model

The power calculator considers the following scenario:
 - A trial is defined as a subject seeing one data point / AI advice and filling in answers (predict target, delegate to AI, ... ).
 - Each trial is assumed to be 10 seconds, therefore 5 mins dedicated to a phase mean 30 trials per subjects for this phase.
 - A phase is split into several sub-phases with different levels of hidden features (called uncertainty splits). In the case where we want to try hiding 0%, 20%, and then 50% of features, there would be 3 uncertainty splits. The calculator assumes that the total number of trials is evenly split between uncertainty levels.
 - The underlying statistical model assumes that we want to compare the proportion of time the AI is being delegated to (or any boolean variable really) for each level of hidden features (uncertainty splits). More concretely, for 3 levels of uncertainty, we consider $X_1 \sim \\text{Ber}(p_1)$, $X_2 \sim \\text{Ber}(p_2)$ and $X_3 \sim \\text{Ber}(p_3)$ and want to know the significance of two hidden parameters being different (i.e. $p_i \neq p_j$ ?).
 - The calculator gives the level of statistical significance we can expect depending on the difference in proportions we observe. More accurately, the model tests for a gap $\delta$ the p-value of the difference between the proportions $0.5-\delta/2$ and $0.5+\delta/2$. The p-value comes from a z-test for proportions.
 - Assuming that we want to compare each proportion $p_i$ to each other one $p_{j\\neq i}$, the calculator applies a Bonferroni correction for multiple testing (multiplying the p-value by the number of tests made on each dataset, in this case $1-N_{\\text{Uncertaitnty aplots}}$).
 
### Example

The following screenshot shows the power calculation results for 5 minuts of trials (aka 24 trials per subject) and two uncertainty splits (say 0% and 50%). The final plot shows that, with $400$ subjects, we can get a p-value of $0.001$ for any difference in proportions larger than $7\%$, anything between $5\%-7\%$ will get a p-value below $0.05$ and the smallest significant proportion we could get is just above $4\%$.

"""