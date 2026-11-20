# Chip AI — Vercel starter

Upload the **contents of this folder** to the GitHub repository root. Delete the old root `chat.py`, `pyproject.toml`, and any previous conflicting `vercel.json` or Python build configuration. The new backend is `api/chat.py` and Vercel installs packages from `requirements.txt`.

1. Import repository into Vercel, Framework Preset: Other, Root Directory: `./`.
2. Project Settings → Environment Variables (sometimes shown under Environment/Variables):
   - `AI_API_KEY`: your provider's secret key
   - `AI_MODEL`: exact provider model ID
   - `AI_BASE_URL`: `https://openrouter.ai/api/v1` (optional; default set)
   Select Production and save. Redeploy after changing variables.
3. Visit `/` for the interface and `/api/health` for backend health. `configured: false` means variables have not been configured.

The UI is functional, but image generation and live web browsing are not implemented. Provider free tiers may have quotas. Do not put secrets in frontend files or GitHub.
