import { getToken } from '$lib/utils';

const API_BASE_URL = '';

export async function apiFetch(url: string, options: RequestInit = {}): Promise<Response> {
	const token = getToken();
	const res = await fetch(`${API_BASE_URL}${url}`, {
		...options,
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...options.headers
		}
	});
	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'API Error' }));
		throw new Error(error.detail || 'API Error');
	}
	return res;
}

export async function apiJson<T>(url: string, options: RequestInit = {}): Promise<T> {
	const res = await apiFetch(url, options);
	return res.json();
}
