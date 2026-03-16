import { apiJson } from '$lib/apis';
import type { TokenResponse, User } from '$lib/types';

export async function signUp(email: string, name: string, password: string): Promise<TokenResponse> {
	return apiJson<TokenResponse>('/api/auth/signup', {
		method: 'POST',
		body: JSON.stringify({ email, name, password })
	});
}

export async function signIn(email: string, password: string): Promise<TokenResponse> {
	return apiJson<TokenResponse>('/api/auth/signin', {
		method: 'POST',
		body: JSON.stringify({ email, password })
	});
}

export async function getMe(): Promise<User> {
	return apiJson<User>('/api/auth/me');
}
