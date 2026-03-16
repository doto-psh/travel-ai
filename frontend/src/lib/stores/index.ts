import { writable } from 'svelte/store';
import type { User, Chat, Message } from '$lib/types';

export const user = writable<User | null>(null);
export const chats = writable<Chat[]>([]);
export const currentChat = writable<Chat | null>(null);
export const messages = writable<Message[]>([]);
export const selectedModel = writable<string>('gpt-4o');
export const isStreaming = writable<boolean>(false);
export const sidebarOpen = writable<boolean>(true);
