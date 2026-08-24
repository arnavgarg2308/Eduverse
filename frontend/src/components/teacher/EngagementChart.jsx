function EngagementChart({ data }) {
  const maxStudents = Math.max(
    ...data.map((item) => item.students),
    1,
  )

  const totalStudents = data.reduce(
    (total, item) => total + item.students,
    0,
  )

  const averageStudents = Math.round(
    totalStudents / data.length,
  )

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.15em] text-orange-500">
            Analytics
          </p>

          <h2 className="mt-1 text-xl font-black text-slate-900">
            Student Engagement
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Active students over the last 7 days.
          </p>
        </div>

        <div className="rounded-xl bg-orange-50 px-3 py-2">
          <p className="text-[10px] font-bold uppercase tracking-wider text-orange-500">
            Avg. Daily
          </p>

          <p className="text-sm font-black text-orange-700">
            {averageStudents} students
          </p>
        </div>
      </div>

      <div className="mt-8 flex h-56 items-end gap-2 sm:gap-4">
        {data.map((item) => {
          const height =
            (item.students / maxStudents) * 100

          const isHighest =
            item.students === maxStudents

          return (
            <div
              key={item.day}
              className="flex h-full flex-1 flex-col items-center justify-end"
            >
              <span
                className={`mb-2 text-[10px] font-bold ${
                  isHighest
                    ? 'text-orange-600'
                    : 'text-slate-400'
                }`}
              >
                {item.students}
              </span>

              <div className="flex h-40 w-full items-end justify-center">
                <div
                  className={`w-full max-w-10 rounded-t-xl transition-all duration-700 ${
                    isHighest
                      ? 'bg-gradient-to-t from-orange-600 to-amber-400'
                      : 'bg-orange-100 hover:bg-orange-200'
                  }`}
                  style={{
                    height: `${Math.max(height, 8)}%`,
                  }}
                />
              </div>

              <span
                className={`mt-3 text-[11px] font-semibold ${
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
    </div>
  )
}

export default EngagementChart