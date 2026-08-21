import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import TeacherLayout from '../../components/layout/TeacherLayout'
import ContentCard from '../../components/teacher/ContentCard'
import ContentFilters from '../../components/teacher/ContentFilters'

import {
  uploadedContent,
  contentTypes,
  contentStatuses,
} from '../../data/teacherData'

function TeacherContentPage() {
  const navigate = useNavigate()

  const [search, setSearch] = useState('')
  const [type, setType] = useState('All Content')
  const [status, setStatus] = useState('All Status')

  const filteredContent = useMemo(() => {
    const normalizedSearch = search.toLowerCase().trim()

    return uploadedContent.filter((content) => {
      const matchesSearch =
        !normalizedSearch ||
        content.title.toLowerCase().includes(normalizedSearch) ||
        content.subject.toLowerCase().includes(normalizedSearch)

      const matchesType =
        type === 'All Content' ||
        content.type === type

      const matchesStatus =
        status === 'All Status' ||
        content.status === status

      return (
        matchesSearch &&
        matchesType &&
        matchesStatus
      )
    })
  }, [search, type, status])

  const clearFilters = () => {
    setSearch('')
    setType('All Content')
    setStatus('All Status')
  }

  const hasFilters =
    search ||
    type !== 'All Content' ||
    status !== 'All Status'

  return (
    <TeacherLayout>
      {/* =====================================================
          HEADER
      ====================================================== */}
      <header className="border-b border-orange-100 bg-white">
        <div className="flex items-center justify-between px-6 py-5 lg:px-8">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
              EduVerse
            </p>

            <h1 className="mt-1 text-xl font-black text-slate-900">
              Content Library
            </h1>
          </div>

          <button
            type="button"
            onClick={() =>
              navigate('/teacher/upload')
            }
            className="rounded-xl bg-orange-500 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-orange-600"
          >
            + Upload Content
          </button>
        </div>
      </header>

      {/* =====================================================
          MAIN
      ====================================================== */}
      <main className="px-6 py-8 lg:px-8">
        <div className="mx-auto max-w-7xl">
          {/* =================================================
              INTRO
          ================================================== */}
          <section>
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
              Manage Resources
            </p>

            <div className="mt-2 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h2 className="text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
                  Your Content Library
                </h2>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
                  Manage your educational resources, monitor their
                  processing status and see how students are using them.
                </p>
              </div>

              <div className="rounded-2xl border border-orange-100 bg-orange-50 px-5 py-4">
                <p className="text-xs font-bold uppercase tracking-wider text-orange-500">
                  Total Resources
                </p>

                <p className="mt-1 text-2xl font-black text-slate-900">
                  {uploadedContent.length}
                </p>
              </div>
            </div>
          </section>

          {/* =================================================
              FILTERS
          ================================================== */}
          <section className="mt-8">
            <ContentFilters
              search={search}
              type={type}
              status={status}
              contentTypes={contentTypes}
              contentStatuses={contentStatuses}
              onSearchChange={setSearch}
              onTypeChange={setType}
              onStatusChange={setStatus}
              onClear={clearFilters}
            />
          </section>

          {/* =================================================
              RESULTS HEADER
          ================================================== */}
          <section className="mt-8">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                  Resources
                </p>

                <h2 className="mt-1 text-2xl font-black text-slate-900">
                  {hasFilters
                    ? 'Filtered Results'
                    : 'All Content'}
                </h2>
              </div>

              <span className="rounded-xl bg-white px-3 py-2 text-xs font-bold text-slate-500 shadow-sm ring-1 ring-slate-100">
                {filteredContent.length}{' '}
                {filteredContent.length === 1
                  ? 'resource'
                  : 'resources'}
              </span>
            </div>
          </section>

          {/* =================================================
              CONTENT GRID
          ================================================== */}
          {filteredContent.length > 0 ? (
            <section className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {filteredContent.map((content) => (
                <ContentCard
                  key={content.id}
                  content={content}
                />
              ))}
            </section>
          ) : (
            <EmptyState onClear={clearFilters} />
          )}

          {/* =================================================
              INFO BANNER
          ================================================== */}
          {!hasFilters && (
            <section className="mt-10 pb-8">
              <div className="overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 to-slate-800 p-6 text-white shadow-xl sm:p-8">
                <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-400">
                      EduVerse AI
                    </p>

                    <h3 className="mt-2 text-xl font-black">
                      Transform your next lesson.
                    </h3>

                    <p className="mt-1 max-w-xl text-sm leading-6 text-slate-400">
                      Upload new educational material and let EduVerse
                      create accessible, multilingual and engaging
                      learning experiences.
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() =>
                      navigate('/teacher/upload')
                    }
                    className="shrink-0 rounded-xl bg-orange-500 px-5 py-3 text-sm font-bold text-white transition hover:bg-orange-600"
                  >
                    Upload New Content →
                  </button>
                </div>
              </div>
            </section>
          )}
        </div>
      </main>
    </TeacherLayout>
  )
}

function EmptyState({ onClear }) {
  return (
    <div className="mt-5 rounded-3xl border border-slate-200 bg-white px-6 py-16 text-center shadow-sm">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-orange-50 text-2xl">
        🔎
      </div>

      <h3 className="mt-5 text-lg font-black text-slate-900">
        No content found
      </h3>

      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
        Try changing your search or filters to find the content
        you're looking for.
      </p>

      <button
        type="button"
        onClick={onClear}
        className="mt-5 rounded-xl bg-orange-500 px-5 py-2.5 text-xs font-bold text-white transition hover:bg-orange-600"
      >
        Clear Filters
      </button>
    </div>
  )
}

export default TeacherContentPage