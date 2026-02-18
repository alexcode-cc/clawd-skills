/**
 * List chat items from LINE OA chat list with unread detection.
 * Run via browser evaluate on chat.line.biz.
 *
 * Returns: [{ name, time, lastMsg, unread }]
 * Unread selector: span.badge.badge-pin
 */
(() => {
  const items = document.querySelectorAll('.list-group-item-chat');
  return Array.from(items).map(el => {
    const h6 = el.querySelector('h6');
    const preview = el.querySelector('.text-muted.small');
    const prevText = preview?.textContent?.trim() || '';

    // Time: short .text-muted that isn't the preview
    const allMuted = el.querySelectorAll('.text-muted');
    let time = '';
    for (const m of allMuted) {
      const t = m.textContent.trim();
      if (t && t.length < 20 && t !== prevText) time = t;
    }

    // Unread: green dot badge
    const dot = el.querySelector('span.badge.badge-pin');
    const unread = !!dot && getComputedStyle(dot).display !== 'none';

    return {
      name: h6?.textContent?.trim() || '',
      time,
      lastMsg: prevText.substring(0, 100),
      unread
    };
  }).filter(i => i.name);
})()
