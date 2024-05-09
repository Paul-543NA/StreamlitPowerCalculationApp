import streamlit as st
from power_calculaations import plot_subjectsVSDiff

st.title('Power calculation for the UVA experiment')

st.write("""
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
""")

# Render a link of markdown text
st.markdown('## Parameters selection')

# Inputs the number of minutes as a discrete slider from 2 to 10
minutes_for_trials = st.slider('Minutes for trials', 2, 10, 4)
# And the number of uncertainty slits as a dropdown from 2 to 5
n_uncertatinty_splits = st.selectbox('Number of uncertainty splits', [2, 3, 4, 5])

# Render a link of markdown text
st.markdown('## Results')

# Get the figure
fig = plot_subjectsVSDiff(minutes_for_trials=minutes_for_trials, n_uncertatinty_splits=n_uncertatinty_splits)
# title="Minimum number of subjects to get a certain p-value\nfor a given difference in proportions",
st.write('The plot shows the minimum number of subjects needed to get a certain p-value for a given difference in proportions, using the parameters above.')

# Plot the figure
# The plot should not be wider than the content area
st.plotly_chart(fig, use_container_width=True)

