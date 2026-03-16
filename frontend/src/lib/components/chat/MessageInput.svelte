<script lang="ts">
	import { isStreaming } from '$lib/stores';

	let { onsend }: { onsend: (content: string) => void } = $props();
	let inputText = $state('');
	let textareaEl: HTMLTextAreaElement;

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			send();
		}
	}

	function send() {
		const text = inputText.trim();
		if (!text || $isStreaming) return;
		onsend(text);
		inputText = '';
		if (textareaEl) textareaEl.style.height = 'auto';
	}

	function autoResize(e: Event) {
		const el = e.target as HTMLTextAreaElement;
		el.style.height = 'auto';
		el.style.height = Math.min(el.scrollHeight, 200) + 'px';
	}
</script>

<div class="border-t border-border bg-white p-4">
	<div class="mx-auto flex max-w-3xl items-end gap-2">
		<textarea
			bind:this={textareaEl}
			bind:value={inputText}
			onkeydown={handleKeydown}
			oninput={autoResize}
			placeholder="Send a message..."
			rows="1"
			class="flex-1 resize-none rounded-xl border border-border px-4 py-3 text-sm focus:border-primary focus:outline-none"
			disabled={$isStreaming}
		></textarea>
		<button
			onclick={send}
			disabled={$isStreaming || !inputText.trim()}
			class="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-white transition hover:bg-primary-dark disabled:opacity-50"
			aria-label="Send message"
		>
			<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19V5m-7 7l7-7 7 7" />
			</svg>
		</button>
	</div>
</div>
