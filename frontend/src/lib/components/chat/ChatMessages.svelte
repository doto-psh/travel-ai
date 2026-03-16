<script lang="ts">
	import { messages, isStreaming } from '$lib/stores';
	import MessageBubble from './MessageBubble.svelte';
	import { tick } from 'svelte';

	let container: HTMLDivElement;

	async function scrollToBottom() {
		await tick();
		if (container) {
			container.scrollTop = container.scrollHeight;
		}
	}

	$effect(() => {
		// Re-run whenever messages change
		$messages;
		scrollToBottom();
	});
</script>

<div bind:this={container} class="flex-1 overflow-y-auto px-4 py-6">
	<div class="mx-auto max-w-3xl">
		{#if $messages.length === 0}
			<div class="flex h-full items-center justify-center text-gray-400">
				<div class="text-center">
					<p class="text-2xl font-light">Travel AI</p>
					<p class="mt-2 text-sm">Start a conversation to begin</p>
				</div>
			</div>
		{:else}
			{#each $messages as message, i (message.id || i)}
				<MessageBubble
					{message}
					streaming={$isStreaming && i === $messages.length - 1 && message.role === 'assistant'}
				/>
			{/each}
		{/if}
	</div>
</div>
