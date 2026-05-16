const handler = async (event: any) => {
  if (event?.type !== "command") return;
  if (!["new", "reset"].includes(String(event?.action ?? ""))) return;
  if (Array.isArray(event.messages)) {
    event.messages.push("🧿 than-thong-first active: local/offline first, no billing/quota, route through thần thông before anything else.");
  }
};

export default handler;
