<script lang="ts">
	import type { Snippet } from 'svelte';
	let { show = false, title = '', onclose, children }: { show: boolean; title?: string; onclose: () => void; children: Snippet } = $props();
</script>

{#if show}
	<!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onclick={onclose}>
		<!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
		<div class="mx-4 w-full max-w-md rounded-lg bg-white p-6 shadow-xl" onclick={(e) => e.stopPropagation()}>
			{#if title}
				<h2 class="mb-4 text-lg font-semibold">{title}</h2>
			{/if}
			{@render children()}
		</div>
	</div>
{/if}
