<script lang="ts">
	import { goto } from '$app/navigation';
	import { signIn, signUp, getMe } from '$lib/apis/auths';
	import { user } from '$lib/stores';
	import { setToken } from '$lib/utils';

	let isSignUp = $state(false);
	let email = $state('');
	let name = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;

		try {
			const tokens = isSignUp
				? await signUp(email, name, password)
				: await signIn(email, password);

			setToken(tokens.access_token, tokens.refresh_token);
			const me = await getMe();
			user.set(me);
			goto('/');
		} catch (err: any) {
			error = err.message || 'An error occurred';
		} finally {
			loading = false;
		}
	}
</script>

<div class="flex min-h-screen items-center justify-center bg-surface">
	<div class="w-full max-w-sm rounded-xl bg-white p-8 shadow-lg">
		<h1 class="mb-6 text-center text-2xl font-bold text-gray-800">
			{isSignUp ? 'Create Account' : 'Sign In'}
		</h1>

		{#if error}
			<div class="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>
		{/if}

		<form onsubmit={handleSubmit} class="space-y-4">
			{#if isSignUp}
				<div>
					<label for="name" class="mb-1 block text-sm font-medium text-gray-700">Name</label>
					<input
						id="name"
						type="text"
						bind:value={name}
						required
						class="w-full rounded-lg border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
					/>
				</div>
			{/if}
			<div>
				<label for="email" class="mb-1 block text-sm font-medium text-gray-700">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					required
					class="w-full rounded-lg border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
				/>
			</div>
			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-gray-700">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					minlength="6"
					class="w-full rounded-lg border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
				/>
			</div>
			<button
				type="submit"
				disabled={loading}
				class="w-full rounded-lg bg-primary py-2.5 text-sm font-medium text-white transition hover:bg-primary-dark disabled:opacity-50"
			>
				{loading ? 'Loading...' : isSignUp ? 'Sign Up' : 'Sign In'}
			</button>
		</form>

		<p class="mt-4 text-center text-sm text-gray-600">
			{isSignUp ? 'Already have an account?' : "Don't have an account?"}
			<button onclick={() => (isSignUp = !isSignUp)} class="font-medium text-primary hover:underline">
				{isSignUp ? 'Sign In' : 'Sign Up'}
			</button>
		</p>
	</div>
</div>
