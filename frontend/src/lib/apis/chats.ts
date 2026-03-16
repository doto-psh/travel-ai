import { apiJson, apiFetch } from '$lib/apis';
import type { Chat, ChatDetail } from '$lib/types';

export async function listChats(): Promise<Chat[]> {
	return apiJson<Chat[]>('/api/chats/');
}

export async function createChat(title: string = 'New Chat'): Promise<Chat> {
	return apiJson<Chat>('/api/chats/', {
		method: 'POST',
		body: JSON.stringify({ title })
	});
}

export async function getChat(chatId: string): Promise<ChatDetail> {
	return apiJson<ChatDetail>(`/api/chats/${chatId}`);
}

export async function updateChat(chatId: string, title: string): Promise<Chat> {
	return apiJson<Chat>(`/api/chats/${chatId}`, {
		method: 'PUT',
		body: JSON.stringify({ title })
	});
}

export async function deleteChat(chatId: string): Promise<void> {
	await apiFetch(`/api/chats/${chatId}`, { method: 'DELETE' });
}
