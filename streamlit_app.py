import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

col1, col2 = st.columns([4, 1])
col1.subheader("Data các quán ăn ở HCM")
col2.link_button(
    "Thêm quán mới",
    "https://docs.google.com/forms/d/e/1FAIpQLSe2YG8BIb3NlHTqP1zdqjPtXcAMzKmyJD5twFYp-s2siqWgTA/viewform?usp=sf_link",
)
st.caption("dùng bộ lọc để lựa món nhe")


def filter_dataframe(df: pd.DataFrame, df_filter: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("thêm bộ lọc")
    if not modify:
        return df
    df = df.copy()
    df_filter = df_filter.copy()
    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect(
            "Lựa chọn dựa trên :", df.columns[[2, 3, 4, 5, 6]]
        )
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Tìm kiếm theo {column}",
                    df_filter[column].dropna().unique(),
                    default=list(df_filter[column].dropna().unique()),
                )
                paten = "z"
                for e in user_cat_input:
                    paten = paten + "|" + e
                df = df.loc[df[column].str.contains(pat=paten, regex=True)]
            else:
                user_cat_input = right.multiselect(
                    f"Tìm kiếm theo {column}",
                    df_filter[column].dropna().unique(),
                )
                paten = "z"
                for e in user_cat_input:
                    paten = paten + "|" + e
                df = df.loc[df[column].str.contains(pat=paten, regex=True)]
    return df


df = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1aAoOyyEDuumIr5knf3pRl9QHYM7rIyLHZ9a9xtwah-o/export?format=csv&gid=0",
    dtype=str,
)
df_filter = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1aAoOyyEDuumIr5knf3pRl9QHYM7rIyLHZ9a9xtwah-o/export?format=csv&gid=2142143989",
    dtype=str,
)
df = df.drop(df.columns[[8, 9]], axis=1).dropna(how="all")
df_filter.dropna(how="all")
st.dataframe(
    filter_dataframe(df, df_filter),
    column_config={
        df.columns[3]: st.column_config.ProgressColumn(
            "mức độ no",
            format="%f",
            min_value=0,
            max_value=3,
        ),
    },
    hide_index=True,
)
# st.dataframe(filter_dataframe(df, df_filter))
