import DashboardLayout from '../../components/layout/DashboardLayout'
import ProgressStatCard from '../../components/progress/ProgressStatCard'
import SubjectProgressCard from '../../components/progress/SubjectProgressCard'
import WeeklyActivity from '../../components/progress/WeeklyActivity'
import RecentActivity from '../../components/progress/RecentActivity'
import Achievements from '../../components/progress/Achievements'

import {
  progressStats,
  subjectProgress,
  weeklyActivity,
  recentActivity,
  achievements,
} from '../../data/progressData'

function ProgressPage() {
  return (
    <DashboardLayout role="student" title="Progress">
      {/* =====================================================
          HEADER
      ====================================================== */}
      <section>
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-orange-500">
              Your Journey
            </p>

            <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
              Track your progress.
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
              See how far you've come, understand your learning habits
              and keep moving toward your goals.
            </p>
          </div>

          <div className="rounded-2xl border border-orange-100 bg-gradient-to-br from-orange-50 to-amber-50 px-5 py-4">
            <p className="text-xs font-bold uppercase tracking-wider text-orange-500">
              Overall Progress
            </p>

            <div className="mt-1 flex items-end gap-1">
              <span className="text-3xl font-black text-slate-900">
                {progressStats.overallProgress}%
              </span>

              <span className="mb-1 text-xs font-medium text-slate-500">
                completed
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* =====================================================
          STAT CARDS
      ====================================================== */}
      <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <ProgressStatCard
          icon="◔"
          label="Overall Progress"
          value={`${progressStats.overallProgress}%`}
          description="Your overall learning completion"
          accent="orange"
        />

        <ProgressStatCard
          icon="✓"
          label="Courses Completed"
          value={progressStats.coursesCompleted}
          description={`${progressStats.coursesInProgress} courses currently in progress`}
          accent="green"
        />

        <ProgressStatCard
          icon="◷"
          label="Learning Hours"
          value={`${progressStats.learningHours}h`}
          description="Total time spent learning"
          accent="purple"
        />

        <ProgressStatCard
          icon="★"
          label="Average Quiz Score"
          value={`${progressStats.averageQuizScore}%`}
          description={`${progressStats.quizzesCompleted} quizzes completed`}
          accent="blue"
        />
      </section>

      {/* =====================================================
          OVERALL PROGRESS CARD
      ====================================================== */}
      <section className="mt-6">
        <div className="overflow-hidden rounded-3xl border border-orange-100 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 p-6 text-white shadow-xl sm:p-8">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-xl">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-orange-400">
                Keep Going
              </p>

              <h2 className="mt-3 text-2xl font-black sm:text-3xl">
                You're making great progress.
              </h2>

              <p className="mt-3 text-sm leading-6 text-slate-400">
                You've completed {progressStats.overallProgress}% of your
                current learning journey. Keep your momentum going and
                finish the courses you've started.
              </p>
            </div>

            <div className="w-full max-w-md">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400">
                  Overall completion
                </span>

                <span className="text-sm font-black text-orange-400">
                  {progressStats.overallProgress}%
                </span>
              </div>

              <div className="mt-3 h-3 overflow-hidden rounded-full bg-white/10">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-400"
                  style={{
                    width: `${progressStats.overallProgress}%`,
                  }}
                />
              </div>

              <div className="mt-3 flex justify-between text-[10px] text-slate-500">
                <span>Started</span>
                <span>Halfway there</span>
                <span>Completed</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =====================================================
          SUBJECT PROGRESS
      ====================================================== */}
      <section className="mt-10">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            Subjects
          </p>

          <h2 className="mt-1 text-2xl font-black text-slate-900">
            Subject Progress
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            See how you're progressing across different subjects.
          </p>
        </div>

        <div className="mt-5 grid gap-4 md:grid-cols-2">
          {subjectProgress.map((subject) => (
            <SubjectProgressCard
              key={subject.id}
              subject={subject.subject}
              progress={subject.progress}
              completedLessons={subject.completedLessons}
              totalLessons={subject.totalLessons}
              color={subject.color}
            />
          ))}
        </div>
      </section>

      {/* =====================================================
          ACTIVITY
      ====================================================== */}
      <section className="mt-10 grid gap-5 xl:grid-cols-[1.35fr_1fr]">
        <WeeklyActivity activity={weeklyActivity} />

        <RecentActivity activities={recentActivity} />
      </section>

      {/* =====================================================
          ACHIEVEMENTS
      ====================================================== */}
      <section className="mt-10 pb-6">
        <Achievements achievements={achievements} />
      </section>
    </DashboardLayout>
  )
}

export default ProgressPage