import pandas as pd
import random

rows = []

for _ in range(1000):
    stressed = random.randint(1, 10)
    focused = random.randint(1, 10)

    rows.append({
        "stress": stressed,
        "focus": focused,
        "rec_relax": int(stressed > 6),
        "rec_memory": int(focused < 6),
        "rec_number": int(focused > 6),
        "rec_sleep": int(stressed > 8)
    })

df = pd.DataFrame(rows)
df.to_csv("ml/data/neulish_training_data.csv", index=False)
print("✅ Dummy training data generated:", df.shape)
