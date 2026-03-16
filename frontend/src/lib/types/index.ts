export interface User {
	id: string;
	email: string;
	name: string;
	role: string;
}

export interface Chat {
	id: string;
	title: string;
	created_at: string;
	updated_at: string;
}

export interface ChatDetail extends Chat {
	messages: Message[];
}

export interface Message {
	id: string;
	chat_id: string;
	role: 'user' | 'assistant' | 'system';
	content: string;
	model?: string;
	token_count?: number;
	created_at: string;
}

export interface TokenResponse {
	access_token: string;
	refresh_token: string;
	token_type: string;
}

export interface ChatCompletionRequest {
	model: string;
	messages: { role: string; content: string }[];
	stream: boolean;
}
