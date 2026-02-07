def generate_weekly_summary(stats):
    summary = []

    if stats["avg_sleep"] >= 7:
        summary.append(
            "Your sleep was fairly consistent this week, which supports focus and emotional balance."
        )
    else:
        summary.append(
            "Sleep was a bit shorter this week. Gentle sessions seemed especially helpful."
        )

    if stats["stress_trend"] == "down":
        summary.append(
            "You appeared calmer as the week progressed."
        )
    elif stats["stress_trend"] == "up":
        summary.append(
            "Stress felt higher toward the end of the week. Slower sessions may help next week."
        )

    if stats["completion_rate"] >= 0.7:
        summary.append(
            "Consistency mattered more than duration — you showed up regularly."
        )

    summary.append(
        "There’s no need to push. Small, steady steps are working."
    )

    return " ".join(summary)
