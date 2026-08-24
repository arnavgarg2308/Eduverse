import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import DashboardLayout from '../../components/layout/DashboardLayout'
import Card from '../../components/common/Card'
import Badge from '../../components/common/Badge'

import {
  studentStats,
  continueLearning,
  recommendedLessons,
  weakTopics,
  recentActivity,
} from '../../data/studentData'


import api from '../../api/api'
function DashboardPage() {
  const navigate = useNavigate()

  // Map dashboard lesson IDs to actual library course IDs.
  const [courses, setCourses] = useState([])
  const [coursesLoading, setCoursesLoading] = useState(true)
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/api/courses/')

        console.log('Courses from backend:', response.data)

        setCourses(response.data)
      } catch (error) {
        console.error('Failed to fetch courses:', error)
      } finally {
        setCoursesLoading(false)
      }
    }

    fetchCourses()
  }, [])
  const openContinueLearning = () => {
    navigate(`/student/learning/${continueCourseId}`)
  }

  const openRecommendedLesson = (lesson) => {
    const courseId =
      courseIdMap[lesson.id]

    if (courseId) {
      navigate(`/student/learning/${courseId}`)
    }
  }

  return (
    <DashboardLayout
      role="student"
      title="Student Dashboard"
    >
      {/* =====================================================
          WELCOME
      ====================================================== */}
      <section>
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
              Welcome Back
            </p>

            <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
              Keep learning. Keep growing.
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
              Continue where you left off and explore personalized
              learning recommendations.
            </p>
          </div>

          <div className="rounded-2xl border border-orange-100 bg-orange-50 px-4 py-3">
            <p className="text-xs font-semibold text-orange-600">
              Learning Streak
            </p>

            <p className="mt-0.5 text-2xl font-black text-slate-900">
              {studentStats.learningStreak}
              <span className="ml-1 text-xs font-semibold text-slate-500">
                days
              </span>
            </p>
          </div>
        </div>
      </section>

      {/* =====================================================
          STATS
      ====================================================== */}
      <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Overall Progress"
          value={`${studentStats.overallProgress}%`}
          description="Across your learning"
          icon="◔"
        />

        <StatCard
          label="Lessons Completed"
          value={studentStats.lessonsCompleted}
          description="Keep building momentum"
          icon="✓"
        />

        <StatCard
          label="Quiz Accuracy"
          value={`${studentStats.quizAccuracy}%`}
          description="Your average score"
          icon="★"
        />

        <StatCard
          label="Learning Streak"
          value={studentStats.learningStreak}
          description="Consecutive days"
          icon="🔥"
        />
      </section>

      {/* =====================================================
          CONTINUE LEARNING
      ====================================================== */}
      <section className="mt-8">
        <Card className="overflow-hidden border-orange-100 p-0">
          <div className="grid lg:grid-cols-[1.5fr_1fr]">
            {/* Main Content */}
            <div className="bg-gradient-to-br from-orange-500 via-orange-500 to-amber-500 p-6 text-white sm:p-8">
              <div className="flex items-center gap-2">
                <span className="rounded-lg bg-white/15 px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider">
                  Continue Learning
                </span>

                <span className="text-xs text-orange-100">
                  {continueLearning.type}
                </span>
              </div>

              <h2 className="mt-5 max-w-xl text-2xl font-black sm:text-3xl">
                {continueLearning.title}
              </h2>

              <p className="mt-2 text-sm text-orange-50">
                {continueLearning.subject} ·{' '}
                {continueLearning.level}
              </p>

              <p className="mt-4 max-w-xl text-sm leading-6 text-orange-50">
                Pick up exactly where you stopped and continue your
                learning journey.
              </p>

              <div className="mt-6 flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={openContinueLearning}
                  className="rounded-xl bg-white px-5 py-3 text-sm font-black text-orange-600 shadow-lg transition hover:-translate-y-0.5 hover:bg-orange-50"
                >
                  Continue Learning →
                </button>

                <span className="rounded-xl bg-white/10 px-4 py-3 text-xs font-bold text-white">
                  {continueLearning.progress}% complete
                </span>
              </div>
            </div>

            {/* Progress */}
            <div className="flex items-center bg-white p-6 sm:p-8">
              <div className="w-full">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-wider text-orange-500">
                      Your Progress
                    </p>

                    <p className="mt-2 text-3xl font-black text-slate-900">
                      {continueLearning.progress}%
                    </p>
                  </div>

                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-orange-50 text-2xl text-orange-500">
                    ▶
                  </div>
                </div>

                <div className="mt-6 h-3 overflow-hidden rounded-full bg-slate-100">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-500"
                    style={{
                      width: `${continueLearning.progress}%`,
                    }}
                  />
                </div>

                <div className="mt-3 flex items-center justify-between text-xs">
                  <span className="font-medium text-slate-400">
                    {continueLearning.duration}
                  </span>

                  <span className="font-bold text-orange-600">
                    {100 - continueLearning.progress}% remaining
                  </span>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </section>

      {/* =====================================================
          RECOMMENDED LESSONS
      ====================================================== */}
      <section className="mt-10">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
              Personalized
            </p>

            <h2 className="mt-1 text-2xl font-black text-slate-900">
              Recommended For You
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Learning content selected based on your activity.
            </p>
          </div>

          <button
            type="button"
            onClick={() =>
              navigate('/student/library')
            }
            className="w-fit text-sm font-bold text-orange-600 transition hover:text-orange-700"
          >
            View Library →
          </button>
        </div>

        <div className="mt-5 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {recommendedLessons.map((lesson) => (
            <RecommendedCard
              key={lesson.id}
              lesson={lesson}
              onClick={() =>
                openRecommendedLesson(lesson)
              }
            />
          ))}
        </div>
      </section>

      {/* =====================================================
          LOWER GRID
      ====================================================== */}
      <section className="mt-10 grid gap-6 xl:grid-cols-2">
        {/* Weak Topics */}
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-orange-500">
                Focus Areas
              </p>

              <h2 className="mt-1 text-xl font-black text-slate-900">
                Topics to Improve
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Spend a little extra time on these topics.
              </p>
            </div>

            <span className="rounded-xl bg-orange-50 px-3 py-2 text-xs font-bold text-orange-600">
              {weakTopics.length} topics
            </span>
          </div>

          <div className="mt-6 space-y-3">
            {weakTopics.map((topic) => (
              <div
                key={topic.id}
                className="rounded-2xl border border-slate-100 bg-slate-50 p-4"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      {topic.title}
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      {topic.subject}
                    </p>
                  </div>

                  <span className="text-sm font-black text-orange-600">
                    {topic.score}%
                  </span>
                </div>

                <div className="mt-3 h-2 overflow-hidden rounded-full bg-white">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-orange-400 to-amber-400"
                    style={{
                      width: `${topic.score}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Recent Activity */}
        <Card>
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-orange-500">
              Activity
            </p>

            <h2 className="mt-1 text-xl font-black text-slate-900">
              Recent Activity
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Your latest learning progress.
            </p>
          </div>

          <div className="mt-6 space-y-4">
            {recentActivity.map((activity) => (
              <div
                key={activity.id}
                className="flex items-start gap-3"
              >
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
                  {activity.type === 'Quiz'
                    ? '✓'
                    : '▶'}
                </div>

                <div className="min-w-0 flex-1">
                  <p className="text-sm font-bold text-slate-800">
                    {activity.title}
                  </p>

                  <div className="mt-1 flex items-center gap-2">
                    <Badge
                      variant={
                        activity.type === 'Quiz'
                          ? 'info'
                          : 'primary'
                      }
                    >
                      {activity.type}
                    </Badge>

                    <span className="text-[11px] text-slate-400">
                      {activity.time}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </section>

      {/* =====================================================
          LEARNING TIP
      ====================================================== */}
      <section className="mt-10">
        <div className="relative overflow-hidden rounded-3xl bg-slate-900 p-6 text-white shadow-lg sm:p-8">
          <div className="absolute -right-16 -top-20 h-52 w-52 rounded-full bg-orange-500/10" />

          <div className="relative flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-400">
                EduVerse Learning Tip
              </p>

              <h3 className="mt-2 text-xl font-black">
                Small progress every day adds up.
              </h3>

              <p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">
                Keep your learning streak alive by completing one
                focused lesson each day.
              </p>
            </div>

            <button
              type="button"
              onClick={() =>
                navigate('/student/library')
              }
              className="shrink-0 rounded-xl bg-orange-500 px-5 py-3 text-sm font-black text-white transition hover:bg-orange-600"
            >
              Explore Library →
            </button>
          </div>
        </div>
      </section>
    </DashboardLayout>
  )
}

/* =========================================================
   STAT CARD
========================================================= */

function StatCard({
  label,
  value,
  description,
  icon,
}) {
  return (
    <Card
      hover
      className="relative overflow-hidden"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            {label}
          </p>

          <p className="mt-2 text-3xl font-black text-slate-900">
            {value}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {description}
          </p>
        </div>

        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-orange-50 text-orange-500">
          {icon}
        </div>
      </div>
    </Card>
  )
}

/* =========================================================
   RECOMMENDED CARD
========================================================= */

function RecommendedCard({
  lesson,
  onClick,
}) {
  const typeStyles = {
    Video: 'bg-orange-50 text-orange-600',
    Audio: 'bg-purple-50 text-purple-600',
    Quiz: 'bg-blue-50 text-blue-600',
  }

  return (
    <button
      type="button"
      onClick={onClick}
      className="group rounded-3xl border border-slate-200 bg-white p-5 text-left shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-xl focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-orange-100"
    >
      <div className="flex items-start justify-between gap-3">
        <span
          className={`rounded-lg px-2.5 py-1.5 text-[10px] font-bold ${
            typeStyles[lesson.type] ||
            'bg-slate-100 text-slate-600'
          }`}
        >
          {lesson.type}
        </span>

        <span className="text-xs font-semibold text-slate-400">
          {lesson.duration}
        </span>
      </div>

      <h3 className="mt-5 line-clamp-2 text-lg font-black text-slate-900 transition-colors group-hover:text-orange-600">
        {lesson.title}
      </h3>

      <p className="mt-2 text-sm text-slate-500">
        {lesson.subject}
      </p>

      <div className="mt-5 flex items-center justify-between">
        <span className="rounded-lg bg-slate-50 px-2.5 py-1.5 text-[10px] font-bold text-slate-500">
          {lesson.difficulty}
        </span>

        <span className="text-sm font-black text-orange-600 transition-transform group-hover:translate-x-1">
          Start →
        </span>
      </div>
    </button>
  )
}

export default DashboardPage