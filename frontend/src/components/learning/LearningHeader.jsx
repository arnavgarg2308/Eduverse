function LearningHeader({ course }) {
  const progress = Number(course?.progress) || 0

  return (
    <div className="mb-6">
      {/* =====================================================
          COURSE INFORMATION
      ====================================================== */}
      <div className="overflow-hidden rounded-3xl border border-orange-100 bg-gradient-to-br from-orange-50 via-white to-amber-50 shadow-sm">
        <div className="flex flex-col gap-6 p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between lg:p-7">
          {/* Course Info */}
          <div className="flex min-w-0 items-start gap-4">
            {/* Course Icon */}
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-500 to-amber-500 text-xl text-white shadow-lg shadow-orange-200 sm:h-16 sm:w-16 sm:text-2xl">
              {course?.icon || '📚'}
            </div>

            <div className="min-w-0">
              {/* Meta */}
              <div className="flex flex-wrap items-center gap-2">
                {course?.type && (
                  <span className="rounded-lg bg-orange-100 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-orange-600">
                    {course.type}
                  </span>
                )}

                {course?.subject && (
                  <span className="text-xs font-semibold text-slate-400">
                    {course.subject}
                  </span>
                )}
              </div>

              {/* Title */}
              <h1 className="mt-2 break-words text-2xl font-black tracking-tight text-slate-900 sm:text-3xl">
                {course?.title || 'Learning Content'}
              </h1>

              {/* Course Details */}
              <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-slate-500 sm:text-sm">
                {course?.language && (
                  <span>{course.language}</span>
                )}

                {course?.difficulty && (
                  <>
                    <span className="text-slate-300">
                      •
                    </span>

                    <span>{course.difficulty}</span>
                  </>
                )}

                {course?.duration && (
                  <>
                    <span className="text-slate-300">
                      •
                    </span>

                    <span>{course.duration}</span>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* =================================================
              PROGRESS
          ================================================== */}
          <div className="w-full shrink-0 lg:w-56">
            <div className="mb-2 flex items-center justify-between gap-3">
              <span className="text-xs font-bold text-slate-500">
                Your Progress
              </span>

              <span className="text-sm font-black text-orange-600">
                {progress}%
              </span>
            </div>

            <div
              className="h-2.5 overflow-hidden rounded-full bg-orange-100"
              aria-label={`Course progress ${progress}%`}
            >
              <div
                className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-500 transition-all duration-500"
                style={{
                  width: `${Math.min(
                    Math.max(progress, 0),
                    100,
                  )}%`,
                }}
              />
            </div>

            <div className="mt-2 flex items-center justify-between gap-3">
              <span className="text-[10px] font-medium text-slate-400">
                {progress === 100
                  ? 'Completed'
                  : 'In progress'}
              </span>

              <span className="text-[10px] text-slate-400">
                {progress === 100
                  ? '🎉 Great work!'
                  : 'Keep going!'}
              </span>
            </div>
          </div>
        </div>

        {/* Bottom Status */}
        <div className="border-t border-orange-100/80 bg-white/50 px-5 py-3 sm:px-6 lg:px-7">
          <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px] font-medium text-slate-500">
            <span className="inline-flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-green-500" />
              Learning session active
            </span>

            {course?.type && (
              <span>
                Format: {course.type}
              </span>
            )}

            {course?.language && (
              <span>
                Language: {course.language}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default LearningHeader