import { NavigateFunction } from 'react-router-dom';

const SESSION_KEY = 'chainquery_session_id';
const USER_MODE_KEY = 'user_mode';

/**
 * Generates a UUID using crypto.randomUUID or a fallback
 */
function generateUUID(): string {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
        return crypto.randomUUID();
    }
    // Fallback for older browsers
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

/**
 * Handles guest access by creating a session and redirecting to dashboard
 */
export function handleGuestAccess(navigate: NavigateFunction): void {
    // Check if session already exists
    let sessionId = localStorage.getItem(SESSION_KEY);

    if (!sessionId) {
        // Generate a new session ID
        sessionId = generateUUID();
        localStorage.setItem(SESSION_KEY, sessionId);
    }

    // Set user mode to guest
    localStorage.setItem(USER_MODE_KEY, 'guest');

    // Redirect to dashboard
    navigate('/dashboard');
}

/**
 * Check if current user is a guest
 */
export function isGuestUser(): boolean {
    return localStorage.getItem(USER_MODE_KEY) === 'guest';
}

/**
 * Get the current session ID
 */
export function getSessionId(): string | null {
    return localStorage.getItem(SESSION_KEY);
}

/**
 * Clear guest session
 */
export function clearGuestSession(): void {
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem(USER_MODE_KEY);
}
