function SubjectProgressCard({
  subject,
  progress,
  completedLessons,
  totalLessons,
  color = 'orange',
}) {
  const progressStyles = {
    orange: 'from-orange-500 to-amber-500',
    purple: 'from-purple-500 to-violet-500',
    blue: 'from-blue-500 to-cyan-500',
    green: 'from-emerald-500 to-teal-500',
  }

  const iconStyles = {
    orange: 'bg-orange-50 text-orange-600',
    purple: 'bg-purple-50 text-purple-600',
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-emerald-50 text-emerald-600',
  }

  const safeProgress = Math.min(
    Math.max(Number(progress) || 0, 0),
    100,
  )

  const selectedProgressStyle =
    progressStyles[color] || progressStyles.orange

  const selectedIconStyle =
    iconStyles[color] || iconStyles.orange

  const subjectInitial =
    subject?.trim()?.charAt(0)?.toUpperCase() || 'S'

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex min-w-0 items-center gap-3">
          <div
            className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl text-sm font-black ${selectedIconStyle}`}
            aria-hidden="true"
          >
            {subjectInitial}
          </div>

          <div className="min-w-0">
            <h3 className="truncate text-sm font-black text-slate-900">
              {subject || 'Subject'}
            </h3>

            <p className="mt-1 text-xs text-slate-500">
              {completedLessons} of {totalLessons} lessons
            </p>
          </div>
        </div>

        <span className="shrink-0 text-sm font-black text-slate-900">
          {safeProgress}%
        </span>
      </div>

      {/* Progress Bar */}
      <div
        className="mt-5 h-2.5 overflow-hidden rounded-full bg-slate-100"
        aria-label={`${safeProgress}% progress`}
      >
        <div
          className={`h-full rounded-full bg-gradient-to-r ${selectedProgressStyle} transition-all duration-700`}
          style={{
            width: `${safeProgress}%`,
          }}
        />
      </div>

      {/* Footer */}
      <div className="mt-3 flex items-center justify-between gap-3">
        <span className="text-[11px] font-medium text-slate-400">
          Learning progress
        </span>

        <span
          className={`text-[11px] font-bold ${
            safeProgress >= 75
              ? 'text-emerald-600'
              : 'text-orange-600'
          }`}
        >
          {safeProgress >= 100
            ? 'Completed!'
            : safeProgress >= 75
              ? 'Almost there!'
              : 'Keep going'}
        </span>
      </div>
    </div>
  )
}

export default SubjectProgressCard