/**
 * Admin email list. Only these emails can access /admin pages and admin APIs.
 * Add your own email here.
 */
export const ADMIN_EMAILS: string[] = ["dancetoneeraj@gmail.com"];

export function isAdminEmail(email: string | null | undefined): boolean {
  return ADMIN_EMAILS.includes((email ?? "").trim().toLowerCase());
}
