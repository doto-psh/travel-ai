import { env } from '$env/dynamic/private';
import type { RequestHandler } from './$types';

const DEFAULT_BACKEND_URL = 'http://backend:18000';

const proxy: RequestHandler = async ({ fetch, params, request, url }) => {
	const backendUrl = env.BACKEND_INTERNAL_URL || DEFAULT_BACKEND_URL;
	const targetUrl = new URL(`/api/${params.path ?? ''}`, backendUrl);
	targetUrl.search = url.search;

	const headers = new Headers(request.headers);
	headers.delete('host');
	headers.delete('connection');
	headers.delete('content-length');

	const response = await fetch(targetUrl.toString(), {
		method: request.method,
		headers,
		body:
			request.method === 'GET' || request.method === 'HEAD'
				? undefined
				: await request.arrayBuffer(),
		redirect: 'manual'
	});

	return new Response(response.body, {
		status: response.status,
		statusText: response.statusText,
		headers: response.headers
	});
};

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
export const OPTIONS = proxy;
export const HEAD = proxy;
