// Vercel serverless function: the Character Studio asks here for three behaviour variants when it is
// hosted outside the Claude viewer. The page sends the full prompt; this just relays it to Claude.
//
// Environment: ANTHROPIC_API_KEY (required), STUDIO_PASSWORD (optional shared passcode so the public URL
// cannot spend your key), STUDIO_MODEL (optional, default claude-opus-5-5), STUDIO_EFFORT (optional, default low).
import Anthropic from "@anthropic-ai/sdk";

const MODEL = process.env.STUDIO_MODEL || "claude-opus-5-5";
const EFFORT = process.env.STUDIO_EFFORT || "low";

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  const hasKey = Boolean(process.env.ANTHROPIC_API_KEY);
  const guarded = Boolean(process.env.STUDIO_PASSWORD);

  if (req.method === "GET") {
    return res.status(200).json({ ok: true, claude: hasKey, protected: guarded, model: MODEL });
  }
  if (req.method !== "POST") return res.status(405).json({ error: "method_not_allowed" });
  if (!hasKey) return res.status(503).json({ error: "no_key", message: "ANTHROPIC_API_KEY is not set on the server." });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = null; } }
  if (!body || typeof body.prompt !== "string" || !body.prompt.trim()) return res.status(400).json({ error: "bad_request" });
  if (guarded && body.passcode !== process.env.STUDIO_PASSWORD) return res.status(401).json({ error: "passcode" });
  if (body.prompt.length > 60000) return res.status(413).json({ error: "prompt_too_large" });

  const client = new Anthropic();
  try {
    const response = await client.beta.messages.create({
      model: MODEL,
      max_tokens: 8000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      output_config: { effort: EFFORT },
      system: "You are an animator writing keyframe clips for a small character robot. Reply with only the JSON the user asks for: no prose, no code fence.",
      messages: [{ role: "user", content: body.prompt }],
    });
    if (response.stop_reason === "refusal") return res.status(422).json({ error: "refused" });
    const text = response.content.filter((b) => b.type === "text").map((b) => b.text).join("\n");
    if (!text.trim()) return res.status(502).json({ error: "empty" });
    return res.status(200).json({ text, truncated: response.stop_reason === "max_tokens", model: response.model });
  } catch (error) {
    if (error instanceof Anthropic.AuthenticationError) return res.status(500).json({ error: "bad_key" });
    if (error instanceof Anthropic.RateLimitError) return res.status(429).json({ error: "rate_limited" });
    if (error instanceof Anthropic.APIError) return res.status(502).json({ error: "api_error", status: error.status, message: error.message });
    return res.status(502).json({ error: "upstream", message: String(error && error.message || error) });
  }
}
