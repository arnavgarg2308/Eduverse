import { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'

import TeacherLayout from '../../components/layout/TeacherLayout'
import EngagementChart from '../../components/teacher/EngagementChart'

import {
  teacherProfile,
  teacherStats,
  uploadedContent,
  studentEngagement,
} from '../../data/teacherData'

function TeacherAnalyticsPage() {
  const navigate = useNavigate()

  const totalEngagement = useMemo(
    () =>
      studentEngagement.reduce(
        (total, item) => total + item.students,
        0,
      ),
    [],
  )

  const averageEngagement =
    studentEngagement.length > 0
      ? Math.round(
          totalEngagement / studentEngagement.length,
        )
      : 0

  const publishedContent = uploadedContent.filter(
    (content) => content.status === 'Published',
  )

  const totalContentStudents = uploadedContent.reduce(
    (total, content) => total + content.students,
    0,
  )

  const mostUsedContent =
    [...uploadedContent].sort(
      (a, b) => b.students - a.students,
    )[0] || null

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
              Teacher Analytics
            </h1>
          </div>

          <button
            type="button"
            onClick={() =>
              navigate('/teacher/dashboard')
            }
            className="rounded-xl border border-slate-200 px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
          >
            ← Dashboard
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
              Learning Insights
            </p>

            <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
              Understand your students.
            </h2>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
              Track engagement, content usage and learning activity
              across your EduVerse resources.
            </p>
          </section>

          {/* =================================================
              TOP STATS
          ================================================== */}
          <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <AnalyticsStat
              icon="👥"
              label="Total Students"
              value={teacherStats.totalStudents}
              description="Students connected to your content"
              accent="blue"
            />

            <AnalyticsStat
              icon="📈"
              label="Average Engagement"
              value={`${teacherStats.averageEngagement}%`}
              description="Overall learning engagement"
              accent="orange"
            />

            <AnalyticsStat
              icon="📚"
              label="Published Content"
              value={publishedContent.length}
              description="Resources available to students"
              accent="green"
            />

            <AnalyticsStat
              icon="▶"
              label="Avg. Daily Activity"
              value={averageEngagement}
              description="Active student sessions"
              accent="purple"
            />
          </section>

          {/* =================================================
              ENGAGEMENT CHART
          ================================================== */}
          <section className="mt-8">
            <EngagementChart data={studentEngagement} />
          </section>

          {/* =================================================
              CONTENT PERFORMANCE
          ================================================== */}
          <section className="mt-8">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                  Content Performance
                </p>

                <h2 className="mt-1 text-xl font-black text-slate-900">
                  Resource Usage
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  See which learning resources are getting the most
                  student attention.
                </p>
              </div>

              <div className="mt-6 space-y-4">
                {uploadedContent.map((content) => {
                  const percentage =
                    totalContentStudents > 0
                      ? Math.round(
                          (content.students /
                            totalContentStudents) *
                            100,
                        )
                      : 0

                  return (
                    <div
                      key={content.id}
                      className="rounded-2xl border border-slate-100 bg-slate-50 p-4"
                    >
                      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                        <div className="min-w-0">
                          <h3 className="truncate text-sm font-bold text-slate-900">
                            {content.title}
                          </h3>

                          <p className="mt-1 text-xs text-slate-500">
                            {content.subject} • {content.type}
                          </p>
                        </div>

                        <div className="flex items-center gap-4">
                          <div className="text-right">
                            <p className="text-sm font-black text-slate-900">
                              {content.students}
                            </p>

                            <p className="text-[10px] text-slate-400">
                              students
                            </p>
                          </div>

                          <span className="rounded-lg bg-white px-2.5 py-1.5 text-[10px] font-bold text-orange-600 shadow-sm">
                            {content.status}
                          </span>
                        </div>
                      </div>

                      <div className="mt-4 h-2 overflow-hidden rounded-full bg-white">
                        <div
                          className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-400"
                          style={{
                            width: `${Math.max(
                              percentage,
                              5,
                            )}%`,
                          }}
                        />
                      </div>

                      <div className="mt-2 flex justify-between">
                        <span className="text-[10px] text-slate-400">
                          Student usage
                        </span>

                        <span className="text-[10px] font-bold text-orange-600">
                          {percentage}%
                        </span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </section>

          {/* =================================================
              HIGHLIGHTS
          ================================================== */}
          <section className="mt-8 grid gap-6 pb-8 lg:grid-cols-2">
            {/* Most Used */}
            <div className="rounded-3xl border border-orange-100 bg-gradient-to-br from-orange-500 to-amber-500 p-6 text-white shadow-lg shadow-orange-100">
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-100">
                Top Resource
              </p>

              <h2 className="mt-2 text-xl font-black">
                Most Used Content
              </h2>

              {mostUsedContent ? (
                <>
                  <p className="mt-5 text-lg font-bold">
                    {mostUsedContent.title}
                  </p>

                  <p className="mt-1 text-sm text-orange-100">
                    {mostUsedContent.students} students are using
                    this resource.
                  </p>
                </>
              ) : (
                <p className="mt-5 text-sm text-orange-100">
                  No content available yet.
                </p>
              )}
            </div>

            {/* Teacher Overview */}
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                Teacher Overview
              </p>

              <h2 className="mt-2 text-xl font-black text-slate-900">
                {teacherProfile.name}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {teacherProfile.department}
              </p>

              <div className="mt-6 grid grid-cols-2 gap-3">
                <OverviewItem
                  label="Experience"
                  value={teacherProfile.experience}
                />

                <OverviewItem
                  label="Content"
                  value={teacherStats.totalContent}
                />

                <OverviewItem
                  label="Students"
                  value={teacherStats.totalStudents}
                />

                <OverviewItem
                  label="Engagement"
                  value={`${teacherStats.averageEngagement}%`}
                />
              </div>
            </div>
          </section>
        </div>
      </main>
    </TeacherLayout>
  )
}

function AnalyticsStat({
  icon,
  label,
  value,
  description,
  accent,
}) {
  const styles = {
    orange: 'bg-orange-50 text-orange-600',
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-emerald-50 text-emerald-600',
    purple: 'bg-purple-50 text-purple-600',
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:border-orange-200 hover:shadow-md">
      <div className="flex items-start justify-between gap-4">
        <div
          className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl text-lg ${styles[accent]}`}
        >
          {icon}
        </div>

        <p className="text-2xl font-black text-slate-900">
          {value}
        </p>
      </div>

      <h3 className="mt-5 text-sm font-bold text-slate-900">
        {label}
      </h3>

      <p className="mt-1 text-xs leading-5 text-slate-500">
        {description}
      </p>
    </div>
  )
}

function OverviewItem({ label, value }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-4">
      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-black text-slate-800">
        {value}
      </p>
    </div>
  )
}

export default TeacherAnalyticsPage