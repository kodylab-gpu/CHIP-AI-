# Chip AI — Vercel

## Deploy
1. GitHub'da yangi repository yarating.
2. Ushbu papka ICHIDAGI `index.html`, `api/`, `requirements.txt` va `README.md` ni repository ildiziga yuklang.
3. Vercel -> Add New -> Project -> GitHub repository -> Import.
4. Framework Preset: Other; Root Directory: `./`; Build Command va Output Directory override qilmang.
5. Vercel Project -> Settings -> Environment Variables:
   - `AI_API_KEY` = AI provayder API kaliti (maxfiy)
   - `AI_MODEL` = provayderda mavjud model ID (masalan, OpenRouter hisobingizdagi bepul model ID)
   - `AI_BASE_URL` = `https://openrouter.ai/api/v1` (ixtiyoriy)
6. Deploy yoki environment variables qo‘shilgandan keyin Redeploy qiling.

`/` statik `index.html` ni, `/api/chat` esa Vercel Python Function'ni ishlatadi.

Eslatma: Bepul API model mavjudligi, kvotalar va Vercel serverless limitlari o‘zgaradi. Rasm yaratish va real internet qidiruvi hali ulanmagan. Public saytda API sarfini cheklash uchun rate limiting va abuse protection qo‘shish tavsiya etiladi.
