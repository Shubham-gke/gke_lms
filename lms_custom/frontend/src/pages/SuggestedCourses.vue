<template>
	<div class="mx-auto max-w-7xl px-4 py-6 md:px-8 md:py-8">
		<!-- Header -->
		<div class="mb-8">
			<div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
				<div>
					<div class="flex items-center gap-3">
						<div
							class="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-gray-2"
						>
							<span class="text-lg">✦</span>
						</div>

						<div>
							<div class="flex items-center gap-2">
								<h1 class="text-2xl font-semibold text-ink-gray-9">
									{{ __('Suggested Courses') }}
								</h1>

								<span
									v-if="!loading && courses.length"
									class="rounded-full bg-surface-gray-2 px-2 py-0.5 text-xs font-medium text-ink-gray-7"
								>
									{{ courses.length }}
								</span>
							</div>

							<p class="mt-1 text-sm text-ink-gray-6">
								{{
									__(
										'Courses recommended based on your skills and interests.'
									)
								}}
							</p>
						</div>
					</div>
				</div>

				<!-- Search -->
				<div
					v-if="!loading && courses.length"
					class="relative w-full md:w-72"
				>
					<input
						v-model="search"
						type="text"
						:placeholder="__('Search courses...')"
						class="h-9 w-full rounded-lg border border-outline-gray-2 bg-surface-white pl-9 pr-3 text-sm text-ink-gray-8 placeholder-ink-gray-4 outline-none transition focus:border-outline-gray-4 focus:ring-1 focus:ring-outline-gray-3"
					/>

					<span
						class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-sm text-ink-gray-4"
					>
						⌕
					</span>
				</div>
			</div>
		</div>

		<!-- Skill Filters -->
		<div
			v-if="!loading && allSkills.length > 1"
			class="mb-7 rounded-lg border border-outline-gray-2 bg-surface-white p-4"
		>
			<div class="mb-3 flex items-center justify-between">
				<span class="text-sm font-medium text-ink-gray-8">
					{{ __('Filter by skill') }}
				</span>

				<button
					v-if="selectedSkills.length"
					type="button"
					class="text-xs font-medium text-ink-gray-6 underline underline-offset-2 hover:text-ink-gray-9"
					@click="clearSkillFilters"
				>
					{{ __('Clear all') }}
				</button>
			</div>

			<div class="flex flex-wrap gap-2">
				<button
					v-for="skill in allSkills"
					:key="skill"
					type="button"
					class="rounded-full border px-3 py-1.5 text-xs font-medium transition-all"
					:class="
						selectedSkills.includes(skill)
							? 'border-ink-gray-9 bg-ink-gray-9 text-ink-white'
							: 'border-outline-gray-2 bg-surface-white text-ink-gray-7 hover:border-outline-gray-4 hover:bg-surface-gray-2'
					"
					@click="toggleSkill(skill)"
				>
					{{ skill }}
				</button>
			</div>
		</div>

		<!-- Loading -->
		<div
			v-if="loading"
			class="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3"
		>
			<div
				v-for="n in 6"
				:key="n"
				class="overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-white"
			>
				<div class="h-44 animate-pulse bg-surface-gray-2"></div>

				<div class="space-y-3 p-5">
					<div
						class="h-5 w-3/4 animate-pulse rounded bg-surface-gray-2"
					></div>

					<div
						class="h-3 w-full animate-pulse rounded bg-surface-gray-2"
					></div>

					<div
						class="h-3 w-2/3 animate-pulse rounded bg-surface-gray-2"
					></div>

					<div
						class="h-8 w-full animate-pulse rounded bg-surface-gray-2"
					></div>
				</div>
			</div>
		</div>

		<!-- Error -->
		<div
			v-else-if="error"
			class="rounded-xl border border-outline-gray-2 bg-surface-white p-12 text-center"
		>
			<div
				class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-surface-gray-2 text-xl"
			>
				!
			</div>

			<div class="mt-4 text-base font-semibold text-ink-gray-9">
				{{ __('Could not load suggested courses') }}
			</div>

			<p class="mt-1 text-sm text-ink-gray-6">
				{{ __('Please check your connection and try again.') }}
			</p>

			<button
				type="button"
				class="mt-5 inline-flex h-9 items-center rounded-lg bg-ink-gray-9 px-4 text-sm font-medium text-ink-white transition hover:bg-ink-gray-7"
				@click="loadCourses"
			>
				{{ __('Retry') }}
			</button>
		</div>

		<!-- Empty -->
		<div
			v-else-if="courses.length === 0"
			class="rounded-xl border border-dashed border-outline-gray-3 bg-surface-white p-14 text-center"
		>
			<div
				class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-surface-gray-2 text-2xl"
			>
				✦
			</div>

			<div class="mt-4 text-base font-semibold text-ink-gray-9">
				{{ __('No suggested courses yet') }}
			</div>

			<p class="mx-auto mt-1 max-w-md text-sm leading-6 text-ink-gray-6">
				{{
					__(
						'We could not find courses that match your skills, or you are already enrolled in all of them.'
					)
				}}
			</p>
		</div>

		<!-- Filter Empty -->
		<div
			v-else-if="filteredCourses.length === 0"
			class="rounded-xl border border-dashed border-outline-gray-3 bg-surface-white p-14 text-center"
		>
			<div class="text-base font-semibold text-ink-gray-9">
				{{ __('No courses found') }}
			</div>

			<p class="mt-1 text-sm text-ink-gray-6">
				{{ __('Try changing your search or skill filters.') }}
			</p>

			<button
				type="button"
				class="mt-4 text-sm font-medium text-ink-gray-8 underline underline-offset-2"
				@click="clearFilters"
			>
				{{ __('Clear filters') }}
			</button>
		</div>

		<!-- Course Grid -->
		<div
			v-else
			class="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3"
		>
			<a
				v-for="course in filteredCourses"
				:key="course.name"
				:href="`/lms/courses/${course.name}`"
				class="group flex flex-col overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-white transition-all duration-200 hover:-translate-y-0.5 hover:border-outline-gray-4 hover:shadow-lg"
			>
				<!-- Course Image -->
				<div class="relative h-44 overflow-hidden bg-surface-gray-2">
					<img
						v-if="course.image"
						:src="course.image"
						:alt="course.title || course.name"
						class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
					/>

					<div
						v-else
						class="flex h-full w-full items-center justify-center bg-surface-gray-2"
					>
						<div
							class="flex h-16 w-16 items-center justify-center rounded-xl bg-surface-white text-2xl font-semibold text-ink-gray-5 shadow-sm"
						>
							{{
								(course.title || course.name || '?')
									.charAt(0)
									.toUpperCase()
							}}
						</div>
					</div>

					<!-- Match Badge -->
					<div
						class="absolute right-3 top-3 rounded-full bg-surface-white/95 px-3 py-1.5 text-xs font-semibold text-ink-gray-8 shadow-sm backdrop-blur"
					>
						{{ matchPercent(course) }}% {{ __('match') }}
					</div>
				</div>

				<!-- Card Body -->
				<div class="flex flex-1 flex-col p-5">
					<!-- Title -->
					<h2
						class="text-base font-semibold leading-snug text-ink-gray-9 transition group-hover:text-ink-gray-7"
					>
						{{ course.title || course.name }}
					</h2>

					<!-- Introduction -->
					<p
						v-if="course.short_introduction"
						class="mt-2 line-clamp-2 text-sm leading-5 text-ink-gray-6"
					>
						{{ course.short_introduction }}
					</p>

					<!-- Stats -->
					<div
						v-if="hasStats(course)"
						class="mt-4 flex flex-wrap items-center gap-3 text-xs text-ink-gray-6"
					>
						<span
							v-if="course.lessons != null"
							class="rounded-md bg-surface-gray-2 px-2 py-1"
						>
							{{ course.lessons }} {{ __('lessons') }}
						</span>

						<span
							v-if="course.enrollments != null"
							class="rounded-md bg-surface-gray-2 px-2 py-1"
						>
							{{ course.enrollments }} {{ __('enrolled') }}
						</span>

						<span
							v-if="course.rating != null"
							class="rounded-md bg-surface-gray-2 px-2 py-1"
						>
							★ {{ course.rating }}
						</span>
					</div>

					<!-- Matching Skills -->
					<div
						v-if="course.matched_skills?.length"
						class="mt-5"
					>
						<div
							class="mb-2 text-xs font-medium uppercase tracking-wide text-ink-gray-5"
						>
							{{ __('Matching Skills') }}
						</div>

						<div class="flex flex-wrap gap-1.5">
							<span
								v-for="skill in course.matched_skills"
								:key="skill"
								class="rounded-md bg-surface-gray-2 px-2.5 py-1 text-xs font-medium text-ink-gray-7"
							>
								{{ skill }}
							</span>
						</div>
					</div>

					<!-- Match Progress -->
					<div class="mt-5">
						<div class="mb-1.5 flex items-center justify-between">
							<span class="text-xs font-medium text-ink-gray-6">
								{{ __('Skill match') }}
							</span>

							<span class="text-xs font-semibold text-ink-gray-8">
								{{ matchCount(course) }}
								{{
									matchCount(course) === 1
										? __('skill')
										: __('skills')
								}}
							</span>
						</div>

						<div
							class="h-1.5 overflow-hidden rounded-full bg-surface-gray-3"
						>
							<div
								class="h-full rounded-full bg-ink-gray-8 transition-all duration-500"
								:style="{
									width: matchPercent(course) + '%',
								}"
							></div>
						</div>
					</div>

					<!-- CTA -->
					<div
						class="mt-5 flex h-9 items-center justify-center rounded-lg border border-outline-gray-3 text-sm font-medium text-ink-gray-8 transition-all group-hover:border-ink-gray-8 group-hover:bg-ink-gray-9 group-hover:text-ink-white"
					>
						{{ __('View Course') }}

						<span
							class="ml-1 transition-transform group-hover:translate-x-0.5"
						>
							→
						</span>
					</div>
				</div>
			</a>
		</div>
	</div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { call } from 'frappe-ui'

