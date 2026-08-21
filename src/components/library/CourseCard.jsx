function CourseCard({
  course,
  onClick,
}) {
  const gradientStyles = {
    orange: 'from-orange-500 to-amber-500',
    purple: 'from-purple-500 to-violet-500',
    blue: 'from-blue-500 to-cyan-500',
    green: 'from-emerald-500 to-teal-500',
  }

  const typeStyles = {
    Video: 'bg-orange-50 text-orange-600',
    Audio: 'bg-purple-50 text-purple-600',
    Notes: 'bg-emerald-50 text-emerald-600',
    Quiz: 'bg-blue-50 text-blue-600',
  }

  const difficultyStyles = {
    Easy: 'bg-green-50 text-green-700',
    Medium: 'bg-amber-50 text-amber-700',
    Hard: 'bg-red-50 text-red-700',
  }

  const progress = Math.min(
    Math.max(Number(course?.progress) || 0, 0),
    100,
  )

  const isCompleted = progress === 100

  const actionLabel = isCompleted
    ? 'Review →'
    : progress > 0
      ? 'Continue →'
      : 'Start →'

  const handleOpen = () => {
    onClick?.(course)
  }

  const handleKeyDown = (event) => {
    if (
      event.key === 'Enter' ||
      event.key === ' '
    ) {
      event.preventDefault()
      handleOpen()
    }
  }

  return (
    <article
      role="button"
      tabIndex={0}
      onClick={handleOpen}
      onKeyDown={handleKeyDown}
      aria-label={`Open course ${course?.title || 'course'}`}
      className="group cursor-pointer overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm outline-none transition-all duration-300 hover:-translate-y-1 hover:border-orange-200 hover:shadow-xl focus-visible:border-orange-400 focus-visible:ring-4 focus-visible:ring-orange-100"
    >
      {/* =====================================================
          VISUAL HEADER
      ====================================================== */}
      <div
        className={`relative h-40 overflow-hidden bg-gradient-to-br ${
          gradientStyles[course?.gradient] ||
          gradientStyles.orange
        } p-5`}
      >
        {/* Decorative circles */}
        <div className="absolute -right-10 -top-14 h-40 w-40 rounded-full bg-white/10 transition-transform duration-500 group-hover:scale-110" />

        <div className="absolute -bottom-16 left-20 h-32 w-32 rounded-full bg-white/10 transition-transform duration-500 group-hover:scale-110" />

        {/* Content */}
        <div className="relative flex items-start justify-between gap-3">
          {/* Course icon */}
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white/20 text-xl text-white shadow-lg backdrop-blur-sm transition-transform duration-300 group-hover:scale-105">
            {course?.icon || '📚'}
          </div>

          {/* Content type */}
          {course?.type && (
            <span className="rounded-full bg-white/20 px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-white backdrop-blur-sm">
              {course.type}
            </span>
          )}
        </div>

        {/* Subject */}
        <div className="absolute bottom-5 left-5 right-5">
          <p className="text-xs font-semibold text-white/80">
            {course?.subject || 'Learning'}
          </p>
        </div>
      </div>

      {/* =====================================================
          CONTENT
      ====================================================== */}
      <div className="p-5">
        {/* Title + Difficulty */}
        <div className="flex items-start justify-between gap-3">
          <h3 className="line-clamp-2 min-w-0 text-base font-black leading-6 text-slate-900 transition-colors group-hover:text-orange-600">
            {course?.title || 'Untitled Course'}
          </h3>

          {course?.difficulty && (
            <span
              className={`shrink-0 rounded-lg px-2 py-1 text-[10px] font-bold ${
                difficultyStyles[
                  course.difficulty
                ] || 'bg-slate-100 text-slate-600'
              }`}
            >
              {course.difficulty}
            </span>
          )}
        </div>

        {/* Description */}
        <p className="mt-2 line-clamp-2 text-sm leading-5 text-slate-500">
          {course?.description ||
            'Explore this learning content in EduVerse.'}
        </p>

        {/* =================================================
            METADATA
        ================================================== */}
        <div className="mt-4 flex flex-wrap gap-2">
          {course?.language && (
            <span className="rounded-lg bg-slate-50 px-2.5 py-1.5 text-xs text-slate-500">
              🌐 {course.language}
            </span>
          )}

          {course?.duration && (
            <span className="rounded-lg bg-slate-50 px-2.5 py-1.5 text-xs text-slate-500">
              ⏱ {course.duration}
            </span>
          )}

          {course?.lessons !== undefined && (
            <span className="rounded-lg bg-slate-50 px-2.5 py-1.5 text-xs text-slate-500">
              📚 {course.lessons}{' '}
              {course.lessons === 1
                ? 'item'
                : 'lessons'}
            </span>
          )}
        </div>

        {/* =================================================
            PROGRESS
        ================================================== */}
        <div className="mt-5">
          <div className="mb-2 flex items-center justify-between gap-3">
            <span className="text-xs font-semibold text-slate-500">
              {isCompleted
                ? 'Completed'
                : 'Progress'}
            </span>

            <span
              className={`text-xs font-black ${
                isCompleted
                  ? 'text-green-600'
                  : 'text-orange-600'
              }`}
            >
              {progress}%
            </span>
          </div>

          <div
            className="h-2 overflow-hidden rounded-full bg-slate-100"
            aria-label={`Course progress ${progress}%`}
          >
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                isCompleted
                  ? 'bg-green-500'
                  : 'bg-gradient-to-r from-orange-500 to-amber-500'
              }`}
              style={{
                width: `${progress}%`,
              }}
            />
          </div>
        </div>

        {/* =================================================
            BOTTOM ACTION
        ================================================== */}
        <div className="mt-5 flex items-center justify-between gap-3 border-t border-slate-100 pt-4">
          <div
            className={`inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs font-bold ${
              typeStyles[course?.type] ||
              'bg-slate-50 text-slate-600'
            }`}
          >
            <span>{course?.icon || '📚'}</span>

            <span>
              {course?.type || 'Course'}
            </span>
          </div>

          <button
            type="button"
            onClick={(event) => {
              event.stopPropagation()
              handleOpen()
            }}
            className="rounded-lg px-2 py-1.5 text-sm font-black text-orange-600 transition hover:bg-orange-50 hover:text-orange-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-300"
          >
            {actionLabel}
          </button>
        </div>
      </div>
    </article>
  )
}

export default CourseCard