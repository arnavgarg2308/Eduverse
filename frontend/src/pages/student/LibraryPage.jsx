import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import DashboardLayout from '../../components/layout/DashboardLayout'
import Card from '../../components/common/Card'
import Badge from '../../components/common/Badge'

import CourseCard from '../../components/library/CourseCard'
import SearchBar from '../../components/library/SearchBar'
import LibraryFilters from '../../components/library/LibraryFilters'

import {
  libraryCategories,
  libraryLanguages,
  libraryContentTypes,
  libraryCourses,
  recommendedCourses,
} from '../../data/libraryData'

function LibraryPage() {
  const navigate = useNavigate()

  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] =
    useState('All')

  const [selectedLanguage, setSelectedLanguage] =
    useState('All Languages')

  const [selectedContentType, setSelectedContentType] =
    useState('All Content')

  const filteredCourses = useMemo(() => {
    const normalizedSearch = search
      .toLowerCase()
      .trim()

    return libraryCourses.filter((course) => {
      const matchesSearch =
        !normalizedSearch ||
        course.title
          .toLowerCase()
          .includes(normalizedSearch) ||
        course.subject
          .toLowerCase()
          .includes(normalizedSearch) ||
        course.description
          .toLowerCase()
          .includes(normalizedSearch)

      const matchesCategory =
        selectedCategory === 'All' ||
        course.category === selectedCategory

      const matchesLanguage =
        selectedLanguage === 'All Languages' ||
        course.language === selectedLanguage

      const matchesContentType =
        selectedContentType === 'All Content' ||
        course.type === selectedContentType

      return (
        matchesSearch &&
        matchesCategory &&
        matchesLanguage &&
        matchesContentType
      )
    })
  }, [
    search,
    selectedCategory,
    selectedLanguage,
    selectedContentType,
  ])

  const hasActiveFilters =
    Boolean(search.trim()) ||
    selectedCategory !== 'All' ||
    selectedLanguage !== 'All Languages' ||
    selectedContentType !== 'All Content'

  const clearFilters = () => {
    setSearch('')
    setSelectedCategory('All')
    setSelectedLanguage('All Languages')
    setSelectedContentType('All Content')
  }

  const openCourse = (course) => {
    navigate(`/student/learning/${course.id}`)
  }

  return (
    <DashboardLayout
      role="student"
      title="My Learning"
    >
      <div className="mx-auto w-full max-w-7xl">
        {/* =================================================
            HEADER
        ================================================== */}
        <section>
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500 sm:text-sm">
                Learning Library
              </p>

              <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
                Learn something new.
              </h1>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
                Explore your courses, AI-generated lessons and
                personalized learning content.
              </p>
            </div>

            <div className="w-fit rounded-2xl border border-orange-100 bg-orange-50 px-5 py-4">
              <p className="text-xs font-bold uppercase tracking-wider text-orange-600">
                Your Library
              </p>

              <p className="mt-1 text-xl font-black text-slate-900">
                {libraryCourses.length}
                <span className="ml-1 text-xs font-medium text-slate-500">
                  courses
                </span>
              </p>
            </div>
          </div>
        </section>

        {/* =================================================
            SEARCH + FILTERS
        ================================================== */}
        <section className="mt-8">
          <Card className="border-orange-100/70 shadow-sm">
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                <div className="min-w-0 flex-1">
                  <SearchBar
                    value={search}
                    onChange={setSearch}
                  />
                </div>

                {hasActiveFilters && (
                  <button
                    type="button"
                    onClick={clearFilters}
                    className="w-fit rounded-xl px-3 py-2 text-sm font-bold text-orange-600 transition hover:bg-orange-50 hover:text-orange-700"
                  >
                    Clear filters
                  </button>
                )}
              </div>

              <div className="border-t border-slate-100 pt-5">
                <LibraryFilters
                  categories={libraryCategories}
                  languages={libraryLanguages}
                  contentTypes={libraryContentTypes}
                  selectedCategory={selectedCategory}
                  selectedLanguage={selectedLanguage}
                  selectedContentType={selectedContentType}
                  onCategoryChange={
                    setSelectedCategory
                  }
                  onLanguageChange={
                    setSelectedLanguage
                  }
                  onContentTypeChange={
                    setSelectedContentType
                  }
                />
              </div>
            </div>
          </Card>
        </section>

        {/* =================================================
            ACTIVE FILTER SUMMARY
        ================================================== */}
        {hasActiveFilters && (
          <section className="mt-5">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Showing
              </span>

              <Badge variant="primary">
                {filteredCourses.length}{' '}
                {filteredCourses.length === 1
                  ? 'course'
                  : 'courses'}
              </Badge>

              {search.trim() && (
                <span className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-600">
                  Search: "{search.trim()}"
                </span>
              )}

              {selectedCategory !== 'All' && (
                <span className="rounded-lg bg-orange-50 px-3 py-1.5 text-xs font-medium text-orange-700">
                  {selectedCategory}
                </span>
              )}

              {selectedLanguage !== 'All Languages' && (
                <span className="rounded-lg bg-orange-50 px-3 py-1.5 text-xs font-medium text-orange-700">
                  {selectedLanguage}
                </span>
              )}

              {selectedContentType !== 'All Content' && (
                <span className="rounded-lg bg-orange-50 px-3 py-1.5 text-xs font-medium text-orange-700">
                  {selectedContentType}
                </span>
              )}
            </div>
          </section>
        )}

        {/* =================================================
            RECOMMENDED
        ================================================== */}
        {!hasActiveFilters && (
          <section className="mt-9">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Personalized
              </p>

              <h2 className="mt-1 text-2xl font-black text-slate-900">
                Recommended For You
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Based on your learning activity.
              </p>
            </div>

            <div className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {recommendedCourses.map((course) => (
                <CourseCard
                  key={course.id}
                  course={course}
                  onClick={() => openCourse(course)}
                />
              ))}
            </div>
          </section>
        )}

        {/* =================================================
            ALL COURSES
        ================================================== */}
        <section className="mt-10">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Explore
              </p>

              <h2 className="mt-1 text-2xl font-black text-slate-900">
                {hasActiveFilters
                  ? 'Search Results'
                  : 'All Your Learning'}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {hasActiveFilters
                  ? 'Here are the resources matching your filters.'
                  : 'Continue learning from your available courses.'}
              </p>
            </div>

            <Badge variant="primary">
              {filteredCourses.length}{' '}
              {filteredCourses.length === 1
                ? 'course'
                : 'courses'}
            </Badge>
          </div>

          {filteredCourses.length > 0 ? (
            <div className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {filteredCourses.map((course) => (
                <CourseCard
                  key={course.id}
                  course={course}
                  onClick={() => openCourse(course)}
                />
              ))}
            </div>
          ) : (
            <EmptyState
              onClear={clearFilters}
              hasSearch={Boolean(search.trim())}
            />
          )}
        </section>

        {/* =================================================
            LEARNING TIP
        ================================================== */}
        {!hasActiveFilters && (
          <section className="mt-10 pb-8">
            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-orange-500 to-amber-500 p-6 text-white shadow-lg shadow-orange-100 sm:p-8">
              <div className="absolute -right-10 -top-20 h-48 w-48 rounded-full bg-white/10" />
              <div className="absolute -bottom-16 left-1/3 h-32 w-32 rounded-full bg-white/5" />

              <div className="relative flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-100">
                    Learning Tip
                  </p>

                  <h3 className="mt-2 text-xl font-black sm:text-2xl">
                    Mix different learning formats.
                  </h3>

                  <p className="mt-1 max-w-xl text-sm leading-6 text-orange-50">
                    Watch a concept, listen to the explanation and
                    then test yourself with a quiz.
                  </p>
                </div>

                <div className="flex shrink-0 items-center gap-2 text-xl sm:text-2xl">
                  <span>🎥</span>
                  <span className="text-orange-200">
                    →
                  </span>
                  <span>🎧</span>
                  <span className="text-orange-200">
                    →
                  </span>
                  <span>📝</span>
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
    </DashboardLayout>
  )
}

function EmptyState({
  onClear,
  hasSearch,
}) {
  return (
    <Card className="mt-5 py-16 text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-orange-50 text-2xl text-orange-500">
        🔎
      </div>

      <h3 className="mt-5 text-lg font-black text-slate-900">
        No courses found
      </h3>

      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
        {hasSearch
          ? 'No courses matched your search. Try a different keyword or adjust your filters.'
          : 'Try changing your filters to find more learning content.'}
      </p>

      <button
        type="button"
        onClick={onClear}
        className="mt-5 rounded-xl bg-orange-500 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-orange-600"
      >
        Clear Filters
      </button>
    </Card>
  )
}

export default LibraryPage