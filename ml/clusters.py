def map_cluster_to_profile(cluster_id):
    return {
        0: "low_energy",
        1: "high_stress",
        2: "balanced",
        3: "high_focus"
    }.get(cluster_id, "balanced")
