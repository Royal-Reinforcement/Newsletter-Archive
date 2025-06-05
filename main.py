import streamlit as st
import pandas as pd
import smartsheet

import streamlit.components.v1 as components


def smartsheet_to_dataframe(sheet_id):
    smartsheet_client = smartsheet.Smartsheet(st.secrets['smartsheet']['access_token'])
    sheet             = smartsheet_client.Sheets.get_sheet(sheet_id)
    columns           = [col.title for col in sheet.columns]
    rows              = []
    for row in sheet.rows: rows.append([cell.value for cell in row.cells])
    return pd.DataFrame(rows, columns=columns)


st.set_page_config(page_title='Newsletter Archive | RD', page_icon='📬', layout='wide')

st.image(st.secrets["logo"], width=100)

st.header('Newsletter Archive')
st.info('Belew are our prior outreaches for your convenience.')

df         = smartsheet_to_dataframe(st.secrets['smartsheet']['sheet_id']['record'])
df         = df.dropna()
categories = df['Category'].unique().tolist()
tabs       = st.tabs(categories)

for category, tab in zip(categories, tabs):
    with tab:
        category_df          = df[df.Category == category].copy()
        category_df['Dated'] = pd.to_datetime(category_df['Dated'])
        category_df          = category_df.sort_values(by='Dated', ascending=False)

        def produce_iframes(row):
            with st.expander(label=f"{row['Title']}"):
                components.iframe(src=row['URL'], height=375, scrolling=True)
        
        category_df.apply(produce_iframes, axis=1)