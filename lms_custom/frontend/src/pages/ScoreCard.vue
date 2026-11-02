<template>
	<div class="mx-auto max-w-7xl px-4 py-6 md:px-8 md:py-8">
		<!-- Header -->
		<div class="mb-8">
			<div class="flex items-center gap-3">
				<div
					class="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-gray-2"
				>
					<span class="text-lg">★</span>
				</div>

				<div>
					<h1 class="text-2xl font-semibold text-ink-gray-9">
						{{ __('Score Card') }}
					</h1>
					<p class="mt-1 text-sm text-ink-gray-6">
						{{
							__(
								'View appraisal scores, KRA progress and training scores.'
							)
						}}
					</p>
				</div>
			</div>
		</div>

		<!-- Admin employee selector -->
		<div
			v-if="isAdmin"
			class="mb-6 rounded-xl border border-outline-gray-2 bg-surface-white p-5"
		>
			<label
				for="score-card-user"
				class="mb-2 block text-sm font-medium text-ink-gray-8"
			>
				{{ __('Select Employee') }}
			</label>

			<select
				id="score-card-user"
				v-model="selectedUser"
				class="h-10 w-full rounded-lg border border-outline-gray-3 bg-surface-white px-3 text-sm md:max-w-md"
				:disabled="usersLoading || users.length === 0"
			>
				<option value="" disabled>
					{{ __('Select an employee') }}
				</option>

				<option
					v-for="user in users"
					:key="user.name"
					:value="user.name"
				>
					{{ user.full_name || user.name }} ({{ user.name }})
				</option>
			</select>

			<p v-if="usersLoading" class="mt-2 text-sm text-ink-gray-6">
				{{ __('Loading employees...') }}
			</p>

			<p v-else-if="usersError" class="mt-2 text-sm text-red-600">
				{{ usersError }}
			</p>

			<p
				v-else-if="!users.length"
				class="mt-2 text-sm text-ink-gray-6"
			>
				{{ __('No employees found.') }}
			</p>
		</div>

		<!-- Score Card tile -->
		<div class="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
			<div
				class="group flex flex-col overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-white transition-all duration-200 hover:-translate-y-0.5 hover:border-outline-gray-4 hover:shadow-lg"
			>
				<div
					class="relative flex h-44 items-center justify-center overflow-hidden bg-surface-gray-2"
				>
					<div
						class="flex h-16 w-16 items-center justify-center rounded-xl bg-surface-white text-3xl text-ink-gray-6 shadow-sm"
					>
						★
					</div>

					<div
						class="absolute right-3 top-3 rounded-full bg-surface-white/95 px-3 py-1.5 text-xs font-semibold text-ink-gray-8 shadow-sm"
					>
						{{ __('Performance') }}
					</div>
				</div>

				<div class="flex flex-1 flex-col p-5">
					<h2 class="text-base font-semibold leading-snug text-ink-gray-9">
						{{ __('Employee Score Card') }}
					</h2>

					<p class="mt-2 text-sm leading-5 text-ink-gray-6">
						{{
							__(
								'View appraisal score, KRA wise goal completion, courses and quiz scores.'
							)
						}}
					</p>

					<div class="mt-4 flex flex-wrap gap-1.5">
						<span
							v-for="item in highlights"
							:key="item"
							class="rounded-md bg-surface-gray-2 px-2.5 py-1 text-xs font-medium text-ink-gray-7"
						>
							{{ __(item) }}
						</span>
					</div>

					<button
						type="button"
						:disabled="!targetUser"
						class="mt-5 inline-flex h-9 w-full items-center justify-center rounded-lg bg-ink-gray-9 text-sm font-medium text-ink-white transition hover:bg-ink-gray-7 disabled:cursor-not-allowed disabled:opacity-50"
						@click="openScoreCard"
					>
						{{ __('Score Card') }}
						<span class="ml-1">→</span>
					</button>

					<button
						type="button"
						:disabled="!targetUser"
						class="mt-2 inline-flex h-9 w-full items-center justify-center rounded-lg border border-outline-gray-3 text-sm font-medium text-ink-gray-8 transition hover:bg-surface-gray-2 disabled:cursor-not-allowed disabled:opacity-50"
						@click="toggleEmbedded"
					>
						{{ showEmbedded ? __('Hide here') : __('View here') }}
					</button>
				</div>
			</div>
		</div>

		<!-- Embedded Score Card -->
		<div v-if="showEmbedded && targetUser" class="mt-8">
			<div class="mb-3 flex items-center justify-between gap-3">
				<div>
					<h3 class="text-sm font-semibold text-ink-gray-8">
						{{ __('Score Card') }}
					</h3>
					<p class="mt-1 text-xs text-ink-gray-6">
						{{ selectedUserLabel }}
					</p>
				</div>

				<div class="flex items-center gap-4 text-xs font-medium">
					<a
						:href="scoreCardUrl"
						target="_blank"
						rel="noopener noreferrer"
						class="text-ink-gray-6 underline underline-offset-2 hover:text-ink-gray-9"
					>
						{{ __('Open in new tab') }}
					</a>

					<button
						type="button"
						class="text-ink-gray-6 underline underline-offset-2 hover:text-ink-gray-9"
						@click="showEmbedded = false"
					>
						{{ __('Close') }}
					</button>
				</div>
			</div>

			<div
				class="relative overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-white"
			>
				<div
					v-if="iframeLoading"
					class="absolute inset-0 z-10 animate-pulse bg-surface-gray-2"
				></div>

				<iframe
					:key="scoreCardUrl"
					:src="scoreCardUrl"
					:title="__('Score Card')"
					class="h-[80vh] w-full"
					@load="iframeLoading = false"
				></iframe>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { call } from 'frappe-ui'

