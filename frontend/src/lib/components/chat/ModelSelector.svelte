<script lang="ts">
	import { selectedModel } from '$lib/stores';

	const models = [
		{ id: 'gpt-4o', name: 'GPT-4o' },
		{ id: 'gpt-4o-mini', name: 'GPT-4o Mini' },
		{ id: 'gpt-4-turbo', name: 'GPT-4 Turbo' },
		{ id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo' }
	];
</script>

<select
	bind:value={$selectedModel}
	class="rounded-lg border border-border bg-white px-3 py-1.5 text-sm focus:border-primary focus:outline-none"
>
	{#each models as model}
		<option value={model.id}>{model.name}</option>
	{/each}
</select>
