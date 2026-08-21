function WeeklyActivity({ activity = [] }) {
  const safeActivity = Array.isArray(activity)
    ? activity
    : []

  const maxMinutes = Math.max(
    ...safeActivity.map(
      (item) => Number(item.minutes) || 0,
    ),
    1,
  )

  const totalMinutes = safeActivity.reduce(
    (total, item) =>
      total + (Number(item.minutes) || 0),
    0,
  )

  const hours = Math.floor(totalMinutes / 60)
  const minutes = totalMinutes % 60

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      {/* =====================================================
          HEADER
      ====================================================== */}
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            This Week
          </p>

          <h2 className="mt-1 text-xl font-black text-slate-900">
            Learning Activity
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Your daily learning time.
          </p>
        </div>

        <div className="w-fit rounded-xl bg-orange-50 px-3 py-2">
          <p className="text-[10px] font-bold uppercase tracking-wider text-orange-500">
            Total
          </p>

          <p className="text-sm font-black text-orange-700">
            {hours}h {minutes}m
          </p>
        </div>
      </div>

      {/* =====================================================
          EMPTY STATE
      ====================================================== */}
      {safeActivity.length === 0 ? (
        <div className="mt-8 flex h-56 items-center justify-center rounded-2xl bg-slate-50">
          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-orange-500">
              ◔
            </div>

            <p className="mt-3 text-sm font-bold text-slate-700">
              No activity yet
            </p>

            <p className="mt-1 text-xs text-slate-400">
              Your weekly learning activity will appear here.
            </p>
          </div>
        </div>
      ) : (
        /* ===================================================
            ACTIVITY CHART
        ==================================================== */
        <div className="mt-8 flex h-56 items-end gap-2 sm:gap-4">
          {safeActivity.map((item, index) => {
            const itemMinutes =
              Number(item.minutes) || 0

            const height =
              (itemMinutes / maxMinutes) * 100

            const isHighest =
              itemMinutes === maxMinutes &&
              itemMinutes > 0

            return (
              <div
                key={`${item.day}-${index}`}
                className="flex h-full flex-1 flex-col items-center justify-end"
              >
                {/* Minutes */}
                <span
                  className={`mb-2 text-[10px] font-bold ${
                    isHighest
                      ? 'text-orange-600'
                      : 'text-slate-400'
                  }`}
                >
                  {itemMinutes}m
                </span>

                {/* Bar */}
                <div className="flex h-40 w-full items-end justify-center">
                  <div
                    className={`w-full max-w-10 rounded-t-xl transition-all duration-700 ${
                      isHighest
                        ? 'bg-gradient-to-t from-orange-600 to-amber-400'
                        : 'bg-orange-100 hover:bg-orange-200'
                    }`}
                    style={{
                      height: `${Math.max(
                        height,
                        itemMinutes > 0 ? 8 : 2,
                      )}%`,
                    }}
                    title={`${item.day}: ${itemMinutes} minutes`}
                  />
                </div>

                {/* Day */}
                <span
                  className={`mt-3 text-[11px] font-bold ${
                    isHighest
                      ? 'text-orange-600'
                      : 'text-slate-400'
                  }`}
                >
                  {item.day}
                </span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default WeeklyActivity