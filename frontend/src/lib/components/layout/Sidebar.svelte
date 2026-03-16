<script lang="ts">
	import { chats, sidebarOpen } from '$lib/stores';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { createChat, deleteChat } from '$lib/apis/chats';
	import { formatDate } from '$lib/utils';

	async function handleNewChat() {
		const chat = await createChat();
		chats.update((list) => [chat, ...list]);
		goto(`/chat/${chat.id}`);
	}

	async function handleDelete(e: Event, chatId: string) {
		e.stopPropagation();
		await deleteChat(chatId);
		chats.update((list) => list.filter((c) => c.id !== chatId));
		if ($page.params.id === chatId) {
			goto('/');
		}
	}
</script>

{#if $sidebarOpen}
	<aside class="flex h-full w-64 flex-col border-r border-border bg-surface">
		<div class="p-3">
			<button
				onclick={handleNewChat}
				class="flex w-full items-center justify-center gap-2 rounded-lg border border-border px-4 py-2.5 text-sm font-medium hover:bg-gray-100"
			>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
				</svg>
				New Chat
			</button>
		</div>
		<div class="flex-1 overflow-y-auto px-2">
			{#each $chats as chat (chat.id)}
				<!-- svelte-ignore a11y_no_static_element_interactions a11y_click_events_have_key_events -->
				<div
					onclick={() => goto(`/chat/${chat.id}`)}
					class="group mb-0.5 flex w-full cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-left text-sm hover:bg-gray-100 {$page.params.id === chat.id ? 'bg-gray-100' : ''}"
				>
					<span class="truncate">{chat.title}</span>
					<button
						onclick={(e) => handleDelete(e, chat.id)}
						class="hidden rounded p-1 text-gray-400 hover:text-red-500 group-hover:block"
						aria-label="Delete chat"
					>
						<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
						</svg>
					</button>
				</div>
			{/each}
		</div>
	</aside>
{/if}
