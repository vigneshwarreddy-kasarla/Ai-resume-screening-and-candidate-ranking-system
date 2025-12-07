import numpy as np

def cosine_sim(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def rank(job_vec, candidate_vecs, names):
    results = []
    for vec, name in zip(candidate_vecs, names):
        score = cosine_sim(job_vec, vec)
        results.append((score, name))
    return sorted(results, reverse=True)
