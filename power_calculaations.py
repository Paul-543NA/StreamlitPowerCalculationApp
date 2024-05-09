import plotly.graph_objects as go
import numpy as np
from statsmodels.stats.proportion import proportions_ztest


def find_min_with_condition(f, tol, min_step):
    new = 1
    old = 0
    step = 100
    while step > min_step or f(new) > tol:

        if f(new) < tol:
            new = old
            step = step / 10
        else:
            old = new
            new += step

    return new


def plot_subjectsVSDiff(
        minutes_for_trials=4,
        n_uncertatinty_splits=2,
        diff_values=np.arange(0.1, 0.01, -0.01),
) -> go.Figure:
    total_time_for_trials_s = minutes_for_trials * 60
    n_XAI_methods = 4
    p_thresholds = [0.05, 0.01, 0.001]
    single_trial_duration_s = 10
    n_trials = total_time_for_trials_s // single_trial_duration_s
    corresponding_n_subjects = {p: list() for p in p_thresholds}

    def get_n_subjects(p, diff):

        def f(n_participants):
            total_trials_per_arm = n_participants * n_trials // (n_XAI_methods * n_uncertatinty_splits)
            counts1 = int((0.5 + diff / 2) * total_trials_per_arm)
            counts2 = int((0.5 - diff / 2) * total_trials_per_arm)
            bonferroni_correction = (n_uncertatinty_splits - 1)

            count = np.array([counts1, counts2])
            nobs = np.array([total_trials_per_arm, total_trials_per_arm])
            stat, pval = proportions_ztest(count, nobs)
            pval = pval * bonferroni_correction

            return pval

        return find_min_with_condition(f=f, tol=p, min_step=1)

    for p in p_thresholds:
        for diff in diff_values:
            corresponding_n_subjects[p].append(get_n_subjects(p=p, diff=diff))

    fig = go.Figure()
    for p, line_style in zip(p_thresholds, ['solid', 'dot', 'longdash']):
        fig.add_trace(go.Scatter(x=corresponding_n_subjects[p], y=diff_values, mode='lines', name=f"p={p}", line=dict(dash=line_style)))

    # Original xlim should be 0, 1000
    fig.update_layout(
        xaxis_title="Number of subjects",
        yaxis_title="Difference in proportions",
        legend_title="p-value",
        xaxis=dict(range=[0, 1000]),
    )

    return fig


