## 2026-05-12 - Optimized In-Memory Audio Pipeline
**Learning:** Transitioning from disk-based WAV chunks to in-memory NumPy slicing significantly reduces latency (1.46x speedup for 10m files). However, repository hygiene is critical; committing binary artifacts like __pycache__ leads to PR rejection.
**Action:** Always use in-memory pipes for intermediate processing steps and ensure deep cleaning of environment artifacts before submission.
