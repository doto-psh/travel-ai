import { getToken } from '$lib/utils';
import type { ChatCompletionRequest } from '$lib/types';

export async function* streamChatCompletion(
	body: ChatCompletionRequest,
	chatId?: string
): AsyncGenerator<string> {
	const token = getToken();
	const url = chatId
		? `/api/chat/completions?chat_id=${chatId}`
		: '/api/chat/completions';

	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Bearer ${token}` } : {})
		},
		body: JSON.stringify({ ...body, stream: true })
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'Stream error' }));
		throw new Error(error.detail || 'Stream error');
	}

	const reader = response.body!.getReader();
	const decoder = new TextDecoder();
	let buffer = '';

	while (true) {
		const { done, value } = await reader.read();
		if (done) break;

		buffer += decoder.decode(value, { stream: true });
		const lines = buffer.split('\n');
		buffer = lines.pop() || '';

		for (const line of lines) {
			const trimmed = line.trim();
			if (trimmed.startsWith('data: ') && trimmed !== 'data: [DONE]') {
				try {
					const json = JSON.parse(trimmed.slice(6));
					const content = json.choices?.[0]?.delta?.content;
					if (content) yield content;
				} catch {
					// skip malformed JSON
				}
			}
		}
	}
}
