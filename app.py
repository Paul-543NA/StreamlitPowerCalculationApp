import streamlit as st
from power_calculaations import plot_subjectsVSDiff
from contents import markdown_header, markdown_info

st.title('Power calculation for the UVA experiment')

st.write(markdown_header)

## Select on a tab menu to show the calculator page of the info one
calculator_tab, info_tab = st.tabs(['Calculator', 'Statistical model info'])

with calculator_tab:
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

with info_tab:
    st.markdown(markdown_info)
    st.image('./example.png', caption='Example of power calculation results', use_column_width=True)