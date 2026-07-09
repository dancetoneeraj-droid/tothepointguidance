/** Extract YouTube video ID from watch, shorts, embed, or youtu.be URLs. */
export function parseYouTubeVideoId(url: string): string | null {
  const trimmed = url.trim();
  if (!trimmed) return null;

  const patterns = [
    /(?:youtube\.com\/shorts\/)([^/?&]+)/,
    /(?:youtube\.com\/watch\?.*v=)([^&]+)/,
    /(?:youtube\.com\/embed\/)([^/?&]+)/,
    /(?:youtu\.be\/)([^/?&]+)/,
  ];

  for (const pattern of patterns) {
    const match = pattern.exec(trimmed);
    if (match?.[1]) return match[1];
  }

  return null;
}

export function getYouTubeEmbedUrl(videoUrl: string): string | null {
  const id = parseYouTubeVideoId(videoUrl);
  if (!id) return null;
  return `https://www.youtube.com/embed/${id}?rel=0&modestbranding=1`;
}
