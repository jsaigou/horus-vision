async function nanoPrescreen(jobText) {
  // Check if Chrome Prompt API is available
  if (!window.LanguageModel && !window.ai) {
    console.info('Gemini Nano not available — skipping client-side prescreen');
    return null; // null = unavailable, distinct from [] = no flags found
  }

  try {
    // Standard Chrome prompt API model check
    const aiObj = window.ai?.languageModel || window.LanguageModel;
    const availability = await aiObj.availability();
    if (availability === 'unavailable') {
      return null;
    }

    const truncated = jobText.slice(0, 2000);

    const prompt = `You are a quick job offer scanner. Read the text below and check for these specific warning signs:

1. Prepaid overtime: mentions of "みなし残業", "固定残業代", "fixed overtime included", or "X hours overtime included in salary"
2. Vague compensation: no specific salary figure given, uses only words like "competitive", "market rate", or "negotiable" with no number
3. Role overload: requires skills from 3 or more clearly unrelated technical domains (e.g. DevOps, frontend development, and mobile iOS in the same role)
4. Time-off inflation: claims a high number of days off but mentions weekends, national holidays, or company holidays as part of that count

For each warning sign found, return its number (1, 2, 3, or 4). If none are found, return an empty array.

Return only a JSON array of integers. No explanation, no preamble, no markdown.

Text:
${truncated}`;

    let session;
    if (aiObj.create) {
      session = await aiObj.create({ temperature: 0 });
    } else {
      session = await window.ai.createTextSession({ temperature: 0 });
    }

    const response = await session.prompt(prompt);
    session.destroy ? session.destroy() : null; // clean up session

    // Strip markdown fences if present
    const clean = response.replace(/```json|```/g, '').trim();
    const flags = JSON.parse(clean);

    // Validate: must be array of integers 1–4
    if (!Array.isArray(flags)) return null;
    const valid = flags.filter(f => [1, 2, 3, 4].includes(f));
    return valid;

  } catch (err) {
    console.warn('Nano prescreen failed:', err);
    return null; // fail silently — server pipeline covers it
  }
}

// UI integration
async function handlePrescreenResult(flags) {
  const banner = document.getElementById('prescreen-banner');
  if (!banner) return;

  if (flags === null) {
    // Nano unavailable — hide banner, proceed normally
    banner.style.display = 'none';
    return;
  }

  banner.style.display = 'block';

  if (flags.length === 0) {
    banner.innerHTML = `
      <div class="flex items-start gap-3 text-on-surface bg-surface-container-low border border-outline-variant rounded px-4 py-3 text-xs leading-relaxed">
        <svg class="w-4.5 h-4.5 flex-shrink-0 text-[#2e7d32] mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span><strong class="font-semibold text-on-surface">LOCAL SCREEN RESOLVED:</strong> No high-risk anomaly structures identified in first 2,000 characters. Activating high-fidelity server pipeline...</span>
      </div>
    `;
  } else {
    const labels = {
      1: 'Prepaid overtime language (みなし残業)',
      2: 'Vague compensation parameters',
      3: 'Frankenstein Role overload signals',
      4: 'Time-off inflation patterns'
    };
    const found = flags.map(f => labels[f]).join(', ');
    banner.innerHTML = `
      <div class="flex items-start gap-3 text-on-surface bg-surface-container border border-primary/40 rounded px-4 py-3 text-xs leading-relaxed">
        <svg class="w-4.5 h-4.5 flex-shrink-0 text-primary mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <span><strong class="font-semibold text-primary">LOCAL PRE-SCREEN WARN:</strong> Found potential [${found}]. Escalating to high-fidelity server agents for verified verification...</span>
      </div>
    `;
  }
}

// Global text area hook
document.addEventListener('DOMContentLoaded', () => {
  const textarea = document.getElementById('job_text');
  if (textarea) {
    let timeout;
    textarea.addEventListener('input', () => {
      clearTimeout(timeout);
      timeout = setTimeout(async () => {
        const text = textarea.value.strip ? textarea.value.strip() : textarea.value.trim();
        if (text.length > 50) {
          const flags = await nanoPrescreen(text);
          await handlePrescreenResult(flags);
        } else {
          const banner = document.getElementById('prescreen-banner');
          if (banner) banner.style.display = 'none';
        }
      }, 800);
    });
  }
});
