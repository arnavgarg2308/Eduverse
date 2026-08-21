function RecentActivity({ activities = [] }) {
  const iconStyles = {
    green: 'bg-emerald-50 text-emerald-600',
    orange: 'bg-orange-50 text-orange-600',
    blue: 'bg-blue-50 text-blue-600',
    purple: 'bg-purple-50 text-purple-600',
  }

  const safeActivities = Array.isArray(activities)
    ? activities
    : []

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      {/* =====================================================
          HEADER
      ====================================================== */}
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
          Activity
        </p>

        <h2 className="mt-1 text-xl font-black text-slate-900">
          Recent Activity
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Your latest learning achievements.
        </p>
      </div>

      {/* =====================================================
          ACTIVITY LIST
      ====================================================== */}
      {safeActivities.length > 0 ? (
        <div className="mt-6 space-y-2">
          {safeActivities.map((activity, index) => {
            const iconStyle =
              iconStyles[activity.color] ||
              iconStyles.orange

            return (
              <div
                key={
                  activity.id ||
                  `${activity.title}-${index}`
                }
                className="group flex items-center gap-4 rounded-2xl p-3 transition-all duration-200 hover:bg-orange-50"
              >
                {/* Icon */}
                <div
                  className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-sm font-black ${iconStyle}`}
                  aria-hidden="true"
                >
                  {activity.icon || '•'}
                </div>

                {/* Content */}
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-black text-slate-800 transition group-hover:text-orange-600">
                    {activity.title || 'Learning activity'}
                  </p>

                  <div className="mt-1 flex min-w-0 items-center gap-2">
                    {activity.subject && (
                      <span className="truncate text-[11px] text-slate-400">
                        {activity.subject}
                      </span>
                    )}

                    {activity.subject &&
                      activity.type && (
                        <span
                          className="h-1 w-1 shrink-0 rounded-full bg-slate-300"
                          aria-hidden="true"
                        />
                      )}

                    {activity.type && (
                      <span className="shrink-0 text-[11px] text-slate-400">
                        {activity.type}
                      </span>
                    )}
                  </div>
                </div>

                {/* Time */}
                <span className="shrink-0 text-[11px] font-semibold text-slate-400">
                  {activity.time || 'Recently'}
                </span>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="mt-6 rounded-2xl bg-slate-50 p-8 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-orange-500">
            ◷
          </div>

          <p className="mt-3 text-sm font-bold text-slate-700">
            No recent activity
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-400">
            Your learning activity will appear here as you make
            progress.
          </p>
        </div>
      )}

      {/* =====================================================
          FOOTER
      ====================================================== */}
      <button
        type="button"
        disabled
        className="mt-5 w-full cursor-not-allowed rounded-xl border border-slate-100 bg-slate-50 py-2.5 text-xs font-bold text-slate-400"
        title="Full activity page is not available yet"
      >
        View Full Activity →
      </button>
    </div>
  )
}

export default RecentActivity