const API =
	'lms_custom.lms_gke_custom.api.course_assignment.get_similar_courses'

const courses = ref([])
const loading = ref(true)
const error = ref(false)
const search = ref('')
const selectedSkills = ref([])

/* =====================================================
   LOAD COURSES
===================================================== */

const loadCourses = async () => {
	loading.value = true
	error.value = false

	try {
		const response = await call(API)

		console.log('SIMILAR COURSES RESPONSE:', response)

		const data = Array.isArray(response)
			? response
			: response?.message

		courses.value = Array.isArray(data) ? data : []

		console.log('COURSES:', courses.value)
	} catch (err) {
		console.error('FAILED TO LOAD SIMILAR COURSES:', err)

		courses.value = []
		error.value = true
	} finally {
		loading.value = false
	}
}

/* =====================================================
   MATCH COUNT
===================================================== */

const matchCount = (course) =>
	course.match_count || course.matched_skills?.length || 0

/* =====================================================
   MAX MATCH
===================================================== */

const maxMatch = computed(() =>
	Math.max(1, ...courses.value.map(matchCount))
)

/* =====================================================
   MATCH PERCENT
===================================================== */

const matchPercent = (course) =>
	Math.round((matchCount(course) / maxMatch.value) * 100)

/* =====================================================
   COURSE STATS
===================================================== */

