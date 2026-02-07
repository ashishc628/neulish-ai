def evaluate(df):
    return df.groupby("variant")["retention_7d"].mean().to_dict()
