import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';

// Mock API
import * as api from '@/lib/api';

describe('Authentication Integration Tests', () => {
    beforeEach(() => {
        // Clear localStorage before each test
        localStorage.clear();
        vi.clearAllMocks();
    });

    describe('Login Flow', () => {
        it('should login successfully with valid credentials', async () => {
            const mockToken = 'test-jwt-token';
            vi.spyOn(api.authApi, 'login').mockResolvedValue({
                access_token: mockToken,
                token_type: 'bearer'
            });

            // Simulate login
            const result = await api.authApi.login('test@example.com', 'password123');

            expect(result.access_token).toBe(mockToken);
            expect(localStorage.getItem('auth_token')).toBe(mockToken);
        });

        it('should handle login failure', async () => {
            vi.spyOn(api.authApi, 'login').mockRejectedValue(
                new Error('Invalid credentials')
            );

            await expect(
                api.authApi.login('wrong@example.com', 'wrong')
            ).rejects.toThrow('Invalid credentials');
        });
    });

    describe('Signup Flow', () => {
        it('should signup successfully', async () => {
            const mockToken = 'new-jwt-token';
            vi.spyOn(api.authApi, 'signup').mockResolvedValue({
                access_token: mockToken,
                token_type: 'bearer'
            });

            const result = await api.authApi.signup(
                'new@example.com',
                'password123',
                'New User'
            );

            expect(result.access_token).toBe(mockToken);
            expect(localStorage.getItem('auth_token')).toBe(mockToken);
        });
    });

    describe('Guest Access', () => {
        it('should create session_id for guest users', () => {
            const { getSessionId } = require('@/lib/auth');

            // Clear any existing session
            localStorage.removeItem('chainquery_session_id');

            // Get session ID (should create new one)
            const sessionId = getSessionId();

            expect(sessionId).toBeTruthy();
            expect(localStorage.getItem('chainquery_session_id')).toBe(sessionId);
        });

        it('should persist session_id across calls', () => {
            const { getSessionId } = require('@/lib/auth');

            const sessionId1 = getSessionId();
            const sessionId2 = getSessionId();

            expect(sessionId1).toBe(sessionId2);
        });
    });
});

describe('Query Generation Integration Tests', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should generate SQL for guest user', async () => {
        const mockResponse = {
            id: 'test-id',
            user_input: 'Show me top holders',
            sql_output: 'SELECT * FROM solana.holders LIMIT 10',
            created_at: new Date().toISOString(),
            error_message: null,
            chain: 'solana'
        };

        vi.spyOn(api.chainQueryApi, 'generate').mockResolvedValue(mockResponse);

        const result = await api.chainQueryApi.generate(
            'Show me top holders',
            'solana',
            'test-session-id'
        );

        expect(result.sql_output).toBeTruthy();
        expect(result.user_input).toBe('Show me top holders');
    });

    it('should fetch history for session', async () => {
        const mockHistory = [
            {
                id: '1',
                user_input: 'Query 1',
                sql_output: 'SELECT 1',
                created_at: new Date().toISOString(),
                error_message: null,
                chain: 'solana'
            },
            {
                id: '2',
                user_input: 'Query 2',
                sql_output: 'SELECT 2',
                created_at: new Date().toISOString(),
                error_message: null,
                chain: 'solana'
            }
        ];

        vi.spyOn(api.chainQueryApi, 'getHistory').mockResolvedValue(mockHistory);

        const result = await api.chainQueryApi.getHistory('test-session-id');

        expect(result).toHaveLength(2);
        expect(result[0].user_input).toBe('Query 1');
    });
});

describe('Axios Interceptor Tests', () => {
    it('should attach Authorization header when token exists', async () => {
        const mockToken = 'test-token';
        localStorage.setItem('auth_token', mockToken);

        // Import api to trigger interceptor setup
        const { api: apiInstance } = require('@/lib/api');

        // Check if interceptor is set up
        const config = { headers: {} as any };
        const interceptedConfig = apiInstance.interceptors.request.handlers[0].fulfilled(config);

        expect(interceptedConfig.headers.Authorization).toBe(`Bearer ${mockToken}`);
    });

    it('should not attach Authorization header when no token', async () => {
        localStorage.removeItem('auth_token');

        const { api: apiInstance } = require('@/lib/api');

        const config = { headers: {} as any };
        const interceptedConfig = apiInstance.interceptors.request.handlers[0].fulfilled(config);

        expect(interceptedConfig.headers.Authorization).toBeUndefined();
    });
});
