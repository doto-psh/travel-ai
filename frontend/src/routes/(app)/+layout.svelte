<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { user, chats } from '$lib/stores';
	import { getToken } from '$lib/utils';
	import { getMe } from '$lib/apis/auths';
	import { listChats } from '$lib/apis/chats';
	import Navbar from '$lib/components/layout/Navbar.svelte';
	import Sidebar from '$lib/components/layout/Sidebar.svelte';

	let { children } = $props();
	let ready = $state(false);

	onMount(async () => {
		const token = getToken();
		if (!token) {
			goto('/auth');
			return;
		}
		try {
			const me = await getMe();
			user.set(me);
			const chatList = await listChats();
			chats.set(chatList);
			ready = true;
		} catch {
			goto('/auth');
		}
	});
</script>

{#if ready}
	<div class="flex h-screen flex-col">
		<Navbar />
		<div class="flex flex-1 overflow-hidden">
			<Sidebar />
			<main class="flex flex-1 flex-col overflow-hidden">
				{@render children()}
			</main>
		</div>
	</div>
{:else}
	<div class="flex h-screen items-center justify-center">
		<div class="h-8 w-8 animate-spin rounded-full border-2 border-gray-300 border-t-primary"></div>
	</div>
{/if}
