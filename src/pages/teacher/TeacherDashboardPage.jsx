import { useNavigate } from 'react-router-dom'

import TeacherLayout from '../../components/layout/TeacherLayout'

import TeacherStatCard from '../../components/teacher/TeacherStatCard'
import ContentCard from '../../components/teacher/ContentCard'
import ProcessingCard from '../../components/teacher/ProcessingCard'
import EngagementChart from '../../components/teacher/EngagementChart'

import {
  teacherProfile,
  teacherStats,
  uploadedContent,
  processingQueue,
  studentEngagement,
  teacherRecentActivity,
} from '../../data/teacherData'

function TeacherDashboardPage() {
  const navigate = useNavigate()

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
              Teacher Dashboard
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-bold text-slate-900">
                {teacherProfile.name}
              </p>

              <p className="text-xs text-slate-500">
                {teacherProfile.department}
              </p>
            </div>

            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-sm font-black text-white shadow-sm">
              AS
            </div>
          </div>
        </div>
      </header>

      {/* =====================================================
          MAIN
      ====================================================== */}
      <main className="px-6 py-8 lg:px-8">
        <div className="mx-auto max-w-7xl">
          {/* =================================================
              WELCOME
          ================================================== */}
          <section>
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
              Welcome back
            </p>

            <div className="mt-2 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
              <div>
                <h2 className="text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
                  {teacherProfile.name.split(' ')[0]}, ready to teach?
                </h2>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
                  Manage your educational content, monitor AI
                  processing and understand how students are engaging
                  with your lessons.
                </p>
              </div>

              <button
                type="button"
                onClick={() =>
                  navigate('/teacher/upload')
                }
                className="inline-flex items-center justify-center gap-2 rounded-2xl bg-orange-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-orange-100 transition hover:bg-orange-600"
              >
                <span className="text-lg">+</span>
                Upload Content
              </button>
            </div>
          </section>

          {/* =================================================
              STATS
          ================================================== */}
          <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <TeacherStatCard
              icon="📚"
              label="Total Content"
              value={teacherStats.totalContent}
              description="Educational resources in your library"
              accent="orange"
            />

            <TeacherStatCard
              icon="✓"
              label="Published"
              value={teacherStats.publishedContent}
              description="Content available to students"
              accent="green"
            />

            <TeacherStatCard
              icon="✦"
              label="AI Processing"
              value={teacherStats.processingContent}
              description="Resources currently being processed"
              accent="purple"
            />

            <TeacherStatCard
              icon="👥"
              label="Students"
              value={teacherStats.totalStudents}
              description="Students learning from your content"
              accent="blue"
            />
          </section>

          {/* =================================================
              PROCESSING + ENGAGEMENT
          ================================================== */}
          <section className="mt-8 grid gap-6 xl:grid-cols-[0.9fr_1.4fr]">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                    AI Pipeline
                  </p>

                  <h2 className="mt-1 text-xl font-black text-slate-900">
                    Processing Queue
                  </h2>

                  <p className="mt-1 text-sm text-slate-500">
                    AI-generated learning content in progress.
                  </p>
                </div>

                <span className="rounded-xl bg-orange-50 px-3 py-2 text-xs font-bold text-orange-600">
                  {processingQueue.length} active
                </span>
              </div>

              <div className="mt-6 space-y-3">
                {processingQueue.map((item) => (
                  <ProcessingCard
                    key={item.id}
                    item={item}
                  />
                ))}
              </div>
            </div>

            <div>
              <EngagementChart data={studentEngagement} />

              <div className="mt-3 flex justify-end">
                <button
                  type="button"
                  onClick={() =>
                    navigate('/teacher/analytics')
                  }
                  className="rounded-xl px-4 py-2 text-xs font-bold text-orange-600 transition hover:bg-orange-50"
                >
                  View Detailed Analytics →
                </button>
              </div>
            </div>
          </section>

          {/* =================================================
              CONTENT LIBRARY
          ================================================== */}
          <section className="mt-10">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                  Your Resources
                </p>

                <h2 className="mt-1 text-2xl font-black text-slate-900">
                  Content Library
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Manage the educational resources you've uploaded.
                </p>
              </div>

              <button
                type="button"
                onClick={() =>
                  navigate('/teacher/content')
                }
                className="text-sm font-bold text-orange-600 transition hover:text-orange-700"
              >
                View All →
              </button>
            </div>

            <div className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {uploadedContent.slice(0, 3).map((content) => (
                <ContentCard
                  key={content.id}
                  content={content}
                />
              ))}
            </div>
          </section>

          {/* =================================================
              QUICK ACTIONS
          ================================================== */}
          <section className="mt-10">
            <div className="rounded-3xl border border-orange-100 bg-gradient-to-r from-orange-50 to-amber-50 p-6">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                    Quick Actions
                  </p>

                  <h2 className="mt-1 text-xl font-black text-slate-900">
                    Continue building your EduVerse classroom.
                  </h2>
                </div>

                <div className="flex flex-col gap-2 sm:flex-row">
                  <button
                    type="button"
                    onClick={() =>
                      navigate('/teacher/upload')
                    }
                    className="rounded-xl bg-orange-500 px-5 py-3 text-xs font-bold text-white transition hover:bg-orange-600"
                  >
                    + Upload Content
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      navigate('/teacher/content')
                    }
                    className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
                  >
                    Manage Content
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      navigate('/teacher/analytics')
                    }
                    className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-xs font-bold text-slate-600 transition hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600"
                  >
                    View Analytics
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* =================================================
              RECENT ACTIVITY
          ================================================== */}
          <section className="mt-10 pb-8">
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
                  Activity
                </p>

                <h2 className="mt-1 text-xl font-black text-slate-900">
                  Recent Activity
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Your latest teacher actions.
                </p>
              </div>

              <div className="mt-5 grid gap-2 md:grid-cols-2">
                {teacherRecentActivity.map((activity) => (
                  <div
                    key={activity.id}
                    className="flex items-center gap-4 rounded-2xl p-4 transition hover:bg-orange-50"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-sm">
                      {activity.icon}
                    </div>

                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-bold text-slate-800">
                        {activity.title}
                      </p>

                      <div className="mt-1 flex items-center gap-2">
                        <span className="text-[11px] text-slate-400">
                          {activity.type}
                        </span>

                        <span className="h-1 w-1 rounded-full bg-slate-300" />

                        <span className="text-[11px] text-slate-400">
                          {activity.time}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </div>
      </main>
    </TeacherLayout>
  )
}

export default TeacherDashboardPage