const hasStats = (course) =>
	course.lessons != null ||
	course.enrollments != null ||
	course.rating != null

/* =====================================================
   ALL SKILLS
===================================================== */

const allSkills = computed(() => {
	const skills = new Set()

	courses.value.forEach((course) => {
		;(course.matched_skills || []).forEach((skill) => {
			skills.add(skill)
		})
	})

	return [...skills].sort()
})

/* =====================================================
   TOGGLE SKILL
===================================================== */

const toggleSkill = (skill) => {
	selectedSkills.value = selectedSkills.value.includes(skill)
		? selectedSkills.value.filter((s) => s !== skill)
		: [...selectedSkills.value, skill]
}

/* =====================================================
   CLEAR SKILL FILTERS
===================================================== */

const clearSkillFilters = () => {
	selectedSkills.value = []
}

/* =====================================================
   CLEAR ALL FILTERS
===================================================== */

const clearFilters = () => {
	search.value = ''
	selectedSkills.value = []
}

/* =====================================================
   FILTERED COURSES
===================================================== */

const filteredCourses = computed(() => {
	const query = search.value.trim().toLowerCase()

	return courses.value
		.filter((course) => {
			const text =
				`${course.title || ''} ${course.name || ''} ${
					course.short_introduction || ''
				}`.toLowerCase()

			/* Search */
			if (query && !text.includes(query)) {
				return false
			}

			/* Skill filter */
			if (
				selectedSkills.value.length &&
				!selectedSkills.value.every((skill) =>
					(course.matched_skills || []).includes(skill)
				)
			) {
				return false
			}

			return true
		})
		.sort((a, b) => matchCount(b) - matchCount(a))
})

/* =====================================================
   INITIAL LOAD
===================================================== */

onMounted(loadCourses)
</script>