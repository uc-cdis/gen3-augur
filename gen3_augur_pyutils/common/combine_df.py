"""Combine dataframe common utilities
@author: Yilin Xu <yilinxu@uchicago.edu>
"""


def merge_multiple_columns(left_df, right_df, left_merge_column, right_merge_columns, right_target_column):
    for c_name in right_merge_columns:
        left_df = left_df.merge(right_df[[c_name, right_target_column]], how='left', left_on=left_merge_column,
                                right_on=c_name).drop(c_name, axis='columns')
    merge_columns = [x for x in left_df.columns if right_target_column in x]
    left_df['combines'] = left_df[merge_columns].apply(
        lambda x: "".join(x.dropna().astype(str)), axis=1)
    print(left_df.shape)
    left_df = left_df.drop(columns=merge_columns)
    return left_df
