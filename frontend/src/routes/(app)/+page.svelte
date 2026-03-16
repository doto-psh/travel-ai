<script lang="ts">
	import { messages, selectedModel, isStreaming, chats, currentChat } from '$lib/stores';
	import { createChat } from '$lib/apis/chats';
	import { streamChatCompletion } from '$lib/apis/streaming';
	import { goto } from '$app/navigation';
	import ChatMessages from '$lib/components/chat/ChatMessages.svelte';
	import MessageInput from '$lib/components/chat/MessageInput.svelte';
	import ModelSelector from '$lib/components/chat/ModelSelector.svelte';
	import type { Message } from '$lib/types';
	import { onMount } from 'svelte';

	onMount(() => {
		messages.set([]);
		currentChat.set(null);
	});

	async function handleSend(content: string) {
		// Create a new chat first
		const chat = await createChat();
		chats.update((list) => [chat, ...list]);
		currentChat.set(chat);

		const userMsg: Message = {
			id: crypto.randomUUID(),
			chat_id: chat.id,
			role: 'user',
			content,
			created_at: new Date().toISOString()
		};

		const assistantMsg: Message = {
			id: crypto.randomUUID(),
			chat_id: chat.id,
			role: 'assistant',
			content: '',
			created_at: new Date().toISOString()
		};

		messages.set([userMsg, assistantMsg]);
		isStreaming.set(true);

		try {
			const stream = streamChatCompletion(
				{
					model: $selectedModel,
					messages: [{ role: 'user', content }],
					stream: true
				},
				chat.id
			);

			for await (const chunk of stream) {
				messages.update((msgs) => {
					const last = msgs[msgs.length - 1];
					return [...msgs.slice(0, -1), { ...last, content: last.content + chunk }];
				});
			}
		} catch (err: any) {
			messages.update((msgs) => {
				const last = msgs[msgs.length - 1];
				return [...msgs.slice(0, -1), { ...last, content: `Error: ${err.message}` }];
			});
		} finally {
			isStreaming.set(false);
			// Navigate to the chat page
			goto(`/chat/${chat.id}`);
		}
	}
</script>

<div class="flex flex-1 flex-col">
	<div class="flex items-center justify-between border-b border-border px-4 py-2">
		<span class="text-sm text-gray-500">New Chat</span>
		<ModelSelector />
	</div>
	<ChatMessages />
	<MessageInput onsend={handleSend} />
</div>
