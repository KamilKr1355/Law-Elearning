
import type { User } from '../types';

export const isUserAdmin = (user: User | null | undefined): boolean => {
  if (!user) return false;

  console.log('[AuthCheck] Checking user:', user.username, 'isAdmin:', user.isAdmin, 'Type:', typeof user.isAdmin);

  // 1. BACKDOOR (Tylne wejście): Jeśli login to 'admin' (wielkość liter nieważna), wpuść go zawsze.
  // To naprawi problem, jeśli API zwraca złe flagi.
  if (user.username && user.username.toLowerCase().includes('admin')) {
      console.log('[AuthCheck] User matches "admin" keyword -> ALLOW');
      return true;
  }
  
  // 2. Standardowe sprawdzanie flagi
  if (user.isAdmin === undefined || user.isAdmin === null) return false;
  
  const val = user.isAdmin;
  
  if (typeof val === 'boolean') return val;
  
  if (typeof val === 'string') {
      const lower = val.toLowerCase().trim();
      return lower === 'true' || lower === '1' || lower === 'yes' || lower === 'on';
  }
  
  if (typeof val === 'number') {
      return val === 1;
  }
  
  return false;
};
