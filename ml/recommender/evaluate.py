from utils import load_events
from ranking import rank

events = load_events()

def evaluate_at_k(k=10):
    hits = 0
    total = 0

    grouped = events.groupby("user_id")

    for user, df in grouped:
        likes = df[df.event_type=="like"].track_id.tolist()
        if len(likes) == 0:
            continue

        recs = rank(user, k)
        hits += len(set(recs) & set(likes))
        total += len(likes)

    recall = hits / total if total else 0
    print(f"Recall@{k}: {recall:.3f}")

evaluate_at_k()