const SCORE_CARD_URL = '/assets/lms_custom/html/Score_card.html'

const highlights = [
	'Appraisal Score',
	'KRA Progress',
	'Courses & Quizzes',
]

const isAdmin = ref(false)
const currentUser = ref('')
const users = ref([])
const selectedUser = ref('')
const usersLoading = ref(false)
const usersError = ref('')

const showEmbedded = ref(false)
const iframeLoading = ref(true)

const targetUser = computed(() => {
	return isAdmin.value ? selectedUser.value : currentUser.value
})

const selectedUserLabel = computed(() => {
	const user = users.value.find(
		(item) => item.name === targetUser.value
	)

	return user
		? `${user.full_name || user.name} (${user.name})`
		: targetUser.value
})

const scoreCardUrl = computed(() => {
	if (!targetUser.value) return ''

	const separator = SCORE_CARD_URL.includes('?') ? '&' : '?'

	return (
		`${SCORE_CARD_URL}${separator}user_id=` +
		encodeURIComponent(targetUser.value)
	)
})

async function initializeScoreCard() {
	try {
		const response = await call('frappe.auth.get_logged_user')
		currentUser.value =
			typeof response === 'string' ? response : ''

		if (!currentUser.value || currentUser.value === 'Guest') {
			return
		}

		// The backend must authorize this request.
		// Do not rely on a client-side role check for data security.
		try {
			const roles = await call(
				'frappe.core.doctype.user.user.get_roles',
				{ user: currentUser.value }
			)

			isAdmin.value =
				Array.isArray(roles) &&
				(
					roles.includes('System Manager') ||
					roles.includes('Administrator')
				)
		} catch (error) {
			console.error('Could not check admin role:', error)
		}

		if (isAdmin.value) {
			await loadUsers()
		}
	} catch (error) {
		console.error('Could not initialize Score Card:', error)
	}
}

async function loadUsers() {
	usersLoading.value = true
	usersError.value = ''

	try {
		const response = await call(
			'lms_custom.lms_gke_custom.api.score_card.get_score_card_users'
		)

		users.value = Array.isArray(response)
			? response
			: response?.users || []

		// Do not automatically load an employee's private data.
		selectedUser.value = ''
	} catch (error) {
		console.error('Could not load Score Card users:', error)
		usersError.value = __(
			'Unable to load employees. Please check API permissions.'
		)
	} finally {
		usersLoading.value = false
	}
}

function openScoreCard() {
	if (!targetUser.value) return

	window.open(scoreCardUrl.value, '_blank', 'noopener,noreferrer')
}

function toggleEmbedded() {
	if (!targetUser.value) return

	showEmbedded.value = !showEmbedded.value

	if (showEmbedded.value) {
		iframeLoading.value = true
	}
}

// Changing the selected employee reloads the embedded Score Card.
watch(selectedUser, (newUser, oldUser) => {
	if (newUser !== oldUser && showEmbedded.value) {
		iframeLoading.value = true
	}
})

initializeScoreCard()
</script>
