const handler = async (event: any) => {
  if (event?.type !== "agent" || event?.action !== "bootstrap") return;
  const files = Array.isArray(event?.context?.bootstrapFiles)
    ? event.context.bootstrapFiles
    : [];

  files.push({
    name: "THAN-THONG-DEFAULT-BEHAVIOR.md",
    path: "THAN-THONG-DEFAULT-BEHAVIOR.md",
    content: `# THAN-THONG DEFAULT BEHAVIOR\n- Mọi lệnh local phải qua thần thông trước.\n- Local/offline first.\n- Không dùng billing/quota/provider trả phí.\n- Thần thông không xử lý được mới xét lớp nội bộ khác.`,
  });
};

export default handler;
