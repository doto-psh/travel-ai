<script lang="ts">
	import { user, sidebarOpen } from '$lib/stores';
	import { clearToken } from '$lib/utils';
	import { goto } from '$app/navigation';

	function toggleSidebar() {
		sidebarOpen.update((v) => !v);
	}

	function logout() {
		clearToken();
		user.set(null);
		goto('/auth');
	}
</script>

<nav class="flex h-14 items-center justify-between border-b border-border bg-white px-4">
	<div class="flex items-center gap-3">
		<button onclick={toggleSidebar} class="rounded p-1 hover:bg-gray-100" aria-label="Toggle sidebar">
			<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
			</svg>
		</button>
		<span class="text-lg font-semibold text-gray-800">Travel AI</span>
	</div>
	<div class="flex items-center gap-3">
		{#if $user}
			<span class="text-sm text-gray-600">{$user.name}</span>
			<button onclick={logout} class="rounded px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100">
				Logout
			</button>
		{/if}
	</div>
</nav>
