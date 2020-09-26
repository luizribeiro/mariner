export function renderTime(time_secs: number): string {
  const printHours = Math.floor(time_secs / 3600);
  const printMinutes = Math.floor((time_secs % 3600) / 60)
    .toString()
    .padStart(2, "0");
  return `${printHours}h${printMinutes}`;
}
