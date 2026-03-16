<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { messages, selectedModel, isStreaming, currentChat, chats } from '$lib/stores';
	import { getChat } from '$lib/apis/chats';
	import { streamChatCompletion } from '$lib/apis/streaming';
	import ChatMessages from '$lib/components/chat/ChatMessages.svelte';
	import MessageInput from '$lib/components/chat/MessageInput.svelte';
	import ModelSelector from '$lib/components/chat/ModelSelector.svelte';
	import type { Message } from '$lib/types';

	let chatId = $derived($page.params.id);

	onMount(() => {
		loadChat();
	});

	// Reload when chatId changes
	$effect(() => {
		chatId;
		loadChat();
	});

	async function loadChat() {
		if (!chatId) return;
		try {
			const chat = await getChat(chatId);
			currentChat.set(chat);
			messages.set(chat.messages);
		} catch {
			messages.set([]);
		}
	}

	async function handleSend(content: string) {
		const currentMessages = $messages;

		const userMsg: Message = {
			id: crypto.randomUUID(),
			chat_id: chatId,
			role: 'user',
			content,
			created_at: new Date().toISOString()
		};

		const assistantMsg: Message = {
			id: crypto.randomUUID(),
			chat_id: chatId,
			role: 'assistant',
			content: '',
			created_at: new Date().toISOString()
		};

		messages.set([...currentMessages, userMsg, assistantMsg]);
		isStreaming.set(true);

		try {
			const allMessages = [...currentMessages, userMsg].map((m) => ({
				role: m.role,
				content: m.content
			}));

			const stream = streamChatCompletion(
				{
					model: $selectedModel,
					messages: allMessages,
					stream: true
				},
				chatId
			);

			for await (const chunk of stream) {
				messages.update((msgs) => {
					const last = msgs[msgs.length - 1];
					return [...msgs.slice(0, -1), { ...last, content: last.content + chunk }];
				});
			}

			// Refresh chat list to get updated title
			const { listChats } = await import('$lib/apis/chats');
			const updatedChats = await listChats();
			chats.set(updatedChats);
		} catch (err: any) {
			messages.update((msgs) => {
				const last = msgs[msgs.length - 1];
				return [...msgs.slice(0, -1), { ...last, content: `Error: ${err.message}` }];
			});
		} finally {
			isStreaming.set(false);
		}
	}
</script>

<div class="flex flex-1 flex-col">
	<div class="flex items-center justify-between border-b border-border px-4 py-2">
		<span class="text-sm text-gray-500">{$currentChat?.title || 'Chat'}</span>
		<ModelSelector />
	</div>
	<ChatMessages />
	<MessageInput onsend={handleSend} />
</div>
