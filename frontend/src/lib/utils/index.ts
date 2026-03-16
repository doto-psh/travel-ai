import { marked } from 'marked';
import hljs from 'highlight.js';

marked.setOptions({
	highlight(code: string, lang: string) {
		if (lang && hljs.getLanguage(lang)) {
			return hljs.highlight(code, { language: lang }).value;
		}
		return hljs.highlightAuto(code).value;
	},
	breaks: true
});

export function renderMarkdown(content: string): string {
	return marked.parse(content) as string;
}

export function formatDate(dateStr: string): string {
	const date = new Date(dateStr);
	const now = new Date();
	const diff = now.getTime() - date.getTime();
	const days = Math.floor(diff / (1000 * 60 * 60 * 24));

	if (days === 0) return 'Today';
	if (days === 1) return 'Yesterday';
	if (days < 7) return `${days}d ago`;
	return date.toLocaleDateString();
}

export function getToken(): string | null {
	if (typeof window === 'undefined') return null;
	return sessionStorage.getItem('token');
}

export function setToken(access: string, refresh: string): void {
	sessionStorage.setItem('token', access);
	sessionStorage.setItem('refresh_token', refresh);
}

export function clearToken(): void {
	sessionStorage.removeItem('token');
	sessionStorage.removeItem('refresh_token');
}
