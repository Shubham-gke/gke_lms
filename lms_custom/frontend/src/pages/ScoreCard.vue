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
								'Your appraisal score, KRA progress and training scores in one place.'
							)
						}}
					</p>
				</div>
			</div>
		</div>

		<!-- Score Card tile -->
		<div class="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
			<div
				class="group flex flex-col overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-white transition-all duration-200 hover:-translate-y-0.5 hover:border-outline-gray-4 hover:shadow-lg"
			>
				<!-- Visual -->
				<div
					class="relative flex h-44 items-center justify-center overflow-hidden bg-surface-gray-2"
				>
					<div
						class="flex h-16 w-16 items-center justify-center rounded-xl bg-surface-white text-3xl text-ink-gray-6 shadow-sm"
					>
						★
					</div>

					<div
						class="absolute right-3 top-3 rounded-full bg-surface-white/95 px-3 py-1.5 text-xs font-semibold text-ink-gray-8 shadow-sm backdrop-blur"
					>
						{{ __('Performance') }}
					</div>
				</div>

				<!-- Body -->
				<div class="flex flex-1 flex-col p-5">
					<h2 class="text-base font-semibold leading-snug text-ink-gray-9">
						{{ __('Employee Score Card') }}
					</h2>

					<p class="mt-2 text-sm leading-5 text-ink-gray-6">
						{{
							__(
								'See your appraisal score, KRA wise goal completion, courses and quiz scores.'
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

					<!-- Score Card button: opens the page -->
					<button
						type="button"
						class="mt-5 inline-flex h-9 w-full items-center justify-center rounded-lg bg-ink-gray-9 text-sm font-medium text-ink-white transition hover:bg-ink-gray-7"
						@click="openScoreCard"
					>
						{{ __('Score Card') }}
						<span class="ml-1">→</span>
					</button>

					<button
						type="button"
						class="mt-2 inline-flex h-9 w-full items-center justify-center rounded-lg border border-outline-gray-3 text-sm font-medium text-ink-gray-8 transition hover:bg-surface-gray-2"
						@click="toggleEmbedded"
					>
						{{ showEmbedded ? __('Hide here') : __('View here') }}
					</button>
				</div>
			</div>
		</div>

		<!-- Embedded view -->
		<div v-if="showEmbedded" class="mt-8">
			<div class="mb-3 flex items-center justify-between">
				<h3 class="text-sm font-semibold text-ink-gray-8">
					{{ __('Score Card') }}
				</h3>

				<div class="flex items-center gap-4 text-xs font-medium">
					<a
						:href="SCORE_CARD_URL"
						target="_blank"
						rel="noopener"
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
					class="absolute inset-0 animate-pulse bg-surface-gray-2"
				></div>

				<iframe
					:src="SCORE_CARD_URL"
					:title="__('Score Card')"
					class="h-[80vh] w-full"
					@load="iframeLoading = false"
				></iframe>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'

/* =====================================================
   SETTINGS
   Use the full URL (http://host:port/assets/...) if the
   Score Card lives on a different site than this CRM.
===================================================== */

const SCORE_CARD_URL = '/assets/lms_custom/html/Score_card.html'

const highlights = ['Appraisal Score', 'KRA Progress', 'Courses & Quizzes']

const showEmbedded = ref(false)
const iframeLoading = ref(true)

/* =====================================================
   OPEN SCORE CARD (new tab)
===================================================== */

const openScoreCard = () => {
	window.open(SCORE_CARD_URL, '_blank', 'noopener')
}

/* =====================================================
   VIEW INSIDE THIS PAGE
===================================================== */

const toggleEmbedded = () => {
	showEmbedded.value = !showEmbedded.value

	if (showEmbedded.value) {
		iframeLoading.value = true
	}
}
</script>