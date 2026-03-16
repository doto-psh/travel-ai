<script lang="ts">
	import type { Message } from '$lib/types';
	import { renderMarkdown } from '$lib/utils';

	let { message, streaming = false }: { message: Message; streaming?: boolean } = $props();

	const isUser = $derived(message.role === 'user');
</script>

<div class="flex {isUser ? 'justify-end' : 'justify-start'} mb-4">
	<div
		class="max-w-[80%] rounded-2xl px-4 py-3 {isUser
			? 'bg-primary text-white'
			: 'bg-gray-100 text-gray-800'}"
	>
		{#if isUser}
			<p class="whitespace-pre-wrap">{message.content}</p>
		{:else}
			<div class="prose prose-sm max-w-none">
				{@html renderMarkdown(message.content)}
				{#if streaming}
					<span class="inline-block h-4 w-1.5 animate-pulse bg-gray-400"></span>
				{/if}
			</div>
		{/if}
	</div>
</div